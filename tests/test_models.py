import pytest


@pytest.mark.django_db
def test_simple():
        assert 1 == 1