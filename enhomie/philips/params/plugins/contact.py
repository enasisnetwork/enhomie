"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Optional

from encommon.config import ParamsModel

from pydantic import Field

from ...plugins.contact import PhueContactState



class DriverPhueContactParams(ParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    device: Annotated[
        str,
        Field(...,
              description='Device that is in scope',
              min_length=1)]

    states: Annotated[
        Optional[list[PhueContactState]],
        Field(None,
              description='States that will be matched',
              min_length=1)]


    def __init__(
        # NOCVR
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        states = data.get('states')

        if isinstance(states, str):
            data['states'] = [states]

        super().__init__(**data)
