import argparse
from pathlib import Path

from lib.cli import CLI


class Terminal(CLI):
    def __init__(self):
        super().__init__(log_path=f'{Path.home()}/{Path.cwd().stem}/{Path(__file__).stem}.log')
        self.parser = argparse.ArgumentParser(description='xxx', formatter_class=argparse.RawTextHelpFormatter, epilog=f'''
All options can be combined (like independent commands) and are executed in order defined above.    

EXAMPLES:
''')
        self.parser.add_argument('-v', '--verbose', help=f'sets terminal verbosity ({self.logger.file_handler.baseFilename} has always full output)', action='count', default=0)
