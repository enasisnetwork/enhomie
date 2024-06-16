"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from typing import Any

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

    return vars(parser.parse_args())



def operate_main(
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    params = homie.params
    groups = homie.groups
    scenes = homie.scenes


    items = homie.desired.items()

    for name, desire in items:

        group = groups[name]


        active = 'unknown'

        if group.phue_unique:

            _active = (
                homie.scene_get(group))

            if _active is not None:
                active = _active.name


        print_ansi(
            f'<c96>{group.name}<c37>: '
            f'<c36>{desire.name}<c37>/'
            f'<c96>{desire.scene}<c37> '
            f'(<c96>{active}<c37>)<c0>')


        if params.dryrun is True:
            continue

        scene = scenes[desire.scene]

        homie.scene_set(group, scene)

        desire.update_timer()



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
        item='desired',
        status='merged')


    homie = Homie(config)


    operate_main(homie)


    config.logger.log_i(
        base='script',
        item='desired',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
