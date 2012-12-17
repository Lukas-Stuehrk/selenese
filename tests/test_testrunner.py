from selenese.testcases import TestRunner
from selenium.webdriver.chrome.webdriver import WebDriver
from shutil import copyfileobj
import unittest
import os


TEST_FILE = os.path.join(os.path.dirname(__file__), 'data', 'commands.html')
SCREENSHOT_FILES = os.path.join(os.path.dirname(__file__), 'data', 'screenshots.html')
CHROMEDRIVER = os.path.join(os.path.dirname(__file__), 'chromedriver')


class TestTestRunner(unittest.TestCase):
    def test_create_from_file(self):
        with open(TEST_FILE) as file_pointer:
            TestRunner.from_file(file_pointer)

    def test_testrunner(self):
        """
        run the test with a chromium webdriver
        """
        with open(TEST_FILE) as file_pointer:
            testrunner = TestRunner.from_file(file_pointer)
        results = testrunner.run(WebDriver(CHROMEDRIVER))
        self.assertFalse(False in results.results)
        self.assertTrue(True in results.results)


class TestFiles(unittest.TestCase):
    def test_files(self):
        with open(SCREENSHOT_FILES) as file_pointer:
            testrunner = TestRunner.from_file(file_pointer)
        results = testrunner.run(WebDriver(CHROMEDRIVER))
        self.assertEqual(results.files.keys(), ['test.png'])
        with open('/tmp/test.png', 'w') as file_pointer:
            copyfileobj(results.files['test.png'], file_pointer)


class TestStorage(unittest.TestCase):
    pass
