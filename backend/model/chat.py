from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db import Base


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    second_user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('first_user_id', 'second_user_id', name='_first_second_user_uc'),
        CheckConstraint('first_user_id < second_user_id', name='_first_second_user_check')
    )

    first_user = relationship("User", foreign_keys=[first_user_id], lazy='selectin')
    second_user = relationship("User", foreign_keys=[second_user_id], lazy='selectin')
