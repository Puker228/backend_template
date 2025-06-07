from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column()
    login: Mapped[str] = mapped_column(unique=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
