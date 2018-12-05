import mysql.connector

class GameModel(object):

    def __init__(self, connection):
        print("Hello GameModel")
        self.connection = connection

    def update_game(self, data):
        print("BIM BAM BUKI")
        print(data)
        print("")

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
