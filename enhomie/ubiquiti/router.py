"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timers
from encommon.types import merge_dicts
from encommon.types import striplower

from requests import Response
from requests import Session

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

if TYPE_CHECKING:
    from .params import UbiqRouterParams
    from ..homie import Homie



_FETCH = dict[str, Any]
_RAWDEV = dict[str, dict[str, Any]]



disable_warnings(
    category=InsecureRequestWarning)



class UbiqRouter:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automator.
    :param name: Name of the object within the Homie config.
    """

    name: str
    homie: 'Homie'

    params: 'UbiqRouterParams'

    __fetched: Optional[dict[str, _FETCH]]
    __timer: Timers
    __merged: Optional[_RAWDEV]

    __session: Session


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
        routers = params.ubiq_routers

        assert routers is not None

        self.params = routers[name]


        self.__fetched = None
        self.__timer = Timers()
        self.__merged = None

        self.__timer.create(
            unique='fetch',
            minimum=60,
            started='-60s')


        self.__session = Session()


    def authenticate(
        self,
    ) -> None:
        """
        Establish new session obtaining cookie for authorization.
        """

        params = self.params

        username = params.username
        password = params.password

        payload = {
            'username': username,
            'password': password}

        self.__request(
            method='post',
            url='api/auth/login',
            json=payload)


    @property
    def fetched(
        self,
    ) -> _FETCH:
        """
        Collect the complete list of all known clients for site.

        :returns: Complete list of all known clients for site.
        """

        fetched = self.__fetched
        timer = self.__timer

        ready = timer.ready('fetch')

        if fetched and not ready:
            return deepcopy(fetched)


        response = self.request(
            'get', 'rest/user')

        historic = response.json()

        assert isinstance(historic, dict)


        response = self.request(
            'get', 'stat/sta')

        realtime = response.json()

        assert isinstance(realtime, dict)


        self.__fetched = {
            'historic': historic,
            'realtime': realtime}

        self.__merged = None

        timer.update('fetch')

        return deepcopy(self.__fetched)


    def __request(
        self,
        **kwargs: Any,
    ) -> Response:
        """
        Return the response for upstream request to the location.

        :param kwargs: Keyword arguments passed for downstream.
        :returns: Response for upstream request to the location.
        """

        params = self.params
        session = self.__session

        server = params.server

        kwargs['url'] = (
            f'https://{server}/'
            f'{kwargs["url"]}')

        headers = {
            'Content-Type': 'application/json'}

        return session.request(
            headers=headers,
            verify=params.verify,
            **kwargs)


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

        site = self.params.site

        path = (
            'proxy/network/api'
            f'/s/{site}/{path}')

        response = self.__request(
            method=method,
            url=path)

        if response.status_code == 401:

            self.authenticate()

            response = self.__request(
                method=method,
                url=path)

        response.raise_for_status()

        return response


    @property
    def merged(
        self,
    ) -> _RAWDEV:
        """
        Process the response and perform common transformations.

        :returns: Compiled response from the upstream endpoint.
        """

        staged: _RAWDEV = {}
        source: _RAWDEV = {}

        merged = self.__merged

        if merged is not None:
            return deepcopy(merged)

        fetched = self.fetched


        historic = (
            fetched['historic']['data'])

        realtime = (
            fetched['realtime']['data'])


        def _combine(
            target: Literal['historic', 'realtime'],
        ) -> None:

            ubid = item['_id']

            if ubid not in staged:
                staged[ubid] = {}

            source = staged[ubid]

            assert target not in source

            source[target] = (
                deepcopy(item))


        for item in historic:
            _combine('historic')

        for item in realtime:
            _combine('realtime')


        for ubid, fetch in staged.items():

            historic = (
                fetch.get('historic', {}))

            realtime = (
                fetch.get('realtime', {}))

            _fetch: dict[str, Any] = (
                deepcopy(historic))

            merge_dicts(
                dict1=_fetch,
                dict2=deepcopy(realtime),
                force=True)

            source[ubid] = _fetch | {
                '_historic': historic,
                '_realtime': _fetch}


        self.__merged = source

        return deepcopy(self.__merged)


    def get_source(
        self,
        ubid: Optional[str] = None,
        label: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param ubid: Used for filtering resources for matching.
        :param label: Used for filtering resources for matching.
        :returns: Information for matching client from upstream.
        """

        assert ubid or label

        if ubid is not None:
            return self.get_source_ubid(ubid)

        if label is not None:
            return self.get_source_label(label)

        return None  # NOCVR


    def get_source_ubid(
        self,
        ubid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param ubid: Used for filtering resources for matching.
        :returns: Information for matching client from upstream.
        """

        found: list[_FETCH] = []

        merged = self.merged.items()

        for _ubid, fetch in merged:

            values = [striplower(_ubid)]

            if 'mac' in fetch:
                values.append(
                    striplower(fetch['mac']))

            if 'ip' in fetch:
                values.append(
                    striplower(fetch['ip']))

            if ubid not in values:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None


    def get_source_label(
        self,
        label: str,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param label: Used for filtering resources for matching.
        :returns: Information for matching client from upstream.
        """

        found: list[_FETCH] = []

        merged = self.merged.items()

        for _ubid, fetch in merged:

            values: list[str] = []

            if fetch.get('hostname'):
                values.append(
                    striplower(fetch['hostname']))

            if fetch.get('name'):
                values.append(
                    striplower(fetch['name']))

            if label not in values:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None
