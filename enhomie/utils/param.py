"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import clsname

if TYPE_CHECKING:
    from ..homie.childs import HomieChild



_ERROR = Literal[
    'minimal',
    'invalid',
    'missing',
    'noexist']



class InvalidParam(Exception):
    """
    Exception for after invalid parameters are encountered.

    :param error: Simple code describing the invalid error.
    :param child: Child class instance for Homie Automate.
    :param param: Name of the parameter which is not valid.
    :param value: Value if any specified for the parameter.
    """

    error: _ERROR
    child: Optional['HomieChild'] = None
    param: Optional[str] = None
    value: Optional[Any] = None


    def __init__(
        self,
        error: _ERROR,
        *,
        child: Optional['HomieChild'] = None,
        param: Optional[str] = None,
        value: Optional[Any] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        message = (
            f'Error ({error})')


        if param is not None:
            message += (
                f' param ({param})')

        if value is not None:
            message += (
                f' value ({value})')


        if child is not None:

            name = (
                f'{clsname(child)}'
                f'/{child.name}')

            message += (
                f' child ({name})')


        self.error = error
        self.child = child
        self.param = param
        self.value = value

        super().__init__(message)
