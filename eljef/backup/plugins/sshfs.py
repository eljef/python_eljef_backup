# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""SSHFS Mount Plugin"""

import logging

from typing import Tuple

from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)

MOUNT = 'mount'
"""MOUNT holds the constant for mount"""
UNMOUNT = 'unmount'
"""UNMOUNT holds the constant for unmount"""


class SSHFSPlugin(plugin.Plugin):
    """SSHFS Control Class

    Args:
        paths: paths and backup name
        project: name of project
    """
    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.action = ''
        self.config_file = ''
        self.local_path = ''
        self.mount_options = []
        self.remote_addr = ''
        self.remote_path = ''

    def __mount(self) -> list:
        """Builds the command to mount a path with SSHFS"""
        cmd = ['sshfs']
        if self.mount_options:
            cmd += ['-o', ','.join(self.mount_options)]
        if self.config_file:
            cmd += ['-F', self.config_file]
        cmd += [f"{self.remote_addr}:{self.remote_path}", self.local_path]

        return cmd

    def __unmount(self) -> list:
        """Builds the command to unmount the SSHFS path"""
        return ['unmount', self.local_path]

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        if self.action == MOUNT:
            cmd = self.__mount()
        elif self.action == UNMOUNT:
            cmd = self.__unmount()
        else:
            raise ValueError("action must be one of mount or unmount")

        return self.exec(cmd)


class SetupSSHFSPlugin(plugin.SetupPlugin):
    """Set up the SSHFS plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'sshfs'
        self.description = 'mount or unmount an sshfs filesystem'

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
        sshfs_object = SSHFSPlugin(paths, project)
        sshfs_object.action = info.get('action')
        sshfs_object.config_file = info.get('config_file')
        sshfs_object.local_path = info.get('local_path')
        sshfs_object.mount_options = info.get('mount_options')
        sshfs_object.remote_addr = info.get('remote_addr')
        sshfs_object.remote_path = info.get('remote_path')

        if not sshfs_object.action:
            raise ValueError('action must be one of mount or unmount')
        if not sshfs_object.local_path:
            raise ValueError('local_path is empty')
        if not sshfs_object.remote_addr:
            raise ValueError('remote_addr is empty')
        if not sshfs_object.remote_path:
            raise ValueError('remote_path is empty')
        if sshfs_object.mount_options and not isinstance(sshfs_object.mount_options, list):
            raise TypeError('mount_options not list')

        return sshfs_object
