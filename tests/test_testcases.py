from selenese.testcases import TestCase
import unittest
import os


TEST_FILE = os.path.join(os.path.dirname(__file__), 'data', 'testcase.html')


class TestTestCases(unittest.TestCase):
    def setUp(self):
        # load the testcase
        with open(TEST_FILE) as file_pointer:
            self.testcase = TestCase(file_pointer)

    def test_title(self):
        self.assertEqual(self.testcase.name, 'The Test Case')

    def test_commands(self):
        command_list = list(self.testcase.__iter__())
        self.assertEqual(len(command_list), 1)
        self.assertEqual(command_list[0].command, 'open')
        self.assertEqual(command_list[0].target, '/')
        self.assertEqual(command_list[0].value, '')

    def test_baseurl(self):
        self.assertEqual(self.testcase.baseurl, 'http://www.google.de/')
