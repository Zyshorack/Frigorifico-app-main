from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dto.alerts import AlertCreate, AlertStatusUpdate, AlertUpdate
from app.enums import AlertStatus
from app.models import Alert, ColdLocation, SensorDevice, User
from app.models.domain import utc_now
from app.repositories.domain_repository import add, get_by_id


def _ensure_alert_exists(alert: Alert | None) -> Alert:
    if alert is None or not alert.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La alerta indicada no existe.",
        )
    return alert


def _validate_references(db: Session, device_id: int | None, cold_location_id: int | None) -> None:
    if device_id is not None and get_by_id(db, SensorDevice, device_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El sensor indicado no existe.",
        )
    if cold_location_id is not None and get_by_id(db, ColdLocation, cold_location_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La camara o zona indicada no existe.",
        )


def create_alert(db: Session, payload: AlertCreate) -> Alert:
    _validate_references(db, payload.device_id, payload.cold_location_id)
    alert = Alert(
        **payload.model_dump(),
        status=AlertStatus.OPEN.value,
        is_active=True,
    )
    return add(db, alert)


def list_alerts(db: Session, status_filter: AlertStatus | None = None) -> list[Alert]:
    statement = select(Alert).where(Alert.is_active.is_(True))
    if status_filter is not None:
        statement = statement.where(Alert.status == status_filter.value)
    return list(db.scalars(statement.order_by(Alert.created_at.desc(), Alert.id.desc())).all())


def update_alert(db: Session, alert_id: int, payload: AlertUpdate) -> Alert:
    alert = _ensure_alert_exists(get_by_id(db, Alert, alert_id))
    changes = payload.model_dump(exclude_unset=True)

    device_id = changes.get("device_id", alert.device_id)
    cold_location_id = changes.get("cold_location_id", alert.cold_location_id)
    _validate_references(db, device_id, cold_location_id)

    if "alert_type" in changes and changes["alert_type"] is not None:
        alert.alert_type = changes["alert_type"].value
    if "severity" in changes and changes["severity"] is not None:
        alert.severity = changes["severity"].value
    if "status" in changes and changes["status"] is not None:
        alert.status = changes["status"].value
        alert.resolved_at = utc_now() if changes["status"] == AlertStatus.RESOLVED else None
    if "message" in changes and changes["message"] is not None:
        alert.message = changes["message"]
    if "device_id" in changes:
        alert.device_id = changes["device_id"]
    if "cold_location_id" in changes:
        alert.cold_location_id = changes["cold_location_id"]
    if "is_active" in changes and changes["is_active"] is not None:
        alert.is_active = changes["is_active"]

    db.flush()
    db.refresh(alert)
    return alert


def update_alert_status(db: Session, alert_id: int, payload: AlertStatusUpdate) -> Alert:
    alert = _ensure_alert_exists(get_by_id(db, Alert, alert_id))
    if payload.status == AlertStatus.RESOLVED and not payload.action_description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Para resolver una alerta se requiere una accion correctiva.",
        )
    if payload.user_id is not None and get_by_id(db, User, payload.user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario indicado no existe.",
        )

    alert.status = payload.status.value
    if payload.status == AlertStatus.RESOLVED:
        alert.resolved_at = utc_now()
        alert.action_description = payload.action_description
        alert.resolved_by_user_id = payload.user_id
    else:
        alert.resolved_at = None
        alert.action_description = None
        alert.resolved_by_user_id = None
    db.flush()
    db.refresh(alert)
    return alert


def delete_alert(db: Session, alert_id: int) -> None:
    alert = _ensure_alert_exists(get_by_id(db, Alert, alert_id))
    alert.is_active = False
    db.flush()
