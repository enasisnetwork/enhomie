"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.config import ParamsModel



class HomiePluginParams(ParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """
