"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.types import BaseModel



class HomieParamsModel(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """
