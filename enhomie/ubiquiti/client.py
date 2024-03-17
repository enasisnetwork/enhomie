"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""


from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .params import UbiqClientParams
    from .router import UbiqRouter  # noqa: F401
    from .router import _FETCH  # noqa: F401
    from ..homie import Homie



_SOURCES = dict[str, '_FETCH']
_ROUTERS = dict[str, 'UbiqRouter']



class UbiqClient:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automator.
    :param name: Name of the object within the Homie config.
    """

    name: str
    homie: 'Homie'

    params: 'UbiqClientParams'
    sources: Optional[_SOURCES]
    routers: Optional[_ROUTERS]


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
        clients = params.ubiq_clients

        assert clients is not None
        assert self.name in clients

        self.params = clients[self.name]


        self.sources = None
        self.routers = None


    def refresh_source(
        self,
    ) -> None:
        """
        Update the class instance from cached upstream response.
        """

        homie = self.homie
        routers = homie.ubiq_routers
        params = self.params

        assert routers is not None

        _sources: _SOURCES = {}
        _routers: _ROUTERS = {}


        for router in routers.values():

            name = router.name
            _name = params.router

            if (_name is not None
                    and _name != name):
                continue


            found = router.get_source(
                ubid=(
                    params.ubid
                    or params.mac
                    or params.ip),
                label=params.label)

            if found is None:
                continue


            _sources[name] = found
            _routers[name] = router


        self.sources = _sources or None
        self.routers = _routers or None


    @property
    def present(
        self,
    ) -> list[str] | Literal[False]:
        """
        Return the list of routers which the client is present.

        :returns: List of routers which the client is present,
            or `False` boolean when not present on any routers.
        """

        return (
            list(self.sources)
            if self.sources is not None
            else False)
