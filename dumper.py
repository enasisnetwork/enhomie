"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from argparse import Namespace
from json import dumps

from encommon.utils import print_ansi

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
        '--scope',
        required=True,
        choices=[
            'groups', 'scenes', 'desired',
            'phue_bridges', 'ubiq_routers',
            'phue_dumped', 'ubiq_dumped'],
        help=(
            'which kind of objects '
            'are dumped to console'))

    return parser.parse_args()



def print_homie(
    homie: Homie,
    header_about: str,
    header_value: str,
    content: str,
) -> None:
    """
    Print the contents for the object within Homie instance.

    :param homie: Primary class instance for Homie Automator.
    :param header_about: Additional information for output.
    :param header_value: Additional information for output.
    :param content: Primary information content for output.
    """

    print_ansi(f'\n<c96>{"=" * 80}<c0>')
    print_ansi(
        f'<c37>{header_about}: '
        f'<c96;1>{header_value}<c0>')
    print_ansi(f'<c96>{"-" * 80}<c0>')
    print(content)
    print_ansi(f'<c96>{"=" * 80}<c0>\n')



def print_groups(
    homie: Homie,
) -> None:
    """
    Print the contents for the object within Homie instance.

    :param homie: Primary class instance for Homie Automator.
    """

    groups = homie.groups

    for group in groups.values():

        output = (
            group.params
            .model_dump())

        dumped = dumps(
            output,
            default=str,
            indent=2)

        print_homie(
            homie, 'Homie Group',
            group.name, dumped)



def print_scenes(
    homie: Homie,
) -> None:
    """
    Print the contents for the object within Homie instance.

    :param homie: Primary class instance for Homie Automator.
    """

    scenes = homie.scenes

    for scene in scenes.values():

        output = (
            scene.params
            .model_dump())

        dumped = dumps(
            output,
            default=str,
            indent=2)

        print_homie(
            homie, 'Homie Scene',
            scene.name, dumped)



def print_phue_bridges(
    homie: Homie,
) -> None:
    """
    Print the contents for the object within Homie instance.

    :param homie: Primary class instance for Homie Automator.
    """

    bridges = homie.phue_bridges

    for bridge in bridges.values():

        output = (
            bridge.params
            .model_dump())

        if 'token' in output:
            length = len(output['token'])
            output['token'] = '*' * length

        dumped = dumps(
            output,
            default=str,
            indent=2)

        print_homie(
            homie, 'Philips Hue Bridge',
            bridge.name, dumped)



def print_phue_dumped(
    homie: Homie,
) -> None:
    """
    Print the contents for the object within Homie instance.

    :param homie: Primary class instance for Homie Automator.
    """

    bridges = homie.phue_bridges

    for bridge in bridges.values():

        output = bridge.fetched

        dumped = dumps(
            output,
            default=str,
            indent=2)

        print_homie(
            homie, 'Philips Hue Bridge',
            bridge.name, dumped)



def print_ubiq_routers(
    homie: Homie,
) -> None:
    """
    Print the contents for the object within Homie instance.

    :param homie: Primary class instance for Homie Automator.
    """

    routers = homie.ubiq_routers

    for router in routers.values():

        output = (
            router.params
            .model_dump())

        if 'password' in output:
            length = len(output['password'])
            output['password'] = '*' * length

        dumped = dumps(
            output,
            default=str,
            indent=2)

        print_homie(
            homie, 'Ubiquiti Router',
            router.name, dumped)



def print_ubiq_dumped(
    homie: Homie,
) -> None:
    """
    Print the contents for the object within Homie instance.

    :param homie: Primary class instance for Homie Automator.
    """

    routers = homie.ubiq_routers

    for router in routers.values():

        output = router.fetched

        dumped = dumps(
            output,
            default=str,
            indent=2)

        print_homie(
            homie, 'Ubiquiti Router',
            router.name, dumped)



def launcher_main() -> None:
    """
    Perform whatever operations are associated with the file.
    """

    args = vars(launcher_args())

    config = Config(args['config'])
    homie = Homie(config)

    scope = args['scope']


    if scope == 'groups':
        print_groups(homie)

    elif scope == 'scenes':
        print_scenes(homie)


    elif scope == 'phue_bridges':
        print_phue_bridges(homie)

    elif scope == 'phue_dumped':
        print_phue_dumped(homie)


    elif scope == 'ubiq_routers':
        print_ubiq_routers(homie)

    elif scope == 'ubiq_dumped':
        print_ubiq_dumped(homie)



if __name__ == '__main__':
    launcher_main()
