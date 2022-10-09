# -*- coding: UTF-8 -*-
# pylint: disable=too-few-public-methods
#
# Copyright (c) 2020-2022, Jef Oliver
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
# docker_compose.py : ElJef Backup Simple Docker Compose Operations
"""ElJef Backup Simple Docker Compose Operations

Simple docker operations to support backups
"""

import logging
import os

from typing import Tuple

from eljef.backup.plugins import plugin
from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)


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
        cmd = ['docker-compose', '-f', self.docker_file]

        if self.stack_name:
            cmd += ['-p', self.stack_name]

        cmd += [self.action]
        if self.action == 'up':
            cmd += ['-d']

        return self.exec(cmd)


class SetupDockerComposePlugin(plugin.SetupPlugin):
    """Set up the docker compose plugin"""

    def __init__(self) -> None:
        super().__init__()
        self.name = 'docker_compose'
        self.description = 'docker compose operations'

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
        ops = {'down', 'up'}

        action = info.get('action')
        if not action:
            raise SyntaxError('no action set for docker_compose plugin')
        if action not in ops:
            raise SyntaxError('docker_compose plugin actions must be one of down or up')

        docker_file = info.get('path')
        if not docker_file:
            raise SyntaxError('no file set for docker_compose plugin')
        if not os.path.exists(docker_file):
            raise FileNotFoundError('docker file not found')
        if not os.path.isfile(docker_file):
            raise IOError('docker file not a file')

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
                    raise ValueError('run_as.uid/run_as.gid must be integers')

        docker_compose_object = DockerComposePlugin(paths, project)
        docker_compose_object.action = action
        docker_compose_object.docker_file = docker_file
        docker_compose_object.stack_name = info.get('stack_name')
        docker_compose_object.run_as = run_as
        docker_compose_object.uid = uid
        docker_compose_object.gid = gid

        return docker_compose_object
