"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal

from pydantic import BaseModel



GROUP_TYPES = Literal['room', 'zone']



class HomieGroupParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    .. note::
       Value is required for `phue_label` but may one day
       become optional, should another product be supported.

    :param type:
    :param phue_bridge:
    :param phue_label:
    """

    type: GROUP_TYPES

    phue_bridge: str
    phue_label: str



class HomieSceneParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    .. note::
       Value is required for `phue_label` but may one day
       become optional, should another product be supported.

    :param phue_label:
    """

    phue_label: str
