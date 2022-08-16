import time
from typing import Any


def wait_for_callable(f: callable, expected_value: Any, timeout: float, period: float) -> bool:
    """
        Usually a lambda expression or getter method used to wait for an external event, such is variable change in different thread. This can not be passed as immutable variable like expected_value.
        e.g.: wait_for_callable(lambda: var, expected_value=False, timeout=1, period=0.1)
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        if f() == expected_value:
            return True
        time.sleep(period)
    return False


def who(obj: any) -> str:
    """ Convenience for e.g.: logging. """
    return f'{obj.__class__.__name__} {hex(id(obj))}'


def time2next(period: float, start_time: float):
    """ Seconds until next period should be started. Always positive. """
    return max(period - (time.time() - start_time), 0)
