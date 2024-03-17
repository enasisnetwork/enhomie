"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from argparse import Namespace

from enhomie.config import Config
from enhomie.homie import Homie



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

    return parser.parse_args()



def launcher_main() -> None:
    """
    Perform whatever operations are associated with the file.
    """

    args = vars(launcher_args())

    config = Config(args['config'])

    config.logger.start()

    config.logger.log_i(
        base='project',
        item='scener',
        status='merged')

    homie = Homie(config)

    group = args['group']
    scene = args['scene']

    homie.scene_set(group, scene)

    config.logger.log_i(
        base='project',
        item='scener',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
