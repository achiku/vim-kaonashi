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

    def list_note_titles(self):
        """list note titles"""
        endpoint = self.base_url + '/note'
        with request.urlopen(endpoint) as resp:
            data = json.loads(
                resp.read().decode(resp.info().get_param('charset') or 'utf-8'))
            notes = data['data']

        # del vim.current.buffer[:]
        vim.command('40vnew ~/.kaonashi.buff')
        # Here we append some lines above. Aesthetics.
        for note in notes:
            # In the next few lines, we get the post details
            note_id = note.get('id', '')
            title = note.get('title', '')
            updated = note.get('updated', '')
            vim.current.buffer.append("+ ID:{} {}".format(note_id, title))
            vim.current.buffer.append("  [{}]".format(updated))

    def greeting(self, name):
        """greet 5 times"""
        for i in range(5):
            print("hello, " + name)

kaonashi = Kaonashi()
