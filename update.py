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
    sargs = config.sargs
    groups = homie.groups
    scenes = homie.scenes

    _idemp = sargs['idemp']
    _dryrun = sargs['dryrun']

    _group = sargs['group']
    _scene = sargs['scene']
    _level = sargs['level']
    _state = sargs['state']


    group = groups[_group]


    def _state_set() -> None:

        # Based on service method

        current = group.state_get()
        desired = _state.strip()

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


    def _level_set() -> None:

        # Based on service method

        current = group.level_get()
        desired = int(_level)

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


    def _scene_set() -> None:

        # Based on service method

        current = group.scene_get()
        desired = scenes[_scene]

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
        item='update',
        status='merged')


    homie = Homie(config)

    homie.refresh_source()


    operate_main(homie)


    config.logger.log_i(
        base='script',
        item='update',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
