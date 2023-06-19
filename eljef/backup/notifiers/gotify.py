# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
# pylint: disable=too-few-public-methods

"""Gotify Notifier Class"""

import logging
import requests

from eljef.backup.notifiers.notifier import Notifier

LOGGER = logging.getLogger(__name__)


class Gotify(Notifier):
    """Gotify Notifier Class

    Attributes:
        name: name of this notifier
    """
    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self.name = 'gotify'

        self._gotify_key = settings.get('gotify_key', '')
        self._msg_title = settings.get('message_title', '')
        self._url = settings.get('url', '')

    def _send_message(self, payload: dict) -> None:
        """Sends message to gotify.

        Args:
            payload: payload to send with message
        """
        headers = {'Content-Type': 'application/json',
                   'X-Gotify-Key': self._gotify_key}

        url = f"{self._url.rstrip('/')}/message"

        try:
            url_data = requests.post(url, headers=headers, json=payload, timeout=10)
            if url_data.status_code >= 400:
                LOGGER.error("gotify: %d: %s", url_data.status_code, url_data.text)
        except Exception as exception_object:  # pylint: disable=broad-exception-caught
            LOGGER.error("gotify: %s", {exception_object})

    def failure(self, msg) -> None:
        """Sends a failure notification using this notifier.

        Args:
            msg: the notification message to send
        """
        payload = {'message': msg,
                   'priority': 8,
                   'title': f"{self._msg_title}: Failed"}

        self._send_message(payload)

    def info(self, msg) -> None:
        """Sends an informative notification using this notifier.

        Args:
            msg: the notification message to send
        """
        return

    def setup(self) -> str:
        """Set up this notifier.

        Returns:
            An empty string if no errors, error message otherwise.
        """
        if not self._gotify_key:
            msg = "gotify_key not configured"
        elif not self._msg_title:
            msg = "message_title not configured"
        elif not self._url:
            msg = "url not configured"
        else:
            msg = ''

        return msg

    def success(self, msg) -> None:
        """Sends a success notification using this notifier.

        Args:
            msg: the notification message to send
        """
        payload = {'message': msg,
                   'priority': 2,
                   'title': f"{self._msg_title}: Success"}

        self._send_message(payload)
