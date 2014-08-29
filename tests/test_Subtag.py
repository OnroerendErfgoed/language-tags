# -*- coding: utf-8 -*-
import unittest
from language_tags.Subtag import Subtag


class TestSubtag(unittest.TestCase):

    def test_type(self):
        self.assertEqual(Subtag('zh', 'language').type, 'language')
        self.assertEqual(Subtag('IQ', 'region').type, 'region')

    def test_description(self):
        self.assertEqual(Subtag('IQ', 'region').description, ['Iraq'])
        self.assertEqual(Subtag('vsv', 'extlang').description, ['Valencian Sign Language',
                                                                  'Llengua de signes valenciana'])

    def test_preferred(self):
        # Extlang
        subtag = Subtag('vsv', 'extlang')
        preferred = subtag.preferred
        self.assertIsNotNone(preferred)
        self.assertEqual(preferred.type, 'language')
        self.assertEqual(preferred.format, 'vsv')

        # Language
        # Moldovan -> Romanian
        subtag = Subtag('mo', 'language')
        preferred = subtag.preferred
        self.assertIsNotNone(preferred)
        self.assertEqual(preferred.type, 'language')
        self.assertEqual(preferred.format, 'ro')

        # Region
        # Burma -> Myanmar
        subtag = Subtag('BU', 'region')
        preferred = subtag.preferred
        self.assertIsNotNone(preferred)
        self.assertEqual(preferred.type, 'region')
        self.assertEqual(preferred.format, 'MM')

        # Variant
        subtag = Subtag('heploc', 'variant')
        preferred = subtag.preferred
        self.assertIsNotNone(preferred)
        self.assertEqual(preferred.type, 'variant')
        self.assertEqual(preferred.format, 'alalc97')

        # Should return None if no preferred value.
        # Latin America and the Caribbean
        subtag = Subtag('419', 'region')
        self.assertIsNone(subtag.preferred)

    def test_format(self):
        # Language
        self.assertEqual(Subtag('en', 'language').format, 'en')
        self.assertEqual(Subtag('EN', 'language').format, 'en')

        # Region
        self.assertEqual(Subtag('GB', 'region').format, 'GB')
        self.assertEqual(Subtag('gb', 'region').format, 'GB')

        # Script
        self.assertEqual(Subtag('Latn', 'script').format, 'Latn')
        self.assertEqual(Subtag('latn', 'script').format, 'Latn')

    def test_script(self):
        subtag = Subtag('en', 'language')
        script = subtag.script
        self.assertIsNotNone(script)
        self.assertEqual(script.type, 'script')
        self.assertEqual(script.format, 'Latn')

        # Should return null if no script.
        # A macrolanguage like 'zh' should have no suppress-script.
        subtag = Subtag('zh', 'language')
        script = subtag.script
        self.assertIsNone(script)

    def test_scope(self):
        self.assertEqual(Subtag('zh', 'language').scope, 'macrolanguage')
        self.assertEqual(Subtag('nah', 'language').scope, 'collection')
        self.assertIsNone(Subtag('en', 'language').scope)
        self.assertIsNone(Subtag('IQ', 'region').scope)

    def test_deprecated(self):
        self.assertEqual(Subtag('DD', 'region').deprecated, '1990-10-30')
        self.assertIsNone(Subtag('DE', 'region').deprecated)

    def test_added(self):
        self.assertEqual(Subtag('DD', 'region').added, '2005-10-16')
        self.assertEqual(Subtag('DG', 'region').added, '2009-07-29')

    def test_comments(self):
        self.assertEqual(Subtag('YU', 'region').comments, ['see BA, HR, ME, MK, RS, or SI'])