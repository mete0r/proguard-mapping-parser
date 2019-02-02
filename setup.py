# -*- coding: utf-8 -*-
#
#   proguard-mapping-parser: ProGuard's mapping.txt parser
#   Copyright (C) 2015-2019 mete0r <mete0r@sarangbang.or.kr>
#
#   This file is part of proguard-mapping-parser.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import with_statement
from contextlib import contextmanager
from distutils.command.build import build as _build
import io
import os.path
import re


def setup_dir(f):
    ''' Decorate f to run inside the directory where setup.py resides.
    '''
    setup_dir = os.path.dirname(os.path.abspath(__file__))

    def wrapped(*args, **kwargs):
        with chdir(setup_dir):
            return f(*args, **kwargs)

    return wrapped


@contextmanager
def chdir(new_dir):
    old_dir = os.path.abspath(os.curdir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


@setup_dir
def import_setuptools():
    try:
        import setuptools
        return setuptools
    except ImportError:
        pass

    import ez_setup
    ez_setup.use_setuptools()
    import setuptools
    return setuptools


@setup_dir
def readfile(path):
    with io.open(path, encoding='utf-8') as f:
        return f.read()


@setup_dir
def get_version():
    source = readfile('src/proguard_mapping_parser/__init__.py')
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              source, re.M)
    if not version_match:
        raise RuntimeError('Unable to find version string.')
    return version_match.group(1)


def alltests():
    import sys
    import unittest
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    args = sys.argv[:]
    defaults = ['--test-path', here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)


setup_requires = readfile('requirements/setup.in')

install_requires_filename = 'requirements.in'
install_requires = readfile(install_requires_filename)

tests_require = readfile('requirements/test.in')


setup_info = {
    'name': 'proguard-mapping-parser',
    'version': get_version(),
    'description': 'ProGuard\'s mapping.txt parser',
    'long_description': '\n'.join([readfile('README.rst'),
                                   readfile('CHANGES.rst')]),

    'author': 'mete0r',
    'author_email': 'mete0r@sarangbang.or.kr',
    'license': 'GNU Lesser General Public License v3 or later (LGPLv3+)',
    # 'url': 'https://github.com/mete0r/proguard-mapping-parser',

    'packages': [
        'proguard_mapping_parser',
        'proguard_mapping_parser.recipe',
    ],
    # do not use '.'; just omit to specify setup.py directory
    'package_dir': {
        '': 'src',
    },
    'package_data': {
        'proguard_mapping_parser': [
            'locale/*/*/*.mo',
        ],
        # 'proguard_mapping_parser.tests': [
        #   'files/*',
        # ],
    },
    'install_requires': install_requires,
    'test_suite': '__main__.alltests',
    'tests_require': tests_require,
    'extras_require': {
        'test': tests_require,
    },
    'setup_requires': setup_requires,
    'message_extractors': {
        'src/proguard_mapping_parser': [
            ('**.py', 'python', None),
        ]
    },
    'entry_points': {
        'console_scripts': [
            'proguard-mapping-parser = proguard_mapping_parser.cli:main',
        ],
        'zc.buildout': [
            'default = proguard_mapping_parser.recipe:Recipe',
        ],
        'zc.buildout.uninstall': [
            'default = proguard_mapping_parser.recipe:uninstall',
        ],
        'paste.app_factory': [
            'main = proguard_mapping_parser.wsgi:app_factory',
        ],
    },
    'classifiers': [
        'Development Status :: 1 - Planning',
        # 'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',  # noqa
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: Implementation :: CPython',
    ],
    'keywords': [
    ],
    'zip_safe': False,
}


class build(_build):
    def run(self):
        self.run_command('compile_catalog')
        _build.run(self)


project_root_directory = os.path.abspath(os.path.dirname(__file__))
requirements_path = 'requirements.txt'


@setup_dir
def main():
    setuptools = import_setuptools()
    setup_info['cmdclass'] = {
        'build': build,
    }
    setuptools.setup(**setup_info)


if __name__ == '__main__':
    main()
