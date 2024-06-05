from .utils import *
from Fast_Api.routers.users import get_current_user, get_db
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'patman'
    assert response.json()['email'] == 'pati.muru@gmail.com'
    assert response.json()['first_name'] == 'pati'
    assert response.json()['last_name'] == 'murusidze'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '599930419'



def test_change_password_success(test_user):
    response = client.put('/users/password', json={'password': 'pati1234', 'new_password': 'pati123'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_user_password(test_user):
    response = client.put('/users/password', json={'password': 'wrong_password', 'new_password': 'pati123'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}



def test_change_phone_number_success(test_user):
    response = client.put('users/update_number/', json={'phone_number': 599930419, 'new_phone_number': 59930319})
    assert response.status_code == status.HTTP_204_NO_CONTENT
