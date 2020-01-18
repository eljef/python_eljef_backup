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
# compress_previous.py : ElJef Backup Compress Previous Backups Plugin
"""ElJef Backup Compress Previous Backups Plugin

Functionality to compress previously run backups.
"""

import logging
import os

from typing import Tuple

from eljef.backup.backup import compress_backup_directory
from eljef.backup.project import Paths
from eljef.backup.plugins import plugin
from eljef.core import fops

LOGGER = logging.getLogger(__name__)


class CompressPreviousPlugin(plugin.Plugin):
    """Compresses Previous backups"""

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        backups = os.listdir(self.paths.backups_path)
        for name in backups:
            full_path = os.path.join(self.paths.backups_path, name)
            if os.path.isdir(full_path):
                compress_backup_directory(self.paths.backups_path, full_path, name)
                fops.delete(full_path)

        return True, ''


class SetupCompressPreviousPlugin(plugin.SetupPlugin):
    """Setup Plugin Class that sets up the compression plugin class for operations"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'compress_previous'
        self.description = 'compresses backups'

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
        compress_previous_plugin = CompressPreviousPlugin(paths, project)

        return compress_previous_plugin
