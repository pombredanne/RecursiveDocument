# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of RecursiveDocument. http://jacquev6.github.com/RecursiveDocument

# RecursiveDocument is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# RecursiveDocument is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with RecursiveDocument.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import textwrap

from recdoc import *

class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.doc = Document()

    def testFormatEmptyDocument(self):
        self.assertEqual(self.doc.format(), "")

    def testFormatDocumentWithOneSection(self):
        section = self.doc.add(Section("First section"))
        section.add(Paragraph("Some text"))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                First section:
                  Some text
                """
            )
        )
