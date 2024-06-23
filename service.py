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



STOP_STREAM = AsyncEvent()
STOP_ACTION = AsyncEvent()

ALOOPS: dict[str, AbstractEventLoop] = {}
THREADS: dict[str, Thread] = {}



@dataclass
class StreamItem:
    """
    Contain information about the event received from stream.
    """

    event: dict[str, Any]
    times: Times



@dataclass
class PhueStreamItem(StreamItem):
    """
    Contain information about the event received from stream.
    """

    bridge: str



PHUE_STREAM: Queue[PhueStreamItem] = Queue()



def launcher_args() -> dict[str, Any]:
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
        dest='idemp',
        help=(
            'do not make change if '
            'would not change value'))

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
        '--refresh',
        type=int,
        default=15,
        help=(
            'period of time before '
            'refreshing the objects'))

    parser.add_argument(
        '--timeout',
        type=float,
        default=60,
        help=(
            'period of time before '
            'reconnecting to server'))

    parser.add_argument(
        '--pause',
        type=int,
        default=60,
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



class HomieService(Thread):
    """
    Handle when exceptions occur within the thread routine.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name used when creating new thread object.
    """

    __homie: Homie
    __name: str

    __refresh: Timer
    __desires: Timer


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

        _name = f'service/{name}'

        super().__init__(name=_name)


        config = homie.config
        sargs = config.sargs

        self.__refresh = Timer(
            sargs['refresh'])

        _pause = sargs['pause']

        self.__desires = Timer(
            _pause,
            start=f'-{_pause}s')


    def __operate_desires(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie
        timer = self.__desires

        if not timer.ready():
            return

        config = homie.config
        groups = homie.groups
        sargs = config.sargs

        _dryrun = sargs['dryrun']


        desired = homie.desired

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


    def __operate_actions(
        self,
        item: StreamItem,
    ) -> None:
        """
        Perform whatever operations are associated with the file.

        :param item: Queue item that was received from upstream.
        """

        homie = self.__homie
        config = homie.config
        groups = homie.groups
        sargs = config.sargs

        _dryrun = sargs['dryrun']


        event = item.event

        aspired = homie.aspired(event)

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


    def __operate_streams(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        if PHUE_STREAM.empty():
            return

        homie = self.__homie
        config = homie.config
        sargs = config.sargs

        _watcher = sargs['watcher']
        _actions = sargs['actions']


        def _print_phue_event() -> None:

            timestamp = item.times.human

            duration = Duration(
                item.times.since)

            header = {
                'Source': 'Philips Hue',
                'Bridge': phue_bridge.name,
                'Timestamp': timestamp,
                'Elapsed': duration}

            printer(header, item.event)


        phue_bridges = homie.phue_bridges

        while not PHUE_STREAM.empty():

            item = PHUE_STREAM.get()

            phue_bridge = (
                phue_bridges[item.bridge])

            if _watcher is True:
                _print_phue_event()

            if _actions is True:
                self.__operate_actions(item)


    def run(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie
        config = homie.config
        sargs = config.sargs
        timer = self.__refresh

        _desires = sargs['desires']
        _actions = sargs['actions']
        _watcher = sargs['watcher']

        homie.log_i(
            base='script',
            item='service/thread',
            name=self.name,
            status='started')


        enabled = any([
            _desires,
            _actions,
            _watcher])

        if enabled is False:
            launcher_stop()


        def _operate_routines() -> None:

            if timer.ready():
                homie.refresh_source()

            if _watcher or _actions:
                self.__operate_streams()

            if _desires is True:
                self.__operate_desires()


        while not STOP_ACTION.is_set():

            try:
                _operate_routines()

            except Exception as reason:

                homie.log_e(
                    base='script',
                    item='service/thread',
                    name=self.name,
                    status='exception',
                    exc_info=reason)

                block_sleep(1)

            block_sleep(0.15)


        homie.log_i(
            base='script',
            item='service/thread',
            name=self.name,
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
        sargs = config.sargs

        _dryrun = sargs['dryrun']
        _idemp = sargs['idemp']


        current = group.state_get()
        desired = item.state

        assert desired is not None


        changed = False

        if (desired == current
                and _idemp is True):
            changed = False

        elif _dryrun is False:

            homie.state_set(
                group, desired)

            block_sleep(1)

            changed = True

        homie.log_i(
            base='script',
            action='state_set',
            group=group.name,
            current=current,
            desired=desired,
            status=(
                'submit' if changed
                else 'skipped'))


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
        sargs = config.sargs

        _dryrun = sargs['dryrun']
        _idemp = sargs['idemp']


        current = group.level_get()
        desired = item.level

        assert desired is not None


        changed = False

        if (desired == current
                and _idemp is True):
            changed = False

        elif _dryrun is False:

            homie.level_set(
                group, desired)

            block_sleep(1)

            changed = True

        homie.log_i(
            base='script',
            action='level_set',
            group=group.name,
            current=current,
            desired=desired,
            status=(
                'submit' if changed
                else 'skipped'))


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
        scenes = homie.scenes
        sargs = config.sargs

        _dryrun = sargs['dryrun']
        _idemp = sargs['idemp']


        assert item.scene is not None

        current = group.scene_get()
        desired = scenes[item.scene]


        changed = False

        if (desired == current
                and _idemp is True):
            changed = False

        elif _dryrun is False:

            homie.scene_set(
                group, desired)

            block_sleep(1)

            changed = True

        _current = (
            current.name
            if current is not None
            else None)

        homie.log_i(
            base='script',
            action='scene_set',
            group=group.name,
            current=(
                _current if _current
                else 'unset'),
            desired=desired.name,
            status=(
                'submit' if changed
                else 'skipped'))



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

        _name = (
            'stream/phue/'
            f'bridge/{name}')

        super().__init__(name=_name)


    async def __operate_stream(
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

                PHUE_STREAM.put(item)


        while not STOP_STREAM.is_set():

            stream = (
                bridge.bridge
                .events_async(_timeout))

            try:

                homie.log_d(
                    base='script',
                    item='service/thread',
                    name=self.name,
                    status='reading')

                async for datas in stream:
                    _process()

            except CancelledError:

                homie.log_i(
                    base='script',
                    item='service/thread',
                    name=self.name,
                    status='canceled')

            except ReadTimeout:

                homie.log_d(
                    base='script',
                    item='service/thread',
                    name=self.name,
                    status='timeout')

            except Exception as reason:

                homie.log_e(
                    base='script',
                    item='service/thread',
                    name=self.name,
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
            base='script',
            item='service/thread',
            name=self.name,
            status='started')


        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        ALOOPS[self.name] = loop

        loop.run_until_complete(
            self.__operate_stream())

        loop.close()


        homie.log_i(
            base='script',
            item='service/thread',
            name=self.name,
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

        thread = HomieService(homie)

        thread.start()

        name = thread.name

        THREADS[name] = thread


    def _phue_streams() -> None:

        bridges = homie.phue_bridges

        values = bridges.values()

        for bridge in values:

            thread = PhueStream(bridge)

            thread.start()

            name = thread.name

            THREADS[name] = thread


    _homie_service()

    if _actions or _watcher:
        _phue_streams()



def launcher_stop(
    *args: Any,  # noqa: ANN401
    **kwargs: Any,  # noqa: ANN401
) -> None:
    """
    Perform whatever operations are associated with the file.
    """

    STOP_STREAM.set()


    for loop in ALOOPS.values():

        tasks = asyncio.all_tasks(loop)

        for task in tasks:
            task.cancel(True)


    for loop in ALOOPS.values():

        while loop.is_running():
            block_sleep(1)


    STOP_ACTION.set()



def launcher_main() -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    args = launcher_args()

    config = Config(
        args['config'],
        {'dryrun': args['dryrun']},
        sargs=args)

    config.logger.start()

    config.logger.log_i(
        base='script',
        item='service',
        status='merged')


    homie = Homie(config)

    homie.refresh_source()


    signal(SIGINT, launcher_stop)
    signal(SIGTERM, launcher_stop)
    signal(SIGHUP, launcher_stop)


    try:
        operate_main(homie)

    finally:

        threads = THREADS.values()

        for thread in threads:
            thread.join()


    config.logger.log_i(
        base='script',
        item='service',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
