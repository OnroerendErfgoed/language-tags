# -*- coding: utf-8 -*-
import json
from language_tags.Subtag import Subtag
import os

parent_dir = os.path.dirname(__file__)
index = json.load(open(os.path.join(parent_dir, "data/json/index.json")))
registry = json.load(open(os.path.join(parent_dir, "data/json/registry.json")))


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
    def added(self):
        """
        Get the date string of grandfathered or redundant tag when it was added to the registry

        :return: added date string
        """
        if 'record' in self.data:
            return self.data['record']['Added'] if 'Added' in self.data['record'] else None
        else:
            return None

    @property
    def deprecated(self):
        """
        Get the deprecation date of grandfathered or redundant tag if the tag is deprecated

        :return: deprecation date string
        """
        if 'record' in self.data:
            return self.data['record']['Deprecated'] if 'Deprecated' in self.data['record'] else None
        else:
            return None

    @property
    def descriptions(self):
        """
        Get the array of descriptions of the grandfathered or redundant tag.
        If no descriptions available, it returns an empty array

        :return: array of descriptions
        """
        if 'record' in self.data:
            return self.data['record']['Description'] if 'Description' in self.data['data'] else []
        else:
            return []

    @property
    def format(self):
        """
        Get format according to algorithm defined in RFC 5646 section 2.1.1.


        :return: formatted tag
        """
        tag = self.data['tag']
        subtags = tag.split('-')
        if len(subtags) == 1:
            return subtags[0]

        for i, subtag in enumerate(subtags[1:]):
            previous_subtag = subtags[i - 1]

            if len(previous_subtag) == 1:
                return previous_subtag + subtag.upper()

            elif len(subtag) == 2:
                return previous_subtag + '-' + subtag.upper()

            elif len(subtag) == 4:
                return previous_subtag + '-' + subtag.capitalize()

            return previous_subtag + '-' + subtag





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
        for i, code in enumerate(codes):

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
            if 'language' in types and i == 0:
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
        """
        Checks whether the tag is valid

        :return: True if valid otherwise False
        """
        return len(self.errors) < 1

    @property
    def errors(self):
        """
        Get the errors of the tag.
        If the tag is valid, it returns empty array.
        If invalid then the array will consist of errors containing each a code and message explaining the error.
        Each error also refers to the respective (sub)tag(s)

        :return: array of errors of the tag
        """
        errors = []
        data = self.data
        error = self.error

        # Check if the tag is grandfathered and if the grandfathered tag is deprecated (e.g. no-nyn).
        if 'record' in data:
            if 'Deprecated' in data['record']:
                errors.append(error(self.ERR_DEPRECATED))
            # Only check every subtag if the tag is not explicitly listed as grandfathered or redundant.
            return errors

        # Check that all subtag codes are meaningful.
        codes = data['tag'].split('-')
        for i, code in enumerate(codes):
            # Ignore anything after a singleton (break)
            if len(code) < 2:
                # Check that each private-use subtag is within the maximum allowed length.
                for code in codes[i + 1:]:
                    if len(code) > 8:
                        errors.append(error(self.ERR_TOO_LONG, code))
                break

            if code not in index:
                errors.append(error(self.ERR_UNKNOWN, code))
                # Continue to the next item.
                continue

        # Check that first tag is a language tag.
        subtags = self.subtags
        if not len(subtags):
            errors.append(error(self.ERR_NO_LANGUAGE))
            return errors
        elif subtags[0].type != 'language':
            errors.append(error(self.ERR_NO_LANGUAGE))
            return errors

        # Check for more than one of some types and for deprecation.
        found = dict(language=[], extlang=[], variant=[], script=[], region=[])
        for subtag in subtags:
            type = subtag.type

            if subtag.deprecated:
                errors.append(error(self.ERR_SUBTAG_DEPRECATED, subtag))

            if type in found:
                found[type].append(subtag)

            if 'language' == type:
                if len(found['language']) > 1:
                    errors.append(error(self.ERR_EXTRA_LANGUAGE, subtag))
            elif 'region' == type:
                if len(found['region']) > 1:
                    errors.append(error(self.ERR_EXTRA_REGION, subtag))
            elif 'extlang' == type:
                if len(found['extlang']) > 1:
                    errors.append(error(self.ERR_EXTRA_EXTLANG, subtag))
            elif 'script' == type:
                if len(found['language']) > 1:
                    errors.append(error(self.ERR_EXTRA_SCRIPT, subtag))
                # Check if script is same as language suppress-script.
                else:
                    script = subtags[0].script
                    if script:
                        if script.format == subtag.format:
                            errors.append(error(self.ERR_SUPPRESS_SCRIPT, subtag))
            elif 'variant' == type:
                if len(found['variant']) > 1:
                    for variant in found['variant']:
                        if variant.format == subtag.format:
                            errors.append(error(self.ERR_DUPLICATE_VARIANT, subtag))

        # Check for correct order.
        priority = dict(language=4, extlang=5, script=6, region=7, variant=8)
        for i, subtag in enumerate(subtags):
            next = subtags[i + 1]
            if next:
                if priority[subtag.type] > priority[next.type]:
                    errors.append(error(self.ERR_WRONG_ORDER, [subtag, next]))

        return errors

    def error(self, code, subtag=None):
        """
        Get the Tag.error of a specific Tag error code.
        The error creates a message explaining the error given the Tag error code.
        It also refers to the respective (sub)tag(s)

        :param code: a Tag error error (1=Tag.ERR_DEPRECATED, 2=Tag.ERR_NO_LANGUAGE, 3=Tag.ERR_UNKNOWN,
        4=Tag.ERR_TOO_LONG, 5=Tag.ERR_EXTRA_REGION, 6=Tag.ERR_EXTRA_EXTLANG, 7=Tag.ERR_EXTRA_SCRIPT,
        8=Tag.ERR_DUPLICATE_VARIANT, 9=Tag.ERR_WRONG_ORDER, 10=Tag.ERR_SUPPRESS_SCRIPT, 11=Tag.ERR_SUBTAG_DEPRECATED,
        12=Tag.ERR_EXTRA_LANGUAGE)
        :param subtag: The (sub)tag(s) creating the error
        :return: An exception class containing a Tag error input code, derived message with the given subtag input
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
            message = 'The subtag \'%s\' should not appear before \'%s\'.' % (subtag[0], subtag[1])

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
