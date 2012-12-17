from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tempfile import NamedTemporaryFile
from selenese.locators import create_locator
from selenese.patterns import create_pattern
from time import sleep


class Executor(object):
    """
    Executes selenese commands on a selenium WebDriver
    """
    timeout = 30

    def __init__(self, testcase, webdriver):
        self.testcase = testcase
        self.webdriver = webdriver
        self._storage = {}
        self._directory = {}

    def _create_file(self, filename):
        """
        :return: a file-like object
        """
        # replace all variables
        for key in self._storage:
            filename = filename.replace('${%s}' % key, self._storage[key])
        # create the file like object
        file_pointer = NamedTemporaryFile()
        self._directory[filename] = file_pointer
        return file_pointer

    def _andWait(self):
        for i in range(self.timeout):
            sleep(1)
            ready_state = self.webdriver.execute_script('return document.readyState')
            if ready_state == 'complete':
                return True
            i # XXX
        return False

    # Commands
    def addSelection(self, target, value):
        pass

    def altKeyDown(self, target, value):
        pass

    def altKeyUp(self, target, value):
        pass

    def captureEntirePageScreenshot(self, target, value):
        self.webdriver.get_screenshot_as_file(self._create_file(target).name)
        return True

    def check(self, target, value):
        element = create_locator(target).get_element(self.webdriver)
        if element.get_attribute('type') == 'checkbox' and not element.get_attribute('checked'):
            element.click()

    def click(self, target, value):
        create_locator(target).get_element(self.webdriver).click()

    def close(self, target, value):
        self.webdriver.close()

    def controlKeyDown(self, target, value):
        ActionChains(self.driver).key_down(Keys.CONTROL).perform()

    def controlKeyUp(self, target, value):
        ActionChains(self.driver).key_up(Keys.CONTROL).perform()

    def createCookie(self, target, value):
        name, value = target.split('=')
        data = {
            'name': name,
            'value': value,
        }
        for chunk in value.split(','):
            if chunk.startsWith('path='):
                data['path'] = chunk[5:]
            elif chunk.startsWith('max_age='):
                data['expiry'] = chunk[7:]
            elif chunk.startsWith('domain='):
                data['domain'] = chunk[7]
            elif chunk.startsWith('secure='):
                data['secure'] = bool(chunk[7:])
        self.webdriver.addCookie(data)

    def deleteAllVisibleCookies(self, target, value):
        self.webdriver.delete_all_cookies()

    def deleteCookie(self, target, value):
        self.webdriver.delete_cookie(target)

    def deselectPopUp(self, target, value):
        self.webdriver.switch_to_window()

    def doubleClick(self, target, value):
        pass

    def focus(self, target, value):
        locator = create_locator(target)
        element = locator.get_element(self.webdriver)
        if element.get_attribute('id'):
            self.webdriver.execute_script('document.getElementById("%s").focus();' %
                                          element.get_attribute('id'))
        # TODO

    def goBack(self, target, value):
        self.webdriver.back()

    def open(self, target, value):
        if not target.startswith('http://') and not target.startswith('https://'):
            if self.testcase.baseurl.endswith('/') and target.startswith('/'):
                url = self.testcase.baseurl + target[1:]
            else:
                url = self.testcase.baseurl + target
        else:
            url = target
        self.webdriver.get(url)

    def refresh(self, target, value):
        self.webdriver.refresh()

    def removeScript(self, target, value):
        pass

    def runScript(self, target, value):
        pass

    def selectPopUp(self, target, value):
        # TODO
        self.webdriver.switch_to_window(target)

    def selectWindow(self, target, value):
        # TODO
        self.webdriver.switch_to_window(target)

    def submit(self, target, value):
        pass

    def type(self, target, value):
        pass

    def typeKeys(self, target, value):
        create_locator(target).get_element(self.webdriver).send_keys(value)

    def uncheck(self, target, value):
        element = create_locator(target).get_element(self.webdriver)
        if element.get_attribute('type') == 'checkbox' and not element.get_attribute('checked'):
            element.click()

    def windowMaximize(self, target, value):
        self.webdriver.maximize_window()

    # Accessors
    def _getAllButtons(self):
        # note: only submit buttons will be selected since the reference implementation (Selenium
        # IDE does not select button elements
        id_list = []
        for button in self.webdriver.find_elements_by_css_selector('input[type="submit"]'):
            id_list.append(button.get_attribute('id'))
        return ','.join(id_list)

    def _getAllFields(self):
        # get all input fields
        id_list = []
        for field in self.webdriver.find_elements_by_css_selector('input[type="text"]'):
            id_list.append(field.get_attribute('id'))
        return ','.join(id_list)

    def assertAlert(self, target, value):
        return create_pattern(target).compare(self.webdriver.switch_to_alert().text)

    def assertAlertNotPresent(self, target, value):
        try:
            self.webdriver.switch_to_alert().text
        except NoAlertPresentException:
            return True
        return False

    def assertAlertPresent(self, target, value):
        return self.assertAlertNotPresent(target, value) == False

    def assertAllButtons(self, target, value):
        return create_pattern(target).compare(self._getAllButtons())

    def assertAllFields(self, target, value):
        return create_pattern(target).compare(self._getAllFields())

    def assertAllLinks(self, target, value):
        pass

    def assertAllWindowIds(self, target, value):
        pass

    def assertAllWindowTitles(self, target, value):
        pass

    def assertAllWindowNames(self, target, value):
        pass

    def assertCookiePresent(self, target, value):
        return self.webdriver.get_cookie(target) != None

    def assertCookieNotPresent(self, target, value):
        return self.assertCookiePresent(target, value) == False

    def assertCssCount(self, target, value):
        elements = self.webdriver.find_elements_by_css_selector(target)
        return create_pattern(value).compare(len(elements))

    def assertElementNotPresent(self, target, value):
        return self.assertElementPresent(target, value) == False

    def assertElementPresent(self, target, value):
        try:
            create_locator(target).get_element(self.webdriver)
            return True
        except NoSuchElementException:
            return False

    def assertLocation(self, target, value):
        return create_pattern(target).compare(self.webdriver.current_url)

    def assertNotCssCount(self, target, value):
        return self.assertCssCount(target, value) == False

    def assertText(self, target, value):
        locator = create_locator(target)
        pattern = create_pattern(value)
        return pattern.compare(locator.get_element(self.webdriver).text)

    def assertTextNotPresent(self, target, value):
        return self.assertTextPresent(target, value) == False

    def assertTextPresent(self, target, value):
        pattern = create_pattern(target)
        return pattern.compare(self.webdriver.find_element_by_tag_name('body').text)

    def assertTitle(self, target, value):
        pattern = create_pattern(target)
        return pattern.compare(self.webdriver.title)

    def storeAlert(self, target, value):
        self._storage[target] = self.webdriver.switch_to_alert().text

    def storeAlertPresent(self, target, value):
        pass

    def storeAllButtons(self, target, value):
        self._storage[target] = self._getAllButtons()

    def storeAllFields(self, target, value):
        self._storage[target] = self._getAllFields()

    def storeLocation(self, target, value):
        self._storage[target] = self.webdriver.current_url

    def storeBodyText(self, target, value):
        self._storage[target] = self.webdriver.find_element_by_tag_name('body').text
