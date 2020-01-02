# -*- coding: UTF-8 -*-
# Copyright (c) 2020, Jef Oliver
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU Lesser General Public License,
# version 2.1, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
# more details.
#
# Authors:
# Jef Oliver <jef@eljef.me>
#
# __args__.py : ElJef Backup CLI Arguments
"""ElJef Backup CLI Arguments

ElJef CLI Backup command line arguments.
"""

CMD_LINE_ARGS = [
    {
        'short': '-d',
        'long': '--debug',
        'opts': {
            'dest': 'debug_log',
            'action': 'store_true',
            'help': 'Enable debug output.'
        }
    },
    {
        'short': '-f',
        'long': '--file',
        'opts': {
            'dest': 'config_file',
            'metavar': 'config.yaml',
            'help': 'Path to configuration file.'
        }
    },
    {
        'short': '-v',
        'long': '--version',
        'opts': {
            'dest': 'version_out',
            'action': 'store_true',
            'help': 'Print version and exit.'
        }
    }
]
