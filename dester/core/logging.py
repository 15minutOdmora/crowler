import logging
import os

# Re-configure webdriver_manager logging
def _disable_webdriver_manager_logging():
    logging.getLogger('WDM').setLevel(logging.NOTSET)


def setup():
    """
    Sets up all logging functionality.
    """
    _disable_webdriver_manager_logging()
