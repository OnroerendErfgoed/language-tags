# -*- coding: utf-8 -*-
import os
import json

from language_tags.Subtag import Subtag
from language_tags.Tag import Tag


parent_dir = os.path.dirname(__file__)
index = json.load(open(os.path.join(parent_dir, "data/json/index.json")))
registry = json.load(open(os.path.join(parent_dir, "data/json/registry.json")))


class tags(Tag):
    def __new__(cls, tag):
        """
        Get a Tag object of a (hyphen-separated) tag

        :param tag: (hyphen-seperated) tag
        :return: Tag object
        """
        return Tag(tag)

    @classmethod
    def check(cls, tag):
        """
        Check if a (hyphen-separated) tag is valid

        :param tag: (hyphen-separated) tag
        :return: bool (True if valid)
        """
        return Tag(tag).valid

    @classmethod
    def types(cls, subtag):
        """
        Get the types of a subtag (excludes redundant and grandfathered). It can return an empty list.

        :param subtag: subtag
        :return: a list of types
        """
        if subtag in index:
            types = index[subtag]
            return [type for type in types.keys() if type != 'redundant' or type != 'grandfathered']
        else:
            return []

    @classmethod
    def subtags(cls, subtags):
        """
        Get a list of existing Subtag objects given the input subtag(s)

        :param subtags: subtag of list of subtags
        :return: a list of existing Subtag objects
        """
        result = []

        if not isinstance(subtags, list):
            subtags = [subtags]

        for subtag in subtags:
            for type in tags.types(subtag):
                result.append(Subtag(subtag, type))

        return result

    @classmethod
    def filter(cls, subtags):
        """
        Get a list of non-existing Subtag objects given the input subtag(s)

        :param subtags: subtag of list of subtags
        :return: a list of non-existing Subtag objects
        """
        if not isinstance(subtags, list):
            subtags = [subtags]
        return [subtag for subtag in subtags if len(tags.types(subtag)) == 0]

    @classmethod
    def search(cls, description, all=False):
        """
        Gets a list of Subtags Objects where the description matches

        :param description: a string or compiled regular expression (For example re.compile('\d{4}'))
        :param all: boolean parameter. If set on True grandfathered and redundant tags will be included
        :return: list of Subtag Objects which include the description
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

    @classmethod
    def description(cls, tag):
        """
        Gets a list of descriptions given the tag. The list can be empty

        :param tag: tag
        :return: list of descriptions
        """
        tag_object = Tag(tag)
        results = tag_object.descriptions
        subtags = tag_object.subtags
        for subtag in subtags:
            results += subtag.description

        return results

    @classmethod
    def languages(cls, macrolanguage):
        """
        Get a list of Subtag objects given the macrolanguage

        :param macrolanguage: subtag macrolanguage
        :return: a list of the macrolanguage Subtag objects
        :raise Exception: if the macrolanguage does not exists
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

    @classmethod
    def type(cls, subtag, type):
        """
        Get a Subtag object by subtag and type. Can be None if not exists.

        :param subtag: subtag string
        :param type: string type
        :return: Subtag object if exists
        """
        subtag = subtag.lower()
        if subtag in index:
            types = index[subtag]
            if type in types:
                return Subtag(subtag, type)
        return None

    @classmethod
    def language(cls, subtag):
        """
        Get a language Subtag object of the subtag string

        :param subtag: subtag string
        :return: language Subtag object if exists
        """
        return tags.type(subtag, 'language')

    @classmethod
    def region(cls, subtag):
        """
        Get a region Subtag object of the subtag string

        :param subtag: subtag string
        :return: region Subtag object if exists
        """
        return tags.type(subtag, 'region')

    @classmethod
    def date(cls):
        """
        Get the file date of the underlying data as a string

        :return: date as string
        """
        meta = json.load(open(os.path.join(parent_dir, "data/json/meta.json")))
        return meta['File-Date']