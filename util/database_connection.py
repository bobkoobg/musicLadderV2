import mysql.connector
from util import const

class DatabaseConnector(object):

    def __init__(self):
        pass

    def get_connection(self):
        return mysql.connector.connect(
          host = const.MYSQL_HOST,
          database = const.MYSQL_DATABASE,
          user = const.MYSQL_USER,
          password = const.MYSQL_PASSWORD,
          autocommit = True, #do not commit at the end of update
          use_pure = True #disable CEXT support
        )
