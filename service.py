"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from argparse import ArgumentParser
from queue import Queue
from signal import SIGHUP
from signal import SIGINT
from signal import SIGTERM
from signal import signal
from threading import Thread
from time import sleep as block_sleep
from typing import Any
from typing import Optional

from enhomie.config import Config
from enhomie.homie import Homie
from enhomie.philipshue import PhueBridge

AbstractEventLoop = asyncio.AbstractEventLoop
AsyncEvent = asyncio.Event



QITEM = dict[str, Any]
STREAM: Queue[Optional[QITEM]] = Queue()

SHUTDOWN = AsyncEvent()
THREADS: dict[str, Thread] = {}



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

    return vars(parser.parse_args())



class HomieService(Thread):
    """
    Handle when exceptions occur within the thread routine.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name used when creating new thread object.
    """

    __homie: Homie
    __name: str


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


    def __operate_desire(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        if SHUTDOWN.is_set():
            return

        block_sleep(1)


    def __operate_action(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        if SHUTDOWN.is_set():
            return

        block_sleep(1)


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

        while not SHUTDOWN.is_set():
            self.__operate_desire()
            self.__operate_action()

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

        while not SHUTDOWN.is_set():

            await asyncio.sleep(1)

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

    SHUTDOWN.set()



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
