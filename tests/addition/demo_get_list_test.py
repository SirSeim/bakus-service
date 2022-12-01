import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests import test_models


@pytest.mark.django_db
def test_demo_get_list(demo_api_client):
    response = demo_api_client.get(reverse("addition-list"))
    assert response.status_code == status.HTTP_200_OK
    expected = [
        test_models.Torrent("demo_addition_1", "demo_addition_1", 0.5).get_json(include_files=False),
        test_models.Download("demo_addition_2").get_json(),
    ]
    assert response.data.get("count") == len(expected)
    assert response.data.get("results") == expected
