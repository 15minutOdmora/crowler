"""
Module containing _BaseDriver used as parent in other drivers for extending functionality.
"""

from __future__ import annotations
from typing import Callable

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


class _BaseDriver:
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
