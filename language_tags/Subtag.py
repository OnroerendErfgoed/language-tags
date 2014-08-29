# -*- coding: utf-8 -*-
import json

index = json.load(open("../data/json/index.json"))
registry = json.load(open("../data/json/registry.json"))



class Subtag:
    def __init__(self, subtag, type):

        """
        A subtag is a part of the hyphen-separated language tag

        :param subtag: subtage code
        :param type: can be 'language', 'extlang', 'script', 'region' or 'variant'
        :return: :raise Error: Checks for Subtag.ERR_NONEXISTENT and Subtag.ERR_TAG
        """
        # Lowercase for consistency (case is only a formatting convention, not a standard requirement).
        subtag = str(subtag).lower()
        type = str(type).lower()

        # Include errror codes
        self.ERR_NONEXISTENT = 1
        self.ERR_TAG = 2
        class Error(Exception):
            def __init__(self, code, message):
                self.code = code
                self.message = message

            def __str__(self):
                return repr("%s: %s" % (self.code, self.message))

        if subtag not in index:
            raise Error(self.ERR_NONEXISTENT, 'Non-existent subtag %s.' % subtag)
        types = index[subtag]

        if type not in types:
            raise Error(self.ERR_NONEXISTENT, 'Non-existent subtag %s of type %s.' % (subtag, type))
        i = types[type]

        record = registry[i]
        if 'Subtag' not in record:
            raise Error(self.ERR_TAG, '%s is a %s tag' % (subtag, type))

        self.data = {
            "subtag": subtag,
            "record": record,
            "type": type
        }

    @property
    def type(self):
        """
        Get the subtag type

        :return: either 'language', 'extlang', 'script', 'region' or 'variant'
        """
        return self.data['type']

    @property
    def description(self):
        """
        Get the subtag description

        :return: an array of description strings
        """
        return self.data['record']['Description']

    @property
    def preferred(self):
        """
        Get the preferred subtag

        :return: preferred Subtag
        """
        if 'Preferred-Value' in self.data['record']:
            preferred = self.data['record']['Preferred-Value']
            type = self.data['type']
            if type == 'extlang':
                type = 'language'
            return Subtag(preferred, type)
        return None

    @property
    def format(self):
        """
        Get the subtag code conventional format according to RFC 5646 section 2.1.1.

        :return: subtag code conventional format
        """
        subtag = self.data['subtag']
        if self.data['type'] == 'region':
            return subtag.upper()
        if self.data['type'] == 'script':
            return subtag.capitalize()
        return subtag

    @property
    def script(self):
        """
        Get the language's default script of the subtag (RFC 5646 section 3.1.9)

        :return: the language's default script
        """
        if 'Suppress-Script' in self.data['record']:
            return Subtag(self.data['record']['Suppress-Script'], 'script')
        return None

    @property
    def scope(self):
        """
        Get the subtag scope

        :return: subtag scope
        """
        return self.data['record']['Scope'] if 'Scope' in self.data['record'] else None

    @property
    def deprecated(self):
        """
        Get the deprecation date

        :return: deprecation date as string if subtag is deprecated
        """
        return self.data['record']['Deprecated'] if 'Deprecated' in self.data['record'] else None

    @property
    def added(self):
        """
        Get the date when the subtag was added to the registry

        :return: date (as string) when the subtag was added to the registry
        """
        return self.data['record']['Added']

    @property
    def comments(self):
        """
        Get the comments of the subtag

        :return: list of comments (can be empty)
        """
        return self.data['record']['Comments'] if 'Comments' in self.data['record'] else []