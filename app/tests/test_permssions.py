import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from main import app1
from app.db.session import get_db
from app.core.security import hash_password
from app.db.models.user import User

@pytest.fixture(scope="module")
def test_db():
    """ Devuelve una sesión de prueba con rollback después de cada test. """
    db: Session = next(get_db())
    yield db
    db.rollback()

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.fixture
def create_users(test_db):
    def create(role, email):
        user = User(
            username=email.split("@")[0],
            email=email,
            hashed_password=hash_password("password123"),
            role=role
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        return user
    return create

@pytest.fixture
async def get_token(client, create_users):
    async def login_user(role):
        email = f"{role}@test.com"
        create_users(role, email)
        response = await client.post("/api/v1/auth/login", data={
            "username": email.split("@")[0],  # login es por username
            "password": "password123"
        })
        return response.json()["access_token"]
    return login_user
