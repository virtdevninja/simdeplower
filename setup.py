#   Copyright 2015 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
from setuptools import setup

import simdeplower

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('test-requirements.txt') as f:
    required_for_tests = f.read().splitlines()

setup(
    name=simdeplower.__appname__,
    version=simdeplower.__version__,
    description=simdeplower.__description__,
    long_description=read('README.rst'),
    packages=['simdeplower'],
    url=simdeplower.__url__,
    install_requires=required,
    license='License :: OSI Approved :: Apache Software License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    platforms=['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'],
    author=simdeplower.__author__,
    author_email=simdeplower.__email__,
    test_suite='tests',
    zip_safe=True,
    tests_require=required_for_tests,
    entry_points={
        "console_scripts": [
            "simdeplow = simdeplower.executable:execute"
        ]
    }
)
