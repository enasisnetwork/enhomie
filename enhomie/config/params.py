"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional

from encommon.config import Params as _Params

from ..homie import HomieGroupParams
from ..homie import HomieSceneParams
from ..philipshue.params import PhueBridgeParams
from ..philipshue.params import PhueDeviceParams
from ..ubiquiti.params import UbiqClientParams
from ..ubiquiti.params import UbiqRouterParams




class Params(_Params):
    """
    Process and validate the Homie configuration parameters.

    :param groups:
    :param scenes:
    :param phue_bridges:
    :param phue_devices:
    :param ubiq_routers:
    :param ubiq_clients:
    """

    groups: Optional[dict[str, HomieGroupParams]] = None
    scenes: Optional[dict[str, HomieSceneParams]] = None

    phue_bridges: Optional[dict[str, PhueBridgeParams]] = None
    phue_devices: Optional[dict[str, PhueDeviceParams]] = None
    ubiq_routers: Optional[dict[str, UbiqRouterParams]] = None
    ubiq_clients: Optional[dict[str, UbiqClientParams]] = None
