# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Backup Functionality"""

import datetime
import inspect
import glob
import logging
import os
import pkgutil
import tarfile

from typing import Union

from eljef.backup.notifiers.holder import Holder
from eljef.backup.plugins.plugin import SetupPlugin
from eljef.backup.project import (Paths, Projects)
from eljef.core import fops
from eljef.core.dictobj import DictObj
from eljef.core.merge import merge_dictionaries
from eljef.core.settings import Settings

LOGGER = logging.getLogger(__name__)


def compress_backup_directory(backup_path: str, parent_path: str, backup_name: str):
    """Compresses the backup directory

    Args:
        backup_path: full path to base backup directory
        parent_path: full path to the parent backup directory
        backup_name: name of the backup folder for the currently running backup
    """
    tar_path = os.path.join(backup_path, f"{backup_name}.tar.bz2")

    with tarfile.open(tar_path, "w:bz2") as tar:
        tar.add(parent_path, arcname=backup_name)


def create_child_backup_directory(backup_path: str, child: str) -> str:
    """Creates a child directory in the parent backup directory

    Args:
        backup_path: full path to parent backup directory
        child: name of child folder

    Returns:
        full path to new child directory
    """
    path = os.path.join(backup_path, child)

    os.makedirs(path, 0o750, True)
    LOGGER.debug("created directory: %s", path)

    return path


def rsync_terminate_path(path: str) -> str:
    """adds a trailing slash to the end of the path

    Args:
        path: path to add trailing slash to

    Returns:
        correctly terminated path
    """
    if os.path.isfile(path):
        return path

    return path if path[-1] == os.path.sep else path + os.path.sep


# pylint: disable=too-many-instance-attributes
class Backup:
    """The Backup running class."""
    def __init__(self, console: bool, config_file: str, defaults: dict) -> None:
        self._config_file = config_file

        self._parent_dir = ''
        self._parent_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self._projects: Union[Projects, None] = None

        self._defaults = defaults
        self._notifier_configs = {}
        self._project_configs = DictObj({})
        self._plugins = DictObj({})
        self._settings = DictObj({})

        self._notif = Holder()
        if console:
            self._notif.add_console()

    def create_parent_backup_directory(self) -> bool:
        """Creates the parent backup directory.

        Returns:
            True if successful, False otherwise.
        """
        if self._settings.backup.skip_backup_directory:
            return True

        if not self._settings.backup.path:
            self._notif.failure('create backup directory: backup path not set')
        try:
            self._parent_dir = os.path.join(self._settings.backup.path, self._parent_name)
            os.makedirs(self._parent_dir, 0o750, True)
        except Exception as exception_object:  # pylint: disable=broad-exception-caught
            self._notif.failure(f"create parent backup directory: {exception_object}")
            return self.__failure_cleanup()

        return True

    def enable_notifiers(self) -> bool:
        """Enables notifiers for loaded configs.

        Returns:
            True if successful, False otherwise
        """
        for name, config in self._notifier_configs.items():
            msg = self._notif.add(name, config)
            if msg:
                self._notif.failure(f"enable notifiers: {msg}")
                return False

        return True

    def __failure_cleanup(self) -> bool:
        """Cleanup the directory used for backup.

        Returns:
            False always
        """
        if not self._settings.backup.skip_backup_directory and self._settings.backup.clean_on_failure:
            try:
                fops.delete(self._parent_dir)
            except Exception as exception_object:  # pylint: disable=broad-exception-caught
                self._notif.failure(f"load config: {exception_object}")
            for ext in ('tar.gz', 'tar.bz2'):
                try:
                    fops.delete(f"{self._parent_dir}.{ext}")
                except FileNotFoundError:
                    pass
                except Exception as exception_object:  # pylint: disable=broad-exception-caught
                    self._notif.failure(f"load config: {exception_object}")

        return False

    def load_config(self) -> bool:
        """Loads the configuration file and any project files loaded in projects_folder if defined

        Returns:
            True if successful, False otherwise
        """
        try:
            settings = Settings(self._defaults, self._config_file, '').get_all()
        except Exception as exception_object:  # pylint: disable=broad-exception-caught
            self._notif.failure(f"load config: {exception_object}")
            return False

        self._settings = DictObj(settings)

        return True

    @staticmethod
    def __load_configs_from_folder() -> dict:
        """Reads YAML files in this directory and loads them as configurations

        Returns:
            A dictionary of file content keyed by file name minus .yaml
        """
        contents = {}
        files = glob.glob("*.yaml")

        for file in files:
            contents[os.path.splitext(file)[0]] = fops.file_read_convert(file, fops.YAML, True)

        return contents

    def __load_configs(self, folder_path: str) -> dict:
        """Loads yaml configuration files from the specified folder_path

        Args:
            folder_path: full path to folder containing configuration files or relative path to CWD

        Returns:
            A dictionary of file content keyed by file name minus .yaml
        """
        if folder_path[:1] == '/':
            full_path = folder_path
        else:
            full_path = os.path.join(os.path.realpath(os.path.dirname(self._config_file)), folder_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError('folder defined but does not exist')
        if not os.path.isdir(full_path):
            raise IOError('folder defined but not a folder')

        with fops.pushd(full_path):
            return self.__load_configs_from_folder()

    def load_notifier_configs(self) -> bool:
        """Loads configs for notifiers.

        Returns:
            True if successful, false otherwise
        """
        path = self._settings.get('backup', {}).get('notifiers_folder')
        if path:
            try:
                notifier_configs = self.__load_configs(path)
                self._notifier_configs = merge_dictionaries(self._settings.get('backup', {}).get('notifiers'),
                                                            notifier_configs)
            except Exception as exception_object:  # pylint: disable=broad-exception-caught
                self._notif.failure(f"load notifiers configs: {exception_object}")
                return False

        return True

    def __load_plugins(self) -> None:
        """Loads plugins"""
        plugins = {}
        imported_package = __import__('eljef.backup.plugins', fromlist=['plugin'])
        for i in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not i.ispkg:
                plugin_module = __import__(i.name, fromlist=['plugin'])
                class_members = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, class_member) in class_members:
                    if issubclass(class_member, SetupPlugin) & (class_member is not SetupPlugin):
                        plugins[class_member().name] = class_member

        self._plugins = DictObj(plugins)

    def load_plugins(self) -> bool:
        """Loads Plugins

        Returns:
            True if successful, False otherwise
        """
        try:
            self.__load_plugins()
        except Exception as exception_object:  # pylint: disable=broad-exception-caught
            self._notif.failure(f"load plugins: {exception_object}")
            return False

        return True

    def load_project_configs(self) -> bool:
        """Loads configs for projects.

        Returns:
            True if successful, false otherwise
        """
        path = self._settings.get('backup', {}).get('projects_folder')
        if path:
            try:
                project_configs = self.__load_configs(path)
                self._project_configs = DictObj(merge_dictionaries(self._settings.get('backup', {}).get('projects'),
                                                                   project_configs))
            except Exception as exception_object:  # pylint: disable=broad-exception-caught
                self._notif.failure(f"load projects: {exception_object}")
                return False

        return True

    def prepare(self) -> bool:
        """Prepares projects for running.

        Returns:
            True if successful, false otherwise
        """
        try:
            paths = Paths(self._settings.backup.path, self._parent_dir, self._parent_name)
            self._projects = Projects(paths, self._plugins, self._project_configs)
        except Exception as exception_object:  # pylint: disable=broad-exception-caught
            self._notif.failure(f"prepare projects: {exception_object}")
            return self.__failure_cleanup()

        return True

    def run(self) -> bool:
        """Runs all projects.

        Returns:
           True if successful, false otherwise
        """
        try:
            finished, error_msg, project = self._projects.run()
            if not finished:
                self._notif.failure(f"{project}: {error_msg}")
                return self.__failure_cleanup()
        except Exception as exception_object:  # pylint: disable=broad-exception-caught
            self._notif.failure(f"run projects: {exception_object}")
            return self.__failure_cleanup()

        return True

    def success(self) -> None:
        """Prints a success message to all notifiers"""
        self._notif.success(f"backup successful: {self._parent_name}")
