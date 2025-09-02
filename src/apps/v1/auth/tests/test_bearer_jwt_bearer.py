from typing import Any
from unittest.mock import patch

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from src.apps.v1.auth.bearers import JWTBearer

MOCK_DECODE_JWT_SERVICE = "src.apps.v1.auth.bearers.decode_jwt_service"

app = FastAPI()
jwt_bearer = JWTBearer()


client = TestClient(app)


@app.get("/protected")
async def protected_route(credentials=Depends(jwt_bearer)) -> dict[str, Any]:
    return {"message": "Access granted!", "token_type": credentials.scheme}


# static method  JWTBearer.verify_jwt
def test_should_return_true() -> None:
    with patch(MOCK_DECODE_JWT_SERVICE, return_value={"id": "data"}) as jwt_service_mock:
        result = JWTBearer.verify_jwt("some_jwt")
    jwt_service_mock.assert_called_once_with("some_jwt")
    assert result


def _test_should_return_false() -> None:
    with patch(MOCK_DECODE_JWT_SERVICE, return_value=None) as jwt_service_mock:
        result = JWTBearer.verify_jwt("some_jwt")
    jwt_service_mock.assert_called_once_with("some_jwt")
    assert not result


# JWTBearer
def test_access_for_success_valid_token() -> None:
    headers = {"Authorization": "Bearer valid_token"}

    with patch(MOCK_DECODE_JWT_SERVICE, return_value={"id": "data"}) as jwt_service_mock:
        response = client.get("/protected", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Access granted!", "token_type": "Bearer"}
    jwt_service_mock.assert_called_once_with("valid_token")


def test_should_denied_for_failed_invalid_token() -> None:
    headers = {"Authorization": "Bearer invalid_token"}

    with patch(MOCK_DECODE_JWT_SERVICE, return_value=None) as jwt_service_mock:
        response = client.get("/protected", headers=headers)

    assert response.status_code == 403
    jwt_service_mock.assert_called_once_with("invalid_token")


def test_should_denied_for_failure_invalid_scheme() -> None:
    headers = {"Authorization": "StrangeSchema invalid_token"}

    with patch(MOCK_DECODE_JWT_SERVICE, return_value={"id": "data"}) as jwt_service_mock:
        response = client.get("/protected", headers=headers)
    jwt_service_mock.assert_not_called()
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid authentication credentials"}
