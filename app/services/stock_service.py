from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dto.stock import BatchUpdate, StockEntryCreate, StockExitCreate
from app.enums import BatchStatus, StockMovementType
from app.models import Batch, ColdLocation, Product, StockMovement
from app.repositories.domain_repository import add, get_by_id, list_batches_for_exit


def _get_active_product(db: Session, product_id: int) -> Product:
    product = get_by_id(db, Product, product_id)
    if product is None or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto indicado no existe o esta inactivo.",
        )
    return product


def _get_active_location(db: Session, location_id: int) -> ColdLocation:
    location = get_by_id(db, ColdLocation, location_id)
    if location is None or not location.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La camara o zona indicada no existe o esta inactiva.",
        )
    return location


def create_stock_entry(db: Session, payload: StockEntryCreate) -> Batch:
    _get_active_product(db, payload.product_id)
    if payload.cold_location_id is not None:
        _get_active_location(db, payload.cold_location_id)

    batch = add(
        db,
        Batch(
            product_id=payload.product_id,
            cold_location_id=payload.cold_location_id,
            quantity=payload.quantity,
            remaining_quantity=payload.quantity,
            supplier=payload.supplier,
            document_number=payload.document_number,
            expiration_date=payload.expiration_date,
            status=BatchStatus.ACTIVE.value,
        ),
    )
    add(
        db,
        StockMovement(
            product_id=payload.product_id,
            batch_id=batch.id,
            cold_location_id=payload.cold_location_id,
            user_id=payload.user_id,
            movement_type=StockMovementType.ENTRY.value,
            quantity=payload.quantity,
            description=payload.description,
        ),
    )
    return batch


def create_stock_exit(db: Session, payload: StockExitCreate) -> tuple[float, list[StockMovement]]:
    _get_active_product(db, payload.product_id)
    if payload.cold_location_id is not None:
        _get_active_location(db, payload.cold_location_id)

    batches = list_batches_for_exit(db, payload.product_id, payload.cold_location_id)
    available = sum(batch.remaining_quantity for batch in batches)
    if available < payload.quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No hay stock suficiente para completar la salida.",
        )

    pending_quantity = payload.quantity
    movements: list[StockMovement] = []
    for batch in batches:
        if pending_quantity <= 0:
            break

        consumed = min(batch.remaining_quantity, pending_quantity)
        batch.remaining_quantity -= consumed
        if batch.remaining_quantity == 0:
            batch.status = BatchStatus.EXHAUSTED.value

        movement = add(
            db,
            StockMovement(
                product_id=payload.product_id,
                batch_id=batch.id,
                cold_location_id=batch.cold_location_id,
                user_id=payload.user_id,
                movement_type=StockMovementType.EXIT.value,
                quantity=consumed,
                description=payload.description,
            ),
        )
        movements.append(movement)
        pending_quantity -= consumed

    db.flush()
    return payload.quantity, movements


def update_batch(db: Session, batch_id: int, payload: BatchUpdate) -> Batch:
    batch = get_by_id(db, Batch, batch_id)
    if batch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El lote indicado no existe.",
        )

    changes = payload.model_dump(exclude_unset=True)
    if "cold_location_id" in changes:
        if changes["cold_location_id"] is not None:
            _get_active_location(db, changes["cold_location_id"])
        batch.cold_location_id = changes["cold_location_id"]
    if "remaining_quantity" in changes and changes["remaining_quantity"] is not None:
        if changes["remaining_quantity"] > batch.quantity:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La cantidad restante no puede superar la cantidad original del lote.",
            )
        batch.remaining_quantity = changes["remaining_quantity"]
        if batch.remaining_quantity == 0 and batch.status == BatchStatus.ACTIVE.value:
            batch.status = BatchStatus.EXHAUSTED.value
    if "expiration_date" in changes and changes["expiration_date"] is not None:
        batch.expiration_date = changes["expiration_date"]
    if "supplier" in changes:
        batch.supplier = changes["supplier"]
    if "document_number" in changes:
        batch.document_number = changes["document_number"]
    if "status" in changes and changes["status"] is not None:
        batch.status = changes["status"].value

    db.flush()
    db.refresh(batch)
    return batch


def delete_batch(db: Session, batch_id: int) -> None:
    batch = get_by_id(db, Batch, batch_id)
    if batch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El lote indicado no existe.",
        )
    batch.status = BatchStatus.DISCARDED.value
    batch.remaining_quantity = 0
    db.flush()


def list_batches(db: Session) -> list[Batch]:
    return list(db.scalars(select(Batch).order_by(Batch.entry_date.desc(), Batch.id.desc())).all())


def list_movements(db: Session) -> list[StockMovement]:
    return list(db.scalars(select(StockMovement).order_by(StockMovement.created_at.desc(), StockMovement.id.desc())).all())
