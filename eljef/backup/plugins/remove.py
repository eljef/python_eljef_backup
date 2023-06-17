# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Remove Paths Plugin"""

import logging
import os

from typing import Tuple

from eljef.backup.plugins import plugin
from eljef.backup.project import Paths
from eljef.core import fops

LOGGER = logging.getLogger(__name__)


class RemovePlugin(plugin.Plugin):
    """Remove paths relative to the project folder in the backup folder

    Notes:
        Backup path is structured as:
        /path/to/backup/2020-01-01_01-01-01/project

        Paths should be relative to this path.

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.remove_paths = []

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        full_path = os.path.join(self.paths.backup_path, self.project)

        for path in self.remove_paths:
            fops.delete(os.path.join(full_path, path))

        return True, ''


class SetupRemovePlugin(plugin.SetupPlugin):
    """Set up the remove plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'remove'
        self.description = 'remove paths from backup'

    def setup(self, paths: Paths, project: str, info: dict) -> object:
        """Sets up a plugin for operations

        Args:
            paths: paths and backup names
            project: name of project this plugin is being setup for
            info: dictionary of information from configuration file, specific to this plugin

        Returns:
            dict: dictionary key: stage_name => object: plugin class to be run
        """
        remove_object = RemovePlugin(paths, project)
        remove_object.remove_paths = info.get('paths')

        if not remove_object.remove_paths or len(remove_object.remove_paths) < 1:
            return self.failure('paths not set for remove')

        return remove_object
