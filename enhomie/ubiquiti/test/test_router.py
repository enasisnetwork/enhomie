"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon import ENPYRWS
from encommon.utils import load_sample
from encommon.utils import prep_sample

from . import SAMPLES
from ...conftest import REPLACES

if TYPE_CHECKING:
    from ...homie import Homie



def test_UbiqRouter(
    tmp_path: Path,
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param homie: Primary class instance for Homie Automator.
    """

    routers = homie.ubiq_routers
    router = routers['jupiter']

    attrs = list(router.__dict__)

    assert attrs == [
        'homie',
        'name',
        'params',
        '_UbiqRouter__fetched',
        '_UbiqRouter__timer',
        '_UbiqRouter__merged',
        '_UbiqRouter__session']


    assert repr(router).startswith(
        '<enhomie.ubiquiti.router')
    assert isinstance(hash(homie), int)
    assert str(router).startswith(
        '<enhomie.ubiquiti.router')


    assert router.name == 'jupiter'
    assert router.homie is not None
    assert router.params is not None


    sample = load_sample(
        path=SAMPLES.joinpath('router/fetched.json'),
        update=ENPYRWS,
        content=router.fetched,
        replace=REPLACES)

    expect = prep_sample(
        content=router.fetched,
        replace=REPLACES)

    assert sample == expect


    sample = load_sample(
        path=SAMPLES.joinpath('router/merged.json'),
        update=ENPYRWS,
        content=router.merged,
        replace=REPLACES)

    expect = prep_sample(
        content=router.merged,
        replace=REPLACES)

    assert sample == expect


    ubid = '65d963e0e9285243cbbe6116'

    source = router.get_source(ubid)

    assert source is not None
    assert source['_id'] == ubid



def test_UbiqRouter_cover(
    tmp_path: Path,
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param homie: Primary class instance for Homie Automator.
    """

    routers = homie.ubiq_routers
    router = routers['jupiter']

    ubid = '65d963e0e9285243cbbe6116'


    source = router.get_source(
        '1a:01:68:00:11:00')

    assert source is not None
    assert source['_id'] == ubid


    source = router.get_source(
        '192.168.1.100')

    assert source is not None
    assert source['_id'] == ubid


    source = router.get_source(
        label='jupiter_desktop')

    assert source is not None
    assert source['_id'] == ubid
