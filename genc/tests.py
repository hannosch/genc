# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

import genc
from genc.regions import Region


class TestAPI(TestCase):

    def test_alpha2(self):
        self.assertEqual(genc.region_by_alpha2('DE').name, 'Germany')
        self.assertEqual(genc.region_by_alpha2('de').name, 'Germany')
        self.assertEqual(genc.region_by_alpha2('None'), None)
        self.assertEqual(genc.region_by_alpha2('None', 1), 1)

    def test_alpha3(self):
        self.assertEqual(genc.region_by_alpha3('DEU').name, 'Germany')
        self.assertEqual(genc.region_by_alpha3('dEu').name, 'Germany')
        self.assertEqual(genc.region_by_alpha3('None'), None)
        self.assertEqual(genc.region_by_alpha3('None', 1), 1)

    def test_name(self):
        self.assertEqual(genc.region_by_name('Germany').alpha2, 'DE')
        self.assertEqual(genc.region_by_name('germANY').alpha2, 'DE')
        self.assertEqual(genc.region_by_name('None', 1), 1)


class TestCache(TestCase):

    def test_length(self):
        self.assertTrue(len(genc._alpha2) > 200)
        self.assertTrue(len(genc._alpha3) > 200)
        self.assertTrue(len(genc._name) > 200)
        self.assertEqual(len(genc._alpha3), len(genc.REGIONS))


class TestData(TestCase):

    def test_length(self):
        self.assertTrue(len(genc.REGIONS) > 200)
        self.assertTrue(len(genc.REGIONS) < 500)

    def test_iterable(self):
        i = 0
        for region in genc.REGIONS:
            i += 1
        self.assertEqual(i, len(genc.REGIONS))


class TestRegion(TestCase):

    def test_new(self):
        region = Region('ABC', 'AB', '012', 'älpha', 'ÄLPHA', 'älpha')
        self.assertEqual(region.alpha3, 'ABC')
        self.assertEqual(region.alpha2, 'AB')
        self.assertEqual(region.numeric, '012')
        self.assertEqual(region.name, 'älpha')
        self.assertEqual(region.uppername, 'ÄLPHA')
        self.assertEqual(region.fullname, 'älpha')
