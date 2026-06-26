from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import BatchStatus, StockMovementType
from app.models import Batch, ColdLocation, Product, ProductCategory, StockMovement, User
from app.repositories.domain_repository import add
from app.services.user_service import DEMO_USERNAME


SEED_LOCATION_NAME = "Camara Seed - Stock inicial"

SEED_PRODUCTS = [
    {
        "category": "Carnes bovinas",
        "code": "BOV-MEDIA-RES",
        "name": "Media res",
        "description": "Producto bovino de referencia para stock frigorifico.",
        "weight": 80,
        "unit": "kg",
        "batches": [
            {"quantity": 80, "expires_in_days": 30, "supplier": "Proveedor seed bovino", "document_number": "SEED-BOV-001", "description": "Lote seed media res 30 dias."},
            {"quantity": 60, "expires_in_days": 45, "supplier": "Proveedor seed bovino", "document_number": "SEED-BOV-002", "description": "Lote seed media res 45 dias."},
        ],
    },
    {
        "category": "Carnes bovinas",
        "code": "BOV-ASADO",
        "name": "Asado",
        "description": "Corte bovino para venta por kilogramo.",
        "weight": 1,
        "unit": "kg",
        "batches": [
            {"quantity": 35, "expires_in_days": 20, "supplier": "Proveedor seed cortes", "document_number": "SEED-CORTE-001", "description": "Lote seed asado."},
        ],
    },
    {
        "category": "Carnes bovinas",
        "code": "BOV-NALGA",
        "name": "Nalga",
        "description": "Corte bovino magro para inventario inicial.",
        "weight": 1,
        "unit": "kg",
        "batches": [
            {"quantity": 28, "expires_in_days": 25, "supplier": "Proveedor seed cortes", "document_number": "SEED-CORTE-002", "description": "Lote seed nalga."},
        ],
    },
    {
        "category": "Embutidos",
        "code": "EMB-CHORIZO",
        "name": "Chorizo",
        "description": "Embutido fresco con control de frio.",
        "weight": 1,
        "unit": "kg",
        "batches": [
            {"quantity": 20, "expires_in_days": 15, "supplier": "Proveedor seed embutidos", "document_number": "SEED-EMB-001", "description": "Lote seed chorizo fresco."},
        ],
    },
]


def ensure_seed_data(db: Session) -> None:
    location = _get_or_create_location(db)
    demo_user = db.scalar(select(User).where(User.username == DEMO_USERNAME))

    for item in SEED_PRODUCTS:
        category = _get_or_create_category(db, item["category"])
        product = _get_or_create_product(db, item, category.id)
        _ensure_product_batches(db, product, location.id, demo_user.id if demo_user else None, item["batches"])


def _get_or_create_category(db: Session, name: str) -> ProductCategory:
    category = db.scalar(select(ProductCategory).where(ProductCategory.name == name))
    if category is not None:
        return category

    return add(
        db,
        ProductCategory(
            name=name,
            description="Categoria creada por datos seed.",
            is_active=True,
        ),
    )


def _get_or_create_product(db: Session, item: dict, category_id: int) -> Product:
    product = db.scalar(select(Product).where(Product.name == item["name"]))
    if product is not None:
        if product.code is None:
            product.code = item["code"]
        if product.weight is None:
            product.weight = item["weight"]
        if product.unit != item["unit"]:
            product.unit = item["unit"]
        return product

    return add(
        db,
        Product(
            category_id=category_id,
            code=item["code"],
            name=item["name"],
            description=item["description"],
            weight=item["weight"],
            unit=item["unit"],
            is_active=True,
        ),
    )


def _get_or_create_location(db: Session) -> ColdLocation:
    location = db.scalar(select(ColdLocation).where(ColdLocation.name == SEED_LOCATION_NAME))
    if location is not None:
        return location

    return add(
        db,
        ColdLocation(
            name=SEED_LOCATION_NAME,
            location_type="chamber",
            description="Camara inicial para lotes seed.",
            min_temperature=0,
            max_temperature=5,
            is_active=True,
        ),
    )


def _ensure_product_batches(
    db: Session,
    product: Product,
    location_id: int,
    user_id: int | None,
    batch_specs: list[dict],
) -> None:
    existing_batch = db.scalar(select(Batch.id).where(Batch.product_id == product.id).limit(1))
    if existing_batch is not None:
        fallback_supplier = batch_specs[0]["supplier"] if batch_specs else None
        fallback_document = batch_specs[0]["document_number"] if batch_specs else None
        if fallback_supplier:
            for batch in db.scalars(select(Batch).where(Batch.product_id == product.id, Batch.supplier.is_(None))).all():
                batch.supplier = fallback_supplier
        if fallback_document:
            for batch in db.scalars(select(Batch).where(Batch.product_id == product.id, Batch.document_number.is_(None))).all():
                batch.document_number = fallback_document
        return

    for spec in batch_specs:
        batch = add(
            db,
            Batch(
                product_id=product.id,
                cold_location_id=location_id,
                quantity=spec["quantity"],
                remaining_quantity=spec["quantity"],
                supplier=spec["supplier"],
                document_number=spec["document_number"],
                expiration_date=date.today() + timedelta(days=spec["expires_in_days"]),
                status=BatchStatus.ACTIVE.value,
            ),
        )
        add(
            db,
            StockMovement(
                product_id=product.id,
                batch_id=batch.id,
                cold_location_id=location_id,
                user_id=user_id,
                movement_type=StockMovementType.ENTRY.value,
                quantity=spec["quantity"],
                description=spec["description"],
            ),
        )
