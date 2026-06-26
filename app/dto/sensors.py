from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.enums import SensorType


class SensorCreate(BaseModel):
    cold_location_id: int
    name: str = Field(min_length=2, max_length=120)
    sensor_type: SensorType = SensorType.MIXED


class SensorUpdate(BaseModel):
    cold_location_id: int | None = None
    name: str | None = Field(default=None, min_length=2, max_length=120)
    sensor_type: SensorType | None = None
    is_active: bool | None = None


class SensorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cold_location_id: int
    name: str
    sensor_type: str
    is_active: bool


class SensorReadingCreate(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    recorded_at: datetime | None = None

    @model_validator(mode="after")
    def require_at_least_one_measurement(self) -> "SensorReadingCreate":
        if self.temperature is None and self.humidity is None:
            raise ValueError("Se requiere temperatura o humedad para registrar una lectura.")
        return self


class SensorReadingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: int
    temperature: float | None
    humidity: float | None
    recorded_at: datetime
