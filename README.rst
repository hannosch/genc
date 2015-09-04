====
Genc
====

``Genc`` provides the information in the Geopolitical Entities, Names
and Codes (GENC) standard as a Python distribution.

Installation
============

::

  $ pip install genc


Usage
=====

::

    >>> import genc
    >>> genc.region_by_alpha3('DEU')
    Region(alpha3='DEU', alpha2='DE', numeric='276', name='Germany',
           uppername='GERMANY', fullname='Federal Republic of Germany')

    >>> genc.region_by_alpha2('DE').name
    'Germany'

    >>> genc.region_by_name('germany').alpha2
    'DE'

    >>> genc.region_by_name('unknown region') is None
    True

    >>> for region in genc.REGIONS:
    ...     # do something
    ...     pass


License
=======

``genc`` is offered under the Apache License 2.0.
