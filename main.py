import sys
from pathlib import Path

from controls.control import Control
from cli import Terminal


def main() -> int:
    t = Terminal(log_path=f'{Path.home()}/{Path.cwd().stem}/{Path.cwd().stem}.log')
    all(t.execute_args())

    control = Control()
    control.main_loop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
