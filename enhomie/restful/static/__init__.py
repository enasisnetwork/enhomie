"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import FileResponse



APIROUTER = APIRouter(
    tags=['Static Content'])



@APIROUTER.get(
    '/static/{file}')
async def get_static(
    request: Request,
    file: str,
) -> FileResponse:
    """
    Handle the API request and return using response model.
    """

    static = (
        Path(__file__).parents[1]
        / f'static/{file}')

    if not static.exists():
        raise HTTPException(404)

    await asyncio.sleep(0)

    return FileResponse(str(static))
