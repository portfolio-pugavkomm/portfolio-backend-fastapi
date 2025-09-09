from pydantic import BaseModel, Field

from src.schemas_base.at_least_one_required import AtLeastOneFieldRequired


class AddResourceSkillSchema(BaseModel):
    name: str = Field(...)
    weight: int = Field(...)


class ResourceSkillSchema(AddResourceSkillSchema):
    id: int = Field(...)


class ResourceSkillPartialSchema(AtLeastOneFieldRequired):
    _required_fields = ("name", "weight")
    name: str | None = Field(None)
    weight: int | None = Field(None)
