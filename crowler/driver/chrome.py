"""
Chrome driver module.
"""

from __future__ import annotations

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from crowler.driver._base import _BaseDriver


class ChromeDriver(_BaseDriver, Chrome):
    """
    Class for creating a Chrome based driver object. This class inherits from the parent class selenium.webdriver.Chrome.
    Extends parent by setting window size, window position, implicit wait and if it should run headless or not and contains
    additional methods found in _BaseDriver.
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
