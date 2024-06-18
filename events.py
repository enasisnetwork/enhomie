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
        '--print',
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
        '--actions',
        action='store_true',
        default=False,
        help=(
            'perform the actions on '
            'the received events'))

    return vars(parser.parse_args())



def iterate(
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    config = homie.config
    groups = homie.groups
    scenes = homie.scenes

    _print = config.sargs['print']
    actions = config.sargs['actions']


    def _actions(
        event: QITEM,
    ) -> None:

        aspired = homie.aspired(event)

        dumped = {
            k: v.homie_dumper()
            for k, v
            in aspired.items()}

        if len(dumped) == 0:
            return

        if _print is True:
            print_ansi(
                f'<c31>{"-" * 64}<c0>\n'
                f'{array_ansi(dumped)}\n'
                f'<c31>{"-" * 64}<c0>')


        if actions is True:


            items = aspired.items()

            for name, action in items:

                group = groups[name]


                active = 'unknown'

                if group.phue_unique:

                    _active = (
                        homie.scene_get(group))

                    if _active is not None:
                        active = _active.name


                print_ansi(
                    f'<c96>{group.name}<c37>: '
                    f'<c36>{action.name}<c37>/'
                    f'<c96>{action.scene}<c37> '
                    f'(<c96>{active}<c37>)<c0>')


                scene = scenes[action.scene]

                homie.scene_set(group, scene)

                action.update_timer()


    while True:

        event = QUEUE.get()

        if event is None:
            break

        if _print is True:
            print_ansi(
                f'<c36>{"-" * 64}<c0>\n'
                f'{array_ansi(event)}\n'
                f'<c36>{"-" * 64}<c0>')

        if actions is True:
            _actions(event)



def streams(
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    config = homie.config

    scope = config.sargs['scope']
    name = config.sargs['name']


    if scope == 'phue_bridge':

        bridges = homie.phue_bridges
        bridge = bridges[name]

        homie.log_i(
            base='script',
            item='events/stream',
            type='phue_bridge',
            name=bridge.name,
            status='running')

        ALOOP.run_until_complete(
            phue_stream(bridge))

        homie.log_i(
            base='script',
            item='events/stream',
            type='phue_bridge',
            name=bridge.name,
            status='complete')



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



async def phue_stream(
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
            item='events/stream',
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
                item='events/stream',
                type='phue_bridge',
                name=bridge.name,
                status='canceled')

            break  # noqa: ASYNC104

        except ReadTimeout:

            homie.log_i(
                base='script',
                item='events/stream',
                type='phue_bridge',
                name=bridge.name,
                status='timeout')

            continue

        await asyncio.sleep(0)


    await asyncio.sleep(0)



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
        item='events',
        status='merged')

    homie = Homie(config)


    signal(SIGINT, shutdown)
    signal(SIGTERM, shutdown)
    signal(SIGHUP, shutdown)


    thread = Thread(
        target=iterate,
        args=[homie])

    thread.start()

    config.logger.log_i(
        base='script',
        item='events/queue',
        status='started')


    try:
        streams(homie)

    finally:

        QUEUE.put(None)

        homie.log_i(
            base='script',
            item='events/queue',
            status='stopping')

        thread.join()

        homie.log_i(
            base='script',
            item='events/queue',
            status='stopped')

        ALOOP.close()


    config.logger.log_i(
        base='script',
        item='events',
        status='stopped')



if __name__ == '__main__':

    launcher_main()
