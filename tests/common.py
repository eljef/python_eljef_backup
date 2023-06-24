# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
"""ElJef Backup Common Testing Helpers"""


class MsgWriter:
    """A simple class to catch a message being written to the logger

    Attributes:
        msg: the message written to the logger
        args: args written to the logger
        kwargs: kwargs written to the logger
    """

    def __init__(self) -> None:
        self.args = None
        self.kwargs = None
        self.msg = ''

    def write_msg(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs
