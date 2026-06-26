from collections.abc import Generator

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)

if settings.database_url.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    # Importing models here registers every table in Base.metadata before create_all.
    from app import models  # noqa: F401
    from app.services.seed_service import ensure_seed_data
    from app.services.user_service import ensure_demo_user

    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_columns()
    with SessionLocal() as db:
        ensure_demo_user(db)
        ensure_seed_data(db)
        db.commit()


def _ensure_sqlite_columns() -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    required_columns = {
        "users": [
            ("is_active", "is_active BOOLEAN NOT NULL DEFAULT 1"),
            ("created_at", "created_at DATETIME"),
        ],
        "product_categories": [
            ("is_active", "is_active BOOLEAN NOT NULL DEFAULT 1"),
        ],
        "products": [
            ("code", "code VARCHAR(60)"),
            ("weight", "weight FLOAT"),
            ("is_active", "is_active BOOLEAN NOT NULL DEFAULT 1"),
        ],
        "cold_locations": [
            ("location_type", "location_type VARCHAR(30) NOT NULL DEFAULT 'chamber'"),
            ("is_active", "is_active BOOLEAN NOT NULL DEFAULT 1"),
        ],
        "alerts": [
            ("action_description", "action_description TEXT"),
            ("resolved_by_user_id", "resolved_by_user_id INTEGER"),
            ("is_active", "is_active BOOLEAN NOT NULL DEFAULT 1"),
        ],
        "batches": [
            ("supplier", "supplier VARCHAR(120)"),
            ("document_number", "document_number VARCHAR(120)"),
        ],
    }

    with engine.begin() as connection:
        for table_name, columns in required_columns.items():
            existing = {
                row[1]
                for row in connection.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
            }
            for column_name, definition in columns:
                if column_name not in existing:
                    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {definition}"))
