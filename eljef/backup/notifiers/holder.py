# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Core Notifier Class"""

from typing import List

from eljef.backup.notifiers.console import Console
from eljef.backup.notifiers.gotify import Gotify
from eljef.backup.notifiers.notifier import Notifier


class Holder:
    """This calls holds the base console notifier and any other desired
       notifiers.

    Attributes:
        active: a list of active notifiers
    """
    def __init__(self) -> None:
        self.__notifiers = {'gotify': Gotify}
        self.active: List[Notifier] = []

    def add(self, name: str, settings: dict) -> str:
        """Adds a notifier to the holder.

        Args:
            name: name of the notifier to add
            settings: settings for the notifier

        Returns:
            An error string if there is a failure.
        """
        notifier_class = self.__notifiers.get(name)
        if not notifier_class:
            return f"unknown notifier: {name}"

        new_notifier = notifier_class(settings)
        msg = new_notifier.setup()
        if msg:
            return msg

        self.active.append(new_notifier)
        return ''

    def add_console(self) -> None:
        """Adds the console notifier."""
        console = Console({})
        self.active.append(console)

    def failure(self, msg) -> None:
        """Sends a failure notification to all active notifiers.

        Args:
            msg: the notification message to send
        """
        for notif in self.active:
            notif.failure(msg)

    def info(self, msg) -> None:
        """Sends an informative notification to all active notifiers.

        Args:
            msg: the notification message to send
        """
        for notif in self.active:
            notif.info(msg)

    def success(self, msg) -> None:
        """Sends a success notification to all active notifiers.

        Args:
            msg: the notification message to send
        """
        for notif in self.active:
            notif.success(msg)
