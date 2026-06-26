from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dto.products import ProductCategoryCreate, ProductCategoryUpdate, ProductCreate, ProductUpdate
from app.models import Product, ProductCategory
from app.repositories.domain_repository import (
    add,
    get_category_by_name,
    get_by_id,
    get_product_by_name,
    list_catalog_products,
    get_available_product_by_name_and_category,
)


def _ensure_category_name_available(db: Session, name: str, current_category_id: int | None = None) -> None:
    existing = get_category_by_name(db, name)
    if existing and existing.id != current_category_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una categoria con ese nombre.",
        )


def _ensure_product_name_available(db: Session, name: str, current_product_id: int | None = None) -> None:
    existing = get_product_by_name(db, name)
    if existing and existing.id != current_product_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un producto con ese nombre.",
        )


def _ensure_product_code_available(db: Session, code: str | None, current_product_id: int | None = None) -> None:
    if not code:
        return
    existing = db.scalar(select(Product).where(Product.code == code))
    if existing and existing.id != current_product_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un producto con ese codigo.",
        )


def _get_active_category(db: Session, category_id: int) -> ProductCategory:
    category = get_by_id(db, ProductCategory, category_id)
    if category is None or not category.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoria indicada no existe o esta inactiva.",
        )
    return category


def create_category(db: Session, payload: ProductCategoryCreate) -> ProductCategory:
    _ensure_category_name_available(db, payload.name)
    category = ProductCategory(**payload.model_dump(), is_active=True)
    return add(db, category)


def update_category(db: Session, category_id: int, payload: ProductCategoryUpdate) -> ProductCategory:
    category = get_by_id(db, ProductCategory, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoria indicada no existe.",
        )

    changes = payload.model_dump(exclude_unset=True)
    if "name" in changes:
        _ensure_category_name_available(db, changes["name"], current_category_id=category.id)
        category.name = changes["name"]
    if "description" in changes:
        category.description = changes["description"]
    if "is_active" in changes and changes["is_active"] is not None:
        category.is_active = changes["is_active"]

    db.flush()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_by_id(db, ProductCategory, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoria indicada no existe.",
        )
    category.is_active = False
    db.flush()


def list_categories(db: Session) -> list[ProductCategory]:
    return list(db.scalars(select(ProductCategory).order_by(ProductCategory.name)).all())


def create_product(db: Session, payload: ProductCreate) -> Product:
    _ensure_product_name_available(db, payload.name)
    _ensure_product_code_available(db, payload.code)
    if payload.category_id is not None:
        _get_active_category(db, payload.category_id)

    product = Product(**payload.model_dump(), is_active=True)
    return add(db, product)


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = get_by_id(db, Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto indicado no existe.",
        )

    changes = payload.model_dump(exclude_unset=True)
    if "name" in changes:
        _ensure_product_name_available(db, changes["name"], current_product_id=product.id)
        product.name = changes["name"]
    if "code" in changes:
        _ensure_product_code_available(db, changes["code"], current_product_id=product.id)
        product.code = changes["code"]
    if "category_id" in changes:
        if changes["category_id"] is not None:
            _get_active_category(db, changes["category_id"])
        product.category_id = changes["category_id"]
    if "description" in changes:
        product.description = changes["description"]
    if "weight" in changes:
        product.weight = changes["weight"]
    if "unit" in changes and changes["unit"] is not None:
        product.unit = changes["unit"]
    if "is_active" in changes and changes["is_active"] is not None:
        product.is_active = changes["is_active"]

    db.flush()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_by_id(db, Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto indicado no existe.",
        )
    product.is_active = False
    db.flush()


def list_products(db: Session) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.name)).all())


def catalog(db: Session) -> list[dict]:
    return [
        {
            "id": product.id,
            "category_id": product.category_id,
            "code": product.code,
            "name": product.name,
            "description": product.description,
            "weight": product.weight,
            "unit": product.unit,
            "is_active": product.is_active,
            "available_quantity": available_quantity,
        }
        for product, available_quantity in list_catalog_products(db)
    ]

def product_by_name_and_category(
    db: Session,
    product_name: str | None = None,
    category_name: str | None = None,
):
    if not product_name and not category_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe indicar el nombre del producto, la categoría o ambos.",
        )

    product = get_available_product_by_name_and_category(
        db=db,
        product_name=product_name,
        category_name=category_name,
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado o sin stock disponible",
        )

    return product

def search_products(
    db: Session,
    code: str | None = None,
    category_id: int | None = None,
) -> list[Product]:

    query = select(Product)

    if code:
        query = query.where(
            Product.code.ilike(f"%{code}%")
        )

    if category_id:
        query = query.where(
            Product.category_id == category_id
        )

    query = query.where(
        Product.is_active == True
    )

    return list(db.scalars(query).all())