"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from pathlib import Path
from typing import Any

from encommon.times import Times

from pytest import fixture

from requests_mock import Mocker

from .config import Config
from .homie import Homie
from .homie.test import SAMPLES as CORE_SAMPLES
from .philipshue.test import SAMPLES as PHUE_SAMPLES
from .ubiquiti.test import SAMPLES as UBIQ_SAMPLES



ZULUSTAMP = '%Y-%m-%dT%H:%M:%S%Z'

REPLACES = {

    '__TIMESTAMP__': (
        (Times('-1h')
         .stamp(ZULUSTAMP))),

    '__FSEEN_CUR__': (
        str(int(Times('-9d')))),
    '__LSEEN_CUR__': (
        str(int(Times('-1d')))),
    '__FSEEN_OLD__': (
        str(int(Times('-9d')))),
    '__LSEEN_OLD__': (
        str(int(Times('-1d')))),
    '__ASSOC_TIME__': (
        str(int(Times('-2d')))),
    '__DISCO_CUR__': (
        str(int(Times('-3h')))),
    '__DISCO_OLD__': (
        str(int(Times('-1d'))))}



def config_factory(
    tmp_path: Path,
) -> Config:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    Path.mkdir(
        tmp_path.joinpath('config'),
        exist_ok=True)

    (tmp_path
        .joinpath('config.yml')
        .write_text(
            'enconfig:\n'
            '  paths:\n'
            f'    - {tmp_path}\n'
            f'    - {CORE_SAMPLES}\n'
            f'    - {PHUE_SAMPLES}\n'
            f'    - {UBIQ_SAMPLES}\n'
            'enlogger:\n'
            '  stdo_level: info'))

    return Config(
        f'{tmp_path}/config.yml')



@fixture
def config(
    tmp_path: Path,
) -> Config:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    return config_factory(tmp_path)



def homie_factory(  # noqa: CFQ001
    config: 'Config',
) -> Homie:
    """
    Construct the instance for use in the downstream tests.

    .. note::
       Function has slowly evolved and grown over time, but
       should be refactored and simplified in the future.

    :param config: Primary class instance for configuration.
    :returns: Newly constructed instance of related class.
    """

    homie = Homie(config=config)

    bridges = homie.phue_bridges
    routers = homie.ubiq_routers


    phue_paths = [
        ('https://192.168.1.10'
         '/clip/v2/resource'),
        ('https://192.168.2.10'
         '/clip/v2/resource')]

    phue_files = [
        PHUE_SAMPLES.joinpath('jupiter.json'),
        PHUE_SAMPLES.joinpath('neptune.json')]


    ubiq_paths = [

        ('https://192.168.1.1'
         '/api/auth/login'),
        ('https://192.168.1.1'
         '/proxy/network'
         '/api/s/default/rest/user'),
        ('https://192.168.1.1'
         '/proxy/network'
         '/api/s/default/stat/sta'),

        ('https://192.168.2.1'
         '/api/auth/login'),
        ('https://192.168.2.1'
         '/proxy/network'
         '/api/s/default/rest/user'),
        ('https://192.168.2.1'
         '/proxy/network'
         '/api/s/default/stat/sta')]

    ubiq_files = [

        UBIQ_SAMPLES.joinpath(
            'jupiter/historic.json'),
        UBIQ_SAMPLES.joinpath(
            'jupiter/realtime.json'),

        UBIQ_SAMPLES.joinpath(
            'neptune/historic.json'),
        UBIQ_SAMPLES.joinpath(
            'neptune/realtime.json')]


    def _replaces(
        path: Path,
    ) -> dict[str, Any]:

        content = path.read_text()

        for key, new in REPLACES.items():
            content = (
                content
                .replace(key, new))

        loaded = loads(content)

        assert isinstance(loaded, dict)

        return loaded


    with Mocker() as mocker:


        dumped = _replaces(phue_files[0])

        mocker.get(
            url=phue_paths[0],
            json=dumped)


        dumped = _replaces(phue_files[1])

        mocker.get(
            url=phue_paths[1],
            json=dumped)


        for bridge in bridges.values():
            assert bridge.fetched


        mocker.post(ubiq_paths[0])


        dumped = _replaces(ubiq_files[0])

        mocker.register_uri(
            method='get',
            url=ubiq_paths[1],
            response_list=[
                {'json': dumped,
                 'status_code': 401},
                {'json': dumped}])


        dumped = _replaces(ubiq_files[1])

        mocker.get(
            url=ubiq_paths[2],
            json=dumped)


        mocker.post(ubiq_paths[3])


        dumped = _replaces(ubiq_files[2])

        mocker.register_uri(
            method='get',
            url=ubiq_paths[4],
            response_list=[
                {'json': dumped,
                 'status_code': 401},
                {'json': dumped}])


        dumped = _replaces(ubiq_files[3])

        mocker.get(
            url=ubiq_paths[5],
            json=dumped)


        for router in routers.values():
            assert router.fetched


    return homie



@fixture
def homie(
    tmp_path: Path,
    config: 'Config',
) -> Homie:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :param config: Primary class instance for configuration.
    :returns: Newly constructed instance of related class.
    """

    return homie_factory(config)
