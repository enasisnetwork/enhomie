"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from fastapi.testclient import TestClient

from ...conftest import restful_factory

if TYPE_CHECKING:
    from ..service import HomieRestful
    from ...homie import Homie



def test_HomieRestful(
    restful: 'HomieRestful',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param restful: Ancilary Homie Automate class instance.
    """


    attrs = lattrs(restful)

    assert attrs == [
        '_HomieRestful__homie',
        '_HomieRestful__fastapi',
        '_HomieRestful__uvicorn',
        '_HomieRestful__thread',
        '_HomieRestful__stopped',
        '_HomieRestful__started']


    assert inrepr(
        'service.HomieRestful',
        restful)

    assert isinstance(
        hash(restful), int)

    assert instr(
        'service.HomieRestful',
        restful)


    assert restful.homie

    assert restful.params

    assert restful.fastapi

    assert not restful.running


    restful.start()


    thread = Thread(
        target=restful.operate)

    thread.start()


    block_sleep(5)

    assert restful.running

    restful.stop()

    while restful.running:
        block_sleep(1)  # NOCVR

    thread.join()

    assert not restful.running



def test_HomieRestful_forbid(
    client: TestClient,
    mismatch: TestClient,
    invalid: TestClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Used when testing the FastAPI endpoints.
    :param mismatch: Used when testing the FastAPI endpoints.
    :param invalid: Used when testing the FastAPI endpoints.
    """

    path = '/api/persists'


    response = client.get(path)

    assert response.status_code == 200


    response = mismatch.get(path)

    assert response.status_code == 401


    response = invalid.get(path)

    assert response.status_code == 401



def test_HomieRestful_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    params = (
        homie.params.restful)

    params.bind_port = 8428

    restful = (
        restful_factory(homie))


    restful.stop()
    restful.start()
    restful.start()
    restful.stop()
    restful.stop()
