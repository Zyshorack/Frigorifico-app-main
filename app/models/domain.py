from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False, default="operator")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("product_categories.id"))
    code: Mapped[str | None] = mapped_column(String(60), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    weight: Mapped[float | None] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(20), nullable=False, default="kg")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    category: Mapped[ProductCategory | None] = relationship(back_populates="products")
    batches: Mapped[list["Batch"]] = relationship(back_populates="product")


class ColdLocation(Base):
    __tablename__ = "cold_locations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    location_type: Mapped[str] = mapped_column(String(30), nullable=False, default="chamber")
    description: Mapped[str | None] = mapped_column(Text)
    min_temperature: Mapped[float | None] = mapped_column(Float)
    max_temperature: Mapped[float | None] = mapped_column(Float)
    min_humidity: Mapped[float | None] = mapped_column(Float)
    max_humidity: Mapped[float | None] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sensors: Mapped[list["SensorDevice"]] = relationship(back_populates="cold_location")
    batches: Mapped[list["Batch"]] = relationship(back_populates="cold_location")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="cold_location")


class SensorDevice(Base):
    __tablename__ = "sensor_devices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cold_location_id: Mapped[int] = mapped_column(ForeignKey("cold_locations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(30), nullable=False, default="mixed")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    cold_location: Mapped[ColdLocation] = relationship(back_populates="sensors")
    readings: Mapped[list["SensorReading"]] = relationship(back_populates="device")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="device")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("sensor_devices.id"), nullable=False)
    temperature: Mapped[float | None] = mapped_column(Float)
    humidity: Mapped[float | None] = mapped_column(Float)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    device: Mapped[SensorDevice] = relationship(back_populates="readings")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("sensor_devices.id"))
    cold_location_id: Mapped[int | None] = mapped_column(ForeignKey("cold_locations.id"))
    alert_type: Mapped[str] = mapped_column(String(30), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="open")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    action_description: Mapped[str | None] = mapped_column(Text)
    resolved_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    device: Mapped[SensorDevice | None] = relationship(back_populates="alerts")
    cold_location: Mapped[ColdLocation | None] = relationship(back_populates="alerts")
    resolved_by_user: Mapped[User | None] = relationship()

    @property
    def resolved_by_username(self) -> str | None:
        return self.resolved_by_user.username if self.resolved_by_user else None


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    cold_location_id: Mapped[int | None] = mapped_column(ForeignKey("cold_locations.id"))
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    remaining_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    supplier: Mapped[str | None] = mapped_column(String(120))
    document_number: Mapped[str | None] = mapped_column(String(120))
    entry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")

    product: Mapped[Product] = relationship(back_populates="batches")
    cold_location: Mapped[ColdLocation | None] = relationship(back_populates="batches")


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False)
    cold_location_id: Mapped[int | None] = mapped_column(ForeignKey("cold_locations.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    movement_type: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    product: Mapped[Product] = relationship()
    batch: Mapped[Batch] = relationship()
    cold_location: Mapped[ColdLocation | None] = relationship()
    user: Mapped[User | None] = relationship()

    @property
    def user_name(self) -> str | None:
        return self.user.username if self.user else None
