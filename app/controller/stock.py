from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.stock import BatchRead, BatchUpdate, StockEntryCreate, StockExitCreate, StockExitResult, StockMovementRead
from app.models import Batch, StockMovement
from app.services import stock_service

router = APIRouter(prefix="/stock", tags=["Stock FIFO"])


@router.post("/entry", response_model=BatchRead, status_code=status.HTTP_201_CREATED)
def create_stock_entry(payload: StockEntryCreate, db: Session = Depends(get_db)) -> Batch:
    return stock_service.create_stock_entry(db, payload)


@router.post("/exit", response_model=StockExitResult, status_code=status.HTTP_201_CREATED)
def create_stock_exit(payload: StockExitCreate, db: Session = Depends(get_db)) -> StockExitResult:
    consumed, movements = stock_service.create_stock_exit(db, payload)
    return StockExitResult(requested_quantity=payload.quantity, consumed_quantity=consumed, movements=movements)


@router.get("/batches", response_model=list[BatchRead])
def list_batches(db: Session = Depends(get_db)) -> list[Batch]:
    return stock_service.list_batches(db)


@router.get("/movements", response_model=list[StockMovementRead])
def list_movements(db: Session = Depends(get_db)) -> list[StockMovement]:
    return stock_service.list_movements(db)


@router.patch("/batches/{batch_id}", response_model=BatchRead)
def update_batch(batch_id: int, payload: BatchUpdate, db: Session = Depends(get_db)) -> Batch:
    return stock_service.update_batch(db, batch_id, payload)


@router.delete("/batches/{batch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_batch(batch_id: int, db: Session = Depends(get_db)) -> Response:
    stock_service.delete_batch(db, batch_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
