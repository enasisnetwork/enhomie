"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
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
        '--group',
        required=True,
        help=(
            'which Homie group the '
            'scene will be updated'))

    parser.add_argument(
        '--scene',
        required=True,
        help=(
            'which Homie scnee the '
            'group will be updated'))

    return vars(parser.parse_args())



def operate_main(
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    config = homie.config

    groups = homie.groups
    scenes = homie.scenes


    _group = config.sargs['group']
    _scene = config.sargs['scene']

    group = groups[_group]
    scene = scenes[_scene]


    homie.scene_set(group, scene)



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
        item='scener',
        status='merged')


    homie = Homie(config)


    operate_main(homie)


    config.logger.log_i(
        base='script',
        item='scener',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
