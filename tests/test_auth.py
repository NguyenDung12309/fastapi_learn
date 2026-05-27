from unittest.mock import patch

import pytest

from src.core.security import password_hasher
from src.models import UserModel


def test_login_success(client_fixture, session_fixture):
    from src.models.user_model import UserModel
    from src.common.enum_common import UserRole
    raw_password = "Aa123456@"
    init_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": password_hasher.hash(raw_password),
        "role": UserRole.USER,
        "is_verified": True
    }
    test_user = UserModel(**init_data)
    session_fixture.add(test_user)
    session_fixture.commit()

    response = client_fixture.post(
        "/api/v1/auth/login",
        json={"username": init_data['username'], "password": raw_password}
    )

    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token"] is not None
    assert data["refresh_token"] is not None
    assert isinstance(data["access_token"], str)
    assert isinstance(data["refresh_token"], str)


def test_login_wrong_password(client_fixture, session_fixture):
    response = client_fixture.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Tài khoản hoặc mật khẩu không chính xác"


def test_register_success(client_fixture, session_fixture):
    raw_password = "Aa123456@"
    init_data = {
        "username": "testuser_unique",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": raw_password,
    }

    with patch("src.services.email_service.EmailService.send_registration_email") as mock_email:
        mock_email.return_value = True

        # Gửi request bên trong khối with
        response = client_fixture.post(
            "/api/v1/auth/register",
            json=init_data
        )

        assert response.status_code == 200
        data = response.json()

        mock_email.assert_called_once()

    # 5. Kiểm tra Schema (bên ngoài block mock cũng được)
    try:
        # Lưu ý: UserModel thường yêu cầu ID và các trường DB khác.
        # Nếu 'data' trả về từ API có đầy đủ, dòng này sẽ pass.
        UserModel(**data)
    except Exception as e:
        pytest.fail(f"Response data không khớp với Schema: {e}")
