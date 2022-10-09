# -*- coding: UTF-8 -*-
"""Setup script"""

from setuptools import setup

setup(
    author='Jef Oliver',
    author_email='jef@eljef.me',
    description='Backup functionality and program',
    install_requires=['eljef_core>=2022.2.1'],
    license='LGPLv2.1',
    name='eljef_backup',
    packages=['eljef.backup', 'eljef.backup.cli', 'eljef.backup.plugins'],
    python_requires='>=3.8',
    url='https://github.com/eljef/python_eljef_backup',
    version='2022.10.1',
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
