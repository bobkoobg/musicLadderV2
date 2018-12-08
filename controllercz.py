#import python internal lib
from random import randint

#import own lib
from util.database_connection import DatabaseConnector
from util.tournament_matchup import InitializeCupTournament
from util.rating_calculator import EloCalculator
from model.game import GameModel
from model.song_tournament import SongTournamentModel

#init
db_conn = DatabaseConnector()
connector = db_conn.get_connection()
elo_calc = EloCalculator()
cup_tournament_id = 2
game_model = GameModel(connector)
song_tournament_model = SongTournamentModel(connector)

init_cup_tour = InitializeCupTournament(connector,cup_tournament_id)
(tournament_tuple,games_list,songs_list) = init_cup_tour.initialize()

# print(">>>")
# print(tournament_tuple)
# for(id, title, url, rating, matches, wins, draws, losses, full_name, alias) in songs_list:
#     print(id, url, rating, matches, wins, draws, losses)

for (id, tournament_id, user_id, ucalias, state, round, song_left_id, s1title, s1url, u1alias, song_left_before_rating, song_left_after_rating, song_left_score, song_right_score, song_right_after_rating, song_right_before_rating, song_right_id, s2title, s2url, u2alias, creation_time, modification_time) in games_list:
    # print(id, state, round, song_left_id, song_left_before_rating, "-vs-" , song_left_before_rating, song_right_id)
    left_score = randint(0, 10)
    right_score = 10 - left_score

    song_left_new_rating = song_tournament_model.get_current_rating_by_id(tournament_id,song_left_id)
    song_right_new_rating = song_tournament_model.get_current_rating_by_id(tournament_id,song_right_id)

    result = elo_calc.get_result(song_left_new_rating[0], left_score, True, True, right_score, song_right_new_rating[0])

    game_model.update_game({
        'id': id,
        'tournament_id' : tournament_id,
        'song_left_id' : song_left_id,
        'song_left_before_rating' : song_left_new_rating[0],
        'song_left_after_rating' : result[0][0],
        'song_left_score' : left_score,
        'song_right_score' : right_score,
        'song_right_after_rating' : result[1][0],
        'song_right_before_rating' : song_right_new_rating[0],
        'song_right_id' : song_right_id
    })


#Setup an example that uses this file and the Elo, rename this to the creator

"""
    All (minimalistic) functionality that is needed:
        -1. Setup server
        0. Font awesome, bootstrap, jquery, node plugin for sliders, for list and reorders
        1. Login
        2. Create User
        3. Get all tournaments
        4. Create tournament (cup only)
        5. Add songs to tournament
        6. Add users to tournament
        6. Generate tournament matchup (this)
        7. Display rankings in tournament
                ordered by rating
           and tournaments' current level
                split the logically by "Past; Days"
        8. Voting page, 1 match at a time with rankings by the side (Volleyball like ratios I guess) -
            updates every 5 seconds + projection below the youtube embedded videos(Elo)
        9. Generate page with final version of the tournament (7)
            present winners

    Future functionality:
        0. Lock tournaments
        1. Update user
        2. Privacy in tournament levels
            3 - Full (Participants and current matches visible only);
            2 - Vote creators;
            1 - Vote creators + projections;
            0 - Free
        3. Create tournament (other types)
        4. Add activity of song within a tourmanent
            (if not active cannot be played against)
        5. Make it work for other purposes than youtube videos
"""
