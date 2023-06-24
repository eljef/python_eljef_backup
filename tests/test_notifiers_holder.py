# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
"""ElJef Backup Notifier Holder Testing"""

import unittest

from unittest.mock import patch

from tests.common import MsgWriter

from eljef.backup.notifiers.console import Console
from eljef.backup.notifiers.holder import Holder


class TestHolderInit(unittest.TestCase):
    def test_holder_init(self):
        h = Holder()
        self.assertTrue(len(h.active) == 0, 'active notifiers not empty')


class TestHolderAdd(unittest.TestCase):
    def test_holder_add_bad_name(self):
        h = Holder()
        got = h.add('unknown', {})
        self.assertTrue(got == 'unknown notifier: unknown', 'incorrect error message')

    def test_holder_add_bad_settings(self):
        h = Holder()
        got = h.add('gotify', {})
        self.assertTrue(got == 'gotify_key not configured', 'incorrect error message')

    def test_holder_add_good(self):
        h = Holder()
        got = h.add('gotify', {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'})
        self.assertTrue(got == '', 'error message not empty')
        self.assertTrue(len(h.active) == 1, 'incorrect number of active notifiers')


class TestHolderAddConsole(unittest.TestCase):
    def test_holder_add_console(self):
        h = Holder()
        h.add_console()
        self.assertTrue(len(h.active) == 1, 'incorrect number of active notifiers')


class TestHolderFailure(unittest.TestCase):
    def test_holder_failure(self):
        test_msg = 'test_console_failure'
        catcher = MsgWriter()
        notif = Console({})

        h = Holder()
        h.active.append(notif)

        with patch.object(notif.logger, 'fatal', catcher.write_msg):
            h.failure('test_console_failure')

        self.assertTrue(catcher.msg == test_msg, 'failure msg != test_console_failure')


class TestHolderInfo(unittest.TestCase):
    def test_holder_info(self):
        test_msg = 'test_console_info'
        catcher = MsgWriter()
        notif = Console({})

        h = Holder()
        h.active.append(notif)

        with patch.object(notif.logger, 'info', catcher.write_msg):
            h.info('test_console_info')

        self.assertTrue(catcher.msg == test_msg, 'failure msg != test_console_info')


class TestHolderSuccess(unittest.TestCase):
    def test_holder_success(self):
        test_msg = 'test_console_success'
        catcher = MsgWriter()
        notif = Console({})

        h = Holder()
        h.active.append(notif)

        with patch.object(notif.logger, 'info', catcher.write_msg):
            h.success('test_console_success')

        self.assertTrue(catcher.msg == test_msg, 'failure msg != test_console_success')
