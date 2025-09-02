from .models import UserModel

"""
Get user model for future flexible update.

Returns:
    user model. At this moment returns only UserModel
"""
def get_user_model_util() -> type[UserModel]:
    return UserModel