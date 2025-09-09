from typing import Any, TypeVar

from sqlalchemy.orm import DeclarativeBase

from src.apps.v1.auth.models import UserModel


def get_user_model_util() -> type[UserModel]:
    """
    Get user model for future flexible update.

    Returns:
        user model. At this moment returns only UserModel from auth app inside v1
    """

    return UserModel


T = TypeVar("T", bound=DeclarativeBase)


def update_model_attributes_from_dict(model: T, data: dict[str, Any], strict: bool = True) -> T:
    """Update model attributes from dictionary

    Args:
        model: SQLAlchemy model instance
        data: data for model
        strict: if true then perform getattr

    Returns:
        updated instance

    Raises:
        AttributeError: if at least one dictionary key does not match an instance attribute

    """
    if strict:
        for k in data.keys():
            getattr(model, k)

    for k, v in data.items():
        setattr(model, k, v)
    return model
