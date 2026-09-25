import pytest


def validar_dispositivo(dispositivo_id):

    if dispositivo_id <= 0:

        raise ValueError("ID do dispositivo inválido.")

    return True


def test_dispositivo_valido():

    resultado = validar_dispositivo(1)

    assert resultado == True


def test_dispositivo_invalido():

    with pytest.raises(ValueError):

        validar_dispositivo(0)