# -*- coding: utf-8 -*-
import unittest
import re

from language_tags import tags


class TestSubtag(unittest.TestCase):

    def test_get_tag(self):
        tag = tags.tag('en')
        self.assertIsNotNone(tag)

        tag = tags.tag('en-gb')
        self.assertIsNotNone(tag)
        self.assertEqual(tag.format, 'en-GB')

    def test_undetermined(self):
        tag = tags.tag('und')
        self.assertIsNotNone(tag)
        self.assertEqual(tag.format, 'und')

    def test_checks(self):
        self.assertTrue(tags.check('en'))

    def test_subtags(self):
        subtag = tags.subtags('whatever')
        self.assertEqual(subtag, [])

        subtags = tags.subtags('mt')
        self.assertEqual(len(subtags), 2)
        self.assertIn(subtags[0].type, ['language', 'region'])
        self.assertIn(subtags[0].format, ['mt', 'MT'])
        self.assertIn(subtags[1].type, ['language', 'region'])
        self.assertIn(subtags[1].format, ['mt', 'MT'])

    def test_filter(self):
        filter = tags.filter('whatever')
        self.assertIn('whatever', filter)

    def test_search(self):
        subtags = tags.search('Maltese')
        self.assertGreater(len(subtags), 0)

        self.assertEqual(subtags[0].type, 'language')
        self.assertEqual(subtags[0].format, 'mt')
        self.assertEqual(subtags[1].type, 'language')
        self.assertEqual(subtags[1].format, 'mdl')
        self.assertEqual(subtags[2].type, 'extlang')
        self.assertEqual(subtags[2].format, 'mdl')

        subtags = tags.search('Gibberish')
        self.assertEqual(subtags, [])

        subtags = tags.search('Lojban')
        self.assertEqual(len(subtags), 1)
        subtags = tags.search('Lojban', all=True)
        self.assertEqual(len(subtags), 2)

    def test_search_exact_match(self):
        subtags = tags.search('Dari')
        self.assertGreater(len(subtags), 0)
        self.assertEqual(subtags[0].type, 'language')
        self.assertEqual(subtags[0].format, 'prs')

    def test_search_regexp(self):
        subtags = tags.search(re.compile(r'\d{4}'))
        self.assertGreater(len(subtags), 0)

    def test_type(self):
        subtag = tags.type('Latn', 'script')
        self.assertIsNotNone(subtag)
        self.assertEqual(subtag.format, 'Latn')
        self.assertEqual(subtag.type, 'script')

        self.assertIsNone(tags.type('en', 'script'))

    def test_language(self):
        subtag = tags.language('en')
        self.assertIsNotNone(subtag)
        self.assertEqual(subtag.format, 'en')
        self.assertEqual(subtag.type, 'language')

        self.assertIsNone(tags.language('GB'))

    def test_region(self):
        subtag = tags.region('IQ')
        self.assertIsNotNone(subtag)
        self.assertEqual(subtag.format, 'IQ')
        self.assertEqual(subtag.type, 'region')

    def test_languages(self):
        subtags = tags.languages('zh')
        self.assertGreater(len(subtags), 0)

        self.assertRaises(Exception, tags.languages, 'en')
        with self.assertRaises(Exception) as context:
            tags.languages('en')
        self.assertIn('\'en\' is not a macrolanguage.', context.exception.args)

    def test_date(self):
        self.assertIsNotNone(re.compile(r'\d{4}\-\d{2}\-\d{2}').search(tags.date()))

    def test_description(self):
        description = tags.description('nl-BE')
        self.assertIn('Dutch', description)
        self.assertIn('Flemish', description)
        self.assertIn('Belgium', description)
        description = tags.description('az-Arab')
        self.assertIn('Azerbaijani in Arabic script', description)
        self.assertEqual(len(description), len(tags.description('az-Arab')))
        description = tags.description('123')
        self.assertEqual(0, len(description))
        description = tags.description('vls')
        self.assertIn('Vlaams', description)

    def test_print(self):
        nlbe = tags.tag('nl-Latn-BE')
        print(nlbe)
        self.assertEqual(nlbe.__str__(), 'nl-Latn-BE')
        print(nlbe.language)
        self.assertEqual(nlbe.language.__str__(), 'nl')
        print(nlbe.script)
        self.assertEqual(nlbe.script.__str__(), 'Latn')

    def test_redundant_subtags(self):
        tag = tags.tag('es-419')
        self.assertListEqual(tag.region.description, ['Latin America and the Caribbean'])
        self.assertListEqual(tag.language.description, ['Spanish', 'Castilian'])

        tag = tags.tag('sgn-NL')
        self.assertListEqual(tag.region.description, ['Netherlands'])
        self.assertListEqual(tag.language.description, ['Sign languages'])

    def test_grandfathered_subtags(self):
        tag = tags.tag('i-klingon')
        self.assertIsNone(tag.language)
        self.assertEqual(len(tag.subtags), 0)
