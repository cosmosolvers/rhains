""""""
import inspect
from typing import Callable


def validate_function_default(func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) == 0


def validate_function_ckeck(func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) == 1


def validate_function(func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) >= 0


def validate_function_two_args(func: Callable) -> bool:
    signature = inspect.signature(func)
    return len(signature.parameters) == 2
