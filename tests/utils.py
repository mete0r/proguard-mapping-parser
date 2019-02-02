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
from functools import wraps
import os.path
import shutil

from . import __name__ as testPackageName


def isolated_directory(test_fn):
    @wraps(test_fn)
    def wrapper(self):
        name = self.id()
        name = name[len(testPackageName)+1:]
        path = os.environ.get('TMPDIR', '/tmp')
        path = os.path.join(path, name)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        return test_fn(self, isolated_directory=path)
    return wrapper
