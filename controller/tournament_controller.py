from flask import Flask, request, url_for, render_template, make_response, redirect
from model.tournament_model import TournamentModel
from model.song_tournament_model import SongTournamentModel
from model.game_model import GameModel

import json
class TournamentController(object):

    def __init__(self, connection, tournament_id):
        print("Hello TournamentController")
        self.tournament_model = TournamentModel(connection)
        self.song_tournament_model = SongTournamentModel(connection)
        self.game_model = GameModel(connection)
        self.tournament_id = tournament_id

    def init(self):
        song_tournament = self.song_tournament_model.get_all_songs_by_tournament(self.tournament_id)
        games_played_tournament = self.game_model.get_games_by_tournament_id(1,1)
        games_future_tournament = self.game_model.get_games_by_tournament_id(1,0)

        song_tournament_rating = {}
        for st_val in song_tournament:
            games_per_song = self.game_model.get_games_by_song_id(self.tournament_id,st_val['song_id'])
            song_ratings = []

            if len(games_per_song) > 0:
                if st_val['song_id'] == games_per_song[0]['song_left_id']:
                    song_ratings.append(games_per_song[0]['song_left_before_rating'])
                elif st_val['song_id'] == games_per_song[0]['song_right_id']:
                    song_ratings.append(games_per_song[0]['song_right_before_rating'])

                for gs_val in games_per_song:
                    if st_val['song_id'] == gs_val['song_left_id']:
                        song_ratings.append(gs_val['song_left_after_rating'])
                    elif st_val['song_id'] == gs_val['song_right_id']:
                        song_ratings.append(gs_val['song_right_after_rating'])

            song_tournament_rating[st_val['song_id']] = {
                'song_ratings': song_ratings,
                'song_title': st_val['title']
            }

        tournament = self.tournament_model.get_one(self.tournament_id)
        resp = make_response(
            render_template(
                'tournament.html',
                tournament = tournament,
                song_tournaments = song_tournament,
                song_tournament_rating = song_tournament_rating,
                games_played_tournament = games_played_tournament,
                games_future_tournament = games_future_tournament
            )
        )
        resp.set_cookie('usernametwo', 'theusername')

        return resp
