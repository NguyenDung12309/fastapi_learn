from src.core.security import password_hasher


def test_login_success(client_fixture, session_fixture):
    # 1. Chuẩn bị: Tạo một user mẫu trong DB test
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
