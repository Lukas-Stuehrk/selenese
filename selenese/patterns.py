import re
from fnmatch import fnmatch


class Pattern(object):
    def __init__(self, pattern_string):
        self.pattern_string = pattern_string


class ExactPattern(Pattern):
    def compare(self, string):
        return self.pattern_string == string


class RegexPattern(Pattern):
    def compare(self, string):
        if not hasattr(self, '_regex'):
            self._regex = re.compile(self.pattern_string)
        return self._regex.sub('', string) == ''


class RegexIgnorecasePattern(Pattern):
    def compare(self, string):
        if not hasattr(self, '_regex'):
            self._regex = re.compile(self.pattern_string, flags=re.IGNORECASE)
        return self._regex.sub('', string) == ''


class GlobPattern(Pattern):
    def compare(self, string):
        return fnmatch(string, self.pattern_string)


def create_pattern(pattern_string):
    if pattern_string.startswith('exact:'):
        return ExactPattern(pattern_string[6:])
    elif pattern_string.startswith('glob:'):
        return GlobPattern(pattern_string[5:])
    elif pattern_string.startswith('regexp:'):
        return RegexPattern(pattern_string[7:])
    elif pattern_string.startswith('regexpi:'):
        return RegexIgnorecasePattern(pattern_string[8:])
    # if no pattern scheme is given, asssume that it is a 'glob' pattern
    return GlobPattern(pattern_string)