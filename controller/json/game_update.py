from flask import Flask, request, url_for, render_template, make_response, redirect

from model.song_tournament_model import SongTournamentModel
from model.game_model import GameModel
from util.rating_calculator import EloCalculator

import json

class GameUpdate(object):

    def __init__(self, connection, game_id):
        self.song_tournament_model = SongTournamentModel(connection)
        self.elo_calc = EloCalculator()
        self.game_model = GameModel(connection)
        self.req_data = json.loads(request.data)
        self.game_id = game_id

    def init(self):

        song_left_new_rating = self.song_tournament_model.get_current_rating_by_id(self.req_data['tournament-id'],self.req_data['song-left-id'])
        song_right_new_rating = self.song_tournament_model.get_current_rating_by_id(self.req_data['tournament-id'],self.req_data['song-right-id'])

        print(self.req_data)

        result = self.elo_calc.get_result(
            song_left_new_rating['rating'],
            self.req_data['song-left-score'],
            True, True,
            self.req_data['song-right-score'],
            song_right_new_rating['rating']
        )

        self.game_model.update_game({
            'id': self.game_id,
            'tournament_id' : self.req_data['tournament-id'],
            'song_left_id' : self.req_data['song-left-id'],
            'song_left_before_rating' : song_left_new_rating['rating'],
            'song_left_after_rating' : result[0][0],
            'song_left_score' : self.req_data['song-left-score'],
            'song_right_score' : self.req_data['song-right-score'],
            'song_right_after_rating' : result[1][0],
            'song_right_before_rating' : song_right_new_rating['rating'],
            'song_right_id' : self.req_data['song-right-id']
        })
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
