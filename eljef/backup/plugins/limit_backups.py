# -*- coding: UTF-8 -*-
# pylint: disable=too-few-public-methods
#
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
# limit_backups.py : ElJef Backup Storage Limit
"""ElJef Backup Storage Limit

ElJef Backup Storage Limit Functionality
"""

import logging
import os

from typing import Tuple

from eljef.backup.project import Paths
from eljef.backup.plugins import plugin
from eljef.core import fops

LOGGER = logging.getLogger(__name__)


class LimitPlugin(plugin.Plugin):
    """Limit Backups

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.total = 5

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        if self.total < 1:
            return True, ''

        files = sorted(os.listdir(self.paths.backups_path))
        current_count = len(files)
        while current_count > self.total:
            backup_name = files.pop(0)
            fops.delete(os.path.join(self.paths.backups_path, backup_name))
            current_count -= 1

        return True, ''


class SetupLimitPlugin(plugin.SetupPlugin):
    """Setup Plugin Class that sets up the backups limit plugin class for operations"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'limit_backups'
        self.description = 'limit the number of stored backups'

    @staticmethod
    def setup(paths: Paths, project: str, info: dict) -> object:
        """Sets up a plugin for operations

        Args:
            paths: paths and backup names
            project: name of project this plugin is being setup for
            info: dictionary of information from configuration file, specific to this plugin

        Returns:
            dict: dictionary key: stage_name => object: plugin class to be run
        """

        limit_plugin = LimitPlugin(paths, project)

        backups_total = info.get('total')
        if backups_total:
            if not isinstance(backups_total, int):
                raise ValueError('limit_backups.total must be an integer')
            if backups_total < 1:
                raise ValueError('limit_backups.total must be greater than zero')
            limit_plugin.total = backups_total

        return limit_plugin
