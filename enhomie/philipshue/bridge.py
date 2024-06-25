"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timer
from encommon.times import Times
from encommon.types import setate
from encommon.types import striplower

from enconnect.philipshue import Bridge
from enconnect.philipshue import BridgeParams


if TYPE_CHECKING:
    from ..homie import Homie
    from ..homie.params import HOMIE_STATE



_FETCH = dict[str, Any]
_RAWDEV = dict[str, dict[str, Any]]



class PhueBridge:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: BridgeParams
    __bridge: Bridge

    __name: str

    __fetched: Optional[_FETCH]
    __refresh: Timer
    __merged: Optional[_RAWDEV]


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.log_d(
            base='PhueBridge',
            name=name,
            status='initial')


        bridges = (
            homie.params
            .phue_bridges)

        assert bridges is not None

        params = bridges[name]


        self.__homie = homie
        self.__params = params
        self.__bridge = Bridge(params)
        self.__name = name
        self.__fetched = None
        self.__merged = None


        self.__refresh = Timer(
            60, start='-60s')


        homie.log_d(
            base='PhueBridge',
            name=name,
            status='created')


    @property
    def homie(
        self,
    ) -> 'Homie':
        """
        Return the Homie instance to which this instance belongs.

        :returns: Homie instance to which this instance belongs.
        """

        return self.__homie


    @property
    def params(
        self,
    ) -> BridgeParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def bridge(
        self,
    ) -> Bridge:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__bridge


    @property
    def name(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__name


    @property
    def connect(
        self,
    ) -> bool:
        """
        Return the boolean indicating connection is established.

        :returns: Boolean indicating connection is established.
        """

        return bool(self.__merged)


    def refresh(
        self,
    ) -> None:
        """
        Refresh the cached information for the remote upstream.
        """

        timer = self.__refresh

        timer.update(
            f'-{int(timer.timer)}s')

        assert timer.ready(False)

        self.fetched
        self.merged

        assert not timer.ready()


    @property
    def fetched(
        self,
    ) -> _FETCH:
        """
        Collect the complete dump of all resources within bridge.

        :returns: Complete dump of all resources within bridge.
        """

        fetched = self.__fetched
        timer = self.__refresh
        bridge = self.__bridge
        request = bridge.request

        ready = timer.ready(False)

        if fetched and not ready:
            return deepcopy(fetched)


        runtime = Times()

        try:

            response = request(
                'get', 'resource')

            response.raise_for_status()

            fetched = response.json()

            self.homie.log_d(
                base='PhueBridge',
                name=self.name,
                item='fetch',
                elapsed=runtime.since,
                status='success')

        except Exception as reason:  # NOCVR

            self.homie.log_e(
                base='PhueBridge',
                name=self.name,
                item='fetch',
                elapsed=runtime.since,
                status='failure',
                exc_info=reason)

            if fetched is None:
                raise

            return deepcopy(fetched)


        assert isinstance(fetched, dict)


        self.__fetched = fetched
        self.__merged = None

        timer.update('now')

        return deepcopy(fetched)


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


        items1 = source.items()

        for key, value in items1:

            if 'services' not in value:
                continue

            items2 = value['services']

            for item in items2:
                _enhance()


        self.__merged = source

        return deepcopy(source)


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

        items = self.merged.items()

        for _phid, fetch in items:

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

        items = self.merged.items()

        for phid, fetch in items:

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


    def state_get(
        self,
        light: str,
    ) -> 'HOMIE_STATE':
        """
        Return the current state of the light within the bridge.

        :param light: Unique identifier of light within bridge.
        :returns: Current state of the light within the bridge.
        """

        state = (
            self.merged[light]
            ['on']['on'])

        return (
            'on' if state
            else 'off')


    def state_set(
        self,
        light: str,
        state: 'HOMIE_STATE',
    ) -> None:
        """
        Update the current state of the light within the bridge.

        :param light: Unique identifier of light within bridge.
        :param state: Desired state for the lights within group.
        """

        self.homie.log_d(
            base='PhueBridge',
            item='state/set',
            light=light,
            value=state,
            status='attempt')

        runtime = Times()


        path = (
            'resource/grouped_light'
            f'/{light}')


        payload: dict[str, Any] = {}

        key = 'on/on'
        value = state == 'on'

        setate(payload, key, value)


        self.bridge.request(
            method='put',
            path=path,
            json=payload)


        self.homie.log_d(
            base='PhueBridge',
            item='state/set',
            light=light,
            value=state,
            elapsed=runtime.since,
            status='success')


    def level_get(
        self,
        light: str,
    ) -> int:
        """
        Return the current level of the light within the bridge.

        :param light: Unique identifier of light within bridge.
        :returns: Current level of the light within the bridge.
        """

        return int(
            self.merged[light]
            ['dimming']
            ['brightness'])


    def level_set(
        self,
        light: str,
        level: int,
    ) -> None:
        """
        Update the current level of the light within the bridge.

        :param light: Unique identifier of light within bridge.
        :param level: Desired level for the lights within group.
        """

        self.homie.log_d(
            base='PhueBridge',
            item='level/set',
            light=light,
            value=level,
            status='attempt')

        runtime = Times()


        path = (
            'resource/grouped_light'
            f'/{light}')


        payload: dict[str, Any] = {}

        key = 'dimming/brightness'
        value = int(level)

        setate(payload, key, value)


        self.bridge.request(
            method='put',
            path=path,
            json=payload)


        self.homie.log_d(
            base='PhueBridge',
            action='level/set',
            light=light,
            value=level,
            elapsed=runtime.since,
            status='success')


    def scene_get(
        self,
        group: str,
    ) -> Optional[str]:
        """
        Return the current scene of the group within the bridge.

        :param group: Unique identifier of group in bridge.
        :returns: Current scene of the group within the bridge.
        """

        items = self.merged.items()

        for phid, fetch in items:

            if 'group' not in fetch:
                continue

            _group = fetch['group']
            _phid = _group['rid']

            if _phid != group:
                continue

            status = fetch['status']
            active = status['active']

            if active != 'inactive':
                return phid

        return None


    def scene_set(
        self,
        scene: str,
    ) -> None:
        """
        Update the current scene of the group within the bridge.

        :param scene: Unique identifier of group within bridge.
        """

        self.homie.log_d(
            base='PhueBridge',
            item='scene/set',
            value=scene,
            status='attempt')

        runtime = Times()


        path = (
            'resource/scene'
            f'/{scene}')


        payload: dict[str, Any] = {}

        key = 'recall/action'
        value = 'active'

        setate(payload, key, value)


        self.bridge.request(
            method='put',
            path=path,
            json=payload)


        self.homie.log_d(
            base='PhueBridge',
            item='scene/set',
            value=scene,
            elapsed=runtime.since,
            status='success')


    def homie_dumper(
        self,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        :returns: Content related to the project dumper script.
        """

        params = deepcopy(
            self.params.model_dump())

        params['token'] = (
            '*' * len(params['token']))

        return {
            'name': self.name,
            'connect': self.connect,
            'params': params}
