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

        # Include errror codes
        self.ERR_DEPRECATED = 1
        self.ERR_NO_LANGUAGE = 2
        self.ERR_UNKNOWN = 3
        self.ERR_TOO_LONG = 4
        self.ERR_EXTRA_REGION = 5
        self.ERR_EXTRA_EXTLANG = 6
        self.ERR_EXTRA_SCRIPT = 7
        self.ERR_DUPLICATE_VARIANT = 8
        self.ERR_WRONG_ORDER = 9
        self.ERR_SUPPRESS_SCRIPT = 10
        self.ERR_SUBTAG_DEPRECATED = 11
        self.ERR_EXTRA_LANGUAGE = 12

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
            # Language subtags may only appear at the beginning of the tag, otherwise the subtag type is indeterminate.
            if 'language' in types and codes.index(code) == 0:
                if types['language']:
                    subtags.append(Subtag(code, 'language'))
                    continue

            if len(code) == 2:
                # Should be a region
                if 'region' in types:
                    subtags.append(Subtag(code, 'region'))
                # Error case: language subtag in the wrong place.
                elif 'language' in types:
                    subtags.append(Subtag(code, 'language'))

            elif len(code) == 3:
                # Could be a numeric region code e.g. '001' for 'World'.
                if 'region' in types:
                    subtags.append(Subtag(code, 'region'))
                elif 'extlang' in types:
                    subtags.append(Subtag(code, 'extlang'))
                # Error case: language subtag in the wrong place.
                elif 'language' in types:
                    subtags.append(Subtag(code, 'language'))

            elif len(code) == 4:
                # Could be a numeric variant
                if 'variant' in types:
                    subtags.append(Subtag(code, 'variant'))
                elif 'script' in types:
                    subtags.append(Subtag(code, 'script'))

            else:
                # Should be a variant
                if 'variant' in types:
                    subtags.append(Subtag(code, 'variant'))

        return subtags

    @property
    def valid(self):
        return len(self.errors) < 1

    @property
    def errors(self):
        errors = []
        data = self.data

        if 'record' in data:
            # Check if the tag is grandfathered and if the grandfathered tag is deprecated (e.g. no-nyn).
            if 'Deprecated' in data['record']:
                errors.append(self.error(self.ERR_DEPRECATED))
            # Only check every subtag if the tag is not explicitly listed as grandfathered or redundant.
            return errors

        # Check that all subtag codes are meaningful.
        codes = data['tag'].split('-')
        for code in codes:
            # Ignore anything after a singleton.
            if len(code) < 2:
                # Check that each private-use subtag is within the maximum allowed length.
                for code in codes[codes.index(code) + 1:]:
                    if len(code) > 8:
                        errors.append(self.error(self.ERR_TOO_LONG, code))
                break


            if code not in index:
                errors.append(self.error(self.ERR_UNKNOWN, code))

            # todo: add and test errors
        return errors


    def error(self, code, subtag=None):

        """

        :param code:
        :param subtag:
        :return:
        """
        message = ""
        data = self.data

        if code == self.ERR_DEPRECATED:
            message = 'The tag %s is deprecated.' % data['tag']

            # Note that a record that contains a 'Deprecated' field and no corresponding 'Preferred-Value' field
            # has no replacement mapping (RFC 5646 section 3.1.6).
            if 'Preferred-Value' in self.data['record']:
                message += ' Use \'%s\' instead.' % data['record']['Preferred-Value']

        if code == self.ERR_SUBTAG_DEPRECATED:
            message = 'The subtag \'%s\' is deprecated.' % subtag

        if code == self.ERR_NO_LANGUAGE:
            if not len(data['tag']):
                message = 'Empty tag.'
            else:
                message = 'Missing language tag in \'%s\'.' % data['tag']

        if code == self.ERR_UNKNOWN:
            message = 'Unknown code \'%s\'' % subtag

        if code == self.ERR_TOO_LONG:
            message = 'The private-use subtag \'%s\' is too long.' % subtag

        if code in [self.ERR_EXTRA_LANGUAGE,
                    self.ERR_EXTRA_EXTLANG,
                    self.ERR_EXTRA_REGION,
                    self.ERR_EXTRA_SCRIPT]:
            message = 'Extra %s subtag \'%s\' found.' % (subtag.type, subtag)

        if code == self.ERR_DUPLICATE_VARIANT:
            message = 'Duplicate variant subtag \'%s\' found.' % subtag

        if code == self.ERR_WRONG_ORDER:
            message = 'Duplicate variant subtag \'%s\' found.' % subtag

        if code == self.ERR_SUPPRESS_SCRIPT:
            message = 'The script subtag \'%s\' is the same as the language suppress-script.' % subtag

        class Error(Exception):
            def __init__(self, code, message, tag, subtag):
                self.code = code
                self.message = message
                self.tag = tag
                self.subtag = subtag

            def __str__(self):
                return repr("%s: %s (Tag %s; Subtag %s)" % (self.code, self.message, self.tag, str(self.subtag)))

        return Error(code, message, data['tag'], subtag)
