from unittest import TestCase
import io

import tlog

class TestTlog(TestCase):
    def test_single_put_get(self):
        keywritten = b'key'
        valuewritten = b'value'
        f = io.BytesIO()
        tlog.put(f, keywritten, valuewritten)
        f.seek(0)
        keyread, valueread = tlog.get(f)
        self.assertTrue(keyread == keywritten)
        self.assertTrue(valueread == valuewritten)

    def test_multi_put_get(self):
        f = io.BytesIO()
        for n in range(1000):
            key = str(n)
            value = str(n + 1)
            tlog.put(f, key.encode('ascii'), value.encode('ascii'))
        f.seek(0)
        for n in range(1000):
            key, value = tlog.get(f)
            self.assertTrue(int(key.decode('ascii')) == n)
            self.assertTrue(int(value.decode('ascii')) == n + 1)
