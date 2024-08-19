import asyncio
import io

from ._test_async_common import _get_all
from .test_base import FileBasedTests, generate_test_cases


class AsyncReader:
    def __init__(self, data):
        if type(data) == bytes:
            self.data = io.BytesIO(data)
        else:
            self.data = io.StringIO(data)

    async def read(self, n=-1):
        await asyncio.sleep(0)
        return self.data.read(n)

get_all = _get_all(AsyncReader)

# Generating real TestCase classes for each importable backend
generate_test_cases(globals(), 'Async', '_async', FileBasedTests)