# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Main CLI Functionality"""

import logging

from eljef.backup.backup import Backup
from eljef.backup.cli.__args__ import CMD_LINE_ARGS
from eljef.backup.cli.__vars__ import (DEFAULTS, PROJECT_DESCRIPTION, PROJECT_NAME, PROJECT_VERSION)
from eljef.core import cli
from eljef.core.applog import setup_app_logging

LOGGER = logging.getLogger()


def check_fail(ret: bool) -> None:
    """Checks the return status of a function and exits if False.

    Args:
        ret: return status from function
    """
    if not ret:
        raise SystemExit(1)


def main() -> None:
    """Main function"""
    args = cli.args_simple(PROJECT_NAME, PROJECT_DESCRIPTION, CMD_LINE_ARGS)

    if args.version_out:
        cli.print_version(PROJECT_NAME, PROJECT_VERSION)

    setup_app_logging(args.debug_log)

    backup = Backup(True, args.config_file, DEFAULTS)
    check_fail(backup.load_config())
    check_fail(backup.load_notifier_configs())
    check_fail(backup.enable_notifiers())
    check_fail(backup.load_plugins())
    check_fail(backup.load_project_configs())
    check_fail(backup.create_parent_backup_directory())
    check_fail(backup.prepare())
    check_fail(backup.run())
    backup.success()


if __name__ == '__main__':
    main()
