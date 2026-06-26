from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.products import (
    CatalogProductRead,
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from app.models import Product, ProductCategory
from app.services import product_service


router = APIRouter(tags=["Catalogo y Productos"])


@router.post("/categories", response_model=ProductCategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: ProductCategoryCreate, db: Session = Depends(get_db)) -> ProductCategory:
    return product_service.create_category(db, payload)


@router.get("/categories", response_model=list[ProductCategoryRead])
def list_categories(db: Session = Depends(get_db)) -> list[ProductCategory]:
    return product_service.list_categories(db)


@router.patch("/categories/{category_id}", response_model=ProductCategoryRead)
def update_category(category_id: int, payload: ProductCategoryUpdate, db: Session = Depends(get_db)) -> ProductCategory:
    return product_service.update_category(db, category_id, payload)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> Response:
    product_service.delete_category(db, category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    return product_service.create_product(db, payload)


@router.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    return product_service.list_products(db)


@router.patch("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)) -> Product:
    return product_service.update_product(db, product_id, payload)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> Response:
    product_service.delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/catalog", response_model=list[CatalogProductRead])
def catalog(db: Session = Depends(get_db)) -> list[dict]:
    return product_service.catalog(db)

@router.get("/products/search", response_model=ProductRead)
def product_by_name_and_category(
    product_name: str | None = None,
    category_name: str | None = None,
    db: Session = Depends(get_db),
) -> Product:
    return product_service.product_by_name_and_category(
        db,
        product_name,
        category_name,
    )