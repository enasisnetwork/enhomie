"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..homie import Homie



def test_HomieGroup(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    group = homie.groups['jupiter_room']


    attrs = list(group.__dict__)

    assert attrs == [
        'name',
        'params',
        'homie']


    assert repr(group).startswith(
        '<enhomie.homie.objects')
    assert isinstance(hash(group), int)
    assert str(group).startswith(
        '<enhomie.homie.objects')

    assert group.name == 'jupiter_room'
    assert group.params is not None
    assert group.homie is not None

    assert group.type == 'room'
    assert group.phue_bridge is not None
    assert group.phue_label == 'jupiter_room'
    assert group.phue_source is not None
    assert group.phue_unique == (
        'da9031f1-6229-3e2d'
        '-b143-64b2c8223915')



def test_HomieGroup_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    group = homie.groups['jupiter_room']

    group.params.phue_label = 'doesntexist'

    assert not group.phue_unique



def test_HomieScene(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    scene = homie.scenes['awake']
    group = homie.groups['jupiter_room']


    attrs = list(scene.__dict__)

    assert attrs == [
        'name',
        'params',
        'homie']


    assert repr(scene).startswith(
        '<enhomie.homie.objects')
    assert isinstance(hash(scene), int)
    assert str(scene).startswith(
        '<enhomie.homie.objects')

    assert scene.name == 'awake'
    assert scene.params is not None
    assert scene.homie is not None

    assert scene.phue_label == 'Awake'
    phue_source = scene.phue_source(group)
    phue_unique = scene.phue_unique(group)
    assert phue_source is not None
    assert phue_unique == (
        '5808a516-aab3-3ec3'
        '-8eee-4db5152b07b5')



def test_HomieScene_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automator.
    """

    scene = homie.scenes['awake']
    group = homie.groups['jupiter_room']

    scene.params.phue_label = 'doesntexist'

    assert not scene.phue_unique(group)
