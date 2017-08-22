# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import genc
from genc.regions import Region


def test_api_alpha2():
    assert genc.region_by_alpha2('DE').name == 'Germany'
    assert genc.region_by_alpha2('de').name == 'Germany'
    assert genc.region_by_alpha2('None') is None
    assert genc.region_by_alpha2('None', 1) == 1


def test_api_alpha3():
    assert genc.region_by_alpha3('DEU').name == 'Germany'
    assert genc.region_by_alpha3('dEu').name == 'Germany'
    assert genc.region_by_alpha3('None') is None
    assert genc.region_by_alpha3('None', 1) == 1


def test_api_name():
    assert genc.region_by_name('Germany').alpha2 == 'DE'
    assert genc.region_by_name('germANY').alpha2 == 'DE'
    assert genc.region_by_name('None', 1) == 1


def test_cache_length():
    assert len(genc._alpha2) > 200
    assert len(genc._alpha3) > 200
    assert len(genc._name) > 200
    assert len(genc._alpha3) == len(genc.REGIONS)


def test_data_length():
    assert len(genc.REGIONS) > 200
    assert len(genc.REGIONS) < 500


def test_data_iterable():
    i = 0
    for region in genc.REGIONS:
        i += 1
    assert i == len(genc.REGIONS)


def test_region_new():
    region = Region('ABC', 'AB', '012', 'älpha', 'ÄLPHA', 'älpha')
    assert region.alpha3 == 'ABC'
    assert region.alpha2 == 'AB'
    assert region.numeric == '012'
    assert region.name == 'älpha'
    assert region.uppername == 'ÄLPHA'
    assert region.fullname == 'älpha'
