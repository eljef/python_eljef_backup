# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Local RSYNC Plugin"""

import logging

from typing import Tuple

from eljef.backup.backup import (create_child_backup_directory, rsync_terminate_path)
from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)


def _make_backup_path(path: str, subdir: str) -> str:
    """creates the path to be used in backup operation

    Args:
        path: full path to base directory
        subdir: subdir to create in path

    Returns:
        full path to new directory
    """
    backup_path = create_child_backup_directory(path, subdir)

    return rsync_terminate_path(backup_path)


class LocalRsyncPlugin(plugin.Plugin):
    """Local RSYNC Plugin Class

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.rsync_paths = []

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        backup_subdir = self.paths.subdir if self.paths.subdir else self.project
        try:
            backup_path = _make_backup_path(self.paths.backup_path, backup_subdir)
        except Exception as exception_object:  # pylint: disable=broad-exception-caught
            return False, f"create backup path: {backup_subdir}: {exception_object}"

        for copy_path in self.rsync_paths:
            full_backup_path = backup_path
            subdir = copy_path.get('backup_dir')
            if subdir:
                try:
                    full_backup_path = _make_backup_path(backup_path, subdir)
                except Exception as exception_object:  # pylint: disable=broad-exception-caught
                    return False, f"create backup path: {subdir}: {exception_object}"

            path = rsync_terminate_path(copy_path.get('path'))

            cmd = ['rsync', '-a']

            excludes = copy_path.get('excludes', [])
            for exclude in excludes:
                cmd += ['--exclude', exclude]

            cmd += [path, full_backup_path]

            success, err_msg = self.exec(cmd)
            if not success:
                return success, err_msg

        return True, ''


class SetupLocalRsyncPlugin(plugin.SetupPlugin):
    """Set up the local rsync plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'local_rsync'
        self.description = 'backup paths locally using rsync'

    def setup(self, paths: Paths, project: str, info: dict) -> object:
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
            return self.failure('paths empty')
        if not isinstance(rsync_paths, list):
            return self.failure('paths not list')

        for data in rsync_paths:
            path = data.get('path')
            if not path:
                return self.failure('paths must include a path definition')

        paths_object = LocalRsyncPlugin(paths, project)
        paths_object.rsync_paths = rsync_paths

        return paths_object
