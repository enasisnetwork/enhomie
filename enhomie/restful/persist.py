"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from dataclasses import asdict
from typing import Annotated
from typing import Optional

from encommon.times import Time

from fastapi import APIRouter
from fastapi import Request

from pydantic import BaseModel
from pydantic import Field

from ..homie.addons.persist import HomiePersistRecord
from ..homie.params.persist import _PARAM_ABOUT
from ..homie.params.persist import _PARAM_ABOUT_ICON
from ..homie.params.persist import _PARAM_ABOUT_LABEL
from ..homie.params.persist import _PARAM_LEVEL
from ..homie.params.persist import _PARAM_TAGS
from ..homie.params.persist import _PARAM_VALUE_ICON
from ..homie.params.persist import _PARAM_VALUE_LABEL
from ..homie.params.persist import _PARAM_VALUE_UNIT
from ..homie.params.store import _PARAM_UNIQUE
from ..homie.params.store import _PARAM_VALUE



APIROUTER = APIRouter(
    tags=['Persistent Values'])



class HomiePersistEntry(BaseModel, extra='forbid'):
    """
    Contain the information regarding the persistent value.
    """

    unique: _PARAM_UNIQUE

    value: _PARAM_VALUE

    value_unit: _PARAM_VALUE_UNIT

    value_label: _PARAM_VALUE_LABEL

    value_icon: _PARAM_VALUE_ICON

    about: _PARAM_ABOUT

    about_label: _PARAM_ABOUT_LABEL

    about_icon: _PARAM_ABOUT_ICON

    level: _PARAM_LEVEL

    tags: _PARAM_TAGS

    expire: Annotated[
        Optional[str],
        Field(None,
              description='After when the key expires',
              min_length=20)]

    update: Annotated[
        str,
        Field(...,
              description='When the value was updated',
              min_length=20)]


    def __init__(
        self,
        record: 'HomiePersistRecord',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        source = asdict(record)

        if source.get('expire'):
            source['expire'] = (
                source['expire'].simple)

        source['update'] = (
            source['update'].simple)

        super().__init__(**source)



class HomiePersistEntries(BaseModel, extra='forbid'):
    """
    Contain the information regarding the persistent values.
    """

    entries: list[HomiePersistEntry]
    elapsed: float



@APIROUTER.get(
    '/api/persists',
    response_model=HomiePersistEntries)
async def get_persists(
    request: Request,
) -> HomiePersistEntries:
    """
    Handle the API request and return using response model.
    """

    runtime = Time('now')

    homie = request.app.homie
    persist = homie.persist

    await asyncio.sleep(0)

    entries = [
        HomiePersistEntry(x)
        for x in
        persist.records()]

    entries = sorted(
        entries,
        key=lambda x: x.unique)

    return HomiePersistEntries(
        entries=entries,
        elapsed=runtime.since)
