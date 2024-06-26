"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from argparse import ArgumentParser
from dataclasses import dataclass
from queue import Queue
from signal import SIGHUP
from signal import SIGINT
from signal import SIGTERM
from signal import signal
from threading import Thread
from time import sleep as block_sleep
from typing import Any

from encommon.times import Duration
from encommon.times import Timer
from encommon.times import Times
from encommon.utils import array_ansi
from encommon.utils import print_ansi

from enhomie.config import Config
from enhomie.homie import Homie
from enhomie.homie import HomieAction
from enhomie.homie import HomieDesire
from enhomie.homie import HomieGroup
from enhomie.philipshue import PhueBridge

from httpx import ReadTimeout

AbstractEventLoop = asyncio.AbstractEventLoop
AsyncEvent = asyncio.Event
CancelledError = asyncio.CancelledError



NOSTREAM = AsyncEvent()
NOACTION = AsyncEvent()

ALOOPS: dict[str, AbstractEventLoop] = {}
THREADS: dict[str, Thread] = {}



@dataclass
class StreamItem:
    """
    Contain information about the event received from stream.
    """

    event: dict[str, Any]
    times: Times



STREAM: Queue[StreamItem] = Queue()



@dataclass
class PhueStreamItem(StreamItem):
    """
    Contain information about the event received from stream.
    """

    bridge: str



def launcher_args() -> dict[str, Any]:  # noqa: CFQ001
    """
    Construct the arguments that are associated with the file.
    """

    parser = ArgumentParser()

    parser.add_argument(
        '--config',
        required=True,
        help=(
            'complete or relative '
            'path to config file'))

    parser.add_argument(
        '--console',
        action='store_true',
        default=False,
        help=(
            'write log messages '
            'to standard output'))

    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help=(
            'increase logging level '
            'for standard output'))

    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=False,
        dest='dryrun',
        help=(
            'do not execute action '
            'and show what would do'))

    parser.add_argument(
        '--idempotent',
        action='store_true',
        default=False,
        dest='idempt',
        help=(
            'do not make change if '
            'would not change value'))

    parser.add_argument(
        '--quiet',
        action='store_true',
        default=False,
        help=(
            'only log when changes '
            'are made and different'))

    parser.add_argument(
        '--actions',
        action='store_true',
        default=False,
        help=(
            'iterate through actions '
            'operating the objects'))

    parser.add_argument(
        '--desires',
        action='store_true',
        default=False,
        help=(
            'iterate through desires '
            'operating the objects'))

    parser.add_argument(
        '--watcher',
        action='store_true',
        default=False,
        help=(
            'print out the events '
            'that are received'))

    parser.add_argument(
        '--timeout',
        type=float,
        default=60,
        help=(
            'period of time before '
            'reconnecting to server'))

    parser.add_argument(
        '--timer_refresh',
        type=int,
        default=15,
        dest='trefresh',
        help=(
            'period of time before '
            'refreshing the objects'))

    parser.add_argument(
        '--timer_desires',
        type=int,
        default=60,
        dest='tdesires',
        help=(
            'period of time before '
            'reprocessing desired'))

    return vars(parser.parse_args())



def printer(
    header: dict[str, Any],
    source: dict[str, Any],
) -> None:
    """
    Print the contents for the object within Homie instance.

    .. note::
       Currently redundant between dumper.py and service.py.

    :param header: Additional information for output header.
    :param source: Content which will be shown after header.
    """

    print_ansi(
        f'\n<c96>┍{"━" * 63}<c0>')

    items = header.items()

    for key, value in items:

        print_ansi(
            f'<c96>│ <c36;1>{key}'
            f'<c37>: <c0>{value}')

    print_ansi(
        f'<c96>├{"─" * 63}<c0>\n')

    print(array_ansi(
        source, indent=2))

    print_ansi(
        f'\n<c96>┕{"━" * 63}<c0>\n')



class Service(Thread):
    """
    Handle when exceptions occur within the thread routine.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name used when creating new thread object.
    """

    __homie: Homie
    __name: str

    __timers: dict[str, Timer]


    def __init__(
        self,
        homie: 'Homie',
        name: str = 'default',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie
        self.__name = name

        self.__make_timers()

        super().__init__(
            name=f'service/{name}')


    def __make_timers(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        config = homie.config
        sargs = config.sargs

        _refresh = sargs['trefresh']
        _desires = sargs['tdesires']

        refresh = Timer(
            _refresh, start=0)

        desires = Timer(
            _desires, start=0)

        self.__timers = {
            'refresh': refresh,
            'desires': desires}


    def __desired(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie
        timers = self.__timers

        tdesires = timers['desires']
        trefresh = timers['refresh']

        ready = tdesires.ready()

        if ready is False:
            return

        config = homie.config
        params = config.params
        groups = homie.groups

        _dryrun = params.dryrun


        homie.refresh()

        trefresh.update()


        desired = homie.desired(
            reset=not _dryrun)

        dumped = {
            k: v.homie_dumper()
            for k, v
            in desired.items()}

        if len(dumped) == 0:
            return


        items = desired.items()

        for name, desire in items:

            group = groups[name]

            if desire.scene is not None:
                self.__scene_set(
                    group, desire)

            if desire.level is not None:
                self.__level_set(
                    group, desire)

            if desire.state is not None:
                self.__state_set(
                    group, desire)

            if _dryrun is False:
                desire.update_timer()


    def __aspired(
        self,
        item: StreamItem,
    ) -> None:
        """
        Perform whatever operations are associated with the file.

        :param item: Queue item that was received from upstream.
        """

        homie = self.__homie
        config = homie.config
        params = config.params
        groups = homie.groups

        timers = self.__timers
        trefresh = timers['refresh']

        _dryrun = params.dryrun


        aspired = homie.aspired(
            item.event, False)

        if len(aspired) == 0:
            return


        ready = trefresh.ready()

        if ready is True:
            homie.refresh()


        aspired = homie.aspired(
            event=item.event)

        dumped = {
            k: v.homie_dumper()
            for k, v
            in aspired.items()}

        if len(dumped) == 0:
            return


        items = aspired.items()

        for name, action in items:

            group = groups[name]

            if action.scene is not None:
                self.__scene_set(
                    group, action)

            if action.level is not None:
                self.__level_set(
                    group, action)

            if action.state is not None:
                self.__state_set(
                    group, action)

            if _dryrun is False:
                action.update_timer()


        block_sleep(1)


    def __streams(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        if STREAM.empty():
            return

        homie = self.__homie
        config = homie.config
        sargs = config.sargs

        _watcher = sargs['watcher']
        _actions = sargs['actions']


        def _phue_stream(
            item: StreamItem,
        ) -> None:

            related = isinstance(
                item, PhueStreamItem)

            if related is False:
                return

            if _actions is True:
                self.__aspired(item)

            if _watcher is True:
                _phue_print(item)


        def _phue_print(
            item: StreamItem,
        ) -> None:

            assert isinstance(
                item, PhueStreamItem)

            stamp = item.times.human
            since = item.times.since

            duration = Duration(since)

            bridge = (
                homie.phue_bridges
                [item.bridge])

            header = {
                'Source': 'Philips Hue',
                'Bridge': bridge.name,
                'Timestamp': stamp,
                'Elapsed': duration}

            printer(header, item.event)


        while not STREAM.empty():

            item = STREAM.get()

            _phue_stream(item)


    def __operate(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie
        config = homie.config
        sargs = config.sargs

        _desires = sargs['desires']
        _actions = sargs['actions']
        _watcher = sargs['watcher']

        try:

            if _watcher or _actions:
                self.__streams()

            if _desires is True:
                self.__desired()

        except Exception as reason:

            homie.log_e(
                base='Service',
                name=self.name[8:],
                status='exception',
                exc_info=reason)

            block_sleep(1)


    def run(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie
        config = homie.config
        sargs = config.sargs

        homie.log_i(
            base='Service',
            name=self.name[8:],
            status='started')


        enabled = any([
            sargs['desires'],
            sargs['actions'],
            sargs['watcher']])

        if enabled is False:
            shutdown()


        while not NOACTION.is_set():

            self.__operate()

            block_sleep(0.15)


        homie.log_i(
            base='Service',
            name=self.name[8:],
            status='stopped')


    def __state_set(
        self,
        group: HomieGroup,
        item: HomieDesire | HomieAction,
    ) -> None:
        """
        Update the current state of the group within the bridge.

        :param group: Another class instance for Homie Automate.
        :param item: Another class instance for Homie Automate.
        """

        homie = self.__homie
        config = homie.config
        params = config.params

        _dryrun = params.dryrun
        _idempt = params.idempt
        _quiet = params.quiet


        current = group.state_get()
        desired = item.state

        assert desired is not None

        same = desired == current


        changed = False

        if same and _idempt:
            changed = False

        elif _dryrun is False:

            homie.state_set(
                group, desired)

            block_sleep(1)

            changed = True


        level = 'debug'

        if same and not _quiet:
            level = 'info'

        if desired != current:
            level = 'info'


        if changed is True:

            phue_bridge = (
                group.phue_bridge)

            if phue_bridge is not None:
                phue_bridge.refresh()

            homie.refresh_object()


        origin = (
            f'{item.type}/{item.name}')

        status = (
            'issued'
            if changed is True
            else 'skipped')

        homie.log(
            level=level,
            base='Service',
            name=self.name[8:],
            item='state/set',
            origin=origin,
            group=group.name,
            current=current,
            desired=desired,
            status=status)


    def __level_set(
        self,
        group: HomieGroup,
        item: HomieDesire | HomieAction,
    ) -> None:
        """
        Update the current level of the group within the bridge.

        :param group: Another class instance for Homie Automate.
        :param item: Another class instance for Homie Automate.
        """

        homie = self.__homie
        config = homie.config
        params = config.params

        _dryrun = params.dryrun
        _idempt = params.idempt
        _quiet = params.quiet


        current = group.level_get()
        desired = item.level

        assert desired is not None

        same = desired == current


        changed = False

        if same and _idempt:
            changed = False

        elif _dryrun is False:

            homie.level_set(
                group, desired)

            block_sleep(1)

            changed = True


        level = 'debug'

        if same and not _quiet:
            level = 'info'

        if desired != current:
            level = 'info'


        if changed is True:

            phue_bridge = (
                group.phue_bridge)

            if phue_bridge is not None:
                phue_bridge.refresh()

            homie.refresh_object()


        origin = (
            f'{item.type}/{item.name}')

        status = (
            'issued'
            if changed is True
            else 'skipped')

        homie.log(
            level=level,
            base='Service',
            name=self.name[8:],
            item='level/set',
            origin=origin,
            group=group.name,
            current=current,
            desired=desired,
            status=status)


    def __scene_set(
        self,
        group: HomieGroup,
        item: HomieDesire | HomieAction,
    ) -> None:
        """
        Update the current scene of the group within the bridge.

        :param group: Another class instance for Homie Automate.
        :param item: Another class instance for Homie Automate.
        """

        homie = self.__homie
        config = homie.config
        params = config.params
        scenes = homie.scenes

        _dryrun = params.dryrun
        _idempt = params.idempt
        _quiet = params.quiet


        assert item.scene is not None

        current = group.scene_get()
        desired = scenes[item.scene]

        same = desired == current


        changed = False

        if same and _idempt:
            changed = False

        elif _dryrun is False:

            homie.scene_set(
                group, desired)

            block_sleep(1)

            changed = True


        level = 'debug'

        if same and not _quiet:
            level = 'info'

        if desired != current:
            level = 'info'


        if changed is True:

            phue_bridge = (
                group.phue_bridge)

            if phue_bridge is not None:
                phue_bridge.refresh()

            homie.refresh_object()


        origin = (
            f'{item.type}/{item.name}')

        _current = (
            'unset'
            if current is None
            else current.name)

        status = (
            'issued'
            if changed is True
            else 'skipped')

        homie.log(
            level=level,
            base='Service',
            name=self.name[8:],
            item='scene/set',
            origin=origin,
            group=group.name,
            current=_current,
            desired=desired.name,
            status=status)



class PhueStream(Thread):
    """
    Handle when exceptions occur within the thread routine.

    :param bridge: Another class instance for Homie Automate.
    """

    __homie: Homie
    __name: str

    __bridge: 'PhueBridge'


    def __init__(
        self,
        bridge: 'PhueBridge',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie = bridge.homie
        name = bridge.name

        self.__homie = homie
        self.__name = name

        self.__bridge = bridge

        super().__init__(
            name=f'stream/{name}')


    async def __operate(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie
        bridge = self.__bridge
        config = homie.config
        sargs = config.sargs

        _timeout = sargs['timeout']


        def _process() -> None:

            for data in datas:

                item = PhueStreamItem(
                    bridge=bridge.name,
                    event=data,
                    times=Times('now'))

                STREAM.put(item)


        while not NOSTREAM.is_set():

            stream = (
                bridge.bridge
                .events_async(_timeout))

            try:

                homie.log_d(
                    base='PhueStream',
                    name=self.name[7:],
                    status='reading')

                async for datas in stream:
                    _process()

            except CancelledError:

                homie.log_i(
                    base='PhueStream',
                    name=self.name[7:],
                    status='canceled')

            except ReadTimeout:

                homie.log_d(
                    base='PhueStream',
                    name=self.name[7:],
                    status='timeout')

            except Exception as reason:

                homie.log_e(
                    base='PhueStream',
                    name=self.name[7:],
                    status='exception',
                    exc_info=reason)

        await asyncio.sleep(0)


    def run(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie

        homie.log_i(
            base='PhueStream',
            name=self.name[7:],
            status='started')


        ALOOPS[self.name] = (
            asyncio
            .new_event_loop())


        loop = ALOOPS[self.name]

        (asyncio
         .set_event_loop(loop))

        loop.run_until_complete(
            self.__operate())


        loop.close()


        homie.log_i(
            base='PhueStream',
            name=self.name[7:],
            status='stopped')



def operate_main(
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    config = homie.config
    sargs = config.sargs

    _actions = sargs['actions']
    _watcher = sargs['watcher']


    def _homie_service() -> None:

        thread = Service(homie)

        thread.start()

        name = thread.name

        THREADS[name] = thread


    def _phue_streams() -> None:

        bridges = (
            homie.phue_bridges
            .values())

        for bridge in bridges:

            thread = PhueStream(bridge)

            thread.start()

            name = thread.name

            THREADS[name] = thread


    try:

        _homie_service()

        if _actions or _watcher:
            _phue_streams()

    finally:

        threads = THREADS.values()

        for thread in threads:

            homie.log_i(
                base='script',
                thread=thread.name,
                status='joining')

            thread.join()

            homie.log_i(
                base='script',
                thread=thread.name,
                status='joined')



def shutdown(
    *args: Any,  # noqa: ANN401
    **kwargs: Any,  # noqa: ANN401
) -> None:
    """
    Perform whatever operations are associated with the file.
    """

    NOSTREAM.set()


    for loop in ALOOPS.values():

        tasks = (
            asyncio
            .all_tasks(loop))

        for task in tasks:
            task.cancel(True)


    for loop in ALOOPS.values():

        while loop.is_running():
            block_sleep(0.5)


    NOACTION.set()



def launcher_main() -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    args = launcher_args()

    config = Config(
        args['config'],
        sargs=args)

    config.logger.start()

    config.logger.log_i(
        base='script',
        status='started')


    homie = Homie(config)


    signal(SIGINT, shutdown)
    signal(SIGTERM, shutdown)
    signal(SIGHUP, shutdown)


    operate_main(homie)


    config.logger.log_i(
        base='script',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
