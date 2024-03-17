"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.times import Times

from ..params import WhenTimePeriodParams



def test_WhenTimePeriodParams() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    anchor = Times('now')


    start = anchor.shift('-1h@s')
    stop = anchor.shift('+1h@s')

    when = WhenTimePeriodParams(
        start=start,
        stop=stop)

    assert when.start and when.stop

    assert when.start == start
    assert when.stop == stop


    start = anchor.shift('-1h@s')
    stop = anchor.shift('-2h@s')

    when = WhenTimePeriodParams(
        start=start,
        stop=stop)

    assert when.start and when.stop

    assert when.start == start
    assert when.stop >= start
