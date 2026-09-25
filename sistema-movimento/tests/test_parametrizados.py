import pytest


@pytest.mark.parametrize(
    "dispositivo_id",
    [1, 2, 3, 4, 5]
)
def test_dispositivo_valido(dispositivo_id):

    assert dispositivo_id > 0