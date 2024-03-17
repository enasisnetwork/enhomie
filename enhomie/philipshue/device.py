"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bridge import _FETCH
    from .bridge import PhueBridge
    from .params import PhueDeviceParams
    from ..homie import Homie



class PhueDevice:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automator.
    :param name: Name of the object within the Homie config.
    """

    name: str
    homie: 'Homie'

    params: 'PhueDeviceParams'
    source: Optional['_FETCH']
    bridge: Optional['PhueBridge']


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.homie = homie
        self.name = name


        params = homie.params
        devices = params.phue_devices

        assert devices is not None
        assert self.name in devices

        self.params = devices[self.name]


        self.source = None
        self.bridge = None


    def refresh_source(
        self,
    ) -> None:
        """
        Update the class instance from cached upstream response.
        """

        homie = self.homie
        bridges = homie.phue_bridges
        params = self.params

        assert bridges is not None

        self.source = None
        self.bridge = None


        for bridge in bridges.values():

            name = bridge.name
            _name = params.bridge

            if _name != name:
                continue


            found = bridge.get_source(
                phid=params.phid,
                label=params.label)

            if found is None:
                continue


            _type = found['type']

            assert _type == 'device'

            assert not self.source

            self.source = found
            self.bridge = bridge


    @property
    def present(
        self,
    ) -> bool:
        """
        Return the boolean indicating device present on bridge.

        :returns: Boolean indicating device present on bridge.
        """

        return self.source is not None
