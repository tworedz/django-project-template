import base64

from django.conf import settings
from django.core.management import call_command
import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture(autouse=True, scope="session")
def _django_fixtures_setup(django_db_setup, django_db_blocker) -> None:
    # TODO: fixtures
    fixtures = []
    if fixtures:
        with django_db_blocker.unblock():
            call_command("loaddata", *fixtures)


@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_api_client(api_client: APIClient, default_user) -> APIClient:
    token, _ = Token.objects.get_or_create(user=default_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.fixture()
def basic_auth_api_client(api_client: APIClient) -> APIClient:
    credentials = base64.b64encode(
        f"{settings.ONE_C_BASE_USERNAME}:{settings.ONE_C_BASE_PASSWORD}".encode(),
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials.decode()}")
    return api_client
