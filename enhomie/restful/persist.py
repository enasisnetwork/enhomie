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
from ..homie.addons.persist import HomiePersistValue



APIROUTER = APIRouter(
    tags=['Persistent Values'])



class HomiePersistEntry(BaseModel, extra='forbid'):
    """
    Contain the information regarding the persistent value.
    """

    unique: Annotated[
        str,
        Field(...,
              description='Unique key for the value',
              min_length=1)]

    label: Annotated[
        Optional[str],
        Field(None,
              description='Friendly label for the value',
              min_length=1)]

    value: Annotated[
        HomiePersistValue,
        Field(...,
              description='Value stored at the key')]

    unit: Annotated[
        Optional[str],
        Field(None,
              description='Friendly unit for the value',
              min_length=1)]

    icon: Annotated[
        Optional[str],
        Field(None,
              description='Friendly icon for the value',
              min_length=1)]

    about: Annotated[
        Optional[str],
        Field(None,
              description='Friendly about for the value',
              min_length=1)]

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

    return HomiePersistEntries(
        entries=entries,
        elapsed=runtime.since)
