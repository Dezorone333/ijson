import ijson

import pytest


def _get_available_backends():
    backends = []
    for backend in ijson.ALL_BACKENDS:
        try:
            backends.append(ijson.get_backend(backend))
        except ImportError:
            pass
    return backends


_available_backends = _get_available_backends()


def pytest_generate_tests(metafunc):
    if "backend" in metafunc.fixturenames:
        metafunc.parametrize("backend", _available_backends)
