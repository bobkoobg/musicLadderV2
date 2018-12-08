from flask import Flask, request, url_for, render_template, make_response, redirect
from model.tournament_model import TournamentModel
class FrontController(object):

    def __init__(self, connection):
        print("Hello FrontController")
        self.tournament_model = TournamentModel(connection)

    def init(self):
        # print(request.cookies.get('username'))
        resp = make_response(
            render_template(
                'front.html',
                tournaments = self.tournament_model.get_all(),
                WEBSITE_URL = "http://localhost:5000/"
            )
        )
        resp.set_cookie('usernametwo', 'theusername')

        return resp
