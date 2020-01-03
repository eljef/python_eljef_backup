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
# remove.py : ElJef Backup Remove Paths
"""ElJef Backup Remove Paths

Remove paths from the backup
"""

import logging
import os

from typing import Tuple

from eljef.backup.plugins import plugin
from eljef.core import fops

LOGGER = logging.getLogger(__name__)


class RemovePlugin(plugin.Plugin):
    """Remove paths relative to the project folder in the backup folder

    Notes:
        Backup path is structured as:
        /path/to/backup/2020-01-01_01-01-01/project

        Paths should be relative to this path.

    Args:
        path: full path to parent backup directory
        project: name of project
    """

    def __init__(self, path: str, project: str) -> None:
        super().__init__(path, project)
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

        full_path = os.path.join(self.path, self.project)

        for path in self.paths:
            LOGGER.info('removing path from backup: %s', path)
            fops.delete(os.path.join(full_path, path))

        return True, ''


class SetupRemovePlugin(plugin.SetupPlugin):
    """Setup the paths plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'remove'
        self.description = 'remove paths from backup'

    def setup(self, path: str, project: str, info: dict) -> object:
        """Sets up a plugin for operations

        Args:
            path: full path to parent backup directory
            project: name of project this plugin is being setup for
            info: dictionary of information from configuration file, specific to this plugin

        Returns:
            configured local docker plugin object
        """
        remove_object = RemovePlugin(path, project)
        remove_object.paths = info.get('paths')

        if not remove_object.paths or len(remove_object.paths) < 1:
            raise ValueError('paths not set for remove')

        return remove_object
