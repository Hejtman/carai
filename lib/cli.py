import logging
import sys
import time
from pathlib import Path
from typing import Callable, Generator


class TerminalLogger:
    def __init__(self, file_path: str) -> None:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.file_handler = logging.FileHandler(file_path)
        self.terminal_handler = logging.StreamHandler(sys.stdout)

        self.file_handler.setLevel(logging.INFO)
        self.terminal_handler.setLevel(logging.INFO)    # default settings

        root_logger = logging.getLogger()               # should be done only once
        root_logger.setLevel(logging.NOTSET)            # delegate all messages
        root_logger.addHandler(self.file_handler)
        root_logger.addHandler(self.terminal_handler)

    def __getattr__(self, attr: str) -> Callable:
        return getattr(self.logger, attr)

    def stop_logging_to_terminal(self) -> None:
        root_logger = logging.getLogger()
        root_logger.removeHandler(self.terminal_handler)

    def set_terminal_logging(self, verbosity: int) -> None:
        self.file_handler.setLevel(level=logging.DEBUG if verbosity >= 3 else logging.INFO)
        self.terminal_handler.setLevel(level=logging.DEBUG if verbosity >= 3 else logging.INFO)


class CLI:
    """
    Common stuff for CLI APPs.
     * Parsing arguments from terminal
     * Logging INFO level into terminal
     * Logging INFO level into log file (DEBUG with -v option)
    """
    def __init__(self, log_path) -> None:
        self.logger = TerminalLogger(file_path=log_path)
        self.args = None
        self.parser = None

    def execute_args(self) -> Generator:
        """Returns result generator. Arguments from command-line are parsed into commands and executed (in add_argument order above) by reading the results from this generator.
         You can either abort the execution after any result (with appropriate return code) or deplete the generator in order to execute all given arguments."""
        self.logger.debug(f'EXECUTING:{" ".join(sys.argv)} =========== {time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))} {100 * "="}')
        self.args = self.parser.parse_args()
        return (getattr(self, arg)() for arg, value in self.args.__dict__.items() if value)

    def verbose(self) -> None:
        if self.args.verbose:
            self.logger.file_handler.setLevel(level=logging.DEBUG)
