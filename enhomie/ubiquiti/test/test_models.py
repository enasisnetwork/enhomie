"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..models import UbiqModels



def test_UbiqModels_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    models = UbiqModels

    assert models.origin()
    assert models.update()

    drivers = models.drivers()

    assert drivers.client()

    helpers = drivers.helpers()

    assert callable(
        helpers.latest())
