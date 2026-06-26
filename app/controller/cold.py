from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dto.cold import ColdLocationCreate, ColdLocationRead, ColdLocationUpdate
from app.dto.sensors import SensorCreate, SensorRead, SensorReadingCreate, SensorReadingRead, SensorUpdate
from app.models import ColdLocation, SensorDevice, SensorReading
from app.services import cold_service

router = APIRouter(tags=["Frio"])


@router.post("/cold-locations", response_model=ColdLocationRead, status_code=status.HTTP_201_CREATED)
def create_cold_location(payload: ColdLocationCreate, db: Session = Depends(get_db)) -> ColdLocation:
    return cold_service.create_cold_location(db, payload)


@router.get("/cold-locations", response_model=list[ColdLocationRead])
def list_cold_locations(db: Session = Depends(get_db)) -> list[ColdLocation]:
    return cold_service.list_cold_locations(db)


@router.patch("/cold-locations/{location_id}", response_model=ColdLocationRead)
def update_cold_location(location_id: int, payload: ColdLocationUpdate, db: Session = Depends(get_db)) -> ColdLocation:
    return cold_service.update_cold_location(db, location_id, payload)


@router.delete("/cold-locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cold_location(location_id: int, db: Session = Depends(get_db)) -> Response:
    cold_service.delete_cold_location(db, location_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/sensors", response_model=SensorRead, status_code=status.HTTP_201_CREATED)
def create_sensor(payload: SensorCreate, db: Session = Depends(get_db)) -> SensorDevice:
    return cold_service.create_sensor(db, payload)


@router.get("/sensors", response_model=list[SensorRead])
def list_sensors(db: Session = Depends(get_db)) -> list[SensorDevice]:
    return cold_service.list_sensors(db)


@router.get("/sensor-readings", response_model=list[SensorReadingRead])
def list_sensor_readings(db: Session = Depends(get_db)) -> list[SensorReading]:
    return cold_service.list_sensor_readings(db)


@router.patch("/sensors/{sensor_id}", response_model=SensorRead)
def update_sensor(sensor_id: int, payload: SensorUpdate, db: Session = Depends(get_db)) -> SensorDevice:
    return cold_service.update_sensor(db, sensor_id, payload)


@router.delete("/sensors/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)) -> Response:
    cold_service.delete_sensor(db, sensor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/sensors/{sensor_id}/readings", response_model=SensorReadingRead, status_code=status.HTTP_201_CREATED)
def create_sensor_reading(
    sensor_id: int,
    payload: SensorReadingCreate,
    db: Session = Depends(get_db),
) -> SensorReading:
    return cold_service.create_sensor_reading(db, sensor_id, payload)
