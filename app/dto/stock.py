from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums import BatchStatus


class StockEntryCreate(BaseModel):
    product_id: int
    cold_location_id: int | None = None
    quantity: float = Field(gt=0)
    expiration_date: date
    supplier: str | None = Field(default=None, max_length=120)
    document_number: str | None = Field(default=None, max_length=120)
    user_id: int | None = None
    description: str | None = None


class StockExitCreate(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)
    cold_location_id: int | None = None
    user_id: int | None = None
    description: str | None = None


class BatchUpdate(BaseModel):
    cold_location_id: int | None = None
    remaining_quantity: float | None = Field(default=None, ge=0)
    expiration_date: date | None = None
    supplier: str | None = Field(default=None, max_length=120)
    document_number: str | None = Field(default=None, max_length=120)
    status: BatchStatus | None = None


class BatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    cold_location_id: int | None
    quantity: float
    remaining_quantity: float
    supplier: str | None
    document_number: str | None
    entry_date: datetime
    expiration_date: date
    status: str


class StockMovementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    batch_id: int
    cold_location_id: int | None
    user_id: int | None
    user_name: str | None = None
    movement_type: str
    quantity: float
    created_at: datetime
    description: str | None


class StockExitResult(BaseModel):
    requested_quantity: float
    consumed_quantity: float
    movements: list[StockMovementRead]
