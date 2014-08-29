# -*- coding: utf-8 -*-
import unittest
from language_tags.Tag import Tag


class TestTag(unittest.TestCase):

    def test_tag_type_grandfathered(self):
        self.assertIn(Tag("en-GB-oed").type(), 'grandfathered')

    def test_tag_type_redundant(self):
        self.assertIn(Tag("az-Arab").type(), 'redundant')
        self.assertIn(Tag("uz-Cyrl").type(), 'redundant')
        self.assertIn(Tag("zh-cmn-Hant").type(), 'redundant')

    def test_tag_type_tag(self):
        self.assertIn(Tag("mt").type(), 'tag')


