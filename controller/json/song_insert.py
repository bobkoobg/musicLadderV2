from flask import Flask, request, url_for, render_template, make_response, redirect

from model.song_model import SongModel

import json

class SongInsert(object):

    def __init__(self, connection):
        self.song_model = SongModel(connection)
        self.req_data = json.loads(request.data)

    def init(self):
        print(self.req_data)
        self.song_model.insert({
            'song-title': self.req_data['song-title'],
            'song-url': self.req_data['song-url']
        })
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
