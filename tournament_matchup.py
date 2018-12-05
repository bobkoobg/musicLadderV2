import mysql.connector, random, json

from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime

class InitializeCupTournament(object):
    """
        Assumption:
            a tournament exists (in song_TBL)
            N songs exist (in song_tournament_TBL)
        Parameters:
        - tournament_id is the ID of the tournament
    """
    def __init__(self, connection, tournament_id):
        self.tournament_id = tournament_id
        self.connection = connection

    def initialize(self):
        (tournament_obj, songs_list) = self.__get_tournament_owner_and_songs()
        if tournament_obj and len(songs_list) > 0:
            self.__insert_games(
                tournament_obj,
                self.__generate_games_round_robin(songs_list)
            )
        (tournament_tuple,games_list) = self.__query_tournament_matches()
        return (tournament_tuple,games_list,songs_list)

    """
        Get the owner of the tournament and the songs assigned to the tournament
    """
    def __get_tournament_owner_and_songs(self):
        try:
            cursor_obj = self.connection.cursor(prepared=True)

            tournament_statement = "SELECT user_id \
                FROM tournament_TBL \
                WHERE id = ? AND tournament_type = ? AND state = ?"
            cursor_obj.execute(tournament_statement, (self.tournament_id,"cup","open",))
            tournament_obj = cursor_obj.fetchone() #yields a tuple

            cursor_obj.execute("SELECT s.id, s.title, s.url, st.rating, st.matches, st.wins, \
                    st.draws, st.losses, u.full_name, u.alias \
                FROM song_TBL AS s \
                INNER JOIN song_tournament_TBL AS st \
                    ON s.id = st.song_id \
                INNER JOIN user_TBL AS u \
                    ON st.user_id = u.id \
                WHERE st.tournament_id = ? AND st.active = ? \
                ORDER BY st.rating DESC", (self.tournament_id,1,))
            songs_list = cursor_obj.fetchall() #yields a list

            return (tournament_obj, songs_list)
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
            return ((),[])

    """
        Round Robin Algorithm
        https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
        https://stackoverflow.com/questions/26471421/round-robin-algorithm-implementation-java

        Parameters:
        - songs_list - a list of tuples (songs) that must contain unique ID's on index 0.
    """
    def __generate_games_round_robin(self, songs_list = []):
        matches_map = {}

        random.seed(datetime.now())
        random.shuffle(songs_list)

        num_teams = len(songs_list)
        if(num_teams % 2 != 0):
            songs_list.append((-1 ,"" ,"" ,-1 ,-1 ,-1 ,-1 ,-1 ,"" ,""))

        first_elem = songs_list[0]
        songs_list.remove(first_elem)
        num_days = num_teams-1
        half_size = int(num_teams/2)

        num_teams = len(songs_list)

        for day in range(len(songs_list)):
            matches_map[day] = []
            team_idx = day % num_teams

            if songs_list[team_idx][0] > -1:
                matches_map[day].append((songs_list[team_idx][0], first_elem[0]))

            for idx in range(1, half_size):
                first_team = (day + idx) % num_teams
                second_team = (day + num_teams - idx) % num_teams

                if songs_list[first_team][0] > -1 and songs_list[second_team][0] > -1:
                    matches_map[day].append((songs_list[first_team][0],songs_list[second_team][0]))

        return matches_map

    def __insert_games(self, tournament_obj, matches_map):
        try:
            for (day, matches) in matches_map.items():
                for match in matches:
                    cursor_obj = self.connection.cursor(prepared=True)
                    tournament_statement = "INSERT INTO game_TBL  \
                        (tournament_id,round,user_id,song_left_id,song_right_id) VALUES (?, ?, ?, ?, ?)"
                    cursor_obj.execute(tournament_statement, (
                        self.tournament_id,day,tournament_obj[0],match[0],match[1],)
                    )

            tournament_statement = "UPDATE tournament_TBL \
                SET state = ? \
                WHERE id = ?"
            cursor_obj.execute(tournament_statement, (
                "running",self.tournament_id,)
            )
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
            return False
        return True

    def __query_tournament_matches(self):
        games_list = []
        tournament_tuple = ()

        try:
            cursor_obj = self.connection.cursor(prepared=True)
            tournament_statement = "SELECT t.id, t.title, t.tournament_type, t.state, \
                    t.round, t.creation_time, t.modification_time, u.id, u.full_name, \
                    u.alias \
                FROM tournament_TBL AS t \
                INNER JOIN user_TBL AS u \
                    ON t.user_id = u.id \
                WHERE t.id = ? AND t.tournament_type = ? AND t.state = ?"
            cursor_obj.execute(tournament_statement, (self.tournament_id,"cup","running",))
            tournament_tuple = cursor_obj.fetchone() #yields a tuple

            cursor_obj.execute("SELECT g.id, g.tournament_id, g.user_id, uc.alias as ucalias, \
                    g.state, g.round, g.song_left_id, s1.title as s1title, s1.url as s1url, \
                    u1.alias as u1alias, g.song_left_before_rating, g.song_left_after_rating, \
                    g.song_left_score, g.song_right_score, g.song_right_after_rating, \
                    g.song_right_before_rating, g.song_right_id, s2.title as s2title, \
                    s2.url as s2url, u2.alias as u2alias, g.creation_time, g.modification_time \
            	FROM game_TBL AS g \
            	INNER JOIN song_TBL AS s1 \
            		ON g.song_left_id = s1.id \
            	INNER JOIN user_TBL AS u1 \
            		ON s1.user_id = u1.id \
            	INNER JOIN song_TBL AS s2 \
            		ON g.song_right_id = s2.id \
            	INNER JOIN user_TBL AS u2 \
            		ON s2.user_id = u2.id \
            	INNER JOIN user_TBL AS uc \
            		ON g.user_id = uc.id \
            	WHERE g.tournament_id = ? \
                ORDER BY g.round ASC", (self.tournament_id,))
            games_list = cursor_obj.fetchall() #yields a list
        except mysql.connector.Error as error :
            print("Failed to execute query: {0}".format(error))
        return (tournament_tuple,games_list)
