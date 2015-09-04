# -*- coding: utf-8 -*-
from unittest import TestCase

from genc.regions import (
    Region,
    REGIONS,
)


class TestRegion(TestCase):

    def test_new(self):
        region = Region('ABC', 'AB', '012', 'ÄLPHA', 'älpha', 'älpha')
        self.assertEqual(region.alpha3, 'ABC')
        self.assertEqual(region.alpha2, 'AB')
        self.assertEqual(region.numeric, '012')
        self.assertEqual(region.name, 'ÄLPHA')
        self.assertEqual(region.shortname, 'älpha')
        self.assertEqual(region.fullname, 'älpha')


class TestData(TestCase):

    def test_length(self):
        self.assertTrue(len(REGIONS) > 200)
        self.assertTrue(len(REGIONS) < 500)
