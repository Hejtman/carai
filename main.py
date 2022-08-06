import sys
from pathlib import Path

from carai import CarAI
from cli import Terminal


def main() -> int:
    t = Terminal(log_path=f'{Path.home()}/{Path.cwd().stem}/{Path.cwd().stem}.log')
    all(t.execute_args())

    c = CarAI()
    c.main_loop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
