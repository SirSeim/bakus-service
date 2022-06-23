import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from tests import test_constants


def login(create_user=True) -> tuple[Response, APIClient]:
    if create_user:
        User.objects.create_user(username=test_constants.USER_USERNAME, password=test_constants.USER_PASSWORD)
    client = APIClient()
    res = client.post(reverse("knox_login"), test_constants.USER_LOGIN)
    assert res.status_code == status.HTTP_200_OK
    client.credentials(HTTP_AUTHORIZATION=f"Token {res.data['token']}")
    return res, client


@pytest.mark.django_db
def test_basic_login():
    res, _ = login()
    assert set(res.data.keys()) == {"expiry", "token"}


@pytest.mark.django_db
def test_fail_login():
    client = APIClient()
    res = client.post(reverse("knox_login"), test_constants.USER_LOGIN)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_logout():
    _, client = login()
    res = client.post(reverse("knox_logout"))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    # trying to logout again should fail since it's already logged out
    res = client.post(reverse("knox_logout"))
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
