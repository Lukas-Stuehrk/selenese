from selenese import patterns
import unittest


class TestPatterns(unittest.TestCase):
    def test_exact_pattern(self):
        pattern = patterns.ExactPattern('Foobar')
        self.assertTrue(pattern.compare('Foobar'))
        self.assertFalse(pattern.compare('raboof'))

    def test_regex_pattern(self):
        pattern = patterns.RegexPattern('[a-z]')
        self.assertTrue(pattern.compare('peter'))
        self.assertFalse(pattern.compare('Peter'))
        self.assertFalse(pattern.compare('F00bar'))

    def test_regex_ignorecase_pattern(self):
        pattern = patterns.RegexIgnorecasePattern('[A-Z]')
        self.assertTrue(pattern.compare('peter'))
        self.assertTrue(pattern.compare('Peter'))
        self.assertFalse(pattern.compare('F00bar'))

    def test_glob_pattern(self):
        pattern = patterns.GlobPattern('*Foobar*')
        self.assertTrue(pattern.compare('1234Foobar'))
        self.assertTrue(pattern.compare('1234Foobar1234'))
        self.assertFalse(pattern.compare('1234foobar'))


class TestCreatePattern(unittest.TestCase):
    def test_create_exact_pattern(self):
        pattern = patterns.create_pattern('exact:Foobar')
        self.assertTrue(isinstance(pattern, patterns.ExactPattern))
        self.assertEqual(pattern.pattern_string, 'Foobar')

    def test_create_regex_pattern(self):
        pattern = patterns.create_pattern('regexp:[a-z]')
        self.assertTrue(isinstance(pattern, patterns.RegexPattern))
        self.assertEqual(pattern.pattern_string, '[a-z]')

    def test_create_regex_ignorecase_pattern(self):
        pattern = patterns.create_pattern('regexpi:[A-Z]')
        self.assertTrue(isinstance(pattern, patterns.RegexIgnorecasePattern))
        self.assertEqual(pattern.pattern_string, '[A-Z]')

    def test_create_glob_prattern(self):
        pattern = patterns.create_pattern('glob:Foobar')
        self.assertTrue(isinstance(pattern, patterns.GlobPattern))
        self.assertEqual(pattern.pattern_string, 'Foobar')


    def test_create_prattern(self):
        pattern = patterns.create_pattern('Foobar')
        self.assertTrue(isinstance(pattern, patterns.GlobPattern))
        self.assertEqual(pattern.pattern_string, 'Foobar')
