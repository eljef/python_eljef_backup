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

from typing import Tuple

from eljef.backup import backup
from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)


def _correctly_terminate_path(path: str) -> str:
    """adds a trailing slash to the end of the path

    Args:
        path: path to add trailing slash to

    Returns:
        correctly terminated path
    """
    return path if path[-1] == os.path.sep else path + os.path.sep


def _make_backup_path(path: str, subdir: str) -> str:
    """creates the path to be used in backup operation

    Args:
        path: full path to base directory
        subdir: subdir to create in path

    Returns:
        full path to new directory
    """
    backup_path = backup.create_child_backup_directory(path, subdir)

    return _correctly_terminate_path(backup_path)


class LocalRsyncPlugin(plugin.Plugin):
    """Local RSYNC Plugin Class

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.rsync_paths = list()

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        backup_path = _make_backup_path(self.paths.backup_path,
                                        self.paths.subdir if self.paths.subdir else self.project)

        for copy_path in self.rsync_paths:
            full_backup_path = backup_path
            subdir = copy_path.get('backup_dir')
            if subdir:
                full_backup_path = _make_backup_path(backup_path, subdir)

            path = _correctly_terminate_path(copy_path.get('path'))

            cmd = ['rsync', '-a']

            excludes = copy_path.get('excludes', list())
            for exclude in excludes:
                cmd += ['--exclude', exclude]

            cmd += [path, full_backup_path]

            success, err_msg = self.exec(cmd)
            if not success:
                return success, err_msg

        return True, ''


class SetupLocalRsyncPlugin(plugin.SetupPlugin):
    """Setup the paths plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'local_rsync'
        self.description = 'backup paths locally using rsync'

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
        rsync_paths = info.get('paths')
        if not rsync_paths:
            raise ValueError('paths empty')
        if not isinstance(rsync_paths, list):
            raise TypeError('paths not list')

        for data in rsync_paths:
            path = data.get('path')
            if not path:
                raise SyntaxError('paths must include a path definition')

        paths_object = LocalRsyncPlugin(paths, project)
        paths_object.rsync_paths = rsync_paths

        return paths_object
