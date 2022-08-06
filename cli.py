import argparse

from lib.cli import CLI


class Terminal(CLI):
    def __init__(self, log_path):
        super().__init__(log_path)
        self.parser = argparse.ArgumentParser(description='TODO', formatter_class=argparse.RawTextHelpFormatter, epilog=f'''    
TODO
''')
        self.parser.add_argument('-v', '--verbose', help=f'sets file logger verbosity ({self.logger.file_handler.baseFilename} has always full output)', action='count', default=0)
