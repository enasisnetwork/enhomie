"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from pathlib import Path
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import read_text
from encommon.utils import rvrt_sample
from encommon.utils import save_text

from respx import MockRouter

from ..scene import DriverPhueScene
from ...test import SAMPLES
from ....conftest import config_factory
from ....conftest import homie_factory

if TYPE_CHECKING:
    from ....homie import Homie
    from ....utils import TestBodies



def test_DriverPhueScene(
    homie: 'Homie',
    replaces: DictStrAny,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param replaces: Mapping of what to replace in samples.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    origins = childs.origins
    aspires = childs.aspires


    assert homie.refresh()


    planets = bodies.planets

    family = 'philips'

    for planet in planets:

        origin = origins[
            f'{planet}_{family}']

        aspire = aspires[
            f'{planet}_active']

        driver = (
            aspire.occurs[4]
            .drivers[0])

        assert isinstance(
            driver, DriverPhueScene)


        attrs = lattrs(driver)

        assert attrs == [
            '_HomieDriver__plugin',
            '_HomieDriver__params']


        assert inrepr(
            'scene.DriverPhueScene',
            driver)

        assert isinstance(
            hash(driver), int)

        assert instr(
            'scene.DriverPhueScene',
            driver)


        driver.validate()

        assert driver.plugin

        assert driver.family == family

        assert driver.kinds == ['occur']

        assert driver.params


        samples = SAMPLES / 'stream'

        source = read_text(
            f'{samples}/dumped'
            f'/{planet}.json')

        source = rvrt_sample(
            sample=source,
            replace=replaces)

        sample = loads(source)


        sitem = (
            origin.get_stream(
                sample[7]['event']))

        assert driver.occur(sitem)



def test_DriverPhueScene_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
    replaces: DictStrAny,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    :param replaces: Mapping of what to replace in samples.
    :param bodies: Locations and groups for use in testing.
    """

    samples = (
        tmp_path / 'homie')

    samples.mkdir()

    save_text(
        samples / 'test.yml',
        """
        groups:
         jupiter_nexist:
          origin: jupiter_philips
          label: Not exists
         jupiter_norigin:
          devices: jupiter_special
         neptune_nexist:
          origin: neptune_philips
          label: Not exists
         neptune_norigin:
          devices: neptune_special
        aspires:
         pytest:
          groups:
          - ganymede
          - halimede
          occurs:
          - philips_scene:
             scene: active
             group: jupiter_nexist
             states: active
          - philips_scene:
             scene: active
             group: jupiter_norigin
             states: active
          - philips_scene:
             scene: active
             group: neptune_nexist
             states: active
          - philips_scene:
             scene: active
             group: neptune_norigin
             states: active
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs
    origins = childs.origins

    origin = origins[
        'jupiter_philips']

    aspire = (
        childs.aspires
        ['pytest'])

    samples = SAMPLES / 'stream'


    assert homie.refresh()


    planets = bodies.planets

    loaded: list[DictStrAny] = []

    for planet in planets:

        source = read_text(
            f'{samples}/dumped'
            f'/{planet}.json')

        source = rvrt_sample(
            sample=source,
            replace=replaces)

        sample = loads(source)

        loaded.extend(sample)


    for event in loaded:

        sitem = (
            origin.get_stream(
                event['event']))

        occurs = aspire.occurs

        for occur in occurs:

            (occur.drivers[0]
             .occur(sitem))