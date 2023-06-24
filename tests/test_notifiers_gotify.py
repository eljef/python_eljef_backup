# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
"""ElJef Backup Gotify Notifier Testing"""

import requests
import unittest

from unittest.mock import (Mock, patch)

from tests.common import MsgWriter

from eljef.backup.notifiers import gotify


class TestGotifyInit(unittest.TestCase):
    def test_gotify_init(self):
        settings = {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'}
        notif = gotify.Gotify(settings)

        self.assertTrue(notif.name == 'gotify', 'Gotify.name != gotify')
        self.assertDictEqual(notif.settings, settings, 'Settings dictionaries differ')
        self.assertTrue(notif._gotify_key == 'test1', 'Gotify._gotify_key != test1')
        self.assertTrue(notif._msg_title == 'test2', 'Gotify._msg_title != test2')
        self.assertTrue(notif._url == 'https://test3', 'Gotify._url != https://test3')


class TestGotifySendMessage(unittest.TestCase):

    @patch('requests.post')
    def test_gotify_send_message_bad_response(self, mock_post):
        mock_resp = requests.Response()
        mock_resp.status_code = 404
        mock_resp._content = str.encode('not_found')

        mock_post.configure_mock(return_value=mock_resp)

        settings = {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'}
        notif = gotify.Gotify(settings)

        catcher = MsgWriter()

        with patch.object(gotify.LOGGER, 'error', catcher.write_msg):
            notif._send_message({'test': 'data'})

        self.assertTrue(catcher.msg == 'gotify: %d: %s', 'catcher.msg != gotify: %d: %s')
        self.assertTrue(len(catcher.args) == 2, 'len(cather.args) != 2')
        self.assertTrue(catcher.args[0] == 404, 'catcher.args[0] != 404')
        self.assertTrue(catcher.args[1] == 'not_found', 'catcher.args[1] != not_found')

    @patch('requests.post')
    def test_gotify_send_message_exception(self, mock_post):
        mock_post.raiseError.side_effect = Mock(side_effect=Exception('test_exception'))

        settings = {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'}
        notif = gotify.Gotify(settings)

        catcher = MsgWriter()

        with patch.object(gotify.LOGGER, 'error', catcher.write_msg):
            notif._send_message({'test': 'data'})

        self.assertTrue(catcher.msg == 'gotify: %s', 'catcher.msg != gotify: %s')
        self.assertTrue(len(catcher.args) == 1, 'len(cather.args) != 1')


class TestGotifyFailure(unittest.TestCase):

    @patch('requests.post')
    def test_gotify_failure(self, mock_post):
        mock_resp = requests.Response()
        mock_resp.status_code = 200

        mock_post.configure_mock(return_value=mock_resp)

        settings = {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'}
        notif = gotify.Gotify(settings)

        payload = {'message': 'test_failure',
                   'priority': 8,
                   'title': "test2: Failed"}

        notif.failure('test_failure')

        kwargs = mock_post.call_args.kwargs
        self.assertDictEqual(payload, kwargs.get('json'))


class TestGotifyInfo(unittest.TestCase):
    def test_gotify_info(self):
        settings = {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'}
        notif = gotify.Gotify(settings)
        notif.info('nothing_is_actually_here_to_test_but_coverage_demands_it')


class TestGotifySetup(unittest.TestCase):
    def test_gotify_setup_no_gotify_key(self):
        settings = {}
        notif = gotify.Gotify(settings)
        got = notif.setup()

        self.assertTrue(got == 'gotify_key not configured', 'not.setup != gotify_key not configured')

    def test_gotify_setup_no_msg_title(self):
        settings = {'gotify_key': 'test1'}
        notif = gotify.Gotify(settings)
        got = notif.setup()

        self.assertTrue(got == 'message_title not configured', 'not.setup != message_title not configured')

    def test_gotify_setup_no_url(self):
        settings = {'gotify_key': 'test1', 'message_title': 'test2'}
        notif = gotify.Gotify(settings)
        got = notif.setup()

        self.assertTrue(got == 'url not configured', 'url not configured')

    def test_gotify_setup_good(self):
        settings = {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'}
        notif = gotify.Gotify(settings)
        got = notif.setup()

        self.assertTrue(got == '', 'return not empty')


class TestGotifySuccess(unittest.TestCase):

    @patch('requests.post')
    def test_gotify_failure(self, mock_post):
        mock_resp = requests.Response()
        mock_resp.status_code = 200

        mock_post.configure_mock(return_value=mock_resp)

        settings = {'gotify_key': 'test1', 'message_title': 'test2', 'url': 'https://test3'}
        notif = gotify.Gotify(settings)

        payload = {'message': 'test_success',
                   'priority': 2,
                   'title': "test2: Success"}

        notif.success('test_success')

        kwargs = mock_post.call_args.kwargs
        self.assertDictEqual(payload, kwargs.get('json'))
