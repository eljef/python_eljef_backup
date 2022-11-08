# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Backup CLI Arguments"""

from eljef.core import cli

CMD_LINE_ARGS = [
    cli.Arg(['-d', '--debug'],
            {'dest': 'debug_log', 'action': 'store_true', 'help': 'Enable debug output.'}),
    cli.Arg(['-f', '--file'],
            {'dest': 'config_file', 'metavar': 'config.yaml', 'help': 'Path to configuration file.'}),
    cli.Arg(['-v', '--version'],
            {'dest': 'version_out', 'action': 'store_true', 'help': 'Print version and exit.'})
]
