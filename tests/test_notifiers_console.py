# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
"""ElJef Backup Console Notifier Testing"""

import logging
import unittest

from unittest.mock import patch

from tests.common import MsgWriter

from eljef.backup.notifiers.console import Console


class TestConsoleInit(unittest.TestCase):
    def test_console_init(self):
        settings = {}
        notif = Console(settings)

        self.assertTrue(notif.name == 'console', 'Console.name != console')
        self.assertDictEqual(notif.settings, settings, 'Settings dictionaries differ')
        self.assertTrue(isinstance(notif.logger, logging.Logger), 'Console.logger is not a logging.Logger')


class TestConsoleFailure(unittest.TestCase):
    def test_console_failure(self):
        test_msg = 'test_console_failure'
        catcher = MsgWriter()
        notif = Console({})

        with patch.object(notif.logger, 'fatal', catcher.write_msg):
            notif.failure(test_msg)

        self.assertTrue(catcher.msg == test_msg, 'failure msg != test_console_failure')


class TestConsoleInfo(unittest.TestCase):
    def test_console_info(self):
        test_msg = 'test_console_info'
        catcher = MsgWriter()
        notif = Console({})

        with patch.object(notif.logger, 'info', catcher.write_msg):
            notif.info(test_msg)

        self.assertTrue(catcher.msg == test_msg, 'info msg != test_console_info')


class TestConsoleSetup(unittest.TestCase):
    def test_console_setup(self):
        notif = Console({})

        self.assertTrue(notif.setup() == '', 'setup did not return an empty string')


class TestConsoleSuccess(unittest.TestCase):
    def test_console_success(self):
        test_msg = 'test_console_success'
        catcher = MsgWriter()
        notif = Console({})

        with patch.object(notif.logger, 'info', catcher.write_msg):
            notif.success(test_msg)

        self.assertTrue(catcher.msg == test_msg, 'success msg != test_console_success')
