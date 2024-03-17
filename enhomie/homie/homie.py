"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from .objects import HomieGroup
from .objects import HomieScene
from ..philipshue import PhueBridge
from ..philipshue import PhueDevice
from ..ubiquiti import UbiqClient
from ..ubiquiti import UbiqRouter

if TYPE_CHECKING:
    from ..config import Config
    from ..config import Params



class Homie:
    """
    Interact with supported devices to ensure desired state.

    :param config: Primary class instance for configuration.
    """

    __config: 'Config'

    __phue_bridges: dict[str, PhueBridge]
    __phue_devices: dict[str, PhueDevice]
    __ubiq_routers: dict[str, UbiqRouter]
    __ubiq_clients: dict[str, UbiqClient]

    __groups: dict[str, HomieGroup]
    __scenes: dict[str, HomieScene]


    def __init__(
        self,
        config: 'Config',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__config = config

        self.__phue_bridges = {}
        self.__phue_devices = {}
        self.__ubiq_routers = {}
        self.__ubiq_clients = {}

        self.__groups = {}
        self.__scenes = {}

        self.__make_phue_bridges()
        self.__make_phue_devices()
        self.__make_ubiq_routers()
        self.__make_ubiq_clients()

        self.__make_groups()
        self.__make_scenes()


    def __make_groups(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        groups = params.groups

        if groups is None:
            return  # NOCVR

        for name, _ in groups.items():

            group = HomieGroup(self, name)

            self.__groups |= {
                group.name: group}


    def __make_scenes(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        scenes = params.scenes

        if scenes is None:
            return  # NOCVR

        for name, _ in scenes.items():

            scene = HomieScene(self, name)

            self.__scenes |= {
                scene.name: scene}


    def __make_phue_bridges(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        bridges = params.phue_bridges

        if bridges is None:
            return  # NOCVR

        for name, _ in bridges.items():

            bridge = PhueBridge(self, name)

            self.__phue_bridges |= {
                bridge.name: bridge}


    def __make_phue_devices(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        devices = params.phue_devices

        if devices is None:
            return  # NOCVR

        for name, _ in devices.items():

            device = PhueDevice(self, name)

            self.__phue_devices |= {
                device.name: device}


    def __make_ubiq_routers(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        routers = params.ubiq_routers

        if routers is None:
            return  # NOCVR

        for name, _ in routers.items():

            router = UbiqRouter(self, name)

            self.__ubiq_routers |= {
                router.name: router}


    def __make_ubiq_clients(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        clients = params.ubiq_clients

        if clients is None:
            return  # NOCVR

        for name, _ in clients.items():

            client = UbiqClient(self, name)

            self.__ubiq_clients |= {
                client.name: client}


    @property
    def config(
        self,
    ) -> 'Config':
        """
        Return the Config instance containing the configuration.

        :returns: Config instance containing the configuration.
        """

        return self.__config


    @property
    def params(
        self,
    ) -> 'Params':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__config.params


    @property
    def groups(
        self,
    ) -> dict[str, HomieGroup]:
        """
        Return the group instances defined within this instance.

        :returns: Group instances defined within this instance.
        """

        return dict(self.__groups)


    @property
    def rooms(
        self,
    ) -> dict[str, HomieGroup]:
        """
        Return the room instances defined within this instance.

        :returns: Room instances defined within this instance.
        """

        return {
            k: v for k, v in
            self.groups.items()
            if v.type == 'room'}


    @property
    def zones(
        self,
    ) -> dict[str, HomieGroup]:
        """
        Return the zone instances defined within this instance.

        :returns: Zone instances defined within this instance.
        """

        return {
            k: v for k, v in
            self.groups.items()
            if v.type == 'zone'}


    @property
    def scenes(
        self,
    ) -> dict[str, HomieScene]:
        """
        Return the scene instances defined within this instance.

        :returns: Scene instances defined within this instance.
        """

        return dict(self.__scenes)


    @property
    def phue_bridges(
        self,
    ) -> dict[str, PhueBridge]:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return dict(self.__phue_bridges)


    @property
    def phue_devices(
        self,
    ) -> dict[str, PhueDevice]:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return dict(self.__phue_devices)


    @property
    def ubiq_routers(
        self,
    ) -> dict[str, UbiqRouter]:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return dict(self.__ubiq_routers)


    @property
    def ubiq_clients(
        self,
    ) -> dict[str, UbiqClient]:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return dict(self.__ubiq_clients)


    def scene_set(
        self,
        group_name: str,
        scene_name: str,
    ) -> None:
        """
        Update the provided group to activate the provided scene.

        :param group_name: Name of the Homie group for operation.
        :param scene_name: Name of the Homie scene for operation.
        """

        group = self.groups[group_name]
        scene = self.scenes[scene_name]

        group.scene_set(scene)
