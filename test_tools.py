import pytest

from tools import createToken


@pytest.fixture
def get_create_token():
    return createToken("username","password")


