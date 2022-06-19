# Dester

Debugging & testing library that extends the functionality of Selenium with added shell debbugging.

### Install

Currently not yet on pip, so install by cloning this repo:

`pip install -e path/to/local/Dester`

Use `-e` to install via. path, library will get updated when the local repository gets updated.

### Basic usage example

Create driver instance and run a debbugging session:

```python
from dester.driver import ChromeDriver
from dester import dagger

driver = ChromeDriver()

dagger.debug()
```

Once shell is active all variables before running debug() will be available, for example running:

`>>> driver.get("www.google.com")`

Will open that address live.

`ChromeDriver` class extends the basic functionality of drivers in Selenium but it simplifies and adds some other usefull actions. 

### Configuration

Dester uses the [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager) library for installing drivers over their official Github sites, a GH token should be configured for excessive driver installing.

#### GH_TOKEN

**webdriver_manager** downloading some webdrivers from their official GitHub repositories but GitHub has [limitations](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) like 60 requests per hour for unauthenticated users.
In case not to face an error related to github credentials, you need to [create](https://help.github.com/articles/creating-an-access-token-for-command-line-use) github token and place it into your environment: (\*)

Example:

```bash
export GH_TOKEN = "asdasdasdasd"
```

(\*) access_token required to work with GitHub API [more info](https://help.github.com/articles/creating-an-access-token-for-command-line-use/).

There is also possibility to set same variable via ENV VARIABLES, example:

```python
import os

os.environ['GH_TOKEN'] = "asdasdasdasd"
```
