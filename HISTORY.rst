0.3.2
_____
- Upgrade to https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.11
- Added wheel config
- Fixed bug under windows: opening data files using utf-8 encoding.

0.3.1
_____
- Upgrade to https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.8

0.3.0
_____
- Upgrade to https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.6
- Simplify output of __str__ functions. The previous json dump is assigned to the repr function.

    .. code-block:: python

        nlbe = tags.tags('nl-Latn-BE')
        > print(nlbe)
        'nl-Latn-BE'
        > print(nlbe.language)
        'nl'
        > print(nlbe.script)
        'Latn'

0.2.0
_____

- Adjust language, region and script properties of Tag. The properties will return :class:`language_tags.Subtag.Subtag`
  instead of a list of string subtags

    .. code-block:: python

        > print(tags.tag('nl-BE').language)
        '{"subtag": "nl", "record": {"Subtag": "nl", "Suppress-Script": "Latn", "Added": "2005-10-16", "Type": "language", "Description": ["Dutch", "Flemish"]}, "type": "language"}'
        > print(tags.tag('nl-BE').region)
        '{"subtag": "be", "record": {"Subtag": "BE", "Added": "2005-10-16", "Type": "region", "Description": ["Belgium"]}, "type": "region"}'
        > print(tags.tag('en-mt-arab').script)
        '{"subtag": "arab", "record": {"Subtag": "Arab", "Added": "2005-10-16", "Type": "script", "Description": ["Arabic"]}, "type": "script"}'
0.1.1
_____

- Added string and Unicode functions to make it easy to print Tags and Subtags.

    .. code-block:: python

        > print(tags.tag('nl-BE'))
        '{"tag": "nl-be"}'

- Added functions to easily select either the language, region or script subtags strings of a Tag.

    .. code-block:: python

        > print(tags.tag('nl-BE').language)
        ['nl']

0.1.0
_____

- Initial version
