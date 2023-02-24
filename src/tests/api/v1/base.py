import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db()
class TestBase:
    _url: str = None

    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        return reverse(cls._url, args, kwargs)
