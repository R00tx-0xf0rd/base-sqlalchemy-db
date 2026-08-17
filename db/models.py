from __future__ import annotations
from datetime import UTC, datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Bank(Base):
    __tablename__ = "banks"
    id: Mapped[int] = mapped_column(primary_key=True)
    bank_name: Mapped[str]
    bank_url: Mapped[str]
    rates: Mapped[list["Course"]] = relationship(back_populates="bank")


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))
    dt: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    usd_buy: Mapped[float] = mapped_column()
    usd_sell: Mapped[float] = mapped_column()
    eur_buy: Mapped[float] = mapped_column()
    eur_sell: Mapped[float] = mapped_column()
    bank: Mapped["Bank"] = relationship(back_populates="rates")
