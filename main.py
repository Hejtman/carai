import sys
from carai import CarAI
from cli import Terminal


def main() -> int:
    t = Terminal()
    t.execute_args()

    c = CarAI()
    c.start()
    return 0


if __name__ == '__main__':
    sys.exit(main())
