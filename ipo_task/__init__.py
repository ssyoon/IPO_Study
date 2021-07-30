import random
from otree.api import *
c = cu

doc = ''
class Constants(BaseConstants):
    players_per_group = 2
    num_rounds = 2
    name_in_url = 'IPO_Study'
    total_share = 100000
    uniform_informed_endowment = 350000
    uniform_uninformed_endowment = 400000
    fixed_informed_endowment = 100000
    fixed_uninformed_endowment = 150000
    signal_list = [
        ['Low', 'High'],
        ['High', 'Low']
    ]


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_bid_number = models.IntegerField()
    total_bidding = models.FloatField()
    market_price = models.IntegerField()


class Player(BasePlayer):
    price1 = models.FloatField()
    quantity1 = models.IntegerField()
    price2 = models.FloatField(blank=True)
    quantity2 = models.IntegerField(blank=True)
    price3 = models.FloatField(blank=True)
    quantity3 = models.IntegerField(blank=True)
    combined_earnings = models.IntegerField()
    player_total_bid_amount = models.FloatField()
    player_total_bid_number = models.IntegerField()
    market_signal = models.StringField()
    current_budget = models.FloatField()

def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = (p1.price1 * p1.quantity1) + (p1.price2 * p1.quantity2) + (p1.price3 * p1.quantity3)
    p2.payoff = (p2.price1 * p2.quantity1) + (p2.price2 * p2.quantity2) + (p2.price3 * p2.quantity3)


class Send(Page):
    form_model = 'player'
    form_fields = ['price1', 'quantity1', 'price2', 'quantity2', 'price3', 'quantity3']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == 1:
            player.current_budget = Constants.uniform_informed_endowment
        else:
            print(player.round_number)
            previous_round = player.in_round(player.round_number-1)
            player.current_budget = previous_round.current_budget - previous_round.player_total_bid_amount

        player_signal_condition = player.id_in_group
        player.market_signal = Constants.signal_list[player.id_in_group-1][player.round_number-1]


class ResultsWaitPage(WaitPage):
    #after_all_players_arrive = 'set_payoffs'
    @staticmethod
    def after_all_players_arrive(group: Group):
        total_bid_number = 0
        total_bidding = 0
        market_price = 1
        for player in group.get_players():
            try:
                bid1_amount = (player.price1 * player.quantity1)
                bid1_quantity = player.quantity1
            except TypeError:
                bid1_quantity = 0
                bid1_amount = 0
            try:
                bid2_quantity = player.quantity2
                bid2_amount = (player.price2 * player.quantity2)
            except TypeError:
                bid2_quantity = 0
                bid2_amount = 0
            try:
                bid3_quantity = player.quantity3
                bid3_amount = (player.price3 * player.quantity3)
            except TypeError:
                bid3_quantity = 0
                bid3_amount = 0
            player.player_total_bid_number = bid1_quantity + bid2_quantity + bid3_quantity
            player.player_total_bid_amount = bid1_amount + bid2_amount + bid3_amount
            total_bid_number += bid1_quantity + bid2_quantity + bid3_quantity
            total_bidding += bid1_amount + bid2_amount + bid3_amount
            if player.market_signal == 'High':
                market_price += 1

        group.total_bid_number = total_bid_number
        group.total_bidding = total_bidding
        group.market_price = market_price


class Results(Page):
    pass

class CombinedResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        all_rounds = player.in_all_rounds()
        combined_payoff = 0
        for p in all_rounds:
            combined_payoff += p.payoff
        return {
            "combined_payoff": combined_payoff
        }




page_sequence = [Send, ResultsWaitPage, Results, CombinedResults]
