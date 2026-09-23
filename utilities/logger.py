'''logger.py'''
import logging
import sys


def setup_logging():
    '''
    Configures logging once for the whole app. Logs go to the console
    with a timestamp, log level, module name, and message.
    '''
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )