import mysql.connector

class SongTournamentModel(object):

    def __init__(self, connection):
        print("Hello SongTournament")
        self.connection = connection

    def get_current_rating_by_id(self, tournament_id, song_id):
        try:
            cursor_obj = self.connection.cursor(prepared=True)

            tournament_statement = "SELECT rating \
                FROM song_tournament_TBL \
                WHERE tournament_id = ? AND song_id = ? AND active = 1"
            cursor_obj.execute(tournament_statement, (tournament_id,song_id,))
            return cursor_obj.fetchone() #yields a tuple
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))

        return ()
