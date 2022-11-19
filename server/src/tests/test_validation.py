import pytest

from telegram.validation import validate_init_data


@pytest.fixture
def init_data():
    return {
        "query_id": "AAG5caYEAAAAALlxpgSWlZde",
        "user": {
            "id": 1,
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "username": "IIvanov",
            "language_code": "ru"
        },
        "auth_date": "1657916614",
        "hash": "979d8a3a3580f96cbe0f5c7db6d3798fb76278a47c05bec58826a5cac97bc8c2"
    }


@pytest.fixture
def bot_token():
    return 'bottoken'


def test_verification_raw(bot_token, init_data):
    assert validate_init_data(init_data, bot_token)
