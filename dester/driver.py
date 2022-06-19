"""
Module for extending webdriver classes for ease of use.
Every type of driver (Chrome, Firefox, ...) should inherit from BaseDriver as it holds all functional methods.
Driver binaries get auto-installed using webdriver_manager so there is minimal work with setting upd driver execution.
"""

from __future__ import annotations
from typing import Callable

from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service

from dester.core import logging
from dester import dagger


logging.setup()


class BaseDriver:
    """
    Base class for all drivers holding methods that slightly extend and simplify the functionality of the driver object.
    """
    def __wait_executor(
        self,
        implicit_wait_time: float,
        ignored_exceptions: tuple,
        waiting_function: Callable,
        selector: str,
        by: By = By.CSS_SELECTOR,
    ) -> WebElement:
        """
        Method executes the WebDriverWait function on self object, waiting the specified implicit time until the
        waiting_function call returns True. Method fetches element at the end, if element is fetched.

        Args:
            implicit_wait_time (float): Time to implicitly wait for waiting_function to return True
            ignored_exceptions (tuple): Tuple of Selenium Exceptions to ignore
            waiting_function (Callable): Callable function, most likely defined in the By package in Selenium.
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR.
            selector (str): Selector to fetch element

        Returns:
            WebElement: Fetched WebElement (if any)
        """
        element = WebDriverWait(
            self,
            implicit_wait_time,
            ignored_exceptions=ignored_exceptions
        ).until(waiting_function((by, selector)))

        return element

    def get_element(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        implicit_wait_time: float = 10,
        ignored_exceptions: tuple = ()
    ) -> WebElement:
        """
        Element tries to fetch the element given by the selector by waiting on its presence.

        Args:
            selector (str): CSS selector of element
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR
            implicit_wait_time (float, optional): Max wait time to wait for element (in seconds). Defaults to 10.
            ignored_exceptions: tuple of Selenium exceptions to ignore

        Returns:
            WebElement: Fetched element
        """
        element = self.__wait_executor(
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions,
            waiting_function=EC.element_to_be_clickable,
            by=by,
            selector=selector
        )
        return element

    def click_on_element(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        implicit_wait_time: float = 10,
        ignored_exceptions: tuple = ()
    ) -> WebElement:
        """
        Method clicks on element given by it's CSS selector. Method waits an implicit_wait_time amount of seconds for
        the element to be click-able in the DOM. It then safely clicks on the element.

        Args:
            selector (str): CSS selector of element to click on.
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR.
            implicit_wait_time (float, optional): Implicit wait before an error gets thrown. Defaults to 10.
            ignored_exceptions: tuple of Selenium exceptions to ignore. Defaults to ().

        Returns:
            WebElement: Clicked element
        """
        element = self.get_element(
            selector,
            by=by,
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions
        )
        element.click()
        return element

    def force_click_on_element(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        implicit_wait_time: float = 10,
        ignored_exceptions: tuple = ()
    ) -> WebElement:
        """
        Method executes JavaScript click on element given its CSS selector.

        Args:
            selector (str): CSS selector of element to click on.
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR.
            implicit_wait_time (float, optional): [description]. Defaults to 10
            ignored_exceptions: tuple of Selenium exceptions to ignore. Defaults to ().
        """
        element = self.get_element(
            selector,
            by=by,
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions
        )
        self.execute_script('arguments[0].click()', element)
        return element

    def wait_on_presence_of_element(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        implicit_wait_time: float = 10,
        ignored_exceptions: tuple = ()
    ) -> WebElement:
        """
        Method will wait until given element by CSS selector is present in the dom.

        Args:
            selector (str): CSS selector of element to click on.
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR.
            implicit_wait_time (float, optional): Implicit wait before an error gets thrown. Defaults to 10.
            ignored_exceptions: tuple of Selenium exceptions to ignore. Defaults to ().
        """
        element = self.__wait_executor(
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions,
            waiting_function=EC.presence_of_element_located,
            selector=selector,
            by=by,
        )
        return element

    def wait_on_visibility_of_element(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        implicit_wait_time: float = 10,
        ignored_exceptions: tuple = ()
    ) -> WebElement:
        """
        Method will wait until given element by CSS selector is visible on page.

        Args:
            selector: CSS selector of element to click on.
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR.
            implicit_wait_time (float, optional): Implicit wait before an error gets thrown. Defaults to 10.
            ignored_exceptions: tuple of Selenium exceptions to ignore. Defaults to ().
        """
        element = self.__wait_executor(
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions,
            waiting_function=EC.visibility_of_element_located,
            by=by,
            selector=selector
        )
        return element

    def extract_attribute_of_element(
        self,
        selector: str,
        attribute: str,
        by: By = By.CSS_SELECTOR,
        implicit_wait_time: float = 10,
        ignored_exceptions: tuple = ()
    ) -> str:
        """
        Method extracts the passed attribute of element given by CSS selector.
        Method waits until the element is visible in the dom.

        Args:
            selector: CSS selector of element to click on.
            attribute: Attribute to extract the value of.
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR.
            implicit_wait_time (float, optional): Implicit wait before an error gets thrown. Defaults to 10.
            ignored_exceptions: tuple of Selenium exceptions to ignore. Defaults to ().

        Returns:
            str: Found value of element attribute
        """
        element = self.wait_on_visibility_of_element(
            selector=selector,
            by=by,
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions
        )
        return element.get_attribute(attribute)

    def get_all_element_attributes(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        implicit_wait_time: float = 5,
        ignored_exceptions: tuple = ()
    ):
        """
        Method extracts all possible attributes the element currently holds.

        Args:
            selector (str): CSS selector of element to click on.
            by (By): Locator strategy. Defaults to By.CSS_SELECTOR.
            implicit_wait_time (float, optional): Implicit wait before an error gets thrown. Defaults to 10.
            ignored_exceptions: tuple of Selenium exceptions to ignore. Defaults to ().

        Returns:
            str: Found value of element attribute
        """
        element = self.wait_on_visibility_of_element(
            selector=selector,
            by=by,
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions
        )
        return element.get_property("attributes")


class ChromeDriver(BaseDriver, Chrome):
    """
    Class for creating a Chrome based driver object. This class inherits from the parent class selenium.webdriver.Chrome.
    Extends parent by setting window size, window position, implicit wait and if it should run headless or not and contains
    additional methods found in BaseDriver.
    """
    def __init__(
        self,
        *args,
        headless: bool = False,
        implicit_wait: int = 10,
        window_size: tuple = (1920, 1080),
        window_position: tuple = (0, 0),
        options: Options = None,
        **kwargs
    ) -> None:
        """
        Args:
            *args: Get passed to the selenium.webdriver.Chrome.__init__() method.
            headless: If execution using this object should be headless. Defaults to False.
            implicit_wait: Implicit wait time for waiting on elements in DOM. Defaults to 15.
            window_size: (width, height) tuple setting the size of the opened window. Defaults to (1280,1440).
            window_position: (x, y) tuple of pixel position pair where the upper left corner of the window should
                be positioned. Defaults to (0,0).
            options: Custom Chrome options object can be passed, if passed the window_size, position and headless
                mode have no effect. Defaults to None.
            **kwargs: Get passed to the selenium.webdriver.Chrome.__init__() method.
        """
        if options:
            self.options = options
        else:
            self.options = Options()
            self.window_size = window_size
            self.window_position = window_position
            self._headless = headless
            self.headless = headless

        # Remove Failed to read descriptor from node connection error   
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Initialize parent class and pass arguments
        super().__init__(service=Service(ChromeDriverManager().install()), *args, options=self.options, **kwargs)
        self.implicitly_wait(implicit_wait)

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, is_headless: bool):
        if is_headless:
            self.options.add_argument("headless")
            # Set window size to full (this might lag out headless mode otherwise)
            self.options.add_argument("--window-size=1920,1080")

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    def window_size(self, size: tuple):
        # Transform to correct string, and pass to options as argument
        size_string = f"--window-size={size[0]},{size[1]}"
        self.options.add_argument(size_string)
        self._window_size = size

    @property
    def window_position(self):
        return self._window_position

    @window_position.setter
    def window_position(self, position: tuple):
        # Transform to correct string, and pass to options as argument
        position_string = f"--window-position={position[0]},{position[1]}"
        self.options.add_argument(position_string)
        self._window_size = position


# This should get imported for checking currently available driver classes and initializing them.
AvailableBrowserDrivers = {
    "chrome": ChromeDriver
}
