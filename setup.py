# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import setuptools
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')
TESTS_REQUIRE = []

def get_version():
    init = open(
        os.path.join(
            HERE,
            "metabadger",
            "bin",
            'version.py'
        )
    ).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


setuptools.setup(
    name="metabadger",
    include_package_data=True,
    version=get_version(),
    author="Ashish Patel",
    author_email="ashishrpatel.io@gmail.com",
    description="AWS Security Tool that gives you the ability to analyze and harden the Instance Metadata Service. ",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/salesforce/metabadger",
    packages=setuptools.find_packages(exclude=['test*', 'tmp*']),
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'boto3',
        'botocore',
        'click',
        'click_option_group',
        'tabulate',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": "metabadger=metabadger.bin.cli:main"},
    zip_safe=True,
    keywords='aws iam roles policy policies privileges security',
    python_requires='>=3.6',
    # scripts=['cloudsplaining/bin/cloudsplaining'],
)