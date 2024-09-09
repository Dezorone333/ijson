import enum

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


class InputType(enum.Enum):
    ASYNC_FILE = enum.auto()
    ASYNC_TYPES_COROUTINES_FILE = enum.auto()
    FILE = enum.auto()
    SENDABLE = enum.auto()


class BackendAdaptor:
    """
    Ties a backend together with an input type to provide easy access to
    calling the backend's methods and retrieving all results in a single call.
    """
    def __init__(self, backend, input_type, suffix, get_all):
        self.backend = backend
        self._input_type = input_type
        self._suffix = suffix
        self._get_all = get_all

    @property
    def pytest_parameter_id(self):
        return f"{self.backend.backend_name}-{self._input_type.name.lower()}"

    def __getattr__(self, name):
        routine = getattr(self.backend, name + self._suffix)
        def get_all_for_name(*args, **kwargs):
            return self._get_all(routine, *args, **kwargs)
        return get_all_for_name


from .test_async import get_all as get_all_async
from .test_async_types_coroutines import get_all as get_all_async_types_coroutines
from .test_coroutines import get_all as get_all_coro
from .test_generators import get_all as get_all_gen

_all_backend_adaptors = [
    backend_adaptor
    for backend in _available_backends
    for backend_adaptor in [
        BackendAdaptor(backend, InputType.ASYNC_FILE, "_async", get_all_async),
        BackendAdaptor(backend, InputType.ASYNC_TYPES_COROUTINES_FILE, "_async", get_all_async_types_coroutines),
        BackendAdaptor(backend, InputType.SENDABLE, "_coro", get_all_coro),
        BackendAdaptor(backend, InputType.FILE, "_gen", get_all_gen),
    ]
]

BACKEND_PARAM_NAME = "backend"
ADAPTOR_PARAM_NAME = "adaptor"

def pytest_generate_tests(metafunc):
    requires_backend = BACKEND_PARAM_NAME in metafunc.fixturenames
    requires_adaptor = ADAPTOR_PARAM_NAME in metafunc.fixturenames
    assert not (requires_backend and requires_adaptor)

    names = []

    # if both are required we need to match backend and adaptors correctly
    if requires_backend:
        names = BACKEND_PARAM_NAME
        values = _available_backends
        ids = [backend.backend_name for backend in _available_backends]
    elif requires_adaptor:
        names = ADAPTOR_PARAM_NAME
        values = _all_backend_adaptors
        ids = [adaptor.pytest_parameter_id for adaptor in _all_backend_adaptors]

    if names:
        metafunc.parametrize(names, values, ids=ids)
