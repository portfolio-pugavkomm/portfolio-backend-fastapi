from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, pk_int, str_256


class ResourceSkillModel(Base):
    __tablename__ = "resourse_skills"
    id: Mapped[pk_int]
    name: Mapped[str_256]
    weight: Mapped[int] = mapped_column(default=0)
