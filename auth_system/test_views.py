import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from auth_system.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "username": "user",
        "password": "testpassword1122",
        "re_password": "testpassword1122"
    }


@pytest.fixture
def user_data_add():
    return {
        "email": "test@example.com",
        "username": "user",
        "password": "testpassword1122",
    }


@pytest.mark.django_db
def test_register_user(api_client, user_data):
    url = reverse('auth_system:register')
    response = api_client.post(url, data=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email=user_data['email']).exists()


@pytest.mark.django_db
def test_password_reset_request(api_client, create_user, user_data_add):
    user = create_user(**user_data_add)
    url = reverse('auth_system:reset_password')
    data = {
        "email": user.email,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

# @pytest.fixture
# def activated_user_data():
#     return {
#         "email": "activated@example.com",
#         "username": "activeuser",
#         "password": "testpassword",
#         "is_active": True,
#     }


# @pytest.mark.django_db
# def test_user_activation(api_client, create_user, activated_user_data):
#     user = create_user(**activated_user_data)
#     url = reverse('auth_system:activated_account')
#     data = {
#         "email": user.email,
#         "activation_code": 82391,
#     }
#     response = api_client.post(url, data)
#     assert response.status_code == status.HTTP_200_OK
#     assert User.objects.get(email=user.email).is_active is True


# @pytest.mark.django_db
# def test_password_reset_confirm(api_client, create_user, user_data):
#     user = create_user(**user_data)
#     url = reverse('auth_system:reset_password_confirm')
#     new_password = "newtestpassword"
#     data = {
#         "email": user.email,
#         "new_password": new_password,
#     }
#     response = api_client.patch(url, data, format='json')
#     assert response.status_code == status.HTTP_200_OK
#     assert User.objects.get(email=user.email).check_password(new_password)
