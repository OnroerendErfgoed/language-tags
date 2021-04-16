Changelog
=========

1.1.0
-----

- Update data to version 2020-09-29 (#62)
- Update dependencies and Python (Removed Python 3.5 support, now supports 3.6 to 3.9) (#74, #77)
- Drop pyup support (#80)
- Fix pypi description (#78)
- Include MIT License in package (#67)
- Fix deprecation warnings (#84)

1.0.0
-----

- Drop support for Python 2

0.5.0
-----

- Updated dependencies and Python (Removed Python3.3 and Python3.4 support, added 3.6 and 3.7)

0.4.6
-----

- Avoid modifying tag when getting description

0.4.5
-----

- Close files after opening #38

0.4.4
-----

- Bug fix release: language tag 'aa' is detected as invalid #27

0.4.3
-----

- Upgrade to <https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.18>

0.4.2
-----

- Official python 3.5 compatibility
- Upgrade to <https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.15>

0.4.1
-----

- Included the data folder again in the project package.
- Added bash script (`update_data_files.sh`) to download the
  `language-subtag-registry <https://github.com/mattcg/language-subtag-registry/>`_
  and move this data in the data folder of the project.

0.4.0
-----

- Allow parsing a redundant tag into subtags.
- Added package.json file for easy update of the language subtag registry data using `npm <https://docs.npmjs.com/>`_
  (:code:`npm install` or :code:`npm update`)
- Improvement of the :code:`language-tags.tags.search` function: rank equal description at top.
  See `mattcg/language-tags#4 <https://github.com/mattcg/language-tags/issues/4>`_

0.3.2
-----

- Upgrade to <https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.11>
- Added wheel config
- Fixed bug under windows: opening data files using utf-8 encoding.

0.3.1
-----

- Upgrade to <https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.8>

0.3.0
-----

- Upgrade to <https://github.com/mattcg/language-subtag-registry/releases/tag/v0.3.6>
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
-----

- Adjust language, region and script properties of Tag. The properties will return `language_tags.Subtag.Subtag`
  instead of a list of string subtags

    .. code-block:: python

        > print(tags.tag('nl-BE').language)
        '{"subtag": "nl", "record": {"Subtag": "nl", "Suppress-Script": "Latn", "Added": "2005-10-16", "Type": "language", "Description": ["Dutch", "Flemish"]}, "type": "language"}'
        > print(tags.tag('nl-BE').region)
        '{"subtag": "be", "record": {"Subtag": "BE", "Added": "2005-10-16", "Type": "region", "Description": ["Belgium"]}, "type": "region"}'
        > print(tags.tag('en-mt-arab').script)
        '{"subtag": "arab", "record": {"Subtag": "Arab", "Added": "2005-10-16", "Type": "script", "Description": ["Arabic"]}, "type": "script"}'

0.1.1
-----

- Added string and Unicode functions to make it easy to print Tags and Subtags.

    .. code-block:: python

        > print(tags.tag('nl-BE'))
        '{"tag": "nl-be"}'

- Added functions to easily select either the language, region or script subtags strings of a Tag.

    .. code-block:: python

        > print(tags.tag('nl-BE').language)
        ['nl']

0.1.0
-----

- Initial version
