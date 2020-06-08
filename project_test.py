import pytest
from django.contrib.auth.models import AnonymousUser, User


@pytest.fixture()
def db_setup(request):
    def db_teardown():
        pass
    request.addfinalizer(db_teardown)


def test_1_that_needs_setup(db_setup):
    pass


def test_2_that_does_not():
    pass
