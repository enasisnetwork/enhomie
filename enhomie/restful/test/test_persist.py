"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from fastapi.testclient import TestClient

if TYPE_CHECKING:
    from ..service import HomieRestful
    from ...homie import Homie



def test_get_persists(
    homie: 'Homie',
    restful: 'HomieRestful',
    client: TestClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param restful: Ancilary Homie Automate class instance.
    :param client: Used when testing the FastAPI endpoints.
    """

    persist = homie.persist

    persist.insert(
        unique='one',
        label='Total Bytes',
        value=1000,
        unit='bytes',
        icon='inbox',
        about='Amount of bytes sent',
        expire='1d')

    path = '/api/persists'

    response = client.get(path)

    assert response.status_code == 200

    _response = response.json()

    entries = _response['entries']

    assert entries == [

        {'about': 'Amount of bytes sent',
         'expire': entries[0]['expire'],
         'icon': 'inbox',
         'label': 'Total Bytes',
         'unique': 'one',
         'unit': 'bytes',
         'update': entries[0]['update'],
         'value': 1000}]
