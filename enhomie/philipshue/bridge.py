"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timers
from encommon.types import striplower

from requests import Response
from requests import request

if TYPE_CHECKING:
    from .params import PhueBridgeParams
    from ..homie import Homie



_FETCH = dict[str, Any]
_RAWDEV = dict[str, dict[str, Any]]



class PhueBridge:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automator.
    :param name: Name of the object within the Homie config.
    """

    name: str
    homie: 'Homie'

    params: 'PhueBridgeParams'

    __merged: Optional[_RAWDEV]
    __timer: Timers
    __fetched: Optional[_FETCH]


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
        bridges = params.phue_bridges

        assert bridges is not None

        self.params = bridges[name]


        self.__fetched = None
        self.__timer = Timers()
        self.__merged = None

        self.__timer.create(
            unique='fetch',
            minimum=60,
            started='-60s')


    @property
    def fetched(
        self,
    ) -> _FETCH:
        """
        Collect the complete dump of all resources within bridge.

        :returns: Complete dump of all resources within bridge.
        """

        fetched = self.__fetched
        timer = self.__timer

        ready = timer.ready('fetch')

        if fetched and not ready:
            return deepcopy(fetched)


        response = self.request(
            'get', 'resource')

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        self.__fetched = fetched
        self.__merged = None

        timer.update('fetch')

        return deepcopy(self.__fetched)


    def request(
        self,
        method: str,
        path: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> Response:
        """
        Return the response for upstream request to the location.

        :param method: Method for operation with the API server.
        :param path: Location and path for the upstream endpoint.
        :param payload: Optional payload included with request.
        :returns: Response for upstream request to the location.
        """

        params = self.params

        server = params.server
        token = params.token
        verify = params.verify

        headers = {
            'hue-application-key': token}

        path = (
            f'https://{server}'
            f'/clip/v2/{path}')

        return request(
            method=method,
            url=path,
            headers=headers,
            json=payload,
            verify=verify)


    @property
    def merged(
        self,
    ) -> _RAWDEV:
        """
        Process the response and perform common transformations.

        :returns: Compiled response from the upstream endpoint.
        """

        merged = self.__merged

        if merged is not None:
            return deepcopy(merged)

        fetched = self.fetched


        source = {
            x['id']: x for x in
            fetched['data']}

        origin = deepcopy(source)


        def _enhance() -> None:

            rtype = item['rtype']
            rid = item['rid']

            if 'taurus_' in rtype:
                return

            item['_source'] = (
                origin[rid])


        for key, value in source.items():

            if 'services' not in value:
                continue

            items = value['services']

            for item in items:
                _enhance()


        self.__merged = source

        return deepcopy(self.__merged)


    def get_source(
        self,
        phid: Optional[str] = None,
        label: Optional[str] = None,
        type: Optional[str] = None,
        grid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param phid: Used for filtering resources for matching.
        :param label: Used for filtering resources for matching.
        :param type: Used for filtering resources for matching.
        :param grid: Used for filtering resources for matching.
        :returns: Information for matching resource in upstream.
        """

        assert phid or label

        if phid is not None:
            return self.get_source_phid(
                phid, type, grid)

        if label is not None:
            return self.get_source_label(
                label, type, grid)

        return None  # NOCVR


    def get_source_phid(
        self,
        phid: str,
        type: Optional[str] = None,
        grid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param phid: Used for filtering resources for matching.
        :param type: Used for filtering resources for matching.
        :param grid: Used for filtering resources for matching.
        :returns: Information for matching resource in upstream.
        """

        found: list[_FETCH] = []

        merged = self.merged.items()

        for _phid, fetch in merged:

            _type = fetch['type']

            if type and _type != type:
                continue

            _grid: Optional[str] = (
                fetch.get('group', {})
                .get('rid'))

            if grid and _grid != grid:
                continue

            if _phid != phid:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None


    def get_source_label(
        self,
        label: str,
        type: Optional[str] = None,
        grid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param label: Used for filtering resources for matching.
        :param type: Used for filtering resources for matching.
        :param grid: Used for filtering resources for matching.
        :returns: Information for matching resource in upstream.
        """

        found: list[_FETCH] = []

        label = striplower(label)

        merged = self.merged.items()

        for phid, fetch in merged:

            _type = fetch['type']

            if type and _type != type:
                continue

            _grid: Optional[str] = (
                fetch.get('group', {})
                .get('rid'))

            if grid and _grid != grid:
                continue

            if 'metadata' not in fetch:
                continue

            metadata = fetch['metadata']

            if 'owner' in fetch:
                continue

            name = striplower(
                metadata['name'])

            if name != label:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None


    def scene_set(
        self,
        scene_phid: str,
    ) -> None:
        """
        Activate the provided scene unique identifier in bridge.

        :param scene_phid: Unique identifier of scene in bridge.
        """

        path = (
            'resource/scene'
            f'/{scene_phid}')

        action = {'action': 'active'}
        payload = {'recall': action}

        self.request(
            method='put',
            path=path,
            payload=payload)
