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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from argparse import ArgumentParser
from pprint import pprint
import gettext
import logging
import os.path
import sys

# PYTHON_ARGCOMPLETE_OK
try:
    import argcomplete
except ImportError:
    argcomplete = None

from parsec import ParseError

from . import __version__
from .parser import classMappings

PY3 = sys.version_info.major == 3
logger = logging.getLogger(__name__)

locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
t = gettext.translation('proguard-mapping-parser', locale_dir, fallback=True)
if PY3:
    _ = t.gettext
else:
    _ = t.ugettext


def dump():
    gettext.gettext = t.gettext
    parser = dump_argparse()
    if argcomplete:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()
    configureLogging(args.verbose)
    logger.info('args: %s', args)

    text = sys.stdin.read()
    try:
        parsed = classMappings.parse(text)
    except ParseError as e:
        logger.error('expected: %r', e.expected)
        logger.error('text:     %r', e.text)
        logger.error('index:    %r', e.index)
        logger.error('%s', e.text)
        logger.error('%s^', ' ' * e.index)
    else:
        pprint(parsed)
        logger.info('mappings: %d', len(parsed))


def dump_argparse():
    parser = ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
        help=_('output version information and exit')
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        help=_('increase verbosity')
    )
    return parser


def configureLogging(verbosity):
    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    try:
        import coloredlogs
    except ImportError:
        logging.basicConfig(level=level)
    else:
        coloredlogs.install(level)
