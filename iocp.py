'''iocp tries to mimic Go's io.Copy function (http://golang.org/pkg/io/#Copy)
which copies from everything that is an io.Reader to anything that is an
io.Writer).

The Python world of things is not that organized, so iocp.copy will try to do a
best guess about which are the right function to call when reading and writing.

For example, checking md5 signature of a file::

    md5 = hashlib.md5()
    with open('/path/to/file') as fo:
        iocp(fo, md5)
    print md5.hexdigest()
'''

__version__ = '0.1.0'

READ_FNS = [
    'read',  # file, StringIO ...
    'recv',  # socket
]

WRITE_FNS = [
    'write',  # file, StringIO, ...
    'send',  # socket
    'update',  # hashlib ...
]

# Default buffer size
BUFSIZE = 32 * 1024


def find_fn(obj, names, name):
    '''Find function in from list of names, raise ValueError not found.'''
    for name in names:
        fn = getattr(obj, name, None)
        if fn:
            return fn

    raise ValueError('cannot find {} function for {}'.format(name, obj))


def copy(src, dest, bufsize=BUFSIZE):
    '''Copy from source to destination, return number of bytes read.

    Since Python's "write" functions don't return number of bytes written, we
    return number of bytes read as best estimation.
    '''
    write = find_fn(dest, WRITE_FNS, 'write')
    read = find_fn(src, READ_FNS, 'read')

    nwritten = 0
    while True:
            try:
                buf = read(bufsize)
            except EOFError:
                buf = ''

            if not buf:
                break

            nwritten += len(buf)
            write(buf)

    return nwritten
