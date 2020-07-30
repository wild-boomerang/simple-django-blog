import pytest
from django.contrib.auth.models import AnonymousUser, User


@pytest.fixture()
def db_setup(request):
    def db_teardown():
        pass
    request.addfinalizer(db_teardown)


@pytest.yield_fixture()
def func():
    print('setup')
    yield
    print('teardown')


@pytest.mark.parametrize('x', [3, 2], ids=['x = 3', 'x = 2'])
@pytest.mark.parametrize('y', [0, 1], ids=['y = 0', 'y = 3'])
def test_parametrize(x, y):
    assert x > y


def test_1_that_needs_setup(db_setup):
    pass


def test_2_that_does_not():
    pass
