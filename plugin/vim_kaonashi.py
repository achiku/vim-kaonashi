# -*- coding: utf-8 -*-
import json
from urllib import request

import vim


class Kaonashi(object):

    """Kaonashi interface"""

    def __init__(self):
        self.port = 8080
        self.host = 'localhost'
        self.protocol = 'http'
        self.base_url = '{0}://{1}:{2}'.format(self.protocol, self.host, self.port)

    def vimmodule(self):
        """vim module test"""
        endpoint = self.base_url + '/note'
        notes = None
        with request.urlopen(endpoint) as resp:
            data = json.loads(
                resp.read().decode(resp.info().get_param('charset') or 'utf-8'))
            notes = data['data']
        # vim.current.buffer is the current buffer. It's list-like object.
        # each line is an item in the list. We can loop through them delete
        # them, alter them etc.
        # Here we delete all lines in the current buffer
        del vim.current.buffer[:]

        # Here we append some lines above. Aesthetics.
        vim.current.buffer[0] = 80*"-"

        for note in notes:
            # In the next few lines, we get the post details
            title = note.get('title', '')
            # And here we append line by line to the buffer.
            # First the upvotes
            vim.current.buffer.append("↑ %s" % title)
            # Then the title and the url
            # vim.current.buffer.append("    %s [%s]"%(title, url,))
            # # Then the downvotes and number of comments
            # vim.current.buffer.append("↓ %s    | comments: %s [%s]"%(down, comments, permalink,))
            # # And last we append some "-" for visual appeal.
            vim.current.buffer.append(80*"-")

    def list_note_titles(self):
        """list note titles"""
        endpoint = self.base_url + '/note'
        with request.urlopen(endpoint) as resp:
            data = json.loads(
                resp.read().decode(resp.info().get_param('charset') or 'utf-8'))
            notes = data['data']

        del vim.current.buffer[:]
        # Here we append some lines above. Aesthetics.
        vim.current.buffer[0] = 80*"-"
        for note in notes:
            # In the next few lines, we get the post details
            note_id = note.get('id', '')
            title = note.get('title', '')
            updated = note.get('updated', '')
            vim.current.buffer.append("ID:{} {} [last updated at: {}]".format(note_id, title, updated))
        vim.current.buffer.append(80*"-")

    def greeting(self, name):
        """greet 5 times"""
        for i in range(5):
            print("hello, " + name)

kaonashi = Kaonashi()
