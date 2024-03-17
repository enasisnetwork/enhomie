"""
Functions and routines associated with Enasis Network Home Automator.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon import ENPYRWS
from encommon.utils import load_sample
from encommon.utils import prep_sample

from . import SAMPLES
from ... import PROJECT

if TYPE_CHECKING:
    from ..config import Config



def test_Config(
    tmp_path: Path,
    config: 'Config',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param config: Primary class instance for configuration.
    """

    _config1 = config.config
    _config2 = config.config

    assert _config1 is not _config2

    sample = load_sample(
        path=SAMPLES.joinpath('config.json'),
        update=ENPYRWS,
        content=_config1,
        replace={
            'project': str(PROJECT),
            'tmp_path': str(tmp_path)})

    expect = prep_sample(
        content=_config2,
        replace={
            'project': str(PROJECT),
            'tmp_path': str(tmp_path)})

    assert sample == expect
