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

    def test_subtags_correct_type(self):
        tag = Tag('en')
        subtages = tag.subtags
        self.assertEqual(len(subtages), 1)
        self.assertEqual(subtages[0].type, 'language')
        self.assertEqual(subtages[0].format, 'en')

        # Lowercase - lookup should be case insensitive.
        tag = Tag('en-mt')
        subtages = tag.subtags
        self.assertEqual(len(subtages), 2)
        self.assertEqual(subtages[0].type, 'language')
        self.assertEqual(subtages[0].format, 'en')
        self.assertEqual(subtages[1].type, 'region')
        self.assertEqual(subtages[1].format, 'MT')

        tag = Tag('en-mt-arab')
        subtages = tag.subtags
        self.assertEqual(len(subtages), 3)
        self.assertEqual(subtages[0].type, 'language')
        self.assertEqual(subtages[0].format, 'en')
        self.assertEqual(subtages[1].type, 'region')
        self.assertEqual(subtages[1].format, 'MT')
        self.assertEqual(subtages[2].type, 'script')
        self.assertEqual(subtages[2].format, 'Arab')

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
        subtags =tag.subtags
        self.assertEqual(subtags, [])

    def test_subtags_of_redundant_tag(self):
        tag = Tag('az-Arab')
        self.assertEqual(tag.type, 'redundant')
        subtags = tag.subtags
        self.assertEqual(subtags, [])