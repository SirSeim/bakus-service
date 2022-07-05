import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse

from tests import test_constants


@pytest.mark.django_db
def test_get_account(api_client):
    response = api_client.get(reverse("account-detail"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "username": test_constants.USER_USERNAME,
        "email": "",
        "first_name": "",
        "last_name": "",
    }


@pytest.mark.django_db
def test_get_complete_account(api_client):
    user = User.objects.get(username=test_constants.USER_USERNAME)
    user.username = test_constants.ALT_USERNAME
    user.email = test_constants.ALT_EMAIL
    user.first_name = test_constants.ALT_FIRST_NAME
    user.last_name = test_constants.ALT_LAST_NAME
    user.save()

    response = api_client.get(reverse("account-detail"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == test_constants.ALT_USER_DETAILS
