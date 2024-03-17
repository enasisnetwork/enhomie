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



def test_PhueDevice(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    devices = homie.phue_devices
    device = devices['jupiter_button']

    attrs = list(device.__dict__)

    assert attrs == [
        'homie',
        'name',
        'params',
        'source',
        'bridge']


    assert repr(device).startswith(
        '<enhomie.philipshue.device')
    assert isinstance(hash(homie), int)
    assert str(device).startswith(
        '<enhomie.philipshue.device')


    assert device.name == 'jupiter_button'
    assert device.homie is not None
    assert device.params is not None
    assert device.source is None
    assert device.bridge is None
    assert device.present is False


    device.refresh_source()

    assert device.source is not None
    assert device.bridge is not None
    assert device.present is True


    sample = load_sample(
        path=SAMPLES.joinpath('device/source.json'),
        update=ENPYRWS,
        content=device.source,
        replace=REPLACES)

    expect = prep_sample(
        content=device.source,
        replace=REPLACES)

    assert sample == expect



def test_PhueDevice_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    devices = homie.phue_devices
    device = devices['jupiter_button']


    device.params.phid = None
    device.params.label = 'jupiter_button'

    device.refresh_source()

    assert device.source is not None
    assert device.bridge is not None
    assert device.present is True


    device.params.phid = None
    device.params.label = 'doesntexist'

    device.refresh_source()

    assert device.source is None
    assert device.bridge is None
    assert device.present is False
