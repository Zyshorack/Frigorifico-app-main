from datetime import date
from typing import TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import BatchStatus
from app.models import Batch, Product, ProductCategory, User

ModelT = TypeVar("ModelT")


def get_by_id(db: Session, model: type[ModelT], item_id: int) -> ModelT | None:
    return db.get(model, item_id)


def add(db: Session, item: ModelT) -> ModelT:
    db.add(item)
    db.flush()
    db.refresh(item)
    return item


def list_all(db: Session, model: type[ModelT]) -> list[ModelT]:
    return list(db.scalars(select(model)).all())


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def get_category_by_name(db: Session, name: str) -> ProductCategory | None:
    return db.scalar(select(ProductCategory).where(ProductCategory.name == name))


def get_product_by_name(db: Session, name: str) -> Product | None:
    return db.scalar(select(Product).where(Product.name == name))


def product_available_quantity(db: Session, product_id: int) -> float:
    total = db.scalar(
        select(func.coalesce(func.sum(Batch.remaining_quantity), 0.0)).where(
            Batch.product_id == product_id,
            Batch.status == BatchStatus.ACTIVE,
            Batch.expiration_date >= date.today(),
        )
    )
    return float(total or 0)


def list_catalog_products(db: Session) -> list[tuple[Product, float]]:
    products = db.scalars(select(Product).where(Product.is_active.is_(True)).order_by(Product.name)).all()
    return [(product, product_available_quantity(db, product.id)) for product in products]


def list_batches_for_exit(
    db: Session,
    product_id: int,
    cold_location_id: int | None = None,
) -> list[Batch]:
    statement = select(Batch).where(
        Batch.product_id == product_id,
        Batch.status == BatchStatus.ACTIVE,
        Batch.remaining_quantity > 0,
        Batch.expiration_date >= date.today(),
    )
    if cold_location_id is not None:
        statement = statement.where(Batch.cold_location_id == cold_location_id)
    statement = statement.order_by(Batch.expiration_date, Batch.entry_date, Batch.id)
    return list(db.scalars(statement).all())

def get_available_product_by_name_and_category(
    db: Session,
    product_name: str | None = None,
    category_name: str | None = None,
) -> Product | None:
    stmt = (
        select(Product)
        .join(ProductCategory, Product.category_id == ProductCategory.id)
        .join(Batch, Batch.product_id == Product.id)
        .where(
            Batch.status == BatchStatus.ACTIVE,
            Batch.remaining_quantity > 0,
            Batch.expiration_date >= date.today(),
        )
    )

    if product_name:
        stmt = stmt.where(Product.name == product_name)

    if category_name:
        stmt = stmt.where(ProductCategory.name == category_name)

    stmt = (
        stmt.group_by(Product.id)
        .having(func.sum(Batch.remaining_quantity) > 0)
    )

    return db.scalar(stmt)