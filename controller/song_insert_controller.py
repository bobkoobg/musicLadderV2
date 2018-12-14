from flask import render_template, make_response
from model.song_model import SongModel
class SongInsertController(object):

    def __init__(self, connection):
        print("Hello SongInsertController")
        self.song_model = SongModel(connection)

    def init(self):
        return make_response(render_template('song_insert.html'))
