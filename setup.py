#!/usr/bin/env python

from setuptools import setup


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='MAPClient',
     version='0.10.0',
     description='A framework for managing and sharing workflows.',
     author='MAP Client Developers',
     author_email='mapclient-devs@physiomeproject.org',
     url='https://launchpad.net/mapclient',
     packages=['core', 'mountpoints', 'settings', 'tools', 'tools.annotation', 'tools.pluginwizard', 'tools.pmr', 'tools.pmr.jsonclient', 'widgets'],
     package_dir={'': 'src'},
     py_modules=['mapclient'],
     entry_points={'console_scripts':['mapclient=mapclient:main']}
)
