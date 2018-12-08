from flask import Flask, request, url_for, render_template, make_response, redirect, g
import json

from util.database_connection import DatabaseConnector
from controller.front_controller import FrontController
from controller.tournament_controller import TournamentController


def get_connection():
    db_conn = DatabaseConnector()
    return db_conn.get_connection()

app = Flask(__name__,
    template_folder = "theme/template"
)

@app.before_request
def before_request():
    g.connection = get_connection()

@app.route('/')
def front():
    controller = FrontController(g.connection)
    return controller.init()

@app.route('/tournament/<int:tournament_id>')
def tournament(tournament_id=None):
    controller = TournamentController(g.connection, tournament_id)
    return controller.init()
    return 'tournament_id {0}'.format(tournament_id)

if __name__ == "__main__":
    app.run(debug=True)


    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     print(request.json)
    #     print(request.args.get('bob'))
    #
    #     if request.method == 'POST':
    #         return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    #     else:
    #         return "Show the login form"
