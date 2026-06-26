from datetime import date, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import create_app


def build_client() -> TestClient:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Import models before create_all so metadata knows every table.
    from app import models  # noqa: F401
    from app.services.user_service import ensure_demo_user

    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        ensure_demo_user(db)
        db.commit()

    app = create_app(init_database=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_demo_user_can_login_and_create_users() -> None:
    client = build_client()

    login = client.post(
        "/users/login",
        json={"username": "demo", "password": "demo123"},
    )
    assert login.status_code == 200
    assert login.json()["role"] == "admin"

    created = client.post(
        "/users",
        json={"username": "operador", "password": "secreto1", "role": "operator"},
    )
    assert created.status_code == 201

    users = client.get("/users").json()
    assert {user["username"] for user in users} == {"demo", "operador"}


def test_user_can_be_updated_and_soft_deleted() -> None:
    client = build_client()

    created = client.post("/users", json={"username": "baja", "password": "secreto1"}).json()
    updated = client.patch(f"/users/{created['id']}", json={"username": "baja-editada", "role": "client"})
    assert updated.status_code == 200
    assert updated.json()["username"] == "baja-editada"
    assert updated.json()["role"] == "client"

    deleted = client.delete(f"/users/{created['id']}")
    assert deleted.status_code == 204

    login = client.post("/users/login", json={"username": "baja-editada", "password": "secreto1"})
    assert login.status_code == 401
    users = client.get("/users").json()
    deleted_user = next(user for user in users if user["id"] == created["id"])
    assert deleted_user["is_active"] is False


def test_temperature_alert_and_resolution_requires_evidence() -> None:
    client = build_client()

    location = client.post(
        "/cold-locations",
        json={"name": "Camara 1", "min_temperature": 0, "max_temperature": 5},
    ).json()
    sensor = client.post(
        "/sensors",
        json={"cold_location_id": location["id"], "name": "Sensor A"},
    ).json()

    reading_response = client.post(
        f"/sensors/{sensor['id']}/readings",
        json={"temperature": 8.5, "humidity": 60},
    )
    assert reading_response.status_code == 201
    readings = client.get("/sensor-readings")
    assert readings.status_code == 200
    assert readings.json()[0]["device_id"] == sensor["id"]

    alerts = client.get("/alerts?status=open").json()
    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "temperature"

    without_evidence = client.patch(
        f"/alerts/{alerts[0]['id']}/status",
        json={"status": "resolved"},
    )
    assert without_evidence.status_code == 422

    resolved = client.patch(
        f"/alerts/{alerts[0]['id']}/status",
        json={"status": "resolved", "action_description": "Se ajusto termostato y se verifico puerta.", "user_id": 1},
    )
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "resolved"
    assert resolved.json()["action_description"] == "Se ajusto termostato y se verifico puerta."
    assert resolved.json()["resolved_by_user_id"] == 1
    assert resolved.json()["resolved_by_username"] == "demo"


def test_product_and_category_can_be_updated_and_soft_deleted() -> None:
    client = build_client()

    category = client.post("/categories", json={"name": "Carnes"}).json()
    product = client.post(
        "/products",
        json={"name": "Asado", "code": "BOV-ASADO-T", "weight": 1.2, "unit": "kg", "category_id": category["id"]},
    ).json()

    updated_product = client.patch(
        f"/products/{product['id']}",
        json={"name": "Asado premium", "code": "BOV-ASADO-PREM", "weight": 1.5, "unit": "kg"},
    )
    assert updated_product.status_code == 200
    assert updated_product.json()["name"] == "Asado premium"
    assert updated_product.json()["code"] == "BOV-ASADO-PREM"
    assert updated_product.json()["weight"] == 1.5

    invalid_unit = client.post("/products", json={"name": "Unidad rara", "unit": "caja"})
    assert invalid_unit.status_code == 422

    deleted_product = client.delete(f"/products/{product['id']}")
    assert deleted_product.status_code == 204
    products = client.get("/products").json()
    stored_product = next(item for item in products if item["id"] == product["id"])
    assert stored_product["is_active"] is False
    assert client.get("/catalog").json() == []

    deleted_category = client.delete(f"/categories/{category['id']}")
    assert deleted_category.status_code == 204
    stored_category = next(item for item in client.get("/categories").json() if item["id"] == category["id"])
    assert stored_category["is_active"] is False


def test_stock_exit_consumes_non_expired_batches_by_fifo() -> None:
    client = build_client()

    product = client.post("/products", json={"name": "Media res", "unit": "kg"}).json()
    location = client.post("/cold-locations", json={"name": "Camara FIFO"}).json()

    old_batch = client.post(
        "/stock/entry",
        json={
            "product_id": product["id"],
            "cold_location_id": location["id"],
            "quantity": 10,
            "document_number": "R-TEST-001",
            "user_id": 1,
            "expiration_date": str(date.today() + timedelta(days=5)),
        },
    ).json()
    assert old_batch["document_number"] == "R-TEST-001"
    new_batch = client.post(
        "/stock/entry",
        json={
            "product_id": product["id"],
            "cold_location_id": location["id"],
            "quantity": 10,
            "document_number": "R-TEST-002",
            "user_id": 1,
            "expiration_date": str(date.today() + timedelta(days=10)),
        },
    ).json()

    exit_response = client.post(
        "/stock/exit",
        json={
            "product_id": product["id"],
            "cold_location_id": location["id"],
            "quantity": 12,
            "user_id": 1,
        },
    )
    assert exit_response.status_code == 201

    movements = exit_response.json()["movements"]
    assert movements[0]["batch_id"] == old_batch["id"]
    assert movements[0]["quantity"] == 10
    assert movements[1]["batch_id"] == new_batch["id"]
    assert movements[1]["quantity"] == 2

    catalog = client.get("/catalog").json()
    assert catalog[0]["available_quantity"] == 8

    movement_history = client.get("/stock/movements")
    assert movement_history.status_code == 200
    assert len(movement_history.json()) == 4
    assert {movement["movement_type"] for movement in movement_history.json()} == {"entry", "exit"}
    assert {movement["user_name"] for movement in movement_history.json()} == {"demo"}


def test_batch_can_be_updated_and_soft_deleted() -> None:
    client = build_client()

    product = client.post("/products", json={"name": "Nalga", "unit": "kg"}).json()
    location = client.post("/cold-locations", json={"name": "Camara descarte"}).json()
    batch = client.post(
        "/stock/entry",
        json={
            "product_id": product["id"],
            "cold_location_id": location["id"],
            "quantity": 7,
            "supplier": "Proveedor test",
            "document_number": "F-0001-0007",
            "expiration_date": str(date.today() + timedelta(days=4)),
        },
    ).json()
    assert batch["supplier"] == "Proveedor test"
    assert batch["document_number"] == "F-0001-0007"

    updated = client.patch(
        f"/stock/batches/{batch['id']}",
        json={"remaining_quantity": 5, "supplier": "Proveedor editado", "document_number": "F-0001-0008", "status": "active"},
    )
    assert updated.status_code == 200
    assert updated.json()["remaining_quantity"] == 5
    assert updated.json()["supplier"] == "Proveedor editado"
    assert updated.json()["document_number"] == "F-0001-0008"

    deleted = client.delete(f"/stock/batches/{batch['id']}")
    assert deleted.status_code == 204
    batches = client.get("/stock/batches").json()
    stored_batch = next(item for item in batches if item["id"] == batch["id"])
    assert stored_batch["status"] == "discarded"
    assert stored_batch["remaining_quantity"] == 0
    assert client.get("/catalog").json()[0]["available_quantity"] == 0


def test_seed_data_creates_products_batches_and_is_idempotent() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    from app import models  # noqa: F401
    from app.models import Batch, Product
    from app.services.seed_service import ensure_seed_data
    from app.services.user_service import ensure_demo_user

    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        ensure_demo_user(db)
        ensure_seed_data(db)
        db.commit()
        first_product_count = db.query(Product).count()
        first_batch_count = db.query(Batch).count()

        ensure_seed_data(db)
        db.commit()

        assert db.query(Product).count() == first_product_count
        assert db.query(Batch).count() == first_batch_count
        assert first_product_count >= 4
        assert first_batch_count >= 5
        assert sum(batch.remaining_quantity for batch in db.query(Batch).all()) > 0


def test_alert_can_be_updated_and_soft_deleted() -> None:
    client = build_client()

    created = client.post(
        "/alerts",
        json={"alert_type": "manual", "severity": "low", "message": "Puerta abierta en control manual."},
    ).json()

    updated = client.patch(
        f"/alerts/{created['id']}",
        json={"severity": "high", "message": "Puerta abierta durante recepcion.", "status": "acknowledged"},
    )
    assert updated.status_code == 200
    assert updated.json()["severity"] == "high"
    assert updated.json()["status"] == "acknowledged"

    deleted = client.delete(f"/alerts/{created['id']}")
    assert deleted.status_code == 204
    assert all(alert["id"] != created["id"] for alert in client.get("/alerts").json())
