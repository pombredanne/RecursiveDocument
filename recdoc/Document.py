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


def _wrap(text, prefixLength):
    indent = prefixLength * " "
    return textwrap.wrap(text, initial_indent=indent, subsequent_indent=indent)


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

    def _formatContents(self, prefixLength):
        return _insertWhiteLines(c._format(prefixLength) for c in self.__contents)


class Paragraph:
    def __init__(self, text):
        self.__text = text

    def _format(self, prefixLength):
        return _wrap(self.__text, prefixLength)


class Section(Container):
    def __init__(self, title):
        Container.__init__(self)
        self.__title = title

    def _format(self, prefixLength):
        return itertools.chain(_wrap(self.__title + ":", prefixLength), self._formatContents(prefixLength + 2))


class Document(Container):
    def format(self):
        return "\n".join(self._formatContents(0)) + "\n"


class DefinitionList:
    __maxDefinitionPrefixLength = 24

    def __init__(self):
        self.__items = []

    def add(self, name, definition):
        self.__items.append((name, definition))
        return self

    def _format(self, prefixLength):
        definitionPrefixLength = 2 + max(
            itertools.chain(
                [prefixLength],
                (
                    len(prefixedName)
                    for prefixedName, definition, shortEnough in self.__prefixedItems(prefixLength)
                    if shortEnough
                )
            )
        )
        return itertools.chain.from_iterable(
            self.__formatItem(item, definitionPrefixLength)
            for item in self.__prefixedItems(prefixLength)
        )

    def __prefixedItems(self, prefixLength):
        for name, definition in self.__items:
            prefixedName = prefixLength * " " + name
            shortEnough = len(prefixedName) <= self.__maxDefinitionPrefixLength
            yield prefixedName, definition, shortEnough

    def __formatItem(self, item, definitionPrefixLength):
        prefixedName, definition, shortEnough = item
        subsequentIndent = definitionPrefixLength * " "

        nameMustBeOnItsOwnLine = len(definition) == 0 or not shortEnough

        if nameMustBeOnItsOwnLine:
            yield prefixedName
            initialIndent = subsequentIndent
        else:
            initialIndent = prefixedName + (definitionPrefixLength - len(prefixedName)) * " "

        for line in textwrap.wrap(definition, initial_indent=initialIndent, subsequent_indent=subsequentIndent):
            yield line
