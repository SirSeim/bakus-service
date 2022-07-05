import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse

from tests import test_constants


@pytest.mark.django_db
def test_put_account(api_client):
    response = api_client.put(reverse("account-detail"), test_constants.ALT_USER_DETAILS)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == test_constants.ALT_USER_DETAILS
    user = User.objects.get(username=test_constants.ALT_USERNAME)
    assert user.email == test_constants.ALT_EMAIL
    assert user.first_name == test_constants.ALT_FIRST_NAME
    assert user.last_name == test_constants.ALT_LAST_NAME
