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
        value=1e9,
        value_unit='bytes',
        about='Amount of bytes sent',
        about_label='Total Bytes Sent',
        about_icon='inbox',
        level='success',
        tags=['one', 'two', 'three'],
        expire='1d')

    path = '/api/persists'

    response = client.get(path)

    assert response.status_code == 200

    _response = response.json()

    entries = _response['entries']

    assert entries == [

        {'about': 'Amount of bytes sent',
         'about_icon': 'inbox',
         'about_label': 'Total Bytes Sent',
         'expire': entries[0]['expire'],
         'level': 'success',
         'tags': ['one', 'two', 'three'],
         'unique': 'one',
         'update': entries[0]['update'],
         'value': 1000000000.0,
         'value_icon': None,
         'value_label': None,
         'value_unit': 'bytes'}]
