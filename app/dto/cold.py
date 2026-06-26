from pydantic import BaseModel, ConfigDict, Field

from app.enums import LocationType


class ColdLocationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    location_type: LocationType = LocationType.CHAMBER
    description: str | None = None
    min_temperature: float | None = None
    max_temperature: float | None = None
    min_humidity: float | None = None
    max_humidity: float | None = None


class ColdLocationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    location_type: LocationType | None = None
    description: str | None = None
    min_temperature: float | None = None
    max_temperature: float | None = None
    min_humidity: float | None = None
    max_humidity: float | None = None
    is_active: bool | None = None


class ColdLocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location_type: str
    description: str | None
    min_temperature: float | None
    max_temperature: float | None
    min_humidity: float | None
    max_humidity: float | None
    is_active: bool
