import sys
import time
from pathlib import Path

from controls.control import Control
from cli import Terminal
try:
    from robot_hat import Pin  # noqa
except ModuleNotFoundError:
    from fakes.servo import Pin


def reset_mcu():
    mcu_reset = Pin("MCURST")
    mcu_reset.off()
    time.sleep(0.001)
    mcu_reset.on()
    time.sleep(0.01)


def main() -> int:
    reset_mcu()
    t = Terminal(log_path=f'{Path.home()}/{Path.cwd().stem}/{Path.cwd().stem}.log')
    all(t.execute_args())

    control = Control()
    control.main_loop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
