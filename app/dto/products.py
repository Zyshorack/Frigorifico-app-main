from pydantic import BaseModel, ConfigDict, Field

from app.enums import ProductUnit


class ProductCategoryCreate(BaseModel):
    name: str = Field(min_length=0, max_length=80)
    description: str | None = None


class ProductCategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = None
    is_active: bool | None = None


class ProductCategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    is_active: bool


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    code: str | None = Field(default=None, min_length=1, max_length=60)
    category_id: int | None = None
    description: str | None = None
    weight: float | None = Field(default=None, gt=0)
    unit: ProductUnit = ProductUnit.KG


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    code: str | None = Field(default=None, min_length=1, max_length=60)
    category_id: int | None = None
    description: str | None = None
    weight: float | None = Field(default=None, gt=0)
    unit: ProductUnit | None = None
    is_active: bool | None = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int | None
    code: str | None
    name: str
    description: str | None
    weight: float | None
    unit: str
    is_active: bool


class CatalogProductRead(ProductRead):
    available_quantity: float
