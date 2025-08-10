from src.config import get_app_settings
import importlib

settings = get_app_settings()
_model_file_name = settings.MODEL_FILE_NAME[:-3]

for app in settings.INSTALLED_APPS:
    try:
        importlib.import_module(f"{app}.{_model_file_name}")
        print("Imported app", app)
    except ModuleNotFoundError as e:
        print("Error", e)  # TODO: Replace by logging
        continue
