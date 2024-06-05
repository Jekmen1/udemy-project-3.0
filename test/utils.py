from fastapi.testclient import TestClient
from Fast_Api.database import Base
import pytest
from Fast_Api.models import Todos, Users
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..main import app
from Fast_Api.routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'patman', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(
        title='Learn to code',
        description='need to learn everyday',
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("Delete FROM todos;"))
        connection.commit()


@pytest.fixture()
def test_user():
    user = Users(
        username='patman',
        email='pati.muru@gmail.com',
        first_name='pati',
        last_name='murusidze',
        hashed_password=bcrypt_context.hash('pati1234'),
        role='admin',
        phone_number=599930419
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("Delete FROM users;"))
        connection.commit()