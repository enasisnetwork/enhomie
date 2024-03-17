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

from requests_mock import Mocker

from . import SAMPLES
from ...conftest import REPLACES

if TYPE_CHECKING:
    from ...homie import Homie



SCENE_PHIDS = [

    ('5808a516-aab3-3ec3'
     '-8eee-4db5152b07b5'),

    ('9678ff8b-d452-49f3'
     '-861c-74e5c5b2ca7c')]

SCENE_PATHS = [

    ('https://192.168.1.10'
     '/clip/v2/resource/scene'
     f'/{SCENE_PHIDS[0]}'),

    ('https://192.168.2.10'
     '/clip/v2/resource/scene'
     f'/{SCENE_PHIDS[1]}')]



def test_PhueBridge(
    tmp_path: Path,
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param homie: Primary class instance for Homie Automator.
    """

    bridges = homie.phue_bridges
    bridge = bridges['jupiter']

    attrs = list(bridge.__dict__)

    assert attrs == [
        'homie',
        'name',
        'params',
        '_PhueBridge__fetched',
        '_PhueBridge__timer',
        '_PhueBridge__merged']


    assert repr(bridge).startswith(
        '<enhomie.philipshue.bridge')
    assert isinstance(hash(homie), int)
    assert str(bridge).startswith(
        '<enhomie.philipshue.bridge')


    assert bridge.name == 'jupiter'
    assert bridge.homie is not None
    assert bridge.params is not None


    sample = load_sample(
        path=SAMPLES.joinpath('bridge/fetched.json'),
        update=ENPYRWS,
        content=bridge.fetched,
        replace=REPLACES)

    expect = prep_sample(
        content=bridge.fetched,
        replace=REPLACES)

    assert sample == expect


    sample = load_sample(
        path=SAMPLES.joinpath('bridge/merged.json'),
        update=ENPYRWS,
        content=bridge.merged,
        replace=REPLACES)

    expect = prep_sample(
        content=bridge.merged,
        replace=REPLACES)

    assert sample == expect


    phid = (
        '8155e7b2-e89b-3b1d'
        '-80af-a937994d9a78')

    source = bridge.get_source(phid)

    assert source is not None
    assert source['id'] == phid



def test_PhueBridge_cover(
    tmp_path: Path,
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param homie: Primary class instance for Homie Automator.
    """

    bridges = homie.phue_bridges
    bridge = bridges['jupiter']

    phid = (
        '8155e7b2-e89b-3b1d'
        '-80af-a937994d9a78')


    source = bridge.get_source(
        label='jupiter_button',
        type='device')

    assert source is not None
    assert source['id'] == phid


    source = bridge.get_source(
        phid, type='device')

    assert source is not None
    assert source['id'] == phid


    group = homie.groups['jupiter_room']
    scene = homie.scenes['awake']


    source = bridge.get_source(
        label=scene.phue_label,
        type='scene',
        grid=group.phue_unique)

    assert source is not None
    assert source['id'] == (
        scene.phue_unique(group))


    source = bridge.get_source(
        phid=scene.phue_unique(group),
        type='scene',
        grid=group.phue_unique)

    assert source is not None
    assert source['id'] == (
        scene.phue_unique(group))



def test_PhueBridge_scene(
    tmp_path: Path,
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param homie: Primary class instance for Homie Automator.
    """

    bridges = homie.phue_bridges


    with Mocker() as mocker:

        for path in SCENE_PATHS:
            mocker.put(path)

        bridge = bridges['jupiter']
        bridge.scene_set(SCENE_PHIDS[0])

        bridge = bridges['neptune']
        bridge.scene_set(SCENE_PHIDS[1])
