from typing import Literal

from fastapi import FastAPI

from src.config import get_app_settings

settings = get_app_settings()
app = FastAPI(
    title=settings.API_NAME,
    description="Portfolio project",
    docs_url="/schema/swagger/",
    redoc_url="/schema/redoc/",
)


@app.get("/hello-world/")
def hello_world() -> dict[
    Literal["Hello"],
    Literal["World"],
]:
    return {"Hello": "World"}
