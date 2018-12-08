from flask import Flask, request, url_for, render_template, make_response, redirect
from model.tournament_model import TournamentModel
from model.song_tournament_model import SongTournamentModel
class TournamentController(object):

    def __init__(self, connection, tournament_id):
        print("Hello TournamentController")
        self.tournament_model = TournamentModel(connection)
        self.song_tournament_model = SongTournamentModel(connection)
        self.tournament_id = tournament_id

    def init(self):
        # print(request.cookies.get('username'))
        song_tournament = self.song_tournament_model.get_all_songs_by_tournament(self.tournament_id)
        tournament = self.tournament_model.get_one(self.tournament_id)
        print(song_tournament)
        resp = make_response(
            render_template(
                'tournament.html',
                tournament = tournament,
                song_tournaments = song_tournament
            )
        )
        resp.set_cookie('usernametwo', 'theusername')

        return resp
