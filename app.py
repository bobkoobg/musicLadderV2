from flask import Flask, request, url_for, render_template, make_response, redirect, g

from util.database_connection import DatabaseConnector
from controller.front_controller import FrontController
from controller.tournament_controller import TournamentController
from controller.json.tournament_cup_create import TournamentCupCreate
from controller.json.game_update import GameUpdate


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

@app.route('/tournament/<int:tournament_id>', methods=['GET'])
def tournament(tournament_id=None):
    if request.method == 'GET':
        controller = TournamentController(g.connection, tournament_id)
        return controller.init()

@app.route('/init/tournament/cup/<int:tournament_id>', methods=['POST'])
def init_tournament_cup(tournament_id=None):
    if request.method == 'POST':
        controller = TournamentCupCreate(g.connection, tournament_id)
        return controller.init()

@app.route('/game/<int:game_id>', methods=['POST'])
def game_update(game_id=None):
    if request.method == 'POST':
        controller = GameUpdate(g.connection, game_id)
        return controller.init()

if __name__ == "__main__":
    app.run(debug=True)
