# -*- coding: utf-8 -*-
import json
import re
import sys
from urllib import request

import vim

if sys.version_info >= (3, 0):
    unicode = bytes
    unichr = chr


class Kaonashi(object):

    """Kaonashi interface"""

    def __init__(self):
        self.port = 8080
        self.host = 'localhost'
        self.protocol = 'http'
        self.base_url = '{0}://{1}:{2}'.format(self.protocol, self.host, self.port)
        self.note_id_regx = re.compile('\+ ID:(\d+).*')
        self.current_edit_buf_name = 'edit.kaonashi'

    def bwrite(self, s, target_buffer=None):
        b = target_buffer or vim.current.buffer
        # Never write more than two blank lines in a row
        if not s.strip() and not b[-1].strip() and not b[-2].strip():
            return

        # Vim buffer.append() cannot accept unicode type,
        # must first encode to UTF-8 string
        if isinstance(s, unicode):
            s = s.encode('utf-8', errors='replace')

        # Code block markers for syntax highlighting
        cb = unichr(160)
        if isinstance(cb, unicode):
            cb = cb.encode('utf-8')
        if s == cb and not b[-1]:
            b[-1] = s
            return

        if not b[0]:
            b[0] = s
        else:
            b.append(s)

    def list_note_titles(self):
        """List note titles"""
        endpoint = self.base_url + '/note'
        with request.urlopen(endpoint) as resp:
            data = json.loads(
                resp.read().decode(resp.info().get_param('charset') or 'utf-8'))
            notes = data['data']

        vim.command("enew")
        vim.command("file edit.kaonashi")
        vim.command('40vnew notelist.kaonashi')
        vim.command("set syntax=kaonashi")
        vim.command("setlocal noswapfile")
        vim.command("setlocal buftype=nofile")
        for note in notes:
            note_id = note.get('id', '')
            title = note.get('title', '')
            updated = note.get('updated', '')
            self.bwrite("+ ID:{} {}".format(note_id, title))
            self.bwrite("  [{}]".format(updated))

    def get_note(self):
        """Open a note"""
        line = vim.current.line
        m = self.note_id_regx.match(line)
        if m:
            note_id = m.group(1)
            endpoint = self.base_url + '/note/{}'.format(note_id)
            with request.urlopen(endpoint) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            note = data['data']
            body = note['body']
            title = note['title']
            vim.command("execute bufwinnr(bufnr('{}')).'wincmd w'".format(
                self.current_edit_buf_name))
            vim.command("enew")
            self.current_edit_buf_name = "{0}_{1}".format(note_id, title)
            vim.command("file '{}'".format(self.current_edit_buf_name))
            vim.command("set syntax=kaonashi")
            vim.command("setlocal noswapfile")
            vim.command("setlocal buftype=nofile")
            self.bwrite("#ID {0}: {1}".format(note_id, title))
            self.bwrite(body)
        else:
            pass

kaonashi = Kaonashi()
