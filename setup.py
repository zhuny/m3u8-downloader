from setuptools import setup

setup(
    name='m3u8',
    version='0.0.1',
    description='m3u8 downloader',
    url='git@github.com:zhuny/m3u8-downloader',
    author='Jihun Yang',
    author_email='zhuny936772@gmail.com',
    license='unlicense',
    packages=['m3u8'],
    zip_safe=False,
    install_requires=['requests']
)
