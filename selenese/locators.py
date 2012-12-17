

class Locator(object):
    def __init__(self, locator_string):
        self.locator_string = locator_string


class IdentifierLocator(Locator):
    pass


class IdLocator(Locator):
    def get_element(self, webdriver):
        return webdriver.find_element_by_id(self.locator_string)


class NameLocator(Locator):
    def get_element(self, webdriver):
        return webdriver.find_element_by_name(self.locator_string)


class CssLocator(Locator):
    def get_element(self, webdriver):
        return webdriver.find_element_by_css_selector(self.locator_string)


class LinkLocator(Locator):
    def get_element(self, webdriver):
        return webdriver.find_element_by_link_text(self.locator_string)


class XpathLocator(Locator):
    def get_element(self, webdriver):
        return webdriver.find_element_by_xpath(self.locator_string)


def create_locator(locator_string):
    if locator_string.startswith('identifier='):
        return IdentifierLocator(locator_string[11:])
    elif locator_string.startswith('id='):
        return IdLocator(locator_string[3:])
    elif locator_string.startswith('name='):
        return NameLocator(locator_string[5:])
    elif locator_string.startswith('link='):
        return LinkLocator(locator_string[5:])
    elif locator_string.startswith('css='):
        return CssLocator(locator_string[4:])
    elif locator_string.startswith('xpath='):
        return XpathLocator(locator_string[6:])
    else:
        raise NotImplementedError()

