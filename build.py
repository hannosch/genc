"""
Regenerate the `data/regions.json` file from the GENC zipfile.

Invoke as::
    $ bin/python build.py "data/GENC Standard Index XML Ed3.0.zip"
"""

import collections
import json
import operator
import os
import shutil
import sys
from xml.etree import ElementTree
import zipfile

JSON_FILE = 'data/regions.json'
PY_FILE = 'genc/regions.py'
XML_FILE = 'data/data.xml'
NS = {
    'genc': 'http://api.nsgreg.nga.mil/schema/genc/3.0',
    'genc-cmn': 'http://api.nsgreg.nga.mil/schema/genc/3.0/genc-cmn',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}


def extract_xml(filename):
    if os.path.isfile(XML_FILE):
        return XML_FILE
    with zipfile.ZipFile(filename, 'r') as myzip:
        myzip.extract('GENC Standard Index Ed3.0.xml', 'data/')
    shutil.move('data/GENC Standard Index Ed3.0.xml', XML_FILE)
    return XML_FILE


def parse_xml(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()
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
        regions.append(region)
    return regions


def write_data(regions):
    regions = sorted(regions, key=operator.itemgetter('char3Code'))
    with open(JSON_FILE, 'wt') as fd:
        json.dump(regions, fd, ensure_ascii=False, indent=2)
    return
    # TODO Write a file with Python friendly names and using named
    # tuples instead
    with open(PY_FILE, 'wt') as fd:
        fd.write('# -*- coding: utf-8 -*-\n#\n')
        fd.write('# This file is auto generated.\n\n')
        fd.write('REGIONS = ')
        fd.write(json.dumps(regions, ensure_ascii=False, indent=4))
        fd.write('\n')


def main(filename):
    write_data(parse_xml(extract_xml(filename)))


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        raise ValueError('Required data file argument missing')
    filename = argv[-1].strip()
    main(filename)
