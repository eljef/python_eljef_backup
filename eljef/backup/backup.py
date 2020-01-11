# -*- coding: UTF-8 -*-
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
# backup.py : ElJef Backup Functionality
"""ElJef Backup Functionality

ElJef backup functionality.
"""

import datetime
import inspect
import glob
import logging
import os
import pkgutil
import tarfile

from typing import Tuple

from eljef.backup.plugins.plugin import SetupPlugin
from eljef.core import fops
from eljef.core.dictobj import DictObj

LOGGER = logging.getLogger(__name__)


def compress_backup_directory(backup_path: str, parent_path: str, backup_name: str):
    """Compresses the backup directory

    Args:
        backup_path: full path to base backup directory
        parent_path: full path to the parent backup directory
        backup_name: name of the backup folder for the currently running backup
    """
    tar_path = os.path.join(backup_path, "{0!s}.tar.bz2".format(backup_name))

    LOGGER.info("compressing: %s => %s", parent_path, tar_path)

    with tarfile.open(tar_path, "w:bz2") as tar:
        tar.add(parent_path, arcname=backup_name)


def compress_nocompress(backup_path: str):
    """Compresses nocompress directories from previous runs

    Args:
        backup_path: full path to base backup directory
    """
    os.chdir(backup_path)
    dirs = glob.glob("*.nocompress")
    if dirs:
        for orig_dir in dirs:
            new_dir = orig_dir.replace('.nocompress', '')
            tar_path = "{0!s}.tar.bz2".format(new_dir)

            LOGGER.info("compressing backup: %s", new_dir)
            os.rename(orig_dir, new_dir)

            with tarfile.open(tar_path, "w:bz2") as tar:
                tar.add(new_dir, arcname=new_dir)

            fops.delete(new_dir)


def create_child_backup_directory(backup_path: str, child: str) -> str:
    """Creates a child directory in the parent backup directory

    Args:
        backup_path: full path to parent backup directory
        child: name of child folder

    Returns:
        full path to new child directory
    """
    path = os.path.join(backup_path, child)

    os.makedirs(path, 0x750, True)
    LOGGER.debug("created directory: %s", path)

    return path


def create_parent_backup_directory(path: str) -> Tuple[str, str]:
    """Creates backup directory for current run with the data appended to the name

    Args:
        path: full path to parent directory for backups

    Returns:
        full path to backup directory to be used for the current run
        name of backup directory (to be used when compressing)
    """
    if not path:
        raise ValueError("path cannot be blank")

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(path, current_time)

    os.makedirs(path, 0o750, True)
    LOGGER.debug("created directory: %s", path)

    return path, current_time


def load_plugins() -> DictObj:
    """Loads plugins

    Returns:
        DictObj: plugin name => Setup Plugin object
    """
    plugins = dict()
    imported_package = __import__('eljef.backup.plugins', fromlist=['plugin'])
    for i in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not i.ispkg:
            plugin_module = __import__(i.name, fromlist=['plugin'])
            class_members = inspect.getmembers(plugin_module, inspect.isclass)
            for (_, class_member) in class_members:
                if issubclass(class_member, SetupPlugin) & (class_member is not SetupPlugin):
                    plugins[class_member().name] = class_member

    return DictObj(plugins)
