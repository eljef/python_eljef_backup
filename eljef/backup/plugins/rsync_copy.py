# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""RSYNC Copy Plugin"""

import logging

from typing import Tuple

from eljef.backup.backup import rsync_terminate_path
from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)


class RSYNCCopyPlugin(plugin.Plugin):
    """RSYNC Copy Plugin

    Args:
        paths: paths and backup name
        project: name of project

    Attributes:
        rsync_options: command line flags for the rsync command
        rsync_paths: a list of dictionaries containing paths and excludes

    Notes:
        rsync_paths layout:
            list[dict('from': '/must/be/full/path/',
                      'to': '/must/be/full/path/',
                      'exclude': list['relative/path/to/from', 'other/path']
                      )]
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.rsync_options = ['-a']
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
        for copy_path in self.rsync_paths:
            from_path = rsync_terminate_path(copy_path.get('from'))
            to_path = rsync_terminate_path(copy_path.get('to'))

            cmd = ['rsync'] + self.rsync_options

            excludes = copy_path.get('excludes', [])
            for exclude in excludes:
                cmd += ['--exclude', exclude]

            cmd += [from_path, to_path]

            success, err_msg = self.exec(cmd)
            if not success:
                return success, err_msg

        return True, ''


class SetupRSYNCCopyPlugin(plugin.SetupPlugin):
    """Set up the RSYNC copy plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'rsync_copy'
        self.description = 'copy a path to a new location using rsync'

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
            path = data.get('from')
            if not path:
                return self.failure('each path definition must contain a from')
            path = data.get('to')
            if not path:
                return self.failure('each path definition must contain a to')

        paths_object = RSYNCCopyPlugin(paths, project)
        paths_object.rsync_paths = rsync_paths
        opts = info.get('rsync_options', [])
        if opts:
            paths_object.rsync_options = opts

        return paths_object
