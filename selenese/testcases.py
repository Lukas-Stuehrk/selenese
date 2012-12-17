from lxml import html
from selenese.commands import Executor
from shutil import copyfileobj
import os


class Failure(Exception):
    """Raised if a test fails during execution"""


class Command(object):
    def __init__(self, columns):
        self.columns = columns
        self._command = None
        self._target = None
        self._value = None

    @property
    def command(self):
        if not self._command:
            self._command = self.columns[0].text or ''
            self._command = self._command.strip()
        return self._command

    @property
    def target(self):
        if not self._target:
            self._target = self.columns[1].text or ''
            self._target = self._target.strip()
        return self._target

    @property
    def value(self):
        if not self._value:
            self._value = self.columns[2].text or ''
            self._value = self._value.strip()
        return self._value


class TestCase(object):
    def __init__(self, file_pointer):
        self.tree = html.parse(file_pointer).getroot()
        self._name = None

    def __iter__(self):
        for row in self.tree.xpath('//tr'):
            columns = row.xpath('td')
            if len(columns) == 3:
                yield Command(columns)

    @property
    def name(self):
        if not self._name:
            self._name = self.tree.xpath('//thead//td')[0].text.strip()
        return self._name

    @property
    def baseurl(self):
        if not hasattr(self, '_baseurl'):
            element = self.tree.xpath('//link[@rel="selenium.base"]')
            if len(element) > 0:
                self._baseurl = element[0].attrib['href']
            else:
                self._baseurl = None
        return self._baseurl


class TestRunner(object):
    def __init__(self, testcase):
        self.testcase = testcase

    def run(self, webdriver):
        """
        runs the tests of the TestCase with the given webdriver
        :param  webdriver: a selenium WebDriver
        :return: a TestResults object
        """
        executor = Executor(self.testcase, webdriver)
        results = TestResults(self.testcase, executor)
        for command in self.testcase:
            if command.command.endswith('AndWait'):
                command_name = command.command[:-7]
                wait = True
            else:
                command_name = command.command
                wait = False
            execute = getattr(executor, command_name)
            result = execute(command.target, command.value)
            results.append(result)
            if result == False:
                raise Failure([command.command, command.target, command.value, False])
            if wait:
                executor._andWait()
        return results

    @staticmethod
    def from_file(file_pointer):
        """
        create a new TestRunner for the given selenese HTML file
        :param file_pointer: a file like object with the selenese HTML file
        """
        return TestRunner(TestCase(file_pointer))


class TestResults(object):
    def __init__(self, testcase, executor):
        self.executor = executor
        self.testcase = testcase
        self.results = []

    def append(self, result):
        self.results.append(result)

    def __iter__(self):
        i = 0
        for command in self.testcase:
            yield [command.command, command.target, command.value, self.results[i]]
            i += 1

    def copy_files(self, target_dir):
        """copies all files of the test run into target_dir"""
        for file in self.files.keys():
            # please be sure about the security considerations when using this function, e.g. if a
            # file name starts with '/'
            with open(os.path.join(target_dir, file), 'w') as target_file:
                copyfileobj(self.files[file], target_file)

    @property
    def files(self):
        """
        A dictionary with all files created during the tests, e.g. with captureEntirePageScreenshot.
        The keys of the dictionary is the filename as defined in the command an the value is a
        file-like object.
        Please notice that the files are not created under the defined names in the file system but
        are temporary files that will be deleted if the TestResults object is garbage collected.
        """
        return self.executor._directory

    @property
    def storage(self):
        """a dictionary with all variables that have been declared with a 'store*' accessor"""
        return self.executor._storage
