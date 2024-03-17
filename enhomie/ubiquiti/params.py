"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional

from pydantic import BaseModel



class UbiqRouterParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param server:
    :param username:
    :param password:
    :param site:
    :param verify:
    """

    server: str
    username: str
    password: str
    site: str = 'default'
    verify: bool = True



class UbiqClientParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param router:
    :param ubid:
    :param mac:
    :param ip:
    :param label:
    """

    router: Optional[str] = None
    ubid: Optional[str] = None

    mac: Optional[str] = None
    ip: Optional[str] = None
    label: Optional[str] = None


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)

        router = self.router
        ubid = self.ubid
        mac = self.mac
        ip = self.ip
        label = self.label

        if ubid is not None:
            assert router is not None

        if ubid is None:
            assert mac or ip or label
