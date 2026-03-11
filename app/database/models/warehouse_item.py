# app/database/models/warehouse_item.py
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class WarehouseItem(Base):
    __tablename__ = "warehouse_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity_pieces: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quantity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
