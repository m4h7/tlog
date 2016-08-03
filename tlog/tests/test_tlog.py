from unittest import TestCase
import io

import tlog

class mockFile:
    def __init__(self):
        self.pos = 0
        self.fail_in = None
        self.f = io.BytesIO()
    def write(self, buf):
        if self.fail_in is not None:
            self.fail_in -= 1
            if self.fail_in == 0:
                raise IOError("mock .write failed");
        self.f.write(buf)
    def read(self, size):
        if self.fail_in is not None:
            self.fail_in -= 1
            if self.fail_in == 0:
                raise IOError("mock .read failed");
        return self.f.read(size)
    def tell(self):
        return self.f.tell()
    def seek(self, pos):
        assert pos is not None
        self.f.seek(pos)
    def truncate(self, new_pos = None):
        return self.f.truncate(new_pos)
    def fail_n(self, n):
        self.fail_in = n

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

    def test_ioerror(self):
        f = mockFile()
        tlog.put(f, b'1', b'2')
        prevpos = f.tell()
        # make next put fail (second write() should fail)
        f.fail_n(2)
        exception_seen = False
        try:
            tlog.put(f, b'3', b'4')
        except IOError:
            exception_seen = True
        self.assertTrue(exception_seen)
        # file position should not be affected by the exception
        # (no partial writes)
        self.assertEqual(f.tell(), prevpos)

    def test_read_ioerror(self):
        f = mockFile()
        tlog.put(f, b'1', b'2')
        tlog.put(f, b'3', b'4')
        f.seek(0)
        _, _ = tlog.get(f)

        prevpos = f.tell()
        # make next .get() fail (second read() should fail)
        f.fail_n(2)
        exception_seen = False
        try:
            _, _ = tlog.get(f)
        except IOError:
            exception_seen = True
        self.assertTrue(exception_seen)
        # file position should not be affected by the exception
        # (no partial writes)
        print (f.tell(), prevpos)
        self.assertEqual(f.tell(), prevpos)

