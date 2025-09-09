from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, pk_int, str_256


class ResourceSkillModel(Base):
    __tablename__ = "resource_skills"
    id: Mapped[pk_int]
    name: Mapped[str_256]
    weight: Mapped[int] = mapped_column(default=0)  # TODO: Small integer

    def __repr__(self) -> str:
        return f"{self.name} {self.weight}"


class ResourceTechnology(Base):
    __tablename__ = "resource_technologies"
    id: Mapped[pk_int]
    name: Mapped[str_256]

    def __repr__(self) -> str:
        return f"ID({self.id}){self.name}"


class ResourceWorkTimeLineItemModel(Base):
    __tablename__ = "resource_work_timeline_items"
    id: Mapped[pk_int]
    name: Mapped[str_256]
    start_year: Mapped[int]
    end_year: Mapped[int | None]
    description: Mapped[str]
    technology: Mapped[set["ResourceWorkTimeLineTechnologyAssociation"]] = relationship(
        secondary="association_resource_work_timeline_item_resource_technology",
        back_populates="work_timeline",
    )

    def __repr__(self) -> str:
        return f"ID({self.id}){self.name} {self.start_year}-{self.end_year}"


class ResourceWorkTimeLineTechnologyAssociation(Base):
    __tablename__ = "association_resource_work_timeline_item_resource_technology"
    technology_id: Mapped[pk_int] = mapped_column(ForeignKey("resource_technologies.id"))
    work_timeline_id: Mapped[pk_int] = mapped_column(ForeignKey("resource_work_timeline_items.id"))
    weight: Mapped[int] = mapped_column(SmallInteger(), default=0)
