from typing import TypeVar, Sequence, ClassVar

from pydantic import BaseModel, model_validator


T = TypeVar("T")


class AtLeastOneFieldRequired(BaseModel):
    """A model for use in places where several optional fields are specified, where at least one must be specified

    It's useful to use in filtering, when, for example, we define several restrictive fields, that somehow limit the
    query. It least one filter is missing, then, for example, the output may be large (or large query),
    the class solves such a problem.

    To use, you must specify `_required_fields`, which are objects of the sequence type.

    If necessary, you can override the class method `get_required_fields`, which initially simply uses a sequence
    from `required_fields`.
    """

    _required_fields: ClassVar[Sequence[str] | None] = None

    @classmethod
    def get_required_fields(cls) -> Sequence[str]:
        if cls._required_fields is None:
            raise NotImplementedError(
                "Subclass must define a 'required_fields' attribute or 'get_required_fields class method "
            )
        return cls._required_fields

    @model_validator(mode="before")
    @classmethod
    def at_least_one_required(cls, data: T) -> T:
        if not isinstance(data, dict):
            return data
        required_fields = cls.get_required_fields()
        if not any(data.get(field) is not None for field in required_fields):
            raise ValueError("At least one field must be provided. ")
        return data
