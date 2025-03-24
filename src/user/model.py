from sqlalchemy.orm import Mapped

from core.database import Base


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    age: Mapped[int]
