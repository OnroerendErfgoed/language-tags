        0.1.1
        _____

        - Added string and Unicode functions to make it easy to print Tags and Subtags.

            .. code-block:: python

                > print(tags.tag('nl-BE'))
                {"tag": "nl-be"}

        - Added functions to easily select either the language, region or script subtags strings of a Tag.

            .. code-block:: python

                > tags.tag('nl-BE').language
                ['nl']

0.1.0
_____

- Initial version
