from flask import Flask, request, url_for, render_template, make_response, redirect

from util.tournament_matchup import InitializeCupTournament

import json

class TournamentCupCreate(object):

    def __init__(self, connection, tournament_id):
        self.init_cup_tour = InitializeCupTournament(connection,tournament_id)

    def init(self):

        (tournament_tuple,games_list,songs_list) = self.init_cup_tour.initialize()
        print(tournament_tuple,games_list,songs_list)
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
