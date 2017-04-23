import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = []
with open(os.path.join(here, 'requirements.txt')) as f:
    for line in f.read().splitlines():
        if line.find('--extra-index-url') == -1:
            requires.append(line)


setup(
    name='wunderclient',
    packages=['wunderclient'],
    version='0.0.2',
    description='A Wunderlist API client',
    author='Kevin LaFlamme',
    author_email='k@lamfl.am',
    url='https://github.com/lamflam/wunderclient',
    download_url='https://github.com/lamflam/wunderclient/archive/0.0.2.tar.gz',
    keywords=['wunderlist'],
    install_requires=requires
)
