# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Main CLI Functionality"""

import logging
import time

from eljef.backup import backup
from eljef.backup.cli.__args__ import CMD_LINE_ARGS
from eljef.backup.cli.__vars__ import (DEFAULTS, PROJECT_DESCRIPTION, PROJECT_NAME, PROJECT_VERSION)
from eljef.backup.project import (Paths, Projects)
from eljef.core import (cli, fops)
from eljef.core.applog import setup_app_logging
from eljef.core.dictobj import DictObj

LOGGER = logging.getLogger()


def do_failure_cleanup(path: str, do_cleanup: bool) -> None:
    """Cleanup the directory used for backup

    Args:
        path: full path to parent backup directory
        do_cleanup: cleanup the backup directory on failure if True
    """
    if do_cleanup:
        fops.delete(path)
        for ext in ('tar.gz', 'tar.bz2'):
            try:
                fops.delete(f"{path}.{ext}")
            except FileNotFoundError:
                pass


def main_backup_directory(settings: DictObj, plugins: DictObj) -> None:
    """Main functionality with a backup directory"""
    try:
        parent_dir, parent_name = backup.create_parent_backup_directory(settings.backup.path)
    except (FileNotFoundError, IOError, ValueError) as exception_object:
        raise SystemExit(exception_object) from exception_object

    try:
        paths = Paths(settings.backup.path, parent_dir, parent_name)
        projects = Projects(paths, plugins, settings.backup)

        finished, error_msg = projects.run()
        if not finished:
            do_failure_cleanup(parent_dir, settings.backup.clean_on_failure)
            raise SystemExit(error_msg)

    except (AttributeError, KeyError, TypeError):
        do_failure_cleanup(parent_dir, settings.backup.clean_on_failure)
        raise
    except (SyntaxError, ValueError) as exception_object:
        do_failure_cleanup(parent_dir, settings.backup.clean_on_failure)
        raise SystemExit(str(exception_object)) from exception_object
    except KeyboardInterrupt:
        time.sleep(1)
        do_failure_cleanup(parent_dir, settings.backup.clean_on_failure)
        # There is no need to re-raise from a KeyboardInterrupt
        # pylint: disable=W0707
        raise SystemExit("interrupted by keyboard")


def main_no_backup_directory(settings: DictObj, plugins: DictObj) -> None:
    """Main functionality without a backup directory"""
    try:
        paths = Paths(settings.backup.path, '', '')
        projects = Projects(paths, plugins, settings.backup)

        finished, error_msg = projects.run()
        if not finished:
            raise SystemExit(error_msg)

    except (AttributeError, KeyError, SyntaxError, TypeError, ValueError) as exception_object:
        raise SystemExit(str(exception_object)) from exception_object
    except KeyboardInterrupt:
        time.sleep(1)
        # There is no need to re-raise from a KeyboardInterrupt
        # pylint: disable=W0707
        raise SystemExit("interrupted by keyboard")


def main() -> None:
    """Main function"""
    args = cli.args_simple(PROJECT_NAME, PROJECT_DESCRIPTION, CMD_LINE_ARGS)

    if args.version_out:
        cli.print_version(PROJECT_NAME, PROJECT_VERSION)

    setup_app_logging(args.debug_log)

    try:
        settings = backup.load_config(args.config_file, DEFAULTS)
        plugins = backup.load_plugins()
    except (FileNotFoundError, IOError, ValueError) as exception_object:
        raise SystemExit(exception_object) from exception_object

    if settings.backup.skip_backup_directory:
        main_no_backup_directory(settings, plugins)
        raise SystemExit(0)

    main_backup_directory(settings, plugins)
    raise SystemExit(0)


if __name__ == '__main__':
    main()
