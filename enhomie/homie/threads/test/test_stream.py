"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inlist
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..stream import HomieStreamItem

if TYPE_CHECKING:
    from ...service import HomieService
    from ....utils import TestBodies



def test_HomieStreamItem(
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    homie = service.homie
    childs = homie.childs
    origins = childs.origins

    model = HomieStreamItem


    planets = bodies.planets

    event = {'foo': 'bar'}

    for planet in planets:

        origin = origins[
            f'{planet}_philips']


        item = model(
            origin, event)


        attrs = lattrs(item)

        assert attrs == [
            'event',
            'origin',
            'time']


        assert item.origin == origin.name

        assert item.event == event



def test_HomieStream(
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    member = service.streams
    threads = member.threads


    planets = bodies.planets

    for planet in planets:

        thread = threads[
            f'{planet}_philips']


        attrs = lattrs(thread)

        # Family class inheritence

        assert inlist(
            '_HomieThread__member',
            attrs)

        assert inlist(
            '_HomieThread__origin',
            attrs)


        assert inrepr(
            'Stream(PhueStream',
            thread)

        assert hash(thread) > 0

        assert instr(
            'Stream(PhueStream',
            thread)


        assert thread.homie

        assert thread.member

        assert thread.origin

        assert thread.aqueue

        assert thread.uqueue

        assert thread.squeue
