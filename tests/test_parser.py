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
from unittest import TestCase


class ParseTestCase(TestCase):

    def test_javatype(self):
        from proguard_mapping_parser.parser import javatype
        self.assertEquals(
            ('android.arch.core.internal.SafeIterableMap$Entry', None),
            javatype.parse(
                'android.arch.core.internal.SafeIterableMap$Entry'
            ),
        )

        self.assertEquals(
            ('void', None),
            javatype.parse(
                'void'
            ),
        )

    def test_memberMapping(self):
        from proguard_mapping_parser.parser import memberMapping

        self.assertEquals(
            (((35, 35), ('void', None), '<clinit>', []), '<clinit>'),
            memberMapping.parse(
                '    35:35:void <clinit>() -> <clinit>',
            ),
        )
        self.assertEquals(
            (((35, 37), ('void', None), '<init>', []), '<init>'),
            memberMapping.parse(
                '    35:37:void <init>() -> <init>',
            ),
        )
        self.assertEquals(
            (
                ((66, 66), ('boolean', None), 'contains', [
                    ('java.lang.Object', None),
                ]),
                'a'
            ),
            memberMapping.parse(
                '    66:66:boolean contains(java.lang.Object) -> a',  # noqa
            ),
        )
        self.assertEquals(
            (
                (
                    None,
                    (
                        'android.arch.lifecycle.GeneratedAdapter',
                        '[]',
                    ),
                    'mGeneratedAdapters',
                    None,
                ),
                'a',
            ),
            memberMapping.parse(
                '    android.arch.lifecycle.GeneratedAdapter[] mGeneratedAdapters -> a',  # noqa
            )
        )
        self.assertEquals(
            (
                (
                    None,
                    (
                        'int',
                        '[]',
                    ),
                    '$SwitchMap$android$arch$lifecycle$Lifecycle$Event',
                    None,
                ),
                'a',
            ),
            memberMapping.parse(
                '    int[] $SwitchMap$android$arch$lifecycle$Lifecycle$Event -> a',  # noqa
            ),
        )
        self.assertEquals(
            ((
                None,
                ('android.arch.core.internal.SafeIterableMap$Entry', None),
                'mStart',
                None
            ), 'a'),  # noqa
            memberMapping.parse(
                '    android.arch.core.internal.SafeIterableMap$Entry mStart -> a',  # noqa
            ),
        )
        self.assertEquals(
            (
                (
                    None,
                    ('android.arch.core.internal.SafeIterableMap$Entry', None),
                    'forward',
                    [
                        (
                            'android.arch.core.internal.SafeIterableMap$Entry',
                            None
                        ),
                    ],
                ),
                'a'
            ),
            memberMapping.parse(
                '    android.arch.core.internal.SafeIterableMap$Entry forward(android.arch.core.internal.SafeIterableMap$Entry) -> a',  # noqa
            ),
        )

    def test_memberMappings(self):
        from parsec import sepBy
        from parsec import string
        from proguard_mapping_parser.parser import memberMapping

        members = sepBy(memberMapping, string('\n'))
        self.assertEquals(
            [
                ((None, ('java.util.HashMap', None), 'mHashMap', None), 'a'),
                (((35, 37), ('void', None), '<init>', []), '<init>'),
                (((66, 66), ('boolean', None), 'contains', [
                    ('java.lang.Object', None),
                ]), 'a'),
            ],
            members.parse(
                '    java.util.HashMap mHashMap -> a\n'
                '    35:37:void <init>() -> <init>\n'
                '    66:66:boolean contains(java.lang.Object) -> a\n'
            )
        )

    def test_classMapping(self):
        from proguard_mapping_parser.parser import classMapping
        self.assertEquals(
            (
                (
                    'android.arch.core.internal.FastSafeIterableMap',
                    'android.a.a.a.a'
                ), [
                    (
                        (None, ('java.util.HashMap', None), 'mHashMap', None),
                        'a'
                    ),
                    (
                        ((35, 37), ('void', None), '<init>', []),
                        '<init>'
                    ),
                    (
                        ((66, 66), ('boolean', None), 'contains', [
                            ('java.lang.Object', None),
                        ]),
                        'a'
                    ),  # noqa
                ]
            ),
            classMapping.parse(
                'android.arch.core.internal.FastSafeIterableMap -> android.a.a.a.a:\n'  # noqa
                '    java.util.HashMap mHashMap -> a\n'
                '    35:37:void <init>() -> <init>\n'
                '    66:66:boolean contains(java.lang.Object) -> a\n'
            )
        )
