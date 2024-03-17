"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon import ENPYRWS
from encommon.utils import load_sample
from encommon.utils import prep_sample

from . import SAMPLES
from ...conftest import REPLACES

if TYPE_CHECKING:
    from ...homie import Homie



def test_UbiqClient(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    clients = homie.ubiq_clients
    client = clients['jupiter_desktop']

    attrs = list(client.__dict__)

    assert attrs == [
        'homie',
        'name',
        'params',
        'sources',
        'routers']


    assert repr(client).startswith(
        '<enhomie.ubiquiti.client')
    assert isinstance(hash(homie), int)
    assert str(client).startswith(
        '<enhomie.ubiquiti.client')


    assert client.name == 'jupiter_desktop'
    assert client.homie is not None
    assert client.params is not None
    assert client.sources is None
    assert client.routers is None
    assert client.present is False


    client.refresh_source()

    assert client.sources is not None
    assert client.routers is not None
    assert (
        isinstance(client.present, list)
        and len(client.present) == 1)


    sample = load_sample(
        path=SAMPLES.joinpath('client/sources.json'),
        update=ENPYRWS,
        content=client.sources,
        replace=REPLACES)

    expect = prep_sample(
        content=client.sources,
        replace=REPLACES)

    assert sample == expect



def test_UbiqClient_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    clients = homie.ubiq_clients
    client = clients['jupiter_desktop']


    client.params.ubid = '65d963e0e9285243cbbe6116'
    client.params.mac = None
    client.params.ip = None
    client.params.label = None

    client.refresh_source()

    assert client.sources is not None
    assert client.routers is not None
    assert (
        isinstance(client.present, list)
        and len(client.present) == 1)


    client.params.ubid = None
    client.params.mac = None
    client.params.ip = '192.168.1.100'
    client.params.label = None

    client.refresh_source()

    assert client.sources is not None
    assert client.routers is not None
    assert (
        isinstance(client.present, list)
        and len(client.present) == 1)


    client.params.ubid = None
    client.params.mac = None
    client.params.ip = None
    client.params.label = 'jupiter_desktop'

    client.refresh_source()

    assert client.sources is not None
    assert client.routers is not None
    assert (
        isinstance(client.present, list)
        and len(client.present) == 1)


    client.params.ubid = None
    client.params.mac = None
    client.params.ip = None
    client.params.label = 'doesntexist'

    client.refresh_source()

    assert client.sources is None
    assert client.routers is None
    assert client.present is False


    client.params.router = 'doesntexist'

    client.refresh_source()

    assert client.sources is None
    assert client.routers is None
    assert client.present is False
