import mysql.connector

class TournamentModel(object):

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        try:
            cursor_obj = self.connection.cursor(dictionary=True)
            tournament_statement = "SELECT t.id, t.title, t.tournament_type, t.state, \
                t.round, t.user_id, u.alias, t.creation_time, t.modification_time \
                FROM tournament_TBL AS t \
                    INNER JOIN user_TBL AS u \
                        ON u.id = t.user_id \
                ORDER BY creation_time DESC"
            cursor_obj.execute(tournament_statement)
            return cursor_obj.fetchall() #yields a list
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
            return []

    def get_one(self, tournament_id):
        try:
            cursor_obj = self.connection.cursor(dictionary=True)
            tournament_statement = "SELECT t.id, t.title, t.tournament_type, t.state, \
                t.round, t.user_id, u.alias, t.creation_time, t.modification_time \
                FROM tournament_TBL AS t \
                    INNER JOIN user_TBL AS u \
                        ON u.id = t.user_id \
                ORDER BY creation_time DESC"
            cursor_obj.execute(tournament_statement)
            return cursor_obj.fetchone() #yields a list
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
            return []
