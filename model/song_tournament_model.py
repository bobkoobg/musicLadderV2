import mysql.connector

class SongTournamentModel(object):

    def __init__(self, connection):
        self.connection = connection

    def get_all_songs_by_tournament(self, tournament_id):
        try:
            cursor_obj = self.connection.cursor(dictionary=True)
            statement = "SELECT st.song_id, s.title, u.alias, st.rating, st.matches, st.wins, st.draws, st.losses \
                FROM song_tournament_TBL AS st \
                INNER JOIN user_TBL AS u \
                    ON u.id = st.user_id \
                INNER JOIN song_TBL AS s \
                    ON s.id = st.song_id \
                WHERE st.tournament_id = %s \
                ORDER BY st.rating DESC"
            # cursor_obj.execute(statement,(tournament_id,))
            cursor_obj.execute(statement, (tournament_id,))
            # cursor_obj.execute(statement)
            return cursor_obj.fetchall()
        except mysql.connector.Error as error :
            print("Failed to execute query zzz: {0}".format(error))
            return []

    def get_current_rating_by_id(self, tournament_id, song_id):
        try:
            cursor_obj = self.connection.cursor(dictionary=True)

            tournament_statement = "SELECT rating \
                FROM song_tournament_TBL \
                WHERE tournament_id = ? AND song_id = ? AND active = 1"
            cursor_obj.execute(tournament_statement, (tournament_id,song_id,))
            return cursor_obj.fetchone()
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
            return {}
