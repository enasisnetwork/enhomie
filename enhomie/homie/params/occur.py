"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from pydantic import Field

from .plugin import HomiePluginParams
from ...builtins.params.regexp import DriverBltnRegexpParams
from ...philips.params.plugins.button import DriverPhueButtonParams
from ...philips.params.plugins.contact import DriverPhueContactParams
from ...philips.params.plugins.motion import DriverPhueMotionParams
from ...philips.params.plugins.scene import DriverPhueSceneParams



class HomieOccurParams(HomiePluginParams, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    builtins_regexp: Annotated[
        Optional[DriverBltnRegexpParams],
        Field(None,
              description='Plugin for the operations')]

    philips_button: Annotated[
        Optional[DriverPhueButtonParams],
        Field(None,
              description='Plugin for the operations')]

    philips_contact: Annotated[
        Optional[DriverPhueContactParams],
        Field(None,
              description='Plugin for the operations')]

    philips_motion: Annotated[
        Optional[DriverPhueMotionParams],
        Field(None,
              description='Plugin for the operations')]

    philips_scene: Annotated[
        Optional[DriverPhueSceneParams],
        Field(None,
              description='Plugin for the operations')]
