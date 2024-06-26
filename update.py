"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from time import sleep as block_sleep
from typing import Any

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

    config = homie.config
    params = config.params
    sargs = config.sargs
    groups = homie.groups
    scenes = homie.scenes

    _idempt = params.idempt
    _dryrun = params.dryrun

    _group = sargs['group']
    _scene = sargs['scene']
    _level = sargs['level']
    _state = sargs['state']


    group = groups[_group]


    def _state_set() -> None:

        # Based on service method

        current = group.state_get()
        desired = _state.strip()

        same = desired == current


        changed = False

        if same and _idempt:
            changed = False

        elif _dryrun is False:

            homie.state_set(
                group, desired)

            block_sleep(1)

            changed = True


        if changed is True:

            phue_bridge = (
                group.phue_bridge)

            if phue_bridge is not None:
                phue_bridge.refresh()

            homie.refresh_object()


        status = (
            'issued'
            if changed is True
            else 'skipped')

        homie.log_i(
            base='script',
            item='state/set',
            group=group.name,
            current=current,
            desired=desired,
            status=status)


    def _level_set() -> None:

        # Based on service method

        current = group.level_get()
        desired = int(_level)

        same = desired == current


        changed = False

        if same and _idempt:
            changed = False

        elif _dryrun is False:

            homie.level_set(
                group, desired)

            block_sleep(1)

            changed = True


        if changed is True:

            phue_bridge = (
                group.phue_bridge)

            if phue_bridge is not None:
                phue_bridge.refresh()

            homie.refresh_object()


        status = (
            'issued'
            if changed is True
            else 'skipped')

        homie.log_i(
            base='script',
            item='level/set',
            group=group.name,
            current=current,
            desired=desired,
            status=status)


    def _scene_set() -> None:

        # Based on service method

        current = group.scene_get()
        desired = scenes[_scene]

        same = desired == current


        changed = False

        if same and _idempt:
            changed = False

        elif _dryrun is False:

            homie.scene_set(
                group, desired)

            block_sleep(1)

            changed = True


        if changed is True:

            phue_bridge = (
                group.phue_bridge)

            if phue_bridge is not None:
                phue_bridge.refresh()

            homie.refresh_object()


        _current = (
            'unset'
            if current is None
            else current.name)

        status = (
            'issued'
            if changed is True
            else 'skipped')

        homie.log_i(
            base='script',
            item='scene/set',
            group=group.name,
            current=_current,
            desired=desired.name,
            status=status)


    if _scene is not None:
        _scene_set()

    if _level is not None:
        _level_set()

    if _state is not None:
        _state_set()



def launcher_main() -> None:
    """
    Perform whatever operations are associated with the file.
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


    operate_main(homie)


    config.logger.log_i(
        base='script',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
