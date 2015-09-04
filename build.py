"""
Regenerate the `data/regions.json` file from the GENC zipfile.

Invoke as::
    $ make data
"""

import collections
import json
import operator
import os
import shutil
import sys
from xml.etree import ElementTree
import zipfile

XML_FILE = 'data/data.xml'
NS = {
    'genc': 'http://api.nsgreg.nga.mil/schema/genc/3.0',
    'genc-cmn': 'http://api.nsgreg.nga.mil/schema/genc/3.0/genc-cmn',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}

REGIONS_JSON = 'data/regions.json'
REGIONS_PY = 'genc/regions.py'
REGIONS_PY_PREAMBLE = """\
# -*- coding: utf-8 -*-
#
# This file is auto generated.

from collections import namedtuple

Region = namedtuple('Region', 'alpha3 alpha2 numeric name uppername fullname')

REGIONS = [
"""
REGIONS_PY_NAMEMAP = collections.OrderedDict([
    ('char3Code', 'alpha3'),
    ('char2Code', 'alpha2'),
    ('numericCode', 'numeric'),
    ('shortName', 'name'),
    ('name', 'uppername'),
    ('fullName', 'fullname'),
])
REGION_PY_TEMPLATE = """\
    Region(%s, %s, %s,
           %s,
           %s,
           %s),
"""
SUBDIVISIONS_JSON = 'data/subdivisions.json'


def extract_xml(filename):
    if os.path.isfile(XML_FILE):
        return XML_FILE
    with zipfile.ZipFile(filename, 'r') as myzip:
        myzip.extract('GENC Standard Ed3.0.xml', 'data/')
    shutil.move('data/GENC Standard Ed3.0.xml', XML_FILE)
    return XML_FILE


def parse_regions(root):
    regions = []
    for element in root.iterfind('genc:GeopoliticalEntityEntry', NS):
        region = collections.OrderedDict()
        codes = element.find('genc:encoding', NS)
        for name in ('char3Code', 'char2Code', 'numericCode'):
            value = codes.find('genc-cmn:%s' % name, NS)
            if value is not None:
                region[name] = value.text
            else:
                region[name] = None
        for name in ('name', 'shortName', 'fullName'):
            region[name] = element.find('genc:%s' % name, NS).text
        if region['char3Code'].startswith('AX'):
            # filter out internal regions
            continue
        if region['shortName'].startswith('Entity '):
            # filter out more internal regions
            continue
        regions.append(region)
    return regions


def parse_subdivisions(root):
    subdivisions = []
    for element in root.iterfind('genc:AdministrativeSubdivisionEntry', NS):
        subdivision = collections.OrderedDict()
        codes = element.find('genc:encoding', NS)
        subdivision['char6Code'] = codes.find('genc-cmn:char6Code', NS).text
        subdivision['category'] = element.find(
            'genc:subdivisionCategory', NS).text
        subdivision['country'] = element.find('genc:country', NS).text
        names = element.find('genc:name', NS)
        subdivision['name'] = names.find('genc:name', NS).text
        subdivisions.append(subdivision)
    return subdivisions


def parse_xml(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    return (parse_regions(root), parse_subdivisions(root))


def write_data(regions, subdivisions):
    regions = sorted(regions, key=operator.itemgetter('char3Code'))
    subdivisions = sorted(subdivisions, key=operator.itemgetter('char6Code'))
    with open(REGIONS_JSON, 'wt') as fd:
        json.dump(regions, fd, ensure_ascii=False, indent=2)
    with open(SUBDIVISIONS_JSON, 'wt') as fd:
        json.dump(subdivisions, fd, ensure_ascii=False, indent=2)

    with open(REGIONS_PY, 'wt') as fd:
        fd.write(REGIONS_PY_PREAMBLE)
        for region in regions:
            data = []
            for in_ in REGIONS_PY_NAMEMAP.keys():
                value = region[in_]
                if value is None:
                    data.append("None")
                else:
                    data.append("'%s'" % value)
            fd.write(REGION_PY_TEMPLATE % tuple(data))
        fd.write(']\n')


def main(filename):
    regions, subdivisions = parse_xml(extract_xml(filename))
    write_data(regions, subdivisions)


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        raise ValueError('Required data file argument missing')
    filename = argv[-1].strip()
    main(filename)
