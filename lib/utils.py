import time
from typing import Any


def wait_for_callable(f: callable, expected_value: Any, timeout: float, period: float) -> bool:
    """
        Usually an lambda expression or getter method used to wait for an external event, such is variable change in different thread. This can not be passed as immutable variable like expected_value.
        e.g.: wait_for_callable(lambda: var, expected_value=False, timeout=1, period=0.1)
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        if f() == expected_value:
            return True
        time.sleep(period)
    return False


def who(object: any) -> str:
    """ Convenience for e.g.: logging. """
    return f'{object.__class__.__name__} {hex(id(object))}'
