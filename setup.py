from setuptools import setup
import iocp

setup(
    name='iocp',
    version=iocp.__version__,
    description='A back door to servers.',
    long_description=iocp.__doc__,
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    url='https://bitbucket.org/tebeka/iocp/src',
    license='MIT License',
    platforms=['any'],
    zip_safe=True,
    py_modules=['iocp']
)
