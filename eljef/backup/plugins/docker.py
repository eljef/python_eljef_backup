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
# docker.py : ElJef Backup Simple Docker Operations
"""ElJef Backup Simple Docker Operations

Simple docker operations to support backups
"""

import logging
import subprocess

from typing import Tuple

from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)


class DockerPlugin(plugin.Plugin):
    """Simple Docker Operations Class

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.action = ''
        self.container = ''

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        log_action = "{0!s}ing".format(self.action) if self.action != 'stop' else 'stopping'
        LOGGER.info("%s docker container %s for project %s", log_action, self.container, self.project)

        cmd = ['docker', self.action, self.container]
        cmd_msg = ' '.join(cmd)

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            error_msg = "Failed: {0!s}".format(cmd_msg)
            LOGGER.error(error_msg)
            return False, error_msg

        return True, ''


class SetupDockerPlugin(plugin.SetupPlugin):
    """Setup the paths plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'docker'
        self.description = 'simple docker operations'

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
        docker_object = DockerPlugin(paths, project)
        docker_object.action = info.get('action')
        docker_object.container = info.get('container')

        if not docker_object.action:
            raise ValueError('docker action not set')
        if docker_object.action not in {'restart', 'start', 'stop'}:
            raise ValueError('docker action not one of restart, start, stop')
        if not docker_object.container:
            raise ValueError('docker container not set')

        return docker_object
