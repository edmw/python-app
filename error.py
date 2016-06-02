# coding: utf-8

import textwrap

ERROR_INTERNAL = 500

class Error(Exception):
    def __init__(self, template, *fields):
        if template:
            self.formatMessage(template, *fields)
        else:
            self.message = str(ERROR_INTERNAL)
    def formatMessage(self, template, *fields):
        self.message = textwrap.dedent(template).format(*fields)
