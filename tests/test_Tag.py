import unittest
from language_tags.Tag import Tag

class test_Tag(unittest.TestCase):

    def test_Tagfunction(self):
        tag_nl = Tag("nl")
        tag_az_cyrl = Tag("az-cyrl")
        self.assertIn('language', tag_nl)
        self.assertIn('region', tag_nl)
        self.assertIn('redundant', tag_az_cyrl)

