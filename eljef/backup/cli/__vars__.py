# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Backup CLI Variables"""
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
