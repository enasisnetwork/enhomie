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
from time import sleep
from typing import Any
from typing import Optional

from encommon.utils import array_ansi
from encommon.utils import print_ansi

from enhomie.config import Config
from enhomie.homie import Homie
from enhomie.philipshue import PhueBridge

from httpx import ReadTimeout

CancelledError = asyncio.CancelledError
AsyncEvent = asyncio.Event



QITEM = dict[str, Any]
QUEUE: Queue[Optional[QITEM]] = Queue()

EVENT = AsyncEvent()

ALOOP = asyncio.get_event_loop()



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
        '--print',
        action='store_true',
        default=False,
        help=(
            'print out the events '
            'that are received'))

    parser.add_argument(
        '--idempotent',
        action='store_true',
        default=False,
        dest='idemp',
        help=(
            'do not make change if '
            'would not change value'))

    parser.add_argument(
        '--scope',
        required=True,
        choices=['phue_bridge'],
        help=(
            'which kind of objects '
            'are dumped to console'))

    parser.add_argument(
        '--name',
        required=True,
        help=(
            'name of the object to '
            'stream events from'))

    parser.add_argument(
        '--timeout',
        type=float,
        default=60,
        help=(
            'period of time before '
            'reconnecting to server'))

    return vars(parser.parse_args())



class QueueThread(Thread):
    """
    Handle when exceptions occur within the thread routine.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie

        super().__init__(
            name='queue',
            target=process,
            args=[homie])


    def run(
        self,
    ) -> None:
        """
        Perform whatever operations are associated with the file.
        """

        homie = self.__homie

        try:

            homie.log_i(
                base='script',
                item='aspired/queue/thread',
                status='started')

            super().run()

        except Exception as reason:

            homie.log_e(
                base='script',
                item='aspired/queue/thread',
                status='exception',
                exc_info=reason)

            shutdown()



def process(  # noqa: CFQ001
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    params = homie.params
    config = homie.config
    groups = homie.groups
    scenes = homie.scenes

    _stdout = config.sargs['print']
    _idemp = config.sargs['idemp']


    def _process(  # noqa: CFQ001
        event: QITEM,
    ) -> None:

        aspired = homie.aspired(event)

        dumped = {
            k: v.homie_dumper()
            for k, v
            in aspired.items()}

        if len(dumped) == 0:
            return


        def _state_set() -> None:

            current = group.state_get()
            aspired = action.state

            assert aspired is not None

            changed = False

            if (aspired == current
                    and _idemp is True):
                changed = False

            elif params.dryrun is False:

                homie.state_set(
                    group, aspired)

                sleep(1)

                changed = True

            status['state'] = {
                'current': current,
                'aspired': aspired,
                'changed': changed}


        def _level_set() -> None:

            current = group.level_get()
            aspired = action.level

            assert aspired is not None

            changed = False

            if (aspired == current
                    and _idemp is True):
                changed = False

            elif params.dryrun is False:

                homie.level_set(
                    group, aspired)

                sleep(1)

                changed = True

            status['level'] = {
                'current': current,
                'aspired': aspired,
                'changed': changed}


        def _scene_set() -> None:

            assert action.scene is not None

            current = group.scene_get()
            aspired = scenes[action.scene]

            changed = False

            if (aspired == current
                    and _idemp is True):
                changed = False

            elif params.dryrun is False:

                homie.scene_set(
                    group, aspired)

                sleep(1)

                changed = True

            _current = (
                current.name
                if current is not None
                else None)

            status['scene'] = {
                'current': _current,
                'aspired': aspired.name,
                'changed': changed}


        items = aspired.items()

        for name, action in items:

            group = groups[name]

            status: dict[str, Any] = {
                'group': group.name}

            if action.scene is not None:
                _scene_set()

            if action.level is not None:
                _level_set()

            if action.state is not None:
                _state_set()

            action.update_timer()

            if _stdout is True:
                print_ansi(
                    f'<c31>{"-" * 64}<c0>\n'
                    f'{array_ansi(status)}\n'
                    f'<c31>{"-" * 64}<c0>')


    while True:

        event = QUEUE.get()

        if event is None:
            break

        if _stdout is True:
            print_ansi(
                f'<c36>{"-" * 64}<c0>\n'
                f'{array_ansi(event)}\n'
                f'<c36>{"-" * 64}<c0>')

        homie.refresh()

        _process(event)



def stream(
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    config = homie.config

    scope = config.sargs['scope']
    name = config.sargs['name']


    assert scope == 'phue_bridge'


    bridges = homie.phue_bridges
    bridge = bridges[name]

    homie.log_i(
        base='script',
        item='aspired/stream',
        type='phue_bridge',
        name=bridge.name,
        status='running')

    ALOOP.run_until_complete(
        stream_phue_bridge(bridge))

    homie.log_i(
        base='script',
        item='aspired/stream',
        type='phue_bridge',
        name=bridge.name,
        status='complete')



async def stream_phue_bridge(
    bridge: PhueBridge,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param bridge: Another class instance for Homie Automate.
    """

    homie = bridge.homie

    config = homie.config

    timeout = config.sargs['timeout']


    while not EVENT.is_set():

        stream = (
            bridge.bridge
            .events_async(timeout))

        homie.log_i(
            base='script',
            item='aspired/stream',
            type='phue_bridge',
            name=bridge.name,
            status='reading')

        try:

            async for events in stream:

                for event in events:

                    QUEUE.put(event)

        except CancelledError:  # noqa: ASYNC103

            homie.log_i(
                base='script',
                item='aspired/stream',
                type='phue_bridge',
                name=bridge.name,
                status='canceled')

            break  # noqa: ASYNC104

        except ReadTimeout:

            homie.log_i(
                base='script',
                item='aspired/stream',
                type='phue_bridge',
                name=bridge.name,
                status='timeout')

            continue

        await asyncio.sleep(0)


    await asyncio.sleep(0)



def shutdown(
    *args: Any,  # noqa: ANN401
    **kwargs: Any,  # noqa: ANN401
) -> None:
    """
    Perform whatever operations are associated with the file.
    """

    EVENT.set()

    tasks = asyncio.all_tasks(ALOOP)

    for task in tasks:
        task.cancel(True)



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
        item='aspired',
        status='merged')

    homie = Homie(config)


    signal(SIGINT, shutdown)
    signal(SIGTERM, shutdown)
    signal(SIGHUP, shutdown)


    thread = QueueThread(homie)

    thread.start()

    config.logger.log_i(
        base='script',
        item='aspired/queue',
        status='started')


    try:
        stream(homie)

    finally:

        QUEUE.put(None)

        homie.log_i(
            base='script',
            item='aspired/queue',
            status='stopping')

        thread.join()

        homie.log_i(
            base='script',
            item='aspired/queue',
            status='stopped')

        ALOOP.close()


    config.logger.log_i(
        base='script',
        item='aspired',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
