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
# project.py : ElJef Backup Project Operations
"""ElJef Backup Project Operations

ElJef Backup Project Operations.
"""

import logging

from typing import Tuple

from eljef.core.dictobj import DictObj

LOGGER = logging.getLogger(__name__)


class Paths:
    """Paths holder class

    Args:
        backups_path: path to base backups directory
        backup_path: path to the current backup directory
        backup_name: name of this backup iteration
    """
    def __init__(self, backups_path: str, backup_path: str, backup_name: str) -> None:
        self.backups_path = backups_path
        self.backup_path = backup_path
        self.backup_name = backup_name
        self.subdir = ''

    def copy(self) -> "Paths":
        """Returns a copy of the current paths object

        Returns:
            A copy of the Paths object
        """
        ret = Paths(self.backups_path, self.backup_path, self.backup_name)
        ret.subdir = self.subdir

        return ret


class Project:
    """Project holder class

    Args:
        paths: paths and backup name
        project: name of project
        plugins: loaded plug-ins
        info: project settings
    """

    def __init__(self, paths: Paths, project: str, plugins: DictObj, info: DictObj):
        self.project = project
        self.map = DictObj({})

        self._setup(paths, plugins, info)

    def _setup(self, paths: Paths, plugins: DictObj, info: DictObj) -> None:
        for op_name, op_settings in info.items():
            plugin = op_settings.get('plugin')

            if not plugin:
                raise SyntaxError(f"no plugin defined for '{op_name}'")
            if plugin not in plugins:
                raise ValueError(f"plugin not found: {plugin}")

            self.map[op_name] = plugins[plugin]().setup(paths, self.project, op_settings)

    def run(self) -> Tuple[bool, str]:
        """Run operations for this project

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        LOGGER.info("Project: %s", self.project)

        for pos in sorted(list(self.map.keys())):
            finished, error_msg = self.map[pos].run()
            if not finished:
                return finished, error_msg

        return True, ''


class Projects:
    """Projects holder class

    paths: paths and backup name
    plugins: loaded plug-ins
    info: projects settings
    """

    def __init__(self, paths: Paths, plugins: DictObj, info: DictObj) -> None:
        self.map = DictObj({})

        self._setup(paths, plugins, info)

    def _setup(self, paths: Paths, plugins: DictObj, info: DictObj) -> None:
        projects = info.get('projects')
        if not projects:
            raise SyntaxError("no projects defined")

        for project_name, project_settings in projects.items():
            name = project_settings.pop('name', '')
            if not name:
                name = project_name

            subdir = project_settings.pop('backup_dir', '')
            if subdir:
                new_paths = paths.copy()
                new_paths.subdir = subdir
                self.map[project_name] = Project(new_paths, name, plugins, project_settings)
            else:
                self.map[project_name] = Project(paths, name, plugins, project_settings)

    def run(self) -> Tuple[bool, str]:
        """Run all defined projects

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        for pos in sorted(list(self.map.keys())):
            finished, error_msg = self.map[pos].run()
            if not finished:
                return finished, error_msg

        return True, ''
