# -*- coding: utf-8 -*-
import unittest
from language_tags.Tag import Tag


class TestTag(unittest.TestCase):

    def test_type(self):
        self.assertIn(Tag("en-GB-oed").type, 'grandfathered')
        self.assertIn(Tag("az-Arab").type, 'redundant')
        self.assertIn(Tag("uz-Cyrl").type, 'redundant')
        self.assertIn(Tag("zh-cmn-Hant").type, 'redundant')
        self.assertIn(Tag("mt").type, 'tag')

    def test_repr(self):
        self.assertIn('zh-wuu', repr(Tag('zh-wuu')))
        self.assertIn('redundant', repr(Tag('zh-wuu')))
        # test encoding
        self.assertIn('é', repr(Tag('é')))
        print(Tag('é'))

    def test_subtags_correct_type(self):
        tag = Tag('aa')
        subtags = tag.subtags
        self.assertEqual(len(subtags), 1)
        self.assertEqual(subtags[0].type, 'language')
        self.assertEqual(subtags[0].format, 'aa')

        # Lowercase - lookup should be case insensitive.
        tag = Tag('en-mt')
        subtags = tag.subtags
        self.assertEqual(len(subtags), 2)
        self.assertEqual(subtags[0].type, 'language')
        self.assertEqual(subtags[0].format, 'en')
        self.assertEqual(subtags[1].type, 'region')
        self.assertEqual(subtags[1].format, 'MT')

        tag = Tag('en-mt-arab')
        subtags = tag.subtags
        self.assertEqual(len(subtags), 3)
        self.assertEqual(subtags[0].type, 'language')
        self.assertEqual(subtags[0].format, 'en')
        self.assertEqual(subtags[1].type, 'region')
        self.assertEqual(subtags[1].format, 'MT')
        self.assertEqual(subtags[2].type, 'script')
        self.assertEqual(subtags[2].format, 'Arab')

    def test_only_existent_subtags(self):
        tag = Tag('hello')
        self.assertEqual(tag.subtags, [])

        tag = Tag('en-hello')
        subtags = tag.subtags
        self.assertEqual(len(subtags), 1)
        self.assertEqual(subtags[0].type, 'language')
        self.assertEqual(subtags[0].format, 'en')

    def test_subtags_of_private_tags(self):
        tag = Tag('en-GB-x-Beano')
        subtags = tag.subtags
        self.assertEqual(len(subtags), 2)
        self.assertEqual(subtags[0].type, 'language')
        self.assertEqual(subtags[0].format, 'en')
        self.assertEqual(subtags[1].type, 'region')
        self.assertEqual(subtags[1].format, 'GB')

    def test_subtags_of_grandfathered_tag(self):
        tag = Tag('en-GB-oed')
        self.assertEqual(tag.type, 'grandfathered')
        subtags = tag.subtags
        self.assertEqual(subtags, [])

    def test_subtags_of_redundant_tag(self):
        tag = Tag('az-Arab')
        self.assertEqual(tag.type, 'redundant')
        subtags = tag.subtags
        self.assertGreater(len(subtags), 0)


    def test_language_subtags(self):
        self.assertEqual('nl', Tag('nl-BE').language.format)
        self.assertIsNone(Tag('n-test').language)

    def test_region_subtags(self):
        self.assertEqual(Tag('nl-BE').region.format, 'BE')
        self.assertIsNone(Tag('nl').region)

    def test_script_subtags(self):
        self.assertEqual(Tag('en-mt-arab').script.format, 'Arab')
        self.assertIsNone(Tag('en-mt').script)

    def test_errors_deprecated_grandfathered(self):
        # Grandfathered and deprecated, therefore invalid.
        tag = Tag('art-lojban')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertIsNotNone(tag.deprecated)
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_DEPRECATED)
        self.assertEqual(err.tag, 'art-lojban')
        self.assertEqual(err.message, 'The tag art-lojban is deprecated. Use \'jbo\' instead.')
        self.assertIn(str(err.code), err.__str__())
        self.assertIn(err.message, err.__str__())
        self.assertIn(err.tag, err.__str__())
        self.assertIn(str(err.subtag), err.__str__())

    def test_errors_deprecated_redundant(self):
        # Redundant and deprecated, therefore invalid.
        tag = Tag('zh-cmn')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNotNone(tag.deprecated)
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_DEPRECATED)
        self.assertEqual(err.tag, 'zh-cmn')
        self.assertEqual(err.message, 'The tag zh-cmn is deprecated. Use \'cmn\' instead.')

    def test_errors_deprecated_subtags(self):
        # Moldovan (mo) is deprecated as a language.
        tag = Tag('mo')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_SUBTAG_DEPRECATED)
        self.assertEqual(err.message, 'The subtag \'mo\' is deprecated.')

        # Neutral Zone (NT) is deprecated as a region.
        tag = Tag('en-NT')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_SUBTAG_DEPRECATED)
        self.assertEqual(err.message, 'The subtag \'NT\' is deprecated.')

    def test_empty_errors_if_valid(self):
        self.assertEqual(len(Tag('en').errors), 0)

    def test_errors_no_language_tag(self):
        # test with empty tag.
        tag = Tag('')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_NO_LANGUAGE)
        self.assertEqual(err.message, 'Empty tag.')

        tag = Tag('IQ-Arab')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_NO_LANGUAGE)
        self.assertEqual(err.message, 'Missing language tag in \'iq-arab\'.')

        tag = Tag('419')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_NO_LANGUAGE)
        self.assertEqual(err.message, 'Missing language tag in \'419\'.')

    def test_errors_front_no_language_tag(self):
        tag = Tag('GB-en')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_NO_LANGUAGE)
        self.assertEqual(err.message, 'Missing language tag in \'gb-en\'.')

    def test_errors_multiple_language_subtags(self):
        tag = Tag('en-en')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_LANGUAGE)
        self.assertEqual(err.message, 'Extra language subtag \'en\' found.')

        tag = Tag('en-en-GB')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_LANGUAGE)
        self.assertEqual(err.message, 'Extra language subtag \'en\' found.')

        tag = Tag('ko-en')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_LANGUAGE)
        self.assertEqual(err.message, 'Extra language subtag \'en\' found.')

    def test_errors_multiple_region_subtags(self):
        tag = Tag('en-GB-GB')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_REGION)
        self.assertEqual(err.message, 'Extra region subtag \'GB\' found.')

        tag = Tag('ko-mt-mt')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_REGION)
        self.assertEqual(err.message, 'Extra region subtag \'MT\' found.')

    def test_errors_multiple_script_subtags(self):
        tag = Tag('mt-Arab-Arab')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_SCRIPT)
        self.assertEqual(err.message, 'Extra script subtag \'Arab\' found.')

        tag = Tag('en-Cyrl-Latn')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_SCRIPT)
        self.assertEqual(err.message, 'Extra script subtag \'Latn\' found.')

        # First error should be regarding suppress-script, second should be regarding extra script.
        tag = Tag('en-Latn-Cyrl')
        errs = tag.errors
        self.assertEqual(len(errs), 2)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_SUPPRESS_SCRIPT)
        self.assertEqual(err.message, 'The script subtag \'Latn\' is the same as the language suppress-script.')
        err = errs[1]
        self.assertEqual(err.code, tag.ERR_EXTRA_SCRIPT)
        self.assertEqual(err.message, 'Extra script subtag \'Cyrl\' found.')

    def test_errors_multiple_extlang_subtags(self):
        tag = Tag('en-asp-bog')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_EXTRA_EXTLANG)
        self.assertEqual(err.message, 'Extra extlang subtag \'bog\' found.')

    def test_errors_duplicate_variant_subtags(self):
        tag = Tag('ca-valencia-valencia')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_DUPLICATE_VARIANT)
        self.assertEqual(err.message, 'Duplicate variant subtag \'valencia\' found.')

    def test_errors_length_private_use_subtags(self):
        tag = Tag('en-x-more-than-eight-chars')
        errs = tag.errors
        self.assertEqual(len(errs), 0)

        tag = Tag('en-x-morethaneightchars')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_TOO_LONG)
        self.assertEqual(err.message, 'The private-use subtag \'morethaneightchars\' is too long.')

    def test_errors_supress_script(self):
        tag = Tag('gsw-Latn')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_SUPPRESS_SCRIPT)
        self.assertEqual(err.message, 'The script subtag \'Latn\' is the same as the language suppress-script.')

        tag = Tag('en-Latn-GB')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_SUPPRESS_SCRIPT)
        self.assertEqual(err.message, 'The script subtag \'Latn\' is the same as the language suppress-script.')

    def test_errors_wrong_order_subtags(self):
        tag = Tag('mt-MT-Arab')
        errs = tag.errors
        self.assertEqual(len(errs), 1)
        err = errs[0]
        self.assertEqual(err.code, tag.ERR_WRONG_ORDER)
        self.assertEqual(err.message, 'The subtag \'MT\' should not appear before \'Arab\'.')

    def test_valid_tag(self):
        self.assertTrue(Tag('en').valid)
        self.assertTrue(Tag('en-GB').valid)
        self.assertTrue(Tag('gsw').valid)
        self.assertTrue(Tag('de-CH').valid)

        # returns true for subtag followed by private tag
        self.assertTrue(Tag('en-x-whatever').valid)

    def test_valid_tag_grandfathered(self):
        # Grandfathered but not deprecated, therefore valid.
        tag = Tag('i-default')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertIsNone(tag.deprecated)
        self.assertTrue(tag.valid)

    def test_valid_tag_redundant(self):
        # Redundant but not deprecated, therefore valid.
        tag = Tag('zh-Hans')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNone(tag.deprecated)
        self.assertTrue(tag.valid)

        tag = Tag('es-419')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNone(tag.deprecated)
        self.assertTrue(tag.valid)

    def test_non_valid_non_existent(self):
        self.assertFalse(Tag('zzz').valid)
        self.assertFalse(Tag('zzz-Latn').valid)
        self.assertFalse(Tag('zzz-Lzz').valid)

    def test_non_valid_deprecated_grandfathered(self):
        tag = Tag('art-lojban')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertIsNotNone(tag.deprecated)
        self.assertFalse(tag.valid)

    def test_non_valid_deprecated_redundant(self):
        # Redundant and deprecated, therefore invalid.
        tag = Tag('zh-cmn')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNotNone(tag.deprecated)
        self.assertFalse(tag.valid)

        tag = Tag('zh-cmn-Hans')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNotNone(tag.deprecated)
        self.assertFalse(tag.valid)

    def test_non_valid_deprecated_subtags(self):
        #  Moldovan (mo) is deprecated as a language.
        self.assertFalse(Tag('mo').valid)

        #  Neutral Zone (NT) is deprecated as a region.
        self.assertFalse(Tag('en-NT').valid)

    def test_non_valid_redundant_script(self):
        # Swiss German (gsw) has a suppress script of Latn.
        self.assertFalse(Tag('gsw-Latn').valid)

    def test_non_valid_no_language(self):
        self.assertFalse(Tag('IQ-Arab').valid)
        self.assertFalse(Tag('419').valid)

    def test_non_valid_no_front_language(self):
        self.assertFalse(Tag('GB-en').valid)

    def test_non_valid_multiple_languages(self):
        self.assertFalse(Tag('en-en').valid)
        self.assertFalse(Tag('ko-en').valid)

    def test_non_valid_multiple_regions(self):
        self.assertFalse(Tag('en-001-gb').valid)
        self.assertFalse(Tag('gb-001').valid)

    def test_non_valid_multiple_extlangs(self):
        self.assertFalse(Tag('en-asp-bog').valid)

    def test_non_valid_multiple_scripts(self):
        self.assertFalse(Tag('arb-Latn-Cyrl').valid)

    def test_non_valid_duplicate_variant(self):
        self.assertFalse(Tag('ca-valencia-valencia').valid)

    def test_non_valid_more_private_use_lenght(self):
        self.assertFalse(Tag('en-x-morethaneightchars').valid)

    def test_non_valid_suppress_script(self):
        self.assertFalse(Tag('en-Latn').valid)
        self.assertFalse(Tag('en-GB-Latn').valid)
        self.assertFalse(Tag('gsw-Latn').valid)

    def test_deprecated(self):
        # Redundant and deprecated.
        tag = Tag('zh-cmn-Hant')
        self.assertEqual(tag.type, 'redundant')
        self.assertEqual(tag.deprecated, '2009-07-29')

        # Redundant but not deprecated.
        tag = Tag('zh-Hans')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNone(tag.deprecated)

        # Grandfathered and deprecated.
        tag = Tag('zh-xiang')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertEqual(tag.deprecated, '2009-07-29')

        # Grandfathered but not deprecated.
        tag = Tag('i-default')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertIsNone(tag.deprecated)

        self.assertIsNone(Tag('en').deprecated)

    def test_added(self):
        # Redundant and deprecated.
        tag = Tag('zh-cmn-Hant')
        self.assertEqual(tag.type, 'redundant')
        self.assertEqual(tag.added, '2005-07-15')

        # Redundant but not deprecated.
        tag = Tag('zh-Hans')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNone(tag.deprecated)
        self.assertEqual(tag.added, '2003-05-30')

        # Grandfathered and deprecated.
        tag = Tag('zh-xiang')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertEqual(tag.added, '1999-12-18')

        # Grandfathered but not deprecated.
        tag = Tag('i-default')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertIsNone(tag.deprecated)
        self.assertEqual(tag.added, '1998-03-10')

        self.assertIsNone(Tag('en').added)

    def test_description(self):
        tag = Tag('en-GB-oed')
        self.assertEqual(tag.type, 'grandfathered')
        self.assertEqual('2015-04-17', tag.deprecated)
        self.assertEqual(tag.descriptions, ['English, Oxford English Dictionary spelling'])

        self.assertEqual(Tag('en').descriptions, [])

    def test_format(self):
        self.assertEqual(Tag('en').format, 'en')
        self.assertEqual(Tag('en-x-more-than-eight-chars').format, 'en-x-more-than-eight-chars')
        self.assertEqual(Tag('En').format, 'en')
        self.assertEqual(Tag('EN').format, 'en')
        self.assertEqual(Tag('eN').format, 'en')
        self.assertEqual(Tag('en-gb').format, 'en-GB')
        self.assertEqual(Tag('en-gb-oed').format, 'en-GB-oed')
        self.assertEqual(Tag('az-latn').format, 'az-Latn')
        self.assertEqual(Tag('ZH-hant-hK').format, 'zh-Hant-HK')

    def test_perferred(self):
        tag = Tag('zh-cmn-Hant')
        self.assertEqual(tag.type, 'redundant')
        self.assertIsNotNone(tag.deprecated)
        self.assertIsNotNone(tag.preferred)
        self.assertEqual(tag.preferred.format, 'cmn-Hant')
        self.assertIsNone(Tag('cmn-Hant').preferred)
