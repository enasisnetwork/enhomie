"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

if TYPE_CHECKING:
    from ..service import HomieService



def test_HomieService(
    service: 'HomieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    """


    attrs = lattrs(service)

    assert attrs == [
        '_HomieService__homie',
        '_HomieService__actions',
        '_HomieService__updates',
        '_HomieService__streams',
        '_HomieService__timer',
        '_HomieService__vacate',
        '_HomieService__cancel',
        '_HomieService__started']


    assert inrepr(
        'service.HomieService',
        service)

    assert hash(service) > 0

    assert instr(
        'service.HomieService',
        service)


    assert service.homie

    assert service.params

    assert service.actions

    assert service.updates

    assert service.streams

    assert len(service.running) == 0

    assert len(service.zombies) == 12


    service.start()

    operate = service.operate

    thread = Thread(
        target=operate)

    thread.start()

    for _ in range(50):
        thread.join(0.1)

    assert service.running

    assert not service.zombies

    assert service.congest

    service.soft()

    while service.congest:
        thread.join(0.1)  # NOCVR

    while service.running:
        thread.join(0.1)  # NOCVR

    service.stop()

    thread.join()

    assert service.zombies

    assert not service.congest



def test_HomieService_dryrun(
    service: 'HomieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    """

    homie = service.homie
    params = homie.params

    params.dryrun = True


    service.start()

    operate = service.operate

    thread = Thread(
        target=operate)

    thread.start()

    for _ in range(50):
        thread.join(0.1)

    assert service.running

    assert not service.zombies

    assert service.congest

    service.soft()

    while service.congest:
        thread.join(0.1)  # NOCVR

    while service.running:
        thread.join(0.1)  # NOCVR

    service.stop()

    thread.join()

    assert service.zombies

    assert not service.congest


    block_sleep(1.1)

    service.operate_healths()



def test_HomieService_cover(
    service: 'HomieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    """

    service.stop()
    service.soft()
    service.start()
    service.start()
    service.soft()
    service.soft()
    service.stop()
    service.stop()
