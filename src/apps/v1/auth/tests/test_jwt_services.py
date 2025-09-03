import time
import uuid

import jwt
import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture

from ..config import AuthConfig, get_config
from ..services import decode_jwt_service, jwt_services, refresh_token_service, sign_jwt_service


def test_decode_jwt_service_should_decode_correctly() -> None:
    settings = get_config()
    payload = {
        "user_id": "uuid",
        "type": "access",
        "expires": time.time() + 1000,  # Should alive
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    decoded_token = decode_jwt_service(token)
    assert decoded_token == payload


def test_decode_jwt_service_should_return_none_for_token_expired() -> None:
    settings = get_config()
    payload = {
        "user_id": "uuid",
        "type": "access",
        "expires": time.time() - 1000,  # Should alive
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    decoded_token = decode_jwt_service(token)
    assert decoded_token is None


def test_decode_jwt_service_should_return_none_for_wrong_token() -> None:
    token = "Wrong token"
    decoded_token = decode_jwt_service(token)
    assert decoded_token is None


def test_sign_jwt_service_should_sign_without_refresh() -> None:
    user_id = uuid.uuid4()
    tokens = sign_jwt_service(user_id, False)

    assert tokens.refresh is None
    assert isinstance(tokens.access, str)


def test_sign_jwt_service_should_sign_with_refresh() -> None:
    user_id = uuid.uuid4()
    tokens = sign_jwt_service(user_id, True)

    assert isinstance(tokens.refresh, str)
    assert isinstance(tokens.access, str)


def test_sign_jwt_service_should_be_decodable_with_configured_secret_key() -> None:
    settings = get_config()
    user_id = uuid.uuid4()
    tokens = sign_jwt_service(user_id, True)

    access_token_payload = jwt.decode(tokens.access, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    refresh_token_payload = jwt.decode(tokens.refresh, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

    assert isinstance(access_token_payload, dict)
    assert isinstance(refresh_token_payload, dict)

    assert access_token_payload["type"] == "access"
    assert refresh_token_payload["type"] == "refresh"


def test_refresh_token_service_should_refresh_only_access(mocker: MockerFixture) -> None:
    user_id = uuid.uuid4()
    config = AuthConfig(ROTATE_REFRESH=False)
    mocker.patch.object(jwt_services, "settings", new=config)
    refresh_token = sign_jwt_service(user_id, True).refresh
    sign_jwt_mock = mocker.patch.object(jwt_services, "sign_jwt_service")
    refresh_token_service(refresh_token)
    sign_jwt_mock.assert_called_once_with(str(user_id), False)


def test_refresh_token_service_should_refresh_both_access_and_refresh(mocker: MockerFixture) -> None:
    user_id = uuid.uuid4()
    config = AuthConfig(ROTATE_REFRESH=True)
    mocker.patch.object(jwt_services, "settings", new=config)
    refresh_token = sign_jwt_service(user_id, True).refresh
    sign_jwt_mock = mocker.patch.object(jwt_services, "sign_jwt_service")
    refresh_token_service(refresh_token)
    sign_jwt_mock.assert_called_once_with(str(user_id), True)


def test_refresh_token_service_should_raise_401() -> None:
    token_wrong = "sdasd"
    with pytest.raises(HTTPException) as excinfo:
        refresh_token_service(token_wrong)
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Wrong token or expired"


def test_refresh_token_service_should_raise_401_wrong_type() -> None:
    token_payload = {"expires": time.time() + 100, "type": "wrong_type"}
    settings = get_config()
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        refresh_token_service(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Wrong token type"


def test_refresh_token_service_should_raise_401_expired() -> None:
    token_payload = {"expires": time.time() - 100, "type": "wrong_type"}
    settings = get_config()
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        refresh_token_service(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Wrong token or expired"
