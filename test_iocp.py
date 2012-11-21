from os import urandom, SEEK_SET
from tempfile import NamedTemporaryFile
import hashlib
from threading import Thread
import socket

import iocp


def new_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def socket_server():
    sock = new_socket()
    sock.bind(('localhost', 0))  # 0 will assign a random free port
    port = sock.getsockname()[1]

    def serve():
        sock.listen(1)
        while True:
            conn, addr = sock.accept()
            conn.send(data)
            conn.close()

    thr = Thread(target=serve)
    thr.daemon = True
    thr.start()

    return port


data_size = iocp.BUFSIZE * 3 + 17
data = urandom(data_size)
port = socket_server()


def src_file():
    src = NamedTemporaryFile()
    src.write(data)
    src.flush()
    src.seek(0, SEEK_SET)

    return src


def src_socket():
    sock = new_socket()
    sock.connect(('localhost', port))

    return sock


def read_file(fo):
    fo.seek(0, SEEK_SET)
    return fo.read()


def check_copy(src, dest, expected, readfn):
    iocp.copy(src, dest)
    expected = expected or data
    received = readfn() if readfn else read_file(dest)
    assert received == expected, 'bad copy {} -> {}'.format(src, dest)


def test_copy():
    hasher = hashlib.md5()
    digest = hashlib.md5(data).hexdigest()

    test_cases = [
        (src_file(), NamedTemporaryFile(), None, None),
        (src_file(), hasher, digest, lambda: hasher.hexdigest()),
        (src_socket(), NamedTemporaryFile(), None, None),
    ]

    for src, dest, expected, readfn in test_cases:
        yield check_copy, src, dest, expected, readfn
