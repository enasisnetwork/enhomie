"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.utils import load_sample
from encommon.utils import prep_sample

from . import SAMPLES
from ...conftest import REPLACES

if TYPE_CHECKING:
    from ...homie import Homie



def test_PhueDevice(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    devices = homie.phue_devices
    device = devices['jupiter_button']


    attrs = list(device.__dict__)

    assert attrs == [
        '_PhueDevice__homie',
        '_PhueDevice__params',
        '_PhueDevice__name',
        '_PhueDevice__source',
        '_PhueDevice__bridge']


    assert inrepr(
        'device.PhueDevice object',
        device)

    assert hash(device) > 0

    assert instr(
        'device.PhueDevice object',
        device)


    assert device.homie is homie

    assert device.params is not None

    assert device.name == 'jupiter_button'

    assert device.bridge is None

    assert device.source is None

    assert device.unique is None

    assert device.present is False

    assert device.connect is False

    assert device.changed is False


    device.refresh_source()

    assert device.unique == (
        '8155e7b2-e89b-3b1d'
        '-80af-a937994d9a78')


    sample_path = (
        f'{SAMPLES}/device/source.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=device.source,
        replace=REPLACES)

    expect = prep_sample(
        content=device.source,
        replace=REPLACES)

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/device/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=device.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=device.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_PhueDevice_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    devices = homie.phue_devices
    device = devices['jupiter_button']


    device.params.phid = None
    device.params.label = 'Jupiter Button'

    device.refresh_source()

    assert device.bridge is not None
    assert device.source is not None
    assert device.present is True
    assert device.connect is True
    assert device.changed is not False
    assert len(device.changed) == 4

    device.params.phid = None
    device.params.label = 'noexst'

    device.refresh_source()

    assert device.bridge is None
    assert device.source is None
    assert device.present is False
    assert device.connect is False
    assert device.changed is False
