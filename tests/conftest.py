import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def setup(mocker: MockerFixture):
    mocker.patch("all_weather.portfolio.get_price", return_value=100.0)
