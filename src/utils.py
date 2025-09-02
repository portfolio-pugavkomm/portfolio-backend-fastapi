from src.apps.v1.auth.models import UserModel

"""
Get user model for future flexible update.

Returns:
    user model. At this moment returns only UserModel from auth app inside v1 """


def get_user_model_util() -> type[UserModel]:
    return UserModel
