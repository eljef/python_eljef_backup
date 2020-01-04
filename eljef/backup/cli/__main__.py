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
# __main__.py : ElJef Backup CLI Main
"""ElJef Backup CLI Main

ElJef CLI Main backup functionality.
"""

import logging
import argparse
import shutil
import time

from typing import Tuple

from eljef.backup import backup
from eljef.backup.cli.__args__ import CMD_LINE_ARGS
from eljef.backup.cli.__vars__ import (DEFAULTS, PROJECT_DESCRIPTION, PROJECT_NAME, PROJECT_VERSION)
from eljef.backup.project import Projects
from eljef.core.applog import setup_app_logging
from eljef.core.dictobj import DictObj
from eljef.core.settings import Settings

LOGGER = logging.getLogger()


def do_args() -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    """Returns command line arguments

    Returns:
        A tuple with the argument parser and parsed namespace
    """
    parser = argparse.ArgumentParser(description=PROJECT_DESCRIPTION)
    for arg_dict in CMD_LINE_ARGS:
        parser.add_argument(arg_dict['short'], arg_dict['long'], **arg_dict['opts'])

    args = parser.parse_args()

    return parser, args


def do_backup_path(path: str) -> Tuple[str, str]:
    """Creates the new backup directory for this run.

    Args:
        path: full path to parent backup directory
    """
    try:
        return backup.create_parent_backup_directory(path)
    except ValueError:
        raise SystemExit('backup path cannot be empty')
    except FileNotFoundError:
        raise SystemExit("{0!s}: not found".format(path))


def do_cleanup(path: str) -> None:
    """Cleanup the directory used for backup

    Args:
        path: full path to parent backup directory
    """
    LOGGER.debug("removing backup directory: %s", path)
    shutil.rmtree(path)


def do_compress_only(path: str):
    """Compresses nocompress directories from previous runs

    Args:
        path: full path to base backup directory
    """
    try:
        backup.compress_nocompress(path)
    except FileNotFoundError:
        raise SystemExit("{0!s}: not found".format(path))
    except IOError:
        raise SystemExit("{0!s}: not a directory".format(path))


def do_config_file(path: str) -> DictObj:
    """Returns configuration information

    Args:
        path: full path to configuration file

    Returns:
        configuration information as a dictionary
    """
    try:
        settings = DictObj(Settings(DEFAULTS, path, '').get_all())
        if not settings.get('backup'):
            raise SystemExit("{0!s}: malformed configuration file".format(path))
        if not settings.backup.get('compress'):
            settings.backup['compress'] = True
        if not settings.backup.get('compress_only'):
            settings.backup['compress_only'] = False

        return settings
    except FileNotFoundError:
        raise SystemExit("{0!s}: not found".format(path))
    except IOError:
        raise SystemExit("{0!s}: not a file".format(path))


def do_version() -> None:
    """Prints the program version and exits."""
    print("{0!s} - {1!s}".format(PROJECT_NAME, PROJECT_VERSION))
    raise SystemExit(0)


def main() -> None:
    """Main function"""
    parser, args = do_args()

    if args.version_out:
        do_version()

    setup_app_logging(args.debug_log)

    settings = do_config_file(args.config_file)

    if settings.backup.compress_only:
        do_compress_only(settings.backup.path)
        raise SystemExit(0)

    parent_dir, parent_name = do_backup_path(settings.backup.path)

    try:
        plugins = backup.load_plugins()
        projects = Projects(parent_dir, plugins, settings.backup)

        finished, error_msg = projects.run()
        if not finished:
            do_cleanup(parent_dir)
            raise SystemExit(error_msg)

    except TypeError:
        do_cleanup(parent_dir)
        raise
    except (SyntaxError, ValueError) as exception_object:
        do_cleanup(parent_dir)
        raise SystemExit(str(exception_object))
    except KeyboardInterrupt:
        time.sleep(1)
        do_cleanup(parent_dir)
        raise SystemExit("interrupted by keyboard")

    if settings.backup.compress:
        backup.compress_backup_directory(settings.backup.path, parent_dir, parent_name)
        do_cleanup(parent_dir)
    else:
        backup.nocompress_backup_directory(parent_dir)


if __name__ == '__main__':
    main()
