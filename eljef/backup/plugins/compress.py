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
# compress.py : ElJef Backup Compression Plugin
"""ElJef Backup Compression Plugin

ElJef backup compression functionality.
"""

import logging

from typing import Tuple

from eljef.backup.backup import compress_backup_directory
from eljef.backup.project import Paths
from eljef.backup.plugins import plugin
from eljef.core import fops

LOGGER = logging.getLogger(__name__)


class CompressPlugin(plugin.Plugin):
    """Compresses backups

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.do_compress = False

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        if self.do_compress:
            compress_backup_directory(self.paths.backups_path, self.paths.backup_path, self.paths.backup_name)
            fops.delete(self.paths.backup_path)

        return True, ''


class SetupCompressPlugin(plugin.SetupPlugin):
    """Setup Plugin Class that sets up the compression plugin class for operations"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'compress'
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
        compress_plugin = CompressPlugin(paths, project)
        compress_plugin.do_compress = info.get('do_compress', False)

        return compress_plugin
