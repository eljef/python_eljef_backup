# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Simple Docker Compose Operations"""

import logging
import os

from typing import Tuple

from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)

PLUGIN_NAME = 'docker_compose'
"""PLUGIN_NAME holds the plugin name"""


class DockerComposePlugin(plugin.Plugin):
    """Docker Compose Operations Class

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        super().__init__(paths, project)
        self.action = ''
        self.docker_file = ''
        self.stack_name = ''

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        cmd = ['docker-compose', '-f', self.docker_file, self.action]
        if self.action == 'up':
            cmd += ['-d']

        return self.exec(cmd)


class SetupDockerComposePlugin(plugin.SetupPlugin):
    """Set up the docker compose plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = PLUGIN_NAME
        self.description = 'docker compose operations'
        self.__ops = {'down', 'up'}

    def __validate_action(self, action: str) -> Tuple[str, str]:
        """Checks if the specified action is supported by docker-compose.

        Args:
            action: specified action to run with docker-compose

        Returns:
            A tuple of strings.
            Tuple[0] = action
            Tuple[1] = error message if an error is encountered
        """
        if not action:
            return '', 'no action set'

        if action not in self.__ops:
            return '', 'action must be one of down or up'

        return action, ''

    @staticmethod
    def __validate_docker_compose_path(docker_file) -> Tuple[str, str]:
        """Checks if the specified docker-file exists and is a file.

        Args:
            docker_file: docker-compose.yml to validate

        Returns:
            A tuple of strings.
            Tuple[0] = docker-compose.yml path
            Tuple[1] = error message if an error is encountered
        """
        if not docker_file:
            return '', 'no docker-compose file set'

        if not os.path.exists(docker_file):
            return '', 'docker-compose file not found'

        if not os.path.isfile(docker_file) or \
                (os.path.islink(docker_file) and not os.path.isfile(os.readlink(docker_file))):
            return '', 'specified docker-compose file is not a file'

        return docker_file, ''

    def setup(self, paths: Paths, project: str, info: dict) -> object:
        """Sets up a plugin for operations

        Args:
            paths: paths and backup names
            project: name of project this plugin is being setup for
            info: dictionary of information from configuration file, specific to this plugin

        Returns:
            dict: dictionary key: stage_name => object: plugin class to be run
        """
        action, msg = self.__validate_action(info.get('action'))
        if msg:
            return self.failure(msg)

        docker_file, msg = self.__validate_docker_compose_path(info.get('path'))
        if msg:
            return self.failure(msg)

        uid = 0
        gid = 0
        run_as = False
        run_as_info = info.get('run_as')
        if run_as_info:
            run_as = True
            uid = run_as_info.get('uid')
            gid = run_as_info.get('gid')
            for test_id in (uid, gid):
                if not isinstance(test_id, int):
                    return self.failure('run_as.uid/run_as.gid must be integers')

        docker_compose_object = DockerComposePlugin(paths, project)
        docker_compose_object.action = action
        docker_compose_object.docker_file = docker_file
        docker_compose_object.stack_name = info.get('stack_name')
        docker_compose_object.run_as = run_as
        docker_compose_object.uid = uid
        docker_compose_object.gid = gid

        return docker_compose_object
