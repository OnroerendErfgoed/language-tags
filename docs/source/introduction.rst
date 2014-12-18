Introduction
============

This Python API offers a way to validate and lookup languages tags.

Import the module:

.. code-block:: python

    from language_tags import tags

To check whether the language_tag is valid use :py:func:`tags.check`. For example 'nl-Be' is valid but 'nl-BE-BE' is invalid.

.. code-block:: python

    > print(tags.check('nl-BE'))
    True
    > print(tags.check('nl-BE-BE'))
    False

For meaningful error output see ``tags.tag().errors``:

.. code-block:: python

    > errors = tags.tag('nl-BE-BE').errors
    > for err in errors
    >    print(err.message)
    Extra region subtag 'BE' found.

Lookup descriptions of tags:

.. code-block:: python

    > print(tags.description('nl-BE'));
    ['Dutch', 'Flemish', 'Belgium']

Lookup descriptions of a language subtag:

.. code-block:: python

    > print(tags.language('nl').description);
    ['Dutch', 'Flemish']

Lookup tags by description:

.. code-block:: python

    > language_subtags = tags.search('Flemish')
    > print(language_subtags[0])
    'nl'

Get the language subtag of a tag:

.. code-block:: python

    > print(repr(tags.tag('nl-BE').language))
    '{"subtag": "nl", "record": {"Subtag": "nl", "Suppress-Script": "Latn", "Added": "2005-10-16", "Type": "language", "Description": ["Dutch", "Flemish"]}, "type": "language"}'

For the complete api documentation see next chapter.