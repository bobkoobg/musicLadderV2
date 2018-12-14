class SongModel(object):

    def __init__(self, connection):
        self.connection = connection

    def insert(self, data):
        try:
            cursor_obj = self.connection.cursor(dictionary=True)
            statement = "INSERT INTO song_TBL (title,url,user_id) \
                VALUES (%s,%s,1)"
            cursor_obj.execute(statement, (data['song-title'],data['song-url'],))
            return True
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
            return []
