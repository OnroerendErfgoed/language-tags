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

    > tags.description('nl-BE');
    [u'Dutch', u'Flemish', u'Belgium']

Lookup descriptions of a language subtag:

.. code-block:: python

    > tags.language('nl').description;
    [u'Dutch', u'Flemish']


Lookup tags by description:

.. code-block:: python

    > language_subtags = tags.search('Flemish')
    > print language_subtags[0].format
    nl

For the complete api documentation see next chapter.