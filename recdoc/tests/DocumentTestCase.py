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

    def testEmptyDocument(self):
        self.assertEqual(self.doc.format(), "\n")

    def testOneSectionWithOneParagraph(self):
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

    def testOneSectionWithTwoParagraphs(self):
        section = self.doc.add(Section("First section"))
        section.add(Paragraph("Some text"))
        section.add(Paragraph("Some other text"))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                First section:
                  Some text
                
                  Some other text
                """
            )
        )

    def testSeveralSectionsWithSeveralParagraphs(self):
        section = self.doc.add(Section("Section A"))
        section.add(Paragraph("Text A.1"))
        section.add(Paragraph("Text A.2"))
        section.add(Paragraph("Text A.3"))
        section = self.doc.add(Section("Section B"))
        section.add(Paragraph("Text B.1"))
        section.add(Paragraph("Text B.2"))
        section.add(Paragraph("Text B.3"))
        section = self.doc.add(Section("Section C"))
        section.add(Paragraph("Text C.1"))
        section.add(Paragraph("Text C.2"))
        section.add(Paragraph("Text C.3"))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section A:
                  Text A.1

                  Text A.2

                  Text A.3

                Section B:
                  Text B.1

                  Text B.2

                  Text B.3

                Section C:
                  Text C.1

                  Text C.2

                  Text C.3
                """
            )
        )

    def testParagraphThenSection(self):
        self.doc.add(Paragraph("Some text"))
        self.doc.add(Section("Section title")).add(Paragraph("Section text"))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Some text

                Section title:
                  Section text
                """
            )
        )

    def testSectionThenParagraph(self):
        self.doc.add(Section("Section title")).add(Paragraph("Section text"))
        self.doc.add(Paragraph("Some text"))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section title:
                  Section text

                Some text
                """
            )
        )
