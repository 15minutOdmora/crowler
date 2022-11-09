
from crowler.driver.chrome import ChromeDriver
from crowler.core import logging

# Setup logging at driver import time
logging.setup()

# This should get imported for checking currently available driver classes and initializing them.
AvailableBrowserDrivers = {
    "chrome": ChromeDriver
}
