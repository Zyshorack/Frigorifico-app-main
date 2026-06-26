from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dto.cold import ColdLocationCreate, ColdLocationUpdate
from app.dto.sensors import SensorCreate, SensorReadingCreate, SensorUpdate
from app.enums import AlertSeverity, AlertStatus, AlertType
from app.models import Alert, ColdLocation, SensorDevice, SensorReading
from app.repositories.domain_repository import add, get_by_id


def _ensure_location_name_available(db: Session, name: str, current_location_id: int | None = None) -> None:
    existing = db.scalar(select(ColdLocation).where(ColdLocation.name == name))
    if existing and existing.id != current_location_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una camara o zona con ese nombre.",
        )


def _ensure_sensor_name_available(db: Session, name: str, current_sensor_id: int | None = None) -> None:
    existing = db.scalar(select(SensorDevice).where(SensorDevice.name == name))
    if existing and existing.id != current_sensor_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un sensor con ese nombre.",
        )


def _get_active_location(db: Session, location_id: int) -> ColdLocation:
    location = get_by_id(db, ColdLocation, location_id)
    if location is None or not location.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La camara o zona indicada no existe o esta inactiva.",
        )
    return location


def create_cold_location(db: Session, payload: ColdLocationCreate) -> ColdLocation:
    _ensure_location_name_available(db, payload.name)
    data = payload.model_dump()
    data["location_type"] = payload.location_type.value
    location = ColdLocation(**data, is_active=True)
    return add(db, location)


def update_cold_location(db: Session, location_id: int, payload: ColdLocationUpdate) -> ColdLocation:
    location = get_by_id(db, ColdLocation, location_id)
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La camara o zona indicada no existe.",
        )

    changes = payload.model_dump(exclude_unset=True)
    if "name" in changes:
        _ensure_location_name_available(db, changes["name"], current_location_id=location.id)
        location.name = changes["name"]
    if "location_type" in changes and changes["location_type"] is not None:
        location.location_type = changes["location_type"].value
    for field in ("description", "min_temperature", "max_temperature", "min_humidity", "max_humidity"):
        if field in changes:
            setattr(location, field, changes[field])
    if "is_active" in changes and changes["is_active"] is not None:
        location.is_active = changes["is_active"]

    db.flush()
    db.refresh(location)
    return location


def delete_cold_location(db: Session, location_id: int) -> None:
    location = get_by_id(db, ColdLocation, location_id)
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La camara o zona indicada no existe.",
        )
    location.is_active = False
    db.flush()


def list_cold_locations(db: Session) -> list[ColdLocation]:
    return list(db.scalars(select(ColdLocation).order_by(ColdLocation.name)).all())


def create_sensor(db: Session, payload: SensorCreate) -> SensorDevice:
    _get_active_location(db, payload.cold_location_id)
    _ensure_sensor_name_available(db, payload.name)

    sensor = SensorDevice(
        cold_location_id=payload.cold_location_id,
        name=payload.name,
        sensor_type=payload.sensor_type.value,
        is_active=True,
    )
    return add(db, sensor)


def update_sensor(db: Session, sensor_id: int, payload: SensorUpdate) -> SensorDevice:
    sensor = get_by_id(db, SensorDevice, sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El sensor indicado no existe.",
        )

    changes = payload.model_dump(exclude_unset=True)
    if "name" in changes:
        _ensure_sensor_name_available(db, changes["name"], current_sensor_id=sensor.id)
        sensor.name = changes["name"]
    if "cold_location_id" in changes and changes["cold_location_id"] is not None:
        _get_active_location(db, changes["cold_location_id"])
        sensor.cold_location_id = changes["cold_location_id"]
    if "sensor_type" in changes and changes["sensor_type"] is not None:
        sensor.sensor_type = changes["sensor_type"].value
    if "is_active" in changes and changes["is_active"] is not None:
        sensor.is_active = changes["is_active"]

    db.flush()
    db.refresh(sensor)
    return sensor


def delete_sensor(db: Session, sensor_id: int) -> None:
    sensor = get_by_id(db, SensorDevice, sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El sensor indicado no existe.",
        )
    sensor.is_active = False
    db.flush()


def list_sensors(db: Session) -> list[SensorDevice]:
    return list(db.scalars(select(SensorDevice).order_by(SensorDevice.name)).all())


def list_sensor_readings(db: Session) -> list[SensorReading]:
    return list(db.scalars(select(SensorReading).order_by(SensorReading.recorded_at.desc(), SensorReading.id.desc())).all())


def create_sensor_reading(db: Session, sensor_id: int, payload: SensorReadingCreate) -> SensorReading:
    sensor = get_by_id(db, SensorDevice, sensor_id)
    if sensor is None or not sensor.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El sensor indicado no existe o esta inactivo.",
        )

    location = sensor.cold_location
    if not location.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La camara o zona del sensor esta inactiva.",
        )

    reading_data = payload.model_dump(exclude_none=True)
    reading = SensorReading(device_id=sensor_id, **reading_data)
    add(db, reading)

    if payload.temperature is not None and (
        (location.min_temperature is not None and payload.temperature < location.min_temperature)
        or (location.max_temperature is not None and payload.temperature > location.max_temperature)
    ):
        add(
            db,
            Alert(
                device_id=sensor.id,
                cold_location_id=location.id,
                alert_type=AlertType.TEMPERATURE.value,
                severity=AlertSeverity.MEDIUM.value,
                status=AlertStatus.OPEN.value,
                message=f"Temperatura fuera de rango: {payload.temperature} C.",
            ),
        )

    if payload.humidity is not None and (
        (location.min_humidity is not None and payload.humidity < location.min_humidity)
        or (location.max_humidity is not None and payload.humidity > location.max_humidity)
    ):
        add(
            db,
            Alert(
                device_id=sensor.id,
                cold_location_id=location.id,
                alert_type=AlertType.HUMIDITY.value,
                severity=AlertSeverity.MEDIUM.value,
                status=AlertStatus.OPEN.value,
                message=f"Humedad fuera de rango: {payload.humidity}%.",
            ),
        )

    return reading
