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
# project.py : ElJef Backup Project Operations
"""ElJef Backup Project Operations

ElJef Backup Project Operations.
"""

import logging

from typing import Tuple

from eljef.core.dictobj import DictObj

LOGGER = logging.getLogger(__name__)

_EMPTY_PROJECT_MAP = {
    'ops': dict(),
}


class Project:
    """Project holder class

    Args:
        path: full path to backup directory
        project: name of project
        plugins: loaded plugins
        info: project settings
    """

    def __init__(self, path: str, project: str, plugins: DictObj, info: DictObj):
        self.project = project
        self.map = DictObj(_EMPTY_PROJECT_MAP)

        self._setup(path, plugins, info)

    def _setup(self, path: str, plugins: DictObj, info: DictObj) -> None:
        steps = info.get('steps')
        ops = info.get('ops')
        if len(steps) < 1:
            raise SyntaxError("no steps defined for '{0!s}'".format(self.project))

        for pos, op_name in steps.items():
            if op_name not in ops:
                raise SyntaxError("op '{0!s}' defined but not preset in '{1!s}.ops'".format(op_name, self.project))
            operation = ops.get(op_name)
            plugin = operation.get('plugin')
            if not plugin:
                raise SyntaxError("no plugin defined for '{0!s}'".format(op_name))
            if plugin not in plugins:
                raise ValueError("plugin not found: {0!s}".format(plugin))

            self.map.ops[pos] = plugins[plugin]().setup(path, self.project, operation)

    def run(self) -> Tuple[bool, str]:
        """Run operations for this project

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        for pos in sorted(list(self.map.ops.keys())):
            finished, error_msg = self.map.ops[pos].run()
            if not finished:
                return finished, error_msg

        return True, ''


class Projects:
    """Projects holder class

    path: full path to backup directory
    plugins: loaded plugins
    info: projects settings
    """

    def __init__(self, path: str, plugins: DictObj, info: DictObj) -> None:
        self.map = DictObj(dict())

        self._setup(path, plugins, info)

    def _setup(self, path: str, plugins: DictObj, info: DictObj) -> None:
        order = info.get('order')
        projects = info.get('projects')
        if not order or len(order) < 1:
            raise SyntaxError('no steps defined for backup')
        if not projects or len(projects) < 1:
            raise SyntaxError('no projects defined for backup')

        for pos, project_name in order.items():
            if project_name not in projects:
                raise SyntaxError("project name '{0!s} defined in order but not in projects".format(project_name))
            self.map[pos] = Project(path, project_name, plugins, projects[project_name])

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
