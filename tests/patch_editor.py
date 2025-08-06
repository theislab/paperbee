import sys

# This is a hack to patch the editor module at runtime to avoid the
# ModuleNotFoundError: No module named 'distutils'
# This is necessary because the version of `editor` used by `inquirer`
# is not compatible with Python 3.12.
if sys.version_info >= (3, 12):
    sys.modules["distutils"] = type("distutils", (), {})
    sys.modules["distutils.spawn"] = type("distutils.spawn", (), {"find_executable": lambda x: None})
