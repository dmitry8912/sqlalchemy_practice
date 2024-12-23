import datetime
import decimal
import uuid
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

DeclarativeMeta: orm.DeclarativeMeta = orm.declarative_base()


class User(DeclarativeMeta):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name: str = sa.Column(sa.String, nullable=False)

    balance: int = sa.Column(sa.Integer, nullable=False, default=0)

    timestamp: datetime.datetime = sa.Column(
        sa.DateTime(timezone=False), nullable=False, default=func.now()
    )

    user_orders: Mapped[List["Order"]] = relationship(lazy="selectin", overlaps="owner")

    def __str__(self) -> str:
        return f"User: {self.name} ({self.balance} $)"


class Order(DeclarativeMeta):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    amount: int = sa.Column(sa.Integer, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)

    owner: Mapped["User"] = relationship(lazy="select", overlaps="user_orders")

    timestamp: datetime.datetime = sa.Column(
        sa.DateTime(timezone=False), nullable=False, default=func.now()
    )

    def __str__(self) -> str:
        return f"Order for: {self.user_id} for {self.amount} $"
