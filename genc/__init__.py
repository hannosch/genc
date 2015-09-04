from genc.regions import (
    Region,
    REGIONS,
)

try:
    basestring
except NameError:  # pragma: no cover
    basestring = str


def _build_cache(name):
    idx = Region._fields.index(name)
    return dict([(reg[idx].upper(), reg) for reg in REGIONS
                 if reg[idx] is not None])

_alpha2 = _build_cache('alpha2')
_alpha3 = _build_cache('alpha3')
_name = _build_cache('name')


def region_by_alpha2(code, default=None):
    if isinstance(code, basestring):
        code = code.upper()
    return _alpha2.get(code, default)


def region_by_alpha3(code, default=None):
    if isinstance(code, basestring):
        code = code.upper()
    return _alpha3.get(code, default)


def region_by_name(name, default=None):
    if isinstance(name, basestring):
        name = name.upper()
    return _name.get(name, default)


__all__ = (
    'region_by_alpha2',
    'region_by_alpha3',
    'region_by_name',
    'REGIONS',
)
