import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.routes import app
from api.models import get_session, Base, Users

DATABASE_URL_TEST = "postgresql+psycopg2://postgres:63ponira@localhost/test_twitter"
engine_test = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(engine_test)


def override_get_async_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def create_users():
    with TestingSessionLocal() as session:
        first_user = Users(name="Дмитрий", api_key="test")
        second_user = Users(name="Андрей", api_key="test1")

        session.add(first_user)
        session.add(second_user)

        session.commit()


client = TestClient(app)
