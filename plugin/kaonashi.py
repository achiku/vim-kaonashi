# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import os
import re
import sys

import requests
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

    def refresh_note_list(self):
        """Close note list."""
        vim.command("execute bufwinnr(bufnr('%s')).'wincmd w'" % ('notelist.kaonashi',))
        endpoint = self.base_url + '/note'
        vim.current.buffer[:] = None
        resp = requests.get(endpoint)
        data = resp.json()
        notes = data['data']
        for note in notes:
            note_id = note.get('id', '')
            title = note.get('title', '')
            self.bwrite("+ ID:%s %s" % (note_id, title))
        vim.command("execute bufwinnr(bufnr('%s')).'wincmd w'" % (self.current_edit_buf_name,))

    def list_notes(self):
        """List note titles."""
        endpoint = self.base_url + '/note'
        resp = requests.get(endpoint)
        data = resp.json()
        notes = data['data']

        vim.command("enew")
        vim.command("file edit.kaonashi")
        vim.command('40vnew notelist.kaonashi')
        self.current_edit_buf_name = 'edit.kaonashi'
        vim.command("set syntax=kaonashi")
        vim.command("setlocal noswapfile")
        vim.command("setlocal buftype=nofile")
        for note in notes:
            note_id = note.get('id', '')
            title = note.get('title', '')
            self.bwrite("+ ID:%s %s" % (note_id, title))

    def delete_note(self):
        """Delete a note."""
        line = vim.current.line
        m = self.note_id_regx.match(line)
        if m:
            note_id = m.group(1)
            endpoint = self.base_url + '/note/%s' % (note_id,)
            requests.delete(endpoint)
            self.refresh_note_list()
        else:
            pass

    def get_note(self):
        """Open a note."""
        line = vim.current.line
        m = self.note_id_regx.match(line)
        if m:
            note_id = m.group(1)
            endpoint = self.base_url + '/note/%s' % (note_id,)
            resp = requests.get(endpoint)
            data = resp.json()
            note = data['data']
            body = note['body']
            title = note['title']
            vim.command("execute bufwinnr(bufnr('%s')).'wincmd w'" % (self.current_edit_buf_name,))
            vim.command("enew")
            self.current_edit_buf_name = '%s.kaonashi' % (note_id,)
            vim.command("file %s" % (self.current_edit_buf_name,))
            vim.command("set syntax=markdown")
            vim.command("setlocal noswapfile")
            vim.command("setlocal buftype=nofile")
            vim.command("noremap <buffer> :w :KaonashiSaveNote<CR>")
            note = ["#ID %s: %s" % (note_id, title)]
            if body is not None:
                note.extend(body.split('\n'))
            vim.current.buffer[:] = note
        else:
            pass

    def update_note(self):
        """Update a note."""
        buffer_name = os.path.basename(vim.current.buffer.name)
        note_id = buffer_name.replace('.kaonashi', '')
        m = re.match("#ID (\d+): (.*)", vim.current.buffer[0])
        note_id = m.group(1)
        title = m.group(2)
        body = "\n".join(vim.current.buffer[1:])
        payload = {'data': {'title': title, 'body': body}}
        endpoint = self.base_url+'/note/%s' % (note_id,)
        requests.put(endpoint, data=json.dumps(payload))

    def create_note(self):
        """Create a note."""
        payload = {'data': {'title': '', 'body': ''}}
        endpoint = self.base_url + '/note'
        requests.post(endpoint, data=json.dumps(payload))


if __name__ == '__main__':
    kaonashi = Kaonashi()
