from typing import (
    Literal,
)

from fastapi import (
    FastAPI,
)

app = FastAPI(
    description="Portfolio project",
    docs_url="/schema/swagger/",
    redoc_url="/schema/redoc/",
)


@app.get("/hello-world/")
def hello_world() -> dict[Literal["Hello"], Literal["World"]]:
    return {"Hello": "World"}
