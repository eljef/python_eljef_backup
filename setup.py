# -*- coding: UTF-8 -*-
"""Setup script"""

from setuptools import setup

setup(
    author='Jef Oliver',
    author_email='jef@eljef.me',
    description='Backup functionality and program',
    install_requires=['eljef_core>=1.2.2'],
    license='LGPLv2.1',
    name='eljef_backup',
    packages=['eljef.backup', 'eljef.backup.cli', 'eljef.backup.plugins'],
    python_requires='>=3.7',
    url='https://github.com/eljef/python_eljef_backup',
    version='0.2.0',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'eljef-backup = eljef.backup.cli.__main__:main'
        ]
    },
)
