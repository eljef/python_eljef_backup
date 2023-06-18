# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Core Notifier Class"""


class Notifier:
    """The base notifier class.

    Attributes:
        name: the name of this notifier
        settings: settings dictionary for the notifier
    """
    def __init__(self, settings: dict) -> None:
        self.name = ''
        self.settings = settings

    def failure(self, msg) -> None:
        """Sends a failure notification using this notifier.

        Args:
            msg: the notification message to send
        """
        raise NotImplementedError

    def info(self, msg) -> None:
        """Sends an informative notification using this notifier.

        Args:
            msg: the notification message to send
        """
        raise NotImplementedError

    def setup(self) -> str:
        """Set up this notifier.

        Returns:
            An empty string if no errors, error message otherwise.
        """
        raise NotImplementedError

    def success(self, msg) -> None:
        """Sends a success notification using this notifier.

        Args:
            msg: the notification message to send
        """
        raise NotImplementedError
