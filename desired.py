"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from argparse import Namespace
from typing import Optional

from encommon.utils import print_ansi

from enhomie.config import Config
from enhomie.homie import Homie
from enhomie.homie import HomieScene



def launcher_args() -> Namespace:
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
        help=(
            'do not execute action '
            'and show what would do'))

    return parser.parse_args()



def launcher_main() -> None:
    """
    Perform whatever operations are associated with the file.
    """

    args = vars(launcher_args())

    dryrun = args['dry_run']

    config = Config(
        args['config'],
        {'dryrun': dryrun})

    config.logger.start()

    config.logger.log_i(
        base='project',
        item='desired',
        status='merged')

    homie = Homie(config)

    groups = homie.groups
    scenes = homie.scenes


    items = homie.desired.items()

    for group_name, desire in items:

        group = groups[group_name]
        scene: Optional[HomieScene] = None


        if group.phue_unique:
            scene = homie.scene_get(group)

        current = (
            f'<c96>{scene.name}<c0>'
            if scene is not None
            else '<c36>unknown<c0>')


        print_ansi(
            f'<c96>{group.name}<c37>: '
            f'<c36>{desire.name}<c37>/'
            f'<c96>{desire.scene}<c37> '
            f'(<c96>{current}<c37>)<c0>')


        if dryrun is True:
            continue

        scene = scenes[desire.scene]

        homie.scene_set(group, scene)

        desire.update_timer()


    config.logger.log_i(
        base='project',
        item='desired',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
