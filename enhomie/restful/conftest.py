"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from base64 import b64encode
from typing import TYPE_CHECKING

from fastapi.testclient import TestClient

from pytest import fixture

if TYPE_CHECKING:
    from .service import HomieRestful



@fixture
def client(
    restful: 'HomieRestful',
) -> TestClient:
    """
    Construct the instance for use in the downstream tests.

    :param restful: Ancilary Homie Automate class instance.
    :returns: Newly constructed instance of related class.
    """

    return _create_client(
        restful,
        'username:password')



@fixture
def mismatch(
    restful: 'HomieRestful',
) -> TestClient:
    """
    Construct the instance for use in the downstream tests.

    :param restful: Ancilary Homie Automate class instance.
    :returns: Newly constructed instance of related class.
    """

    return _create_client(
        restful,
        'username:incorrect')



@fixture
def invalid(
    restful: 'HomieRestful',
) -> TestClient:
    """
    Construct the instance for use in the downstream tests.

    :param restful: Ancilary Homie Automate class instance.
    :returns: Newly constructed instance of related class.
    """

    return _create_client(
        restful,
        'userdoes:notexist')



def _create_client(
    restful: 'HomieRestful',
    seed: str,
) -> TestClient:
    """
    Construct the instance for use in the downstream tests.

    :param restful: Ancilary Homie Automate class instance.
    :param seed: Value that will be used in creating hash.
    :returns: Newly constructed instance of related class.
    """

    bseed = seed.encode()

    token = (
        b64encode(bseed)
        .decode('utf-8'))

    headers = {
        'Authorization': f'Basic {token}'}

    client = ('::1', 8429)

    assert restful.fastapi

    return TestClient(
        restful.fastapi,
        headers=headers,
        client=client)
