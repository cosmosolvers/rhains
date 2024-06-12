""""""
import inspect
from typing import Callable


def validate_function_default(self, func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) == 0


def validate_function_ckeck(self, func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) == 1


def validate_function(self, func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) >= 0


def validate_function_two_args(self, func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) == 2
