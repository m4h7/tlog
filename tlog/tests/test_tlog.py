from unittest import TestCase
import io

import tlog

class TestTlog(TestCase):
    def test_put_get(self):
        keywritten = b'key'
        valuewritten = b'value'
        f = io.BytesIO()
        tlog.put(f, keywritten, valuewritten)
        f.seek(0)
        keyread, valueread = tlog.get(f)
        self.assertTrue(keyread == keywritten)
        self.assertTrue(valueread == valuewritten)

