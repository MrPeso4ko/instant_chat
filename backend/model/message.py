from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

if TYPE_CHECKING:
    from model import Chat


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    chat_id: Mapped[int] = mapped_column(ForeignKey('chat.id'), nullable=False)
    from_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    text: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())