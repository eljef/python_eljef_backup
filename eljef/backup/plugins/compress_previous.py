# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Compress Previous Backups Plugin"""

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
