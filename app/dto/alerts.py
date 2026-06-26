from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums import AlertSeverity, AlertStatus, AlertType


class AlertCreate(BaseModel):
    alert_type: AlertType
    message: str = Field(min_length=3)
    severity: AlertSeverity = AlertSeverity.MEDIUM
    device_id: int | None = None
    cold_location_id: int | None = None


class AlertUpdate(BaseModel):
    alert_type: AlertType | None = None
    message: str | None = Field(default=None, min_length=3)
    severity: AlertSeverity | None = None
    status: AlertStatus | None = None
    device_id: int | None = None
    cold_location_id: int | None = None
    is_active: bool | None = None


class AlertStatusUpdate(BaseModel):
    status: AlertStatus
    action_description: str | None = Field(default=None, min_length=3)
    user_id: int | None = None


class AlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: int | None
    cold_location_id: int | None
    alert_type: str
    severity: str
    status: str
    message: str
    created_at: datetime
    resolved_at: datetime | None
    action_description: str | None
    resolved_by_user_id: int | None
    resolved_by_username: str | None = None
    is_active: bool
