import pytest
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse

# AASA - Apple App Site Association


def test_aasa_url_set_properly():
    assert reverse("apple-app-site-association") == "/.well-known/apple-app-site-association"


@pytest.mark.django_db
def test_aasa_content(api_client):
    response = api_client.get(reverse("apple-app-site-association"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"test-field": "testing"}


NEW_AASA_CONTENT = {
    "test-file-field": {
        "foo": "bar",
    }
}


@pytest.mark.django_db
@override_settings(APPLE_APP_SITE_ASSOCIATION=NEW_AASA_CONTENT)
def test_aasa_custom(api_client):
    response = api_client.get(reverse("apple-app-site-association"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == NEW_AASA_CONTENT
