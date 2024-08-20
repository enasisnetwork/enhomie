"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.times import Times

from ...utils import UnexpectedCondition

if TYPE_CHECKING:
    from ..helpers import UbiqFetch



def ubiq_latest(
    source: 'UbiqFetch',
) -> Times:
    """
    Return the timestamp for client association with router.

    :param source: Content which will be shown after header.
    :returns: Timestamp for client association with router.
    """


    gwsecs = (
        source
        .get('_uptime_by_ugw'))

    apsecs = (
        source
        .get('_uptime_by_uap'))

    if (gwsecs is not None
            or apsecs is not None):
        return Times()


    laseen = (
        source
        .get('last_seen'))

    if laseen is not None:
        return Times(laseen[0])


    raise UnexpectedCondition
