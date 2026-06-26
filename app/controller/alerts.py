from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.alerts import AlertCreate, AlertRead, AlertStatusUpdate, AlertUpdate
from app.enums import AlertStatus
from app.models import Alert
from app.services import alert_service

router = APIRouter(prefix="/alerts", tags=["Alertas"])


@router.post("", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
def create_alert(payload: AlertCreate, db: Session = Depends(get_db)) -> Alert:
    return alert_service.create_alert(db, payload)


@router.get("", response_model=list[AlertRead])
def list_alerts(
    status_filter: AlertStatus | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
) -> list[Alert]:
    return alert_service.list_alerts(db, status_filter)


@router.patch("/{alert_id}", response_model=AlertRead)
def update_alert(alert_id: int, payload: AlertUpdate, db: Session = Depends(get_db)) -> Alert:
    return alert_service.update_alert(db, alert_id, payload)


@router.patch("/{alert_id}/status", response_model=AlertRead)
def update_alert_status(alert_id: int, payload: AlertStatusUpdate, db: Session = Depends(get_db)) -> Alert:
    return alert_service.update_alert_status(db, alert_id, payload)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: int, db: Session = Depends(get_db)) -> Response:
    alert_service.delete_alert(db, alert_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
