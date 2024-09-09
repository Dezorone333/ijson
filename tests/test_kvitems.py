from .test_base import ARRAY_JSON, ARRAY_JSON_PARSE_EVENTS, EMPTY_MEMBER_TEST_CASES, JSON, JSON_KVITEMS, JSON_KVITEMS_META, JSON_OBJECT

import pytest


def test_kvitems(adaptor):
    assert JSON_KVITEMS == adaptor.kvitems(JSON, 'docs.item')


def test_kvitems_toplevel(adaptor):
    kvitems = adaptor.kvitems(JSON, '')
    assert 1 == len(kvitems)
    key, value = kvitems[0]
    assert 'docs' == key
    assert JSON_OBJECT['docs'] == value


def test_kvitems_empty(adaptor):
    assert [] == adaptor.kvitems(JSON, 'docs')


def test_kvitems_twodictlevels(adaptor):
    json = b'{"meta":{"view":{"columns":[{"id": -1}, {"id": -2}]}}}'
    view = adaptor.kvitems(json, 'meta.view')
    assert 1 == len(view)
    key, value = view[0]
    assert 'columns' == key
    assert [{'id': -1}, {'id': -2}] == value


def test_kvitems_different_underlying_types(adaptor):
    assert JSON_KVITEMS_META == adaptor.kvitems(JSON, 'docs.item.meta')


def test_kvitems_array(adaptor):
    assert JSON_KVITEMS == adaptor.kvitems(ARRAY_JSON, 'item.docs.item')


@pytest.mark.parametrize("test_case", [
    pytest.param(value, id=name) for name, value in EMPTY_MEMBER_TEST_CASES.items()
])
def test_kvitems_empty_member(adaptor, test_case):
    assert test_case.kvitems == adaptor.kvitems(test_case.json, test_case.prefix)
