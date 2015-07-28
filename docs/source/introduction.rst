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

A redundant tag is a grandfathered registration whose individual subtags appear with the same semantic meaning in the registry [1]_.
A redundant tag has descriptions and can have a preferred tag.

.. code-block:: python

    > redundant_tag = tags.tag('es-419')
    > print(redundant_tag.descriptions)
    ['Latin American Spanish']
    > print(grandfathered_tag.valid)
    True
    > print(redundant_tag.region.description)
    ['Latin America and the Caribbean']
    > print(redundant_tag.region.language)
    ['Spanish', 'Castilian']

The remainder of the previously registered tags are "grandfathered" [1]_. Grandfathered tags cannot be parsed into subtags.
A grandfathered tag has descriptions. Most grandfathered tags have valid perferred tags.

.. code-block:: python

    > grandfathered_tag = tags.tag('i-klingon')
    > print(grandfathered_tag.descriptions)
    ['Klingon']
    > print(grandfathered_tag.valid)
    False
    > print(grandfathered_tag.subtags)
    []
    > print(grandfathered_tag.preferred)
    tlh
    > preferred_tag = grandfathered_tag.preferred
    > print(preferred_tag.language.description)
    ['Klingon', 'tlhIngan-Hol']

For the complete api documentation see next chapter.

.. [1] `RFC 5646 <https://tools.ietf.org/html/bcp47#section-2.2.8>`_