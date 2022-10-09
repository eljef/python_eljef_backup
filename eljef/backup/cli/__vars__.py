# -*- coding: UTF-8 -*-
# Copyright (c) 2020-2022, Jef Oliver
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
# __vars__.py : Variables used by ElJef Backup CLI
"""ElJef Backup CLI Variables

Variables used by ElJef Backup CLI.
"""
import logging

from eljef.backup.__version__ import VERSION

LOGGER = logging.getLogger(__name__)


PROJECT_DESCRIPTION = 'ElJef Backup Functionality'
PROJECT_NAME = 'eljef_backup'
PROJECT_VERSION = VERSION

DEFAULTS = {
    'backup': {
        'clean_on_failure': True,
        'skip_backup_directory': False,
        'path': '',
        'projects_folder': '',
        'projects': {}
    }
}
