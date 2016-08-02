"""trivial log - write and read functions"""
import struct

def get(fileobj):
    kv = fileobj.read(8)
    keylen = struct.unpack(">L", kv[:4])[0]
    valuelen = struct.unpack(">L", kv[4:8])[0]
    bkey = fileobj.read(keylen)
    bvalue = fileobj.read(valuelen)
    return bkey, bvalue

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
            fileobj.truncate(prevpos)
        raise
