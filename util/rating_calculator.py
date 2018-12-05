import math
from util import const

class EloCalculator(object):

    def __calculate_new_rating(self,old_rating,score,expected_score,k_factor):
        return old_rating+(k_factor*(score-expected_score))

    def __get_expected_score(self,rating=1000,opponent_rating=1000):
        return float("{0:.2f}".format(1.0 / (1.0 + math.pow(10.0, float(opponent_rating-rating)/400.0))))

    def __get_k_factor(self,rating=1000,is_newbie=False):
        if(is_newbie):
            return const.ELO_K_FACTOR_NEWBIE
        elif(rating < 2400):
            return const.ELO_K_FACTOR_DOWN2400
        elif(rating >= 2400):
            return const.ELO_K_FACTOR_UP2400
        return const.DEFAULT_ELO_K_FACTOR

    def __get_score(self,score=5,opponent_score=5):
        final_score = score/(score+opponent_score)
        game_state = const.DRAW
        if(final_score > 0.5):
            game_state = const.WIN
        elif(final_score < 0.5):
            game_state = const.LOSS
        return (final_score,game_state)

    def __get_new_rating(self,rating=1000,score=5,opponent_score=5,opponent_rating=1000,is_newbie=False):
        (final_score,game_state) = self.__get_score(score,opponent_score)
        k_factor = self.__get_k_factor(rating,is_newbie)
        expected_score = self.__get_expected_score(rating,opponent_rating)
        new_rating = self.__calculate_new_rating(rating,final_score,expected_score,k_factor)
        return (new_rating,game_state)


    def get_result(self, l_rating, l_score, l_newbie, r_newbie, r_score, r_rating):
        left_tuple = self.__get_new_rating(l_rating, l_score, r_score, r_rating, l_newbie)
        right_tuple = self.__get_new_rating(r_rating, r_score, l_score, l_rating, r_newbie)
        return(left_tuple, right_tuple)

    """
        game idea - tournament
        You choose X players
        FFA - Everyone plays against everyone, startup rating 1k, not newbies
        Algoritmn for choosing MATCHES pairs/ split into rounds like a football league
        A chart and current rankings to keep up with the progression
        Roll back functionality to see how the stats looked 2-3 rounds ago
        Trophies
    """
    def __init__(self):
        pass
