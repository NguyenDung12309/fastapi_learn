import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from sqlmodel.pool import StaticPool
from starlette.testclient import TestClient

from src.__init__ import app
from src.db.main import db_manager

sqlite_url = "sqlite://"  # tạo database tren RAM
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},  # cho phép nhiều thread kết nối
    poolclass=StaticPool  # giữ cho kết nối SQLite In-memory luôn mở trong suốt phiên làm việc
)


@pytest.fixture
def session_fixture():
    SQLModel.metadata.create_all(engine)  # Tạo các bảng trong DB vào engine
    with Session(engine) as session:  # kết nối engine khởi tạo session
        yield session
    SQLModel.metadata.drop_all(engine)  # drop database


@pytest.fixture()
def client_fixture(session_fixture: Session):
    # Override dependency get_db để sử dụng session test
    def get_session_override():
        return session_fixture

    app.dependency_overrides[db_manager.get_db] = get_session_override
    client = TestClient(app)  # tạo ra một đối tượng có khả năng gửi request
    yield client
    app.dependency_overrides.clear()
