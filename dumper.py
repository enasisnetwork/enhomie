"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from typing import Any
from typing import Optional

from encommon.utils import array_ansi
from encommon.utils import print_ansi

from enhomie.config import Config
from enhomie.homie import Homie
from enhomie.homie import HomieGroup



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
        choices=[
            'homie',
            'phue_fetched',
            'phue_merged',
            'phue_bridges',
            'phue_devices',
            'ubiq_fetched',
            'ubiq_merged',
            'ubiq_routers',
            'ubiq_clients',
            'groups',
            'scenes',
            'desires',
            'desired'],
        help=(
            'which kind of objects '
            'are dumped to console'))

    parser.add_argument(
        '--group',
        help=(
            'group name for when '
            'dumping the scenes'))

    return vars(parser.parse_args())



def printer(
    header: dict[str, Any],
    source: dict[str, Any],
) -> None:
    """
    Print the contents for the object within Homie instance.

    .. note::
       Currently redundant between dumper.py and service.py.

    :param header: Additional information for output header.
    :param source: Content which will be shown after header.
    """

    print_ansi(
        f'\n<c96>┍{"━" * 63}<c0>')

    items = header.items()

    for key, value in items:

        print_ansi(
            f'<c96>│ <c36;1>{key}'
            f'<c37>: <c0>{value}')

    print_ansi(
        f'<c96>├{"─" * 63}<c0>\n')

    print(array_ansi(
        source, indent=2))

    print_ansi(
        f'\n<c96>┕{"━" * 63}<c0>\n')



def print_homie(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    header = {'Homie': 'Root Instance'}

    source = homie.homie_dumper()

    printer(header, source)



def print_groups(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    groups = homie.groups

    for group in groups.values():

        header = {'Group': group.name}

        source = group.homie_dumper()

        printer(header, source)



def print_scenes(
    homie: Homie,
    group: Optional[HomieGroup] = None,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    :param group: Group from wherein the scene is located.
    """

    scenes = homie.scenes

    for scene in scenes.values():

        header = {'Scene': scene.name}

        source = scene.homie_dumper(group)

        printer(header, source)



def print_desires(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    desires = homie.desires

    for desire in desires.values():

        header = {'Desire': desire.name}

        source = desire.homie_dumper()

        printer(header, source)



def print_desired(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    groups = homie.groups

    items = homie.desired.items()

    for group_name, desire in items:

        group = groups[group_name]

        kind = group.type.capitalize()

        header = {kind: group.name}

        source = desire.homie_dumper()

        printer(header, source)



def print_phue_fetched(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    bridges = homie.phue_bridges

    for bridge in bridges.values():

        header = {'Bridge': bridge.name}

        source = bridge.fetched

        printer(header, source)



def print_phue_merged(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    bridges = homie.phue_bridges

    for bridge in bridges.values():

        header = {'Bridge': bridge.name}

        source = bridge.merged

        printer(header, source)



def print_phue_bridges(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    bridges = homie.phue_bridges

    for bridge in bridges.values():

        header = {'Bridge': bridge.name}

        source = bridge.homie_dumper()

        printer(header, source)



def print_phue_devices(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    devices = homie.phue_devices

    for device in devices.values():

        header = {'Device': device.name}

        source = device.homie_dumper()

        printer(header, source)



def print_ubiq_fetched(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    routers = homie.ubiq_routers

    for router in routers.values():

        header = {'Router': router.name}

        source = router.fetched

        printer(header, source)



def print_ubiq_merged(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    routers = homie.ubiq_routers

    for router in routers.values():

        header = {'Router': router.name}

        source = router.merged

        printer(header, source)



def print_ubiq_routers(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    routers = homie.ubiq_routers

    for router in routers.values():

        header = {'Router': router.name}

        source = router.homie_dumper()

        printer(header, source)



def print_ubiq_clients(
    homie: Homie,
) -> None:
    """
    Print the contents about the devices within Homie class.

    :param homie: Primary class instance for Homie Automate.
    """

    clients = homie.ubiq_clients

    for client in clients.values():

        header = {'Client': client.name}

        source = client.homie_dumper()

        printer(header, source)



def operate_main(
    homie: Homie,
) -> None:
    """
    Perform whatever operations are associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    config = homie.config


    _scope = config.sargs['scope']
    _group = config.sargs['group']

    group: Optional[HomieGroup] = (
        homie.groups[_group]
        if _group else None)


    if _scope == 'homie':
        print_homie(homie)

    if _scope == 'groups':
        print_groups(homie)

    if _scope == 'scenes':
        print_scenes(homie, group)

    if _scope == 'desires':
        print_desires(homie)

    if _scope == 'desired':
        print_desired(homie)


    if _scope == 'phue_fetched':
        print_phue_fetched(homie)

    if _scope == 'phue_merged':
        print_phue_merged(homie)

    if _scope == 'phue_bridges':
        print_phue_bridges(homie)

    if _scope == 'phue_devices':
        print_phue_devices(homie)


    if _scope == 'ubiq_fetched':
        print_ubiq_fetched(homie)

    if _scope == 'ubiq_merged':
        print_ubiq_merged(homie)

    if _scope == 'ubiq_routers':
        print_ubiq_routers(homie)

    if _scope == 'ubiq_clients':
        print_ubiq_clients(homie)



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
        item='dumper',
        status='merged')


    homie = Homie(config)


    operate_main(homie)


    config.logger.log_i(
        base='script',
        item='dumper',
        status='stopped')



if __name__ == '__main__':
    launcher_main()
