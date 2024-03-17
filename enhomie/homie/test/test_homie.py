"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from requests_mock import Mocker

from ...philipshue.test.test_bridge import SCENE_PATHS

if TYPE_CHECKING:
    from ..homie import Homie



def test_Homie(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """


    attrs = list(homie.__dict__)

    assert attrs == [
        '_Homie__config',
        '_Homie__phue_bridges',
        '_Homie__phue_devices',
        '_Homie__ubiq_routers',
        '_Homie__ubiq_clients',
        '_Homie__groups',
        '_Homie__scenes']


    assert repr(homie).startswith(
        '<enhomie.homie.homie')
    assert isinstance(hash(homie), int)
    assert str(homie).startswith(
        '<enhomie.homie.homie')


    assert homie.config is not None
    assert homie.params is not None
    assert len(homie.groups) == 4
    assert len(homie.rooms) == 2
    assert len(homie.zones) == 2
    assert len(homie.scenes) == 5
    assert len(homie.phue_bridges) == 2
    assert len(homie.phue_devices) == 8
    assert len(homie.ubiq_routers) == 2
    assert len(homie.ubiq_clients) == 6



def test_Homie_scene(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    with Mocker() as mocker:

        for path in SCENE_PATHS:
            mocker.put(path)

        homie.scene_set(
            group_name='jupiter_room',
            scene_name='awake')

        homie.scene_set(
            group_name='neptune_room',
            scene_name='awake')
