# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Console Notifier (logging) Class"""

import logging

from eljef.backup.notifiers.notifier import Notifier

LOGGER = logging.getLogger(__name__)


class Console(Notifier):
    """Console Notifier (logging) Class

    Attributes:
        name: name of this notifier
        logger: logger to use

    Notes:
        It is assumed that the console logger has been set up by the application.
    """
    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self.name = 'console'
        self.logger = LOGGER

    def failure(self, msg) -> None:
        """Sends a failure notification using this notifier.

        Args:
            msg: the notification message to send
        """
        self.logger.fatal(msg)

    def info(self, msg) -> None:
        """Sends an informative notification using this notifier.

        Args:
            msg: the notification message to send
        """
        self.logger.info(msg)

    def setup(self) -> str:
        """Set up this notifier.

        Returns:
            An empty string if no errors, error message otherwise.
        """
        return ''

    def success(self, msg) -> None:
        """Sends a success notification using this notifier.

        Args:
            msg: the notification message to send
        """
        self.logger.info(msg)
