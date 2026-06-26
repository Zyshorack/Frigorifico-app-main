from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    OPERATOR = "operator"
    CLIENT = "client"


class LocationType(StrEnum):
    CHAMBER = "chamber"
    FREEZER = "freezer"
    FRIDGE = "fridge"
    WAREHOUSE = "warehouse"


class ProductUnit(StrEnum):
    KG = "kg"
    G = "g"
    LITERS = "litros"
    UNIT = "unidad"


class SensorType(StrEnum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    MIXED = "mixed"


class AlertType(StrEnum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    STOCK = "stock"
    EXPIRATION = "expiration"
    MANUAL = "manual"


class AlertSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class BatchStatus(StrEnum):
    ACTIVE = "active"
    EXHAUSTED = "exhausted"
    EXPIRED = "expired"
    QUARANTINED = "quarantined"
    DISCARDED = "discarded"


class StockMovementType(StrEnum):
    ENTRY = "entry"
    EXIT = "exit"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    DISCARD = "discard"
