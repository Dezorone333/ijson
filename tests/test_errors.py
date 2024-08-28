import pytest

import ijson

def test_bufsize_nan(backend):
    with pytest.raises(TypeError):
        next(backend.basic_parse(b'', bufsize="not-a-number"))
