# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
"""ElJef Backup Notifier Base Class Testing"""

import unittest
import pytest

from eljef.backup.notifiers.notifier import Notifier


class TestNotifierInit(unittest.TestCase):
    def test_notifier_init(self):
        notif = Notifier({})
        self.assertTrue(notif.name == '', 'name is not blank')


class TestNotifierFailure(unittest.TestCase):
    def test_notifier_failure(self):
        notif = Notifier({})
        with pytest.raises(NotImplementedError):
            notif.failure('test')


class TestNotifierInfo(unittest.TestCase):
    def test_notifier_info(self):
        notif = Notifier({})
        with pytest.raises(NotImplementedError):
            notif.info('test')


class TestNotifierSetup(unittest.TestCase):
    def test_notifier_setup(self):
        notif = Notifier({})
        with pytest.raises(NotImplementedError):
            _ = notif.setup()


class TestNotifierSuccess(unittest.TestCase):
    def test_notifier_success(self):
        notif = Notifier({})
        with pytest.raises(NotImplementedError):
            notif.success('test')
