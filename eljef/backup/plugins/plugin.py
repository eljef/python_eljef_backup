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
# plugin.py : ElJef Backup Plugins Functionality
"""ElJef Backup Plugins Functionality

ElJef backup backup functionality.
"""

from typing import Tuple


class Plugin:
    """Base Plugin Class that plugins must inherit

    Args:
        path: full path to parent backup directory
        project: name of project
    """

    def __init__(self, path: str, project: str) -> None:
        self.path = path
        self.project = project

    def run(self) -> Tuple[bool, str]:
        """Run operations for this plugin

        Notes:
            If the plugin is saving files, it must save them in a subdirectory
            of the parent backup directory.

        Returns:
            bool: operations completed successfully
            str: if operations failed, the error message explaining what failed
        """
        raise NotImplementedError


class SetupPlugin:
    """Base Setup Plugin Class that sets up the plugin class for operations"""

    def __init__(self) -> None:
        self.name = 'NOTIMPLEMENTED'
        self.description = 'NOTIMPLEMENTED'

    def setup(self, path: str, project: str, info: dict) -> object:
        """Sets up a plugin for operations

        Args:
            path: full path to parent backup directory
            project: name of project this plugin is being setup for
            info: dictionary of information from configuration file, specific to this plugin

        Returns:
            dict: dictionary key: stage_name => object: plugin class to be run
        """
        raise NotImplementedError
