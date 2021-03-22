import logging

from wafer_fault_detection.utils import config
from wafer_fault_detection.utils import logging_config


VERSION_PATH = config.PACKAGE_ROOT / 'VERSION'

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_config.get_console_handler())
logger.propagate = False


with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()