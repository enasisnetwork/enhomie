"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING

from .params import GROUP_TYPES
from .params import HomieGroupParams
from .params import HomieSceneParams

if TYPE_CHECKING:
    from .homie import Homie
    from ..philipshue import PhueBridge
    from ..philipshue.bridge import _FETCH as PHUE_FETCH



class HomieGroup:
    """
    Normalize the group parameter across multiple products.

    :param name: Name of the object within the Homie config.
    :param homie: Primary class instance for Homie Automator.
    """

    name: str
    params: 'HomieGroupParams'

    homie: 'Homie'


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.name = name

        groups = (
            homie.params.groups)

        assert groups is not None
        assert self.name in groups

        self.params = (
            groups[self.name])

        self.homie = homie


    @property
    def type(
        self,
    ) -> GROUP_TYPES:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.type


    @property
    def phue_bridge(
        self,
    ) -> 'PhueBridge':
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        params = self.params
        homie = self.homie

        bridges = homie.phue_bridges
        name = params.phue_bridge

        assert name in bridges

        return bridges[name]


    @property
    def phue_label(
        self,
    ) -> str:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.phue_label


    @property
    def phue_source(
        self,
    ) -> Optional['PHUE_FETCH']:
        """
        Return the dictionary containing the source from bridge.

        :returns: Dictionary containing the source from bridge.
        """

        bridge = self.phue_bridge

        return bridge.get_source(
            label=self.phue_label,
            type=self.type)


    @property
    def phue_unique(
        self,
    ) -> Optional[str]:
        """
        Return the unique identifier of group within the bridge.

        :returns: Unique identifier of group within the bridge.
        """

        source = self.phue_source

        if source is None:
            return None

        phid = source['id']

        assert isinstance(phid, str)

        return phid


    def scene_set(
        self,
        scene: 'HomieScene',
    ) -> None:
        """
        Update the current group to activate the provided scene.

        :param scene: Scene instance that will be used in match.
        """

        scene.scene_set(self)



class HomieScene:
    """
    Normalize the scene parameter across multiple products.

    :param name: Name of the object within the Homie config.
    :param homie: Primary class instance for Homie Automator.
    """

    name: str
    params: 'HomieSceneParams'

    homie: 'Homie'


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.name = name

        scenes = (
            homie.params.scenes)

        assert scenes is not None
        assert self.name in scenes

        self.params = (
            scenes[self.name])

        self.homie = homie


    @property
    def phue_label(
        self,
    ) -> str:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.phue_label


    def phue_source(
        self,
        group: 'HomieGroup',
    ) -> Optional['PHUE_FETCH']:
        """
        Return the dictionary containing the source from bridge.

        .. note::
           Scenes only exist within the groups on the bridge.

        :param group: Group from wherein the scene is located.
        :returns: Dictionary containing the source from bridge.
        """

        bridge = group.phue_bridge

        scene_label = self.phue_label
        group_phid = group.phue_unique

        assert group_phid is not None

        return bridge.get_source(
            label=scene_label,
            type='scene',
            grid=group_phid)


    def phue_unique(
        self,
        group: 'HomieGroup',
    ) -> Optional[str]:
        """
        Return the unique identifier of scene within the bridge.

        .. note::
           Scenes only exist within the groups on the bridge.

        :param group: Group from wherein the scene is located.
        :returns: Unique identifier of scene within the bridge.
        """

        source = (
            self.phue_source(group))

        if source is None:
            return None

        phid = source['id']

        assert isinstance(phid, str)

        return phid


    def scene_set(
        self,
        group: 'HomieGroup',
    ) -> None:
        """
        Update the current group to activate the provided scene.

        :param group: Group from wherein the scene is located.
        """

        bridge = group.phue_bridge

        scene_phid = (
            self.phue_unique(group))

        assert scene_phid is not None

        bridge.scene_set(scene_phid)
