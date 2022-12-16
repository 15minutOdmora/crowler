import argparse
from IPython import embed

from crowler.driver import AvailableBrowserDrivers

parser = argparse.ArgumentParser(
    prog = 'Crowler',
    description = 'A Selenium based web crowling',
    prefix_chars='-+'
)

parser.add_argument("-b", "--browser", default="chrome")

args = parser.parse_args()

browser_name = args.browser

if browser_name not in AvailableBrowserDrivers:
    print(f"Could not find the browser {args.browser}, running Chrome.")
    browser_name = "chrome"

driver = AvailableBrowserDrivers[browser_name]()

embed()
