import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from common import hash_id
from tests import test_models


@pytest.mark.django_db
def test_demo_get_detail(demo_api_client):
    response = demo_api_client.get(reverse("addition-detail", args=[hash_id("non-existent")]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == test_models.Torrent(
        id="non-existent",
        name="demo_addition_1",
        progress=50.0,
    ).get_json(include_files=False)


@pytest.mark.django_db
def test_demo_get_list_to_get_detail(demo_api_client):
    list_response = demo_api_client.get(reverse("addition-list"))
    assert list_response.status_code == status.HTTP_200_OK
    first_addition = list_response.data["results"][0]
    detail_response = demo_api_client.get(reverse("addition-detail", args=[first_addition["id"]]))
    assert detail_response.status_code == status.HTTP_200_OK
    assert detail_response.data == test_models.Torrent(
        id="demo_addition_1",
        name="demo_addition_1",
        progress=50.0,
    ).get_json(include_files=False)
