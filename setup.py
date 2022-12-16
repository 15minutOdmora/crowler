from setuptools import find_packages, setup


setup(
    name="crowler",
    packages=find_packages(include=['crowler']),
    version="0.0.1",
    description="A debugging Selenium exstension for running tests and or scripts on websites.",
    author="Liam Mislej",
    author_email="liammislej@gmail.com",
    license="MIT",
    python_requires=">3.6",
    install_requires=[
        "selenium>=4.7.2",
        "webdriver_manager>=3.8.5",
        "ipython>=8.7.0"
    ],
    setup_requires=["pytest-runner==6.0.0"],
    tests_require=["pytest==7.1.2"],
    test_suite="tests",
)
