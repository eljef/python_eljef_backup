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
# local_rsync.py : ElJef Local RSYNC Backup Functionality
"""ElJef Local RSYNC Backup Functionality

Backup files and folders to the local backup path using rsync.
"""

import logging
import os
import subprocess

from typing import Tuple

from eljef.backup import backup
from eljef.backup.plugins import plugin

LOGGER = logging.getLogger(__name__)


class LocalRsyncPlugin(plugin.Plugin):
    """Local RSYNC Plugin Class

    Args:
        path: full path to parent backup directory
        project: name of project
    """

    def __init__(self, path: str, project: str) -> None:
        super().__init__(path, project)
        self.excludes = list()
        self.paths = list()

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        LOGGER.info("copying paths for %s", self.project)

        backup_path = backup.create_child_backup_directory(self.path, self.project)
        backup_path += os.path.sep if backup_path[-1] != os.path.sep else ''

        for copy_path in self.paths:
            copy_path += os.path.sep if copy_path[-1] != os.path.sep else ''

            cmd = ['rsync', '-a']
            if self.excludes:
                for exclude in self.excludes:
                    cmd += ['--exclude', exclude]
            cmd += [copy_path, backup_path]

            cmd_msg = ' '.join(cmd)
            LOGGER.info(cmd_msg)

            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                error_msg = "Failed: {0!s}".format(cmd_msg)
                LOGGER.error(error_msg)
                return False, error_msg

        return True, ''


class SetupLocalRsyncPlugin(plugin.SetupPlugin):
    """Setup the paths plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'local_rsync'
        self.description = 'backup paths locally using rsync'

    def setup(self, path: str, project: str, info: dict) -> object:
        """Sets up a plugin for operations

        Args:
            path: full path to parent backup directory
            project: name of project this plugin is being setup for
            info: dictionary of information from configuration file, specific to this plugin

        Returns:
            configured local rsync plugin object
        """
        excludes = info.get('excludes')
        if excludes and not isinstance(excludes, list):
            raise TypeError('excludes not list')
        paths = info.get('paths')
        if not paths:
            raise ValueError('paths empty')
        if not isinstance(paths, list):
            raise TypeError('paths not list')

        paths_object = LocalRsyncPlugin(path, project)
        paths_object.excludes = excludes
        paths_object.paths = paths

        return paths_object
