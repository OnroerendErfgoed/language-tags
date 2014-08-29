# -*- coding: utf-8 -*-
import json
from language_tags.Subtag import Subtag

index = json.load(open("../data/json/index.json"))
registry = json.load(open("../data/json/registry.json"))


class Tag:
    def __init__(self, tag):
        # Lowercase for consistency (case is only a formatting convention, not a standard requirement).
        """
        Tags for Identifying Languages

        :param tag: tag code
        """
        tag = str(tag).strip().lower()

        self.data = {'tag': tag}

        if tag in index:
            types = index[tag]
            # Check if the input tag is grandfathered or redundant.
            if 'grandfathered' in types or 'redundant' in types:
                self.data['record'] = registry[types['grandfathered']] if 'grandfathered' in types \
                    else registry[types['redundant']]
    @property
    def type(self):
        """
        Get the type of the tag (either grandfathered, redundant or tag see  RFC 5646 section 2.2.8.)

        :return: type of the tag (string)
        """
        if 'record' in self.data:
            return self.data['record']['Type']
        return 'tag'

    @property
    def subtags(self):
        """
        Get the subtags of the tag

        :return: list of subtags that are part of the tag
        """
        data = self.data
        subtags = []

        # No subtags if the tag is grandfathered or redundant.
        if 'record' in data:
            return subtags

        codes = data['tag'].split('-')
        if not len(codes):
            return subtags

        # Try and find the language tag.
        for code in codes:

            # Singletons and anything after are unhandled.
            if len(code) == 1:
                #Stop the loop (stop processing after a singleton).
                break

            # Check for non-existent tag.
            if code not in index:
                continue
            types = index[code]

            # Check against undefined because value could be 0.
            #  Language subtags may only appear at the beginning of the tag, otherwise the subtag type is indeterminate.
            if 'language' in types:
