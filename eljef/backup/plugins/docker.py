# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Simple Docker Operations Plugin"""

import logging

from typing import Tuple

from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)

DOCKER = 'docker'
"""Docker is the docker constant"""


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
        return self.exec(['docker', self.action, self.container])


class SetupDockerPlugin(plugin.SetupPlugin):
    """Set up the docker plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = DOCKER
        self.description = f"simple {DOCKER} operations"

    def setup(self, paths: Paths, project: str, info: dict) -> object:
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
            return self.failure('action not set')
        if docker_object.action not in {'restart', 'start', 'stop'}:
            return self.failure('action not one of restart, start, stop')
        if docker_object.action != 'image_prune' and not docker_object.container:
            return self.failure('container not set')

        return docker_object
