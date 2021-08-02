import random
from otree.api import *
import numpy as np
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
    market_value = models.IntegerField()
    market_price = models.FloatField()
    point_for_earning = models.FloatField()

def make_price_field():
    return models.FloatField(
        min=0, max=6,
        blank=True,
    )

def make_quantity_field():
    return models.IntegerField(
        min=0, max=150000,
        blank=True
    )


class Player(BasePlayer):
    price1 = make_price_field()
    quantity1 = make_quantity_field()
    price2 = make_price_field()
    quantity2 = make_quantity_field()
    price3 = make_price_field()
    quantity3 = make_quantity_field()
    combined_earnings = models.IntegerField()
    player_total_bid_amount = models.FloatField()
    player_total_bid_number = models.IntegerField()
    market_signal = models.StringField()
    current_budget = models.FloatField()
    player_total_point_earning = models.FloatField()
    player_quantity_purchased = models.IntegerField()
    player_point_earning = models.FloatField()
    additional_cost = models.FloatField()

    cumulative_quantity_above_market_price = models.FloatField()
    cumulative_quantity_at_market_price = models.FloatField()



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
            player.current_budget = previous_round.current_budget - previous_round.player_point_earning

        player_signal_condition = player.id_in_group
        player.market_signal = Constants.signal_list[player.id_in_group-1][player.round_number-1]


class ResultsWaitPage(WaitPage):
    #after_all_players_arrive = 'set_payoffs'
    @staticmethod
    def after_all_players_arrive(group: Group):
        # Initial variable settings
        total_bid_number = 0
        total_bidding = 0
        market_value = 1
        market_price = 0
        full_response_set = []

        # Get each player information (responses)
        for player in group.get_players():
            # get price and quantity responses incomplete pairs will be coded -99
            try:
                bid1_price = round(player.price1,2)
                bid1_quantity = round(player.quantity1,2)
            except TypeError:
                bid_price = -99
                bid1_quantity = -99
            try:
                bid2_price = round(player.price2,2)
                bid2_quantity = round(player.quantity2,2)
            except TypeError:
                bid2_price = -99
                bid2_quantity = -99
            try:
                bid3_price = round(player.price3,2)
                bid3_quantity = round(player.quantity3,2)
            except TypeError:
                bid3_price = -99
                bid3_quantity = -99

            # Each player's response matrix
            player_response_set = [[player.id_in_group, 1, bid1_price, bid1_quantity],
                                   [player.id_in_group, 2, bid2_price, bid2_quantity],
                                   [player.id_in_group, 3, bid3_price, bid3_quantity]]
            player_response_set_sorted = sorted(player_response_set, key=lambda x:x[2], reverse=True)
            player_response_set_clean = [pairs for pairs in player_response_set_sorted if -99 not in pairs]
            full_response_set.extend(player_response_set_clean)

            # Total Number of Bids of each player
            player_total_bid_number = 0
            for i in player_response_set_clean:
                player_total_bid_number += i[3]
            player.player_total_bid_number = player_total_bid_number

            # Total bids amount of each player
            player_total_bid_amount = 0
            for i in player_response_set_clean:
                player_total_bid_amount += i[2]*i[3]
            player.player_total_bid_amount = player_total_bid_amount

            total_bid_number += player_total_bid_number
            total_bidding += player_total_bid_amount
            if player.market_signal == 'High':
                market_value += 1
        # Group-level Values
        # Get Market Value of each round
        full_response_set_sorted = sorted(full_response_set, key=lambda x: x[2], reverse=True)
        all_quantity_list = []
        for i in full_response_set_sorted:
            all_quantity_list.append(i[3])
        all_cumulative_quantity = np.cumsum(all_quantity_list)

        # Assign group-level market price and market value
        if total_bid_number <= Constants.total_share:
            market_price = 0 #if total bid quantity is less than available quantity, market price set to zero
        else:
            first_point_after_even_point = np.min(np.where(np.array(all_cumulative_quantity) > Constants.total_share))
            market_price = full_response_set_sorted[first_point_after_even_point][2] #otherwise, market price is the highest submitted price where submitted total quantity exceeds the available quantity
        group.market_price = market_price
        group.point_for_earning = market_value - market_price
        group.total_bid_number = total_bid_number
        group.total_bidding = total_bidding
        group.market_value = market_value

        p1_quantity_purchased = 0
        p2_quantity_purchased = 0
        cumulative_quantity_above_market_price = 0
        total_at_market_price = 0
        for i in full_response_set_sorted:
            if i[2] == market_price:
                total_at_market_price += i[3]

        for i in full_response_set_sorted:
            if i[2] > market_price:
                if i[0] == 1: #i[0] indicates player ID
                    p1_quantity_purchased += i[3] # i[2] indicates player's quantity submitted at the paired price
                    cumulative_quantity_above_market_price += i[3]
                elif i[0] == 2:
                    p2_quantity_purchased += i[3]
                    cumulative_quantity_above_market_price += i[3]
            elif i[2] == market_price: # i[2] indicates player's price submitted
                if i[0] == 1:
                    p1_quantity_purchased += round((Constants.total_share - cumulative_quantity_above_market_price) * (i[3]/total_at_market_price))
                elif i[0] == 2:
                    p2_quantity_purchased += round((Constants.total_share - cumulative_quantity_above_market_price) * (i[3]/total_at_market_price))
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.player_quantity_purchased = p1_quantity_purchased
            p2.player_quantity_purchased = p2_quantity_purchased

        # penalty for bidding more than 100,000
        p1 = p1.group.get_player_by_id(1)
        p2 = p2.group.get_player_by_id(2)
        if p1.player_total_bid_number > 100000:
            p1.additional_cost = 5000
        else:
            p1.additional_cost = 0
        p1.player_point_earning = round(group.point_for_earning * p1_quantity_purchased - p1.additional_cost, 2)

        if p2.player_total_bid_number > 100000:
            p2.additional_cost = 5000
        else:
            p2.additional_cost = 0
        p2.player_point_earning = round(group.point_for_earning * p2_quantity_purchased - p2.additional_cost, 2)


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
