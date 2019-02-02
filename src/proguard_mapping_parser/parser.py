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
import logging

from parsec import joint
from parsec import optional
from parsec import regex
from parsec import string
from parsec import spaces
from parsec import sepBy
from parsec import sepBy1


logger = logging.getLogger(__name__)


optionalspaces = optional(spaces())
arrow = optionalspaces >> string('->') << optionalspaces

identifier = (
    regex('[a-zA-Z_$][a-zA-Z_$0-9]*') ^ string('<init>') ^ string('<clinit>')
)
className = sepBy1(identifier, string('$'))
packagedFullName = sepBy1(identifier, string('.'))
packagedClassName = packagedFullName.parsecmap(lambda l: '.'.join(l))
typeName = packagedClassName | regex('[a-z]+')
javatype = joint(typeName, optional(string('[]')))

methodName = identifier
methodArguments = sepBy(
    optionalspaces >> javatype << optionalspaces,
    string(',')
)
methodArguments = string('(') >> methodArguments << string(')')

linenumber = regex('[0-9]+').parsecmap(lambda s: int(s))
linenumbers = joint(
    linenumber << string(':'),
    linenumber << string(':'),
)

member = joint(
    optional(linenumbers),
    javatype << spaces(),
    identifier,
    optional(methodArguments),
)

memberMapping = string(' ' * 4) >> joint(
    member,
    arrow >> identifier,
)


classMappingHeader = joint(
    packagedClassName,
    arrow >> packagedClassName
) << string(':')


classMapping = joint(
    classMappingHeader << string('\n'),
    sepBy(memberMapping, string('\n')),
)


classMappings = sepBy(
    classMapping,
    optional(string('\n')),
)
