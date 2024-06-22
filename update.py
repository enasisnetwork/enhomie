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
    _level = config.sargs['level']
    _state = config.sargs['state']

    group = groups[_group]


    if _scene is not None:
        scene = scenes[_scene]
        homie.scene_set(group, scene)

    if _level is not None:
        level = int(_level)
        homie.level_set(group, level)

    if _state is not None:
        state = _state.strip()
        homie.state_set(group, state)



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


    operate_main(homie)


    config.logger.log_i(
        base='script',
        item='update',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
