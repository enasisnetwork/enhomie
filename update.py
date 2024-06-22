"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from time import sleep
from typing import Any

from encommon.utils import array_ansi
from encommon.utils import print_ansi

from enhomie.config import Config
from enhomie.homie import Homie



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
        '--group',
        required=True,
        help=(
            'which Homie group the '
            'state will be updated'))

    parser.add_argument(
        '--scene',
        help=(
            'which Homie scene the '
            'group will be updated'))

    parser.add_argument(
        '--state',
        help=(
            'which state value the '
            'group will be updated'))

    parser.add_argument(
        '--level',
        help=(
            'which level value the '
            'group will be updated'))

    return vars(parser.parse_args())



def operate_main(  # noqa: CFQ001
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

    _group = config.sargs['group']
    _scene = config.sargs['scene']
    _level = config.sargs['level']
    _state = config.sargs['state']


    group = groups[_group]

    status: dict[str, Any] = {
        'group': group.name}


    def _state_set() -> None:

        current = group.state_get()
        desired = _state.strip()

        changed = False

        if (desired == current
                and _idemp is True):
            changed = False

        elif params.dryrun is False:

            homie.state_set(
                group, desired)

            sleep(1)

            changed = True

        status['state'] = {
            'current': current,
            'desired': desired,
            'changed': changed}


    def _level_set() -> None:

        current = group.level_get()
        desired = int(_level)

        changed = False

        if (desired == current
                and _idemp is True):
            changed = False

        elif params.dryrun is False:

            homie.level_set(
                group, desired)

            sleep(1)

            changed = True

        status['level'] = {
            'current': current,
            'desired': desired,
            'changed': changed}


    def _scene_set() -> None:

        current = group.scene_get()
        desired = scenes[_scene]

        changed = False

        if (desired == current
                and _idemp is True):
            changed = False

        elif params.dryrun is False:

            homie.scene_set(
                group, desired)

            sleep(1)

            changed = True

        _current = (
            current.name
            if current is not None
            else None)

        status['scene'] = {
            'current': _current,
            'desired': desired.name,
            'changed': changed}


    if _scene is not None:
        _scene_set()

    if _level is not None:
        _level_set()

    if _state is not None:
        _state_set()


    if _stdout is True:
        print_ansi(
            f'<c31>{"-" * 64}<c0>\n'
            f'{array_ansi(status)}\n'
            f'<c31>{"-" * 64}<c0>')



def launcher_main() -> None:
    """
    Perform whatever operations are associated with the file.
    """

    args = launcher_args()

    config = Config(
        args['config'],
        {'dryrun': args['dryrun']},
        sargs=args)

    config.logger.start()

    config.logger.log_i(
        base='script',
        item='update',
        status='merged')


    homie = Homie(config)


    operate_main(homie)


    config.logger.log_i(
        base='script',
        item='update',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
