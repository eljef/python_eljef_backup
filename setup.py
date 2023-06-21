# -*- coding: UTF-8 -*-
"""Setup script"""

from setuptools import setup

setup(
    author='Jef Oliver',
    author_email='jef@eljef.me',
    description='Backup functionality and program',
    install_requires=['eljef-core>=2022.11.2', 'requests'],
    license='0BSD',
    name='eljef_backup',
    packages=['eljef.backup', 'eljef.backup.cli', 'eljef.backup.notifiers', 'eljef.backup.plugins'],
    python_requires='>=3.8',
    url='https://eljef.dev/python/eljef_backup',
    version='2023.06.1',
    entry_points={
        'console_scripts': [
            'ej-backup = eljef.backup.cli.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
    ]
)
