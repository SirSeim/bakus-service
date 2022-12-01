import pytest
from django.contrib.auth.models import User

from addition import models


@pytest.mark.django_db
def test_get_user_settings_nonexistent():
    user = User.objects.create_user("test")
    try:
        settings = models.get_user_settings(user)
    except Exception:
        assert False, "could not handle user without related UserSettings instance"
    assert hasattr(settings, "demo")
    assert not settings.demo


USER_SETTINGS_DEMO_OPTIONS = [
    True,
    False,
]


@pytest.mark.django_db
@pytest.mark.parametrize("demo_option", USER_SETTINGS_DEMO_OPTIONS)
def test_get_user_settings_exists(demo_option):
    user = User.objects.create_user("test")
    models.UserSettings.objects.create(user=user, demo=demo_option)
    try:
        settings = models.get_user_settings(user)
    except Exception:
        assert False, "could not handle user with related UserSettings instance"
    assert hasattr(settings, "demo")
    assert settings.demo == demo_option
