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
from enhomie.philipshue import PhueBridge

AbstractEventLoop = asyncio.AbstractEventLoop
AsyncEvent = asyncio.Event
CancelledError = asyncio.CancelledError



STOP_STREAM = AsyncEvent()
STOP_ACTION = AsyncEvent()

ALOOPS: dict[str, AbstractEventLoop] = {}
THREADS: dict[str, Thread] = {}



@dataclass
class PhueStreamItem:
    """
    Contain information about the event received from stream.
    """

    bridge: str
    event: dict[str, Any]
    times: Times



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
        '--print_events',
        action='store_true',
        default=False,
        dest='stdoute',
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
        '--pause',
        type=float,
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

    __timer: Timer


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

        config = homie.config
        sargs = config.sargs

        _pause = sargs['pause']

        super().__init__(name=_name)

        self.__timer = Timer(
            _pause,
            start=f'-{_pause}s')


    def __operate_desire(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        timer = self.__timer

        if not timer.ready():
            return


    def __operate_stream(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie
        config = homie.config
        sargs = config.sargs


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

            if sargs['stdoute']:
                _print_phue_event()


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

        while not STOP_ACTION.is_set():

            block_sleep(0.15)

            self.__operate_desire()
            self.__operate_stream()

        homie.log_i(
            base='script',
            item='service/thread',
            name=self.name,
            status='stopped')



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


        while not STOP_STREAM.is_set():

            try:

                await asyncio.sleep(
                    sargs['timeout'])

                item = PhueStreamItem(
                    bridge=bridge.name,
                    event={'foo': 'bar'},
                    times=Times('now'))

                PHUE_STREAM.put(item)

            except CancelledError:

                homie.log_i(
                    base='script',
                    item='service/thread',
                    name=self.name,
                    status='canceled')

            except Exception as reason:

                homie.log_i(
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


    _phue_streams()

    _homie_service()



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
        sargs=args)

    config.logger.start()

    config.logger.log_i(
        base='script',
        item='service',
        status='merged')

    homie = Homie(config)


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
