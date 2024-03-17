"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Literal
from typing import Optional

from pydantic import BaseModel



_SENSORS = Literal[
    'button1',
    'button2',
    'button3',
    'button4',
    'motion1']



class PhueBridgeParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param server:
    :param token:
    :param verify:
    """

    server: str
    token: str
    verify: bool = True



class PhueDeviceParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param bridge:
    :param phid:
    :param label:
    """

    bridge: str
    phid: Optional[str] = None

    label: Optional[str] = None


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)

        phid = self.phid
        label = self.label

        assert phid or label
