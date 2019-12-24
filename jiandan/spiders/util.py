import hashlib
import base64

def parse(imgHash, constant):
    q = 4
    hashlib.md5()
    constant = md5(constant)
    o = md5(constant[0:16])
    n = md5(constant[16:32])
    l = imgHash[0:q]
    c = o + md5(o + l)
    imgHash = imgHash[q:]
    k = decode_base64(imgHash)
    h = list(range(256))

    b = list(range(256))

    for g in range(0, 256):
        b[g] = ord(c[g % len(c)])

    f = 0
    for g in range(0, 256):
        f = (f + h[g] + b[g]) % 256
        tmp = h[g]
        h[g] = h[f]
        h[f] = tmp

    result = ""
    p = 0
    f = 0
    for g in range(0, len(k)):
        p = (p + 1) % 256;
        f = (f + h[p]) % 256
        tmp = h[p]
        h[p] = h[f]
        h[f] = tmp
        result += chr(k[g] ^ (h[(h[p] + h[f]) % 256]))
    result = result[26:]

    return result


def md5(src):
    m = hashlib.md5()
    m.update(src.encode("utf8"))
    return m.hexdigest()


def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.b64decode(data)