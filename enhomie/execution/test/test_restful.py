"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..restful import arguments



def test_arguments() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    sargs = arguments([
        '--config', 'path'])

    assert sargs == {
        'config': 'path',
        'console': False,
        'debug': False}
