import mysql.connector

class GameModel(object):

    def __init__(self, connection):
        print("Hello GameModel")
        self.connection = connection

    def get_games_by_song_id(self, tournament_id, song_id):
        try:
            cursor_obj = self.connection.cursor(dictionary=True)
            statement = "SELECT * FROM game_TBL \
                WHERE tournament_id = %s and \
                ( song_left_id = %s OR song_right_id = %s) and state = 1 \
                ORDER BY id"
            input = (tournament_id,song_id, song_id)
            cursor_obj.execute(statement, input)
            return cursor_obj.fetchall()
        except mysql.connector.Error as error :
            print("Failed to execute query q: {0}".format(error))
            return []

    def get_games_by_tournament_id(self, tournament_id, state):
        try:
            cursor_obj = self.connection.cursor(dictionary=True)
            statement = "SELECT g.id, g.tournament_id, g.user_id, \
                    g.state, g.round, g.song_left_id, s1.title as s1title, s1.url as s1url, \
                    g.song_left_before_rating, g.song_left_after_rating, \
                    g.song_left_score, g.song_right_score, g.song_right_after_rating, \
                    g.song_right_before_rating, g.song_right_id, s2.title as s2title, \
                    s2.url as s2url, g.creation_time, g.modification_time \
            	FROM game_TBL AS g \
            	INNER JOIN song_TBL AS s1 \
            		ON g.song_left_id = s1.id \
            	INNER JOIN song_TBL AS s2 \
            		ON g.song_right_id = s2.id \
            	WHERE g.tournament_id = %s AND g.state = %s\
                ORDER BY g.round ASC"
            input = (tournament_id,state,)
            cursor_obj.execute(statement, input)
            return cursor_obj.fetchall()
        except mysql.connector.Error as error :
            print("Failed to execute query q: {0}".format(error))
            return []

    def update_game(self, data):
        try:
            cursor_obj = self.connection.cursor(prepared=True)
            tournament_statement = "UPDATE game_TBL \
               SET song_left_before_rating = ?, song_left_after_rating = ?, song_left_score = ?, \
               song_right_score = ?, song_right_after_rating = ?, song_right_before_rating = ? \
               WHERE id = ? AND tournament_id = ? AND song_left_id = ? AND song_right_id = ?"
            cursor_obj.execute(tournament_statement, (
                data['song_left_before_rating'],
                data['song_left_after_rating'],
                data['song_left_score'],
                data['song_right_score'],
                data['song_right_after_rating'],
                data['song_right_before_rating'],
                data['id'],
                data['tournament_id'],
                data['song_left_id'],
                data['song_right_id'],
            ))
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
            return False
