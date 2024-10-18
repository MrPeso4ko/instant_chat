from sqlalchemy.orm import mapped_column, Mapped

from db import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes]
    salt: Mapped[bytes]

    name: Mapped[str] = mapped_column(unique=True)
