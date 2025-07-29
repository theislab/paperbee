import sys
from unittest.mock import patch

# This file patches the `editor` module at runtime to resolve a `distutils`
# dependency issue that causes tests to fail on Python 3.12. The `distutils`
# module has been deprecated and is no longer included in Python 3.12, but the
# `editor` package, which is a dependency of `inquirer`, still uses it. This
# patch works around the issue by creating a mock `distutils` module that
# allows the tests to run without error.
if sys.version_info >= (3, 12):
    sys.modules['distutils'] = type('distutils', (), {})
    sys.modules['distutils.spawn'] = type('distutils.spawn', (), {'find_executable': lambda x: None})
