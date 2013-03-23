# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of RecursiveDocument. http://jacquev6.github.com/RecursiveDocument

# RecursiveDocument is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# RecursiveDocument is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with RecursiveDocument.  If not, see <http://www.gnu.org/licenses/>.

import textwrap
import itertools


def _wrap(text, prefix):
    return textwrap.wrap(text, initial_indent=prefix, subsequent_indent=prefix)


def _insertWhiteLines(blocks):
    insert = False
    for block in blocks:
        if insert:
            yield ""
        insert = True
        for line in block:
            yield line


class Container:
    def __init__(self):
        self.__contents = []

    def add(self, newContent):
        self.__contents.append(newContent)
        return self

    def _formatContents(self, prefix):
        return _insertWhiteLines(c._format(prefix) for c in self.__contents)


class Paragraph:
    def __init__(self, text):
        self.__text = text

    def _format(self, prefix):
        return _wrap(self.__text, prefix)


class Section(Container):
    def __init__(self, title):
        Container.__init__(self)
        self.__title = title

    def _format(self, prefix):
        return itertools.chain(_wrap(self.__title + ":", prefix), self._formatContents(prefix + "  "))


class Document(Container):
    def format(self):
        return "\n".join(self._formatContents("")) + "\n"


class DefinitionList:
    def __init__(self):
        self.__items = []

    def add(self, name, definition):
        self.__items.append((name, definition))
        return self

    def _format(self, prefix):
        lengthOfLongestItem = max(itertools.chain([0], (len(name) for name, _ in self.__items if len(name) + len(prefix) < 25)))
        return itertools.chain.from_iterable(self.__formatItem(name, definition, lengthOfLongestItem, prefix) for name, definition in self.__items)

    def __formatItem(self, name, definition, lengthOfLongestItem, prefix):
        if len(definition) == 0:
            yield prefix + name
        else:
            if len(name) + len(prefix) < 25:
                for line in textwrap.wrap(definition, initial_indent=prefix + name + (lengthOfLongestItem - len(name) + 2) * " ", subsequent_indent=prefix + (lengthOfLongestItem + 2) * " "):
                    yield line
            else:
                yield prefix + name
                indent = prefix + (lengthOfLongestItem + 2) * " "
                for line in textwrap.wrap(definition, initial_indent=indent, subsequent_indent=indent):
                    yield line
