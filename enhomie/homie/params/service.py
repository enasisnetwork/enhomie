"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated

from encommon.config import ParamsModel

from pydantic import Field



class HomieServiceTimeoutParams(ParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    action: Annotated[
        int,
        Field(5,
              description='Override the actions timeout',
              ge=1, le=30)]

    update: Annotated[
        int,
        Field(3,
              description='Override the updates timeout',
              ge=1, le=30)]

    stream: Annotated[
        int,
        Field(60,
              description='Override the stream timeout',
              ge=1, le=900)]



class HomieServiceRespiteParams(ParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    desire: Annotated[
        int,
        Field(60,
              description='How often desires performed',
              ge=1, le=900)]

    update: Annotated[
        int,
        Field(60,
              description='How often updates performed',
              ge=1, le=900)]

    health: Annotated[
        int,
        Field(3,
              description='How often health is checked',
              ge=1, le=15)]



class HomieServiceParams(ParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    respite: Annotated[
        HomieServiceRespiteParams,
        Field(default_factory=HomieServiceRespiteParams,
              description='When operates are performed')]

    timeout: Annotated[
        HomieServiceTimeoutParams,
        Field(default_factory=HomieServiceTimeoutParams,
              description='Override source or defaults')]
