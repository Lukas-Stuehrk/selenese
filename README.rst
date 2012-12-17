========
selenese
========

Python-selenese is a small lib to execute selenese HTML files on a python selenium WebDriver::

    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenese import TestRunner


    testrunner = TestRunner.from_file('my_testcase.html')
    results = testrunner.run()


Why should I use python-selenese?
=================================

The main benefit for using selenese is the ability to use the Selenium-IDE_ and that test cases
are stored as HTML files and not as source code. So it is easy for non-developers to create test
cases and the test cases can be executed without security considerations.

The HTML selenese files can be executed on every selenium WebDriver, which means that the selenese
test cases can be executed on every browser and can be scheduled in parallel, both not possible with
the Selenium IDE.


Requirements
============

* selenium_
* lxml_


.. _selenium: http://pypi.python.org/pypi/selenium
.. _lxml: http://lxml.de
.. _Selenium-IDE: http://seleniumhq.org/projects/ide/