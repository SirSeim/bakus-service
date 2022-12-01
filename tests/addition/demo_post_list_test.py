import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests import test_models


@pytest.mark.django_db
def test_demo_post_list(demo_api_client):
    response = demo_api_client.post(reverse("addition-list"), {"magnet_link": "testurl"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == test_models.Torrent("demo_addition", "demo_addition", 0.0).get_json(include_files=False)
