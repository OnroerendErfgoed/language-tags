# -*- coding: utf-8 -*-
import os
import json

from io import open

from language_tags.Subtag import Subtag
from language_tags.Tag import Tag


parent_dir = os.path.dirname(__file__)
index = json.load(open(os.path.join(parent_dir, "data/json/index.json"), encoding='utf-8'))
registry = json.load(open(os.path.join(parent_dir, "data/json/registry.json"), encoding='utf-8'))

class tags():

    @staticmethod
    def tag(tag):
        """
        Get a :class:`language_tags.Tag.Tag` of a string (hyphen-separated) tag.

        :param str tag: (hyphen-separated) tag.
        :return: :class:`language_tags.Tag.Tag`.
        """
        return Tag(tag)

    @staticmethod
    def check(tag):
        """
        Check if a string (hyphen-separated) tag is valid.

        :param str tag: (hyphen-separated) tag.
        :return: bool -- True if valid.
        """
        return Tag(tag).valid

    @staticmethod
    def types(subtag):
        """
        Get the types of a subtag string (excludes redundant and grandfathered).


        :param str subtag: subtag.
        :return: list of types. The return list can be empty.
        """
        if subtag in index:
            types = index[subtag]
            return [type for type in types.keys() if type != 'redundant' or type != 'grandfathered']
        else:
            return []

    @staticmethod
    def subtags(subtags):
        """
        Get a list of existing :class:`language_tags.Subtag.Subtag` objects given the input subtag(s).

        :param subtags: string subtag or list of string subtags.
        :return: a list of existing :class:`language_tags.Subtag.Subtag` objects. The return list can be empty.
        """
        result = []

        if not isinstance(subtags, list):
            subtags = [subtags]

        for subtag in subtags:
            for type in tags.types(subtag):
                result.append(Subtag(subtag, type))

        return result

    @staticmethod
    def filter(subtags):
        """
        Get a list of non-existing string subtag(s) given the input string subtag(s).

        :param subtags: string subtag or a list of string subtags.
        :return: list of non-existing string subtags. The return list can be empty.
        """
        if not isinstance(subtags, list):
            subtags = [subtags]
        return [subtag for subtag in subtags if len(tags.types(subtag)) == 0]

    @staticmethod
    def search(description, all=False):
        """
        Gets a list of :class:`language_tags.Subtag.Subtag` objects where the description matches.

        :param description: a string or compiled regular expression. For example: ``search(re.compile('\d{4}'))`` if the
            description of the returned subtag must contain four contiguous numerical digits.
        :type description: str or RegExp
        :param all: If set on True grandfathered and redundant tags will be included in the return
            list.
        :type all: bool, optional
        :return: list of :class:`language_tags.Subtag.Subtag` objects each including the description.
            The return list can be empty.
        """
        results = []

        def append(record):
            if 'Subtag' in record:
                results.append(Subtag(record['Subtag'], record['Type']))
            elif all:
                results.append(Tag(record['Tag']))

        if isinstance(description, str):
            description = description.lower()

            def test(record):
                if description in ', '.join(record['Description']).lower():
                    append(record)

        elif hasattr(description.search, '__call__'):
            def test(record):
                if description.search(', '.join(record['Description'])) is not None:
                    append(record)

        for registry_item in registry:
            test(registry_item)

        return results

    @staticmethod
    def description(tag):
        """
        Gets a list of descriptions given the tag.

        :param str tag: (hyphen-separated) tag.
        :return: list of string descriptions. The return list can be empty.
        """
        tag_object = Tag(tag)
        results = tag_object.descriptions
        subtags = tag_object.subtags
        for subtag in subtags:
            results += subtag.description

        return results

    @staticmethod
    def languages(macrolanguage):
        """
        Get a list of :class:`language_tags.Subtag.Subtag` objects given the string macrolanguage.

        :param string macrolanguage: subtag macrolanguage.
        :return: a list of the macrolanguage :class:`language_tags.Subtag.Subtag` objects.
        :raise Exception: if the macrolanguage does not exists.
        """
        results = []

        macrolanguage = macrolanguage.lower()
        macrolanguage_data = json.load(open(os.path.join(parent_dir, "data/json/macrolanguage.json")))
        if macrolanguage not in macrolanguage_data:
            raise Exception('\'' + macrolanguage + '\' is not a macrolanguage.')
        for registry_item in registry:
            record = registry_item
            if 'Macrolanguage' in record:
                if record['Macrolanguage'] == macrolanguage:
                    results.append(Subtag(record['Subtag'], record['Type']))

        return results

    @staticmethod
    def type(subtag, type):
        """
        Get a :class:`language_tags.Subtag.Subtag` by subtag and type. Can be None if not exists.

        :param str subtag: subtag.
        :param str type: type of the subtag.
        :return: :class:`language_tags.Subtag.Subtag` if exists, otherwise None.
        """
        subtag = subtag.lower()
        if subtag in index:
            types = index[subtag]
            if type in types:
                return Subtag(subtag, type)
        return None

    @staticmethod
    def language(subtag):
        """
        Get a language :class:`language_tags.Subtag.Subtag` of the subtag string.

        :param str subtag: subtag.
        :return: language :class:`language_tags.Subtag.Subtag` if exists, otherwise None.
        """
        return tags.type(subtag, 'language')

    @staticmethod
    def region(subtag):
        """
        Get a region :class:`language_tags.Subtag.Subtag` of the subtag string.

        :param str subtag: subtag.
        :return: region :class:`language_tags.Subtag.Subtag` if exists, otherwise None.
        """
        return tags.type(subtag, 'region')

    @staticmethod
    def date():
        """
        Get the file date of the underlying data as a string.

        :return: date as string (for example: '2014-03-27').
        """
        meta = json.load(open(os.path.join(parent_dir, "data/json/meta.json")))
        return meta['File-Date']
