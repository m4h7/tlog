"""trivial log - write and read functions"""
import struct

def get(fileobj):
    prevpos = fileobj.tell()
    kv = fileobj.read(8)
    keylen = struct.unpack(">L", kv[:4])[0]
    valuelen = struct.unpack(">L", kv[4:8])[0]
    try:
        bkey = fileobj.read(keylen)
        bvalue = fileobj.read(valuelen)
        return bkey, bvalue
    except IOError:
        fileobj.seek(prevpos)
        raise

def put(fileobj, bkey, bvalue):
    """write key (bytes) and value (bytes) to file object"""
    # little endian unsigned long
    keylen = struct.pack(">L", len(bkey))
    assert len(keylen) == 4
    valuelen = struct.pack(">L", len(bvalue))
    assert len(valuelen) == 4

    prevpos = fileobj.tell()
    try:
        fileobj.write(keylen)
        fileobj.write(valuelen)
        fileobj.write(bkey)
        fileobj.write(bvalue)
    except IOError:
        # restore previous position should one of the writes fail
        if fileobj.tell() != prevpos:
            fileobj.seek(prevpos)
            fileobj.truncate()
        raise
