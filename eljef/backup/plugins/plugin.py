# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Base Plugin Functionality"""

import logging
import os
import subprocess

from typing import Callable, Tuple

from eljef.backup.project import Paths

LOGGER = logging.getLogger(__name__)


class Plugin:
    """Base Plugin Class that plugins must inherit

    Args:
        paths: paths and backup name
        project: name of project
    """

    def __init__(self, paths: Paths, project: str) -> None:
        self.gid = 0
        self.uid = 0
        self.run_as = False
        self.paths = paths
        self.project = project

    @staticmethod
    def demote(uid: int, gid: int) -> Callable:
        """Demotes the subprocess to the stored uid and gid

        Returns:
            a callable to demote the run subprocess
        """
        def set_uid_gid():
            os.setgid(gid)
            os.setuid(uid)

        return set_uid_gid

    def exec(self, cmd: list) -> Tuple[bool, str]:
        """Execute a command

        Args:
            cmd: command to execute

        Returns;
            A tuple of True/False if the command executed correctly and an error message if the command failed.
        """
        cmd_msg = ' '.join(cmd)
        LOGGER.debug(cmd_msg)

        try:
            if self.run_as:
                LOGGER.debug("running as: %s - %s", self.uid, self.gid)
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                               preexec_fn=self.demote(self.uid, self.gid))
            else:
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as exception_object:
            if exception_object.stderr:
                LOGGER.error(exception_object.stderr)

            err_msg = f"Failed: {cmd_msg}"
            LOGGER.error(err_msg)

            return False, err_msg

        return True, ''

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
        raise NotImplementedError
