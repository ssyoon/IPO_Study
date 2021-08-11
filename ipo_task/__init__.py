import random
from otree.api import *
import numpy as np
import random
c = cu

doc = ''
class Constants(BaseConstants):
    players_per_group = 2
    num_rounds = 2
    name_in_url = 'IPO_Study'
    total_share = 100000
    fixed_market_price = 1.94
    uniform_informed_endowment = 350000
    uniform_uninformed_endowment = 400000
    fixed_informed_endowment = 100000
    fixed_uninformed_endowment = 150000
    uniform_uninformed_max = 150000
    uniform_informed_max = 80000
    fixed_uninformed_max = 150000
    fixed_informed_max = 80000
    task_list = ["Uniform", "Fixed"]
    signal_list = [
        random.choices(["Low", "High"], [20,20], k=20),
        random.choices(["Low", "High"], [20,20], k=20),
        random.choices(["Low", "High"], [20,20], k=20),
        ['Uninformed']*20
    ]



class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_bid_number = models.IntegerField()
    total_bidding = models.FloatField()
    market_value = models.IntegerField()
    market_price = models.FloatField()
    point_for_earning = models.FloatField()
    task_type = models.StringField()

def make_price_field():
    return models.FloatField(
        min=0, max=6,
        blank=True,
    )

def make_quantity_field():
    return models.IntegerField(
        min=0,
        blank=True
    )


class Player(BasePlayer):
    attention_value_question = models.IntegerField(label =  "If the number of good signals in this round is 2, what is the market value of each unit of the good?")
    attention_price_question = models.IntegerField(label="If in this round the players' bids are as those in the table below, what is the market price?")
    attention_allocation_question = models.IntegerField(label="If in this round the players' bids are as those in the table below, how many units player A will be allocated?")
    attention_earning_question = models.IntegerField(label="Suppose the value of each unit of the goods is 3, how many point earnings does Player A will obtain?")
    task_type = models.StringField()
    fixed_quantity = models.IntegerField(min=0)
    price1 = models.FloatField(min=0, max=6)
    quantity1 = models.IntegerField(min=0)
    price2 = make_price_field()
    quantity2 = make_quantity_field()
    price3 = make_price_field()
    quantity3 = make_quantity_field()
    price4 = make_price_field()
    quantity4 = make_quantity_field()
    price5 = make_price_field()
    quantity5 = make_quantity_field()
    price6 = make_price_field()
    quantity6 = make_quantity_field()
    combined_earnings = models.IntegerField()
    player_total_bid_amount = models.FloatField()
    player_total_bid_number = models.IntegerField()
    market_signal = models.StringField()
    current_budget = models.FloatField()
    player_total_point_earning = models.FloatField()
    player_quantity_purchased = models.IntegerField()
    player_point_earning = models.FloatField()
    additional_cost = models.FloatField()
    starting_budget = models.FloatField()
    max_quantity = models.FloatField()
    cumulative_quantity_above_market_price = models.FloatField()
    cumulative_quantity_at_market_price = models.FloatField()


## Page1: Instructions ===============================================
class Instructions(Page):
    form_model = "player"
    form_fields = ["attention_value_question", "attention_price_question", "attention_allocation_question", "attention_earning_question"]
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True

    @staticmethod
    def vars_for_template(player: Player):
        task_type_index = player.group.id_in_subsession % 2
        player.task_type = Constants.task_list[task_type_index]
        player.group.task_type = Constants.task_list[task_type_index]

    @staticmethod
    def error_message(player: Player, values):
        if values["attention_value_question"] == 3 and values["attention_price_question"] == 0 and values["attention_allocation_question"] == 15 and values["attention_earning_question"] == 45:
            pass
        else:
            return "You submitted wrong answers. Please provide correct answers. If you want to read the instructions again, please go back to the previou spage"


class WaitForOtherPlayer(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        pass


## Page2A: Fixed Condition ===============================================
class FixedBid(Page):
    form_model = 'player'
    form_fields = ['fixed_quantity']

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).task_type == "Fixed":
            return True

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number != 1:
            player.task_type = player.in_round(1).task_type
        if player.id_in_group == 4:
            player.starting_budget = Constants.fixed_uninformed_endowment
            player.current_budget = Constants.fixed_uninformed_endowment
            player.max_quantity = Constants.fixed_uninformed_max
        else:
            player.starting_budget = Constants.fixed_informed_endowment
            player.current_budget = Constants.fixed_informed_endowment
            player.max_quantity = Constants.fixed_informed_max
        if player.round_number != 1:
            previous_round = player.in_round(player.round_number - 1)
            player.current_budget = previous_round.current_budget + previous_round.player_point_earning

        task_type_index = player.group.id_in_subsession % 2
        player.task_type = Constants.task_list[task_type_index]
        player.group.task_type = Constants.task_list[task_type_index]
        player_signal_condition = player.id_in_group
        player.market_signal = Constants.signal_list[player.id_in_group - 1][player.round_number - 1]


## Page2B: Uniform Condition ===============================================
class UniformBid(Page):
    form_model = 'player'
    form_fields = ['price1', 'quantity1', 'price2', 'quantity2', 'price3', 'quantity3', 'price4', 'quantity4', 'price5', 'quantity5', 'price6', 'quantity6']

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).task_type == "Uniform":
            return True

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number != 1:
            player.task_type = player.in_round(1).task_type

        if player.id_in_group == 4:
            player.starting_budget = Constants.uniform_uninformed_endowment
            player.current_budget = Constants.uniform_uninformed_endowment
            player.max_quantity = Constants.uniform_uninformed_max
        else:
            player.starting_budget = Constants.uniform_informed_endowment
            player.current_budget = Constants.uniform_informed_endowment
            player.max_quantity = Constants.uniform_informed_max

        if player.round_number != 1:
            previous_round = player.in_round(player.round_number-1)
            player.current_budget = previous_round.current_budget + previous_round.player_point_earning
            player_signal_condition = player.id_in_group
            player.market_signal = Constants.signal_list[player.id_in_group - 1][player.round_number - 1]


    # Custom Validation
    @staticmethod
    def error_message(player: Player, values):
        player_signal_in_game = Constants.signal_list[player.id_in_group-1][player.round_number-1]
        all_response_list = [[values['price1'], values['quantity1']],
                             [values['price2'], values['quantity2']],
                             [values['price3'], values['quantity3']],
                             [values['price4'], values['quantity4']],
                             [values['price5'], values['quantity5']],
                             [values['price6'], values['quantity6']]]
        total_submitted_quantity = sum([i[1] for i in all_response_list if None not in i])
        if player_signal_in_game == "Uninformed":
            if total_submitted_quantity > Constants.uniform_uninformed_max:
                return "You submitted " + str(total_submitted_quantity) + " which is above the maximum possible bid quantity " + str(Constants.uniform_uninformed_max)
        if player_signal_in_game != "Uninformed":
            if total_submitted_quantity > Constants.uniform_informed_max:
                return "You submitted " + str(total_submitted_quantity) + " which is above the maximum possible bid quantity " + str(Constants.uniform_informed_max)


# Page3: Result Page_Uniform =======================================================================
class ResultsWaitPageUniform(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        if player.task_type == "Uniform":
            return True

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
                bid1_quantity = player.quantity1
            except TypeError:
                bid_price = -99
                bid1_quantity = -99
            try:
                bid2_price = round(player.price2,2)
                bid2_quantity = player.quantity2
            except TypeError:
                bid2_price = -99
                bid2_quantity = -99
            try:
                bid3_price = round(player.price3,2)
                bid3_quantity = player.quantity3
            except TypeError:
                bid3_price = -99
                bid3_quantity = -99
            try:
                bid4_price = round(player.price4, 2)
                bid4_quantity = player.quantity4
            except TypeError:
                bid4_price = -99
                bid4_quantity = -99
            try:
                bid5_price = round(player.price5, 2)
                bid5_quantity = player.quantity5
            except TypeError:
                bid5_price = -99
                bid5_quantity = -99
            try:
                bid6_price = round(player.price6, 2)
                bid6_quantity = player.quantity6
            except TypeError:
                bid6_price = -99
                bid6_quantity = -99

            # Each player's response matrix
            player_response_set = [[player.id_in_group, 1, bid1_price, bid1_quantity],
                                   [player.id_in_group, 2, bid2_price, bid2_quantity],
                                   [player.id_in_group, 3, bid3_price, bid3_quantity],
                                   [player.id_in_group, 4, bid4_price, bid4_quantity],
                                   [player.id_in_group, 5, bid5_price, bid5_quantity],
                                   [player.id_in_group, 6, bid6_price, bid6_quantity]]
            player_response_set_sorted = sorted(player_response_set, key=lambda x: x[2], reverse=True)
            player_response_set_clean = [pairs for pairs in player_response_set_sorted if -99 not in pairs]

            # Tring to impose max quantities and current budget
            player_running_quantity = 0
            player_running_bid_amount = 0
            player_over_quantity = 0
            player_add_cost = 0
            player_over_budget = 0
            for i in player_response_set_clean:
                player_running_quantity += i[3]
                player_running_bid_amount += i[2] * i[3]
                if player_over_quantity == 1:
                    i[3] = 0
                elif player_running_quantity > player.max_quantity:
                    player_over_quantity = 1
                    i[3] += player.max_quantity - player_running_quantity
                    player_running_quantity = player.max_quantity
                if player_running_quantity > 100000:
                    player_add_cost = 5000
                if player_over_budget == 1:
                    i[3] = 0
                elif player_running_bid_amount > player.current_budget - player_add_cost:
                    player_over_budget = 1
                    i[3] += round((player.current_budget - player_add_cost - player_running_bid_amount) / i[2], 2)  # This cap could reduce quantity below addtitional cost threshold, but it seems too complex to compute or explain to players

            #player_response_set_sorted = sorted(player_response_set_clean, key=lambda x: x[2], reverse=True)
            full_response_set.extend(player_response_set_clean)

            # Total Number of Bids of each player
            player_total_bid_number = int(0)
            for i in player_response_set_clean:
                player_total_bid_number += int(i[3])
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
        p3_quantity_purchased = 0
        p4_quantity_purchased = 0
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
                elif i[0] == 3:
                    p3_quantity_purchased += i[3]
                    cumulative_quantity_above_market_price += i[3]
                elif i[0] == 4:
                    p4_quantity_purchased += i[3]
                    cumulative_quantity_above_market_price += i[3]
            elif i[2] == market_price: # i[2] indicates player's price submitted
                if i[0] == 1:
                    p1_quantity_purchased += round((Constants.total_share - cumulative_quantity_above_market_price) * (i[3]/total_at_market_price))
                elif i[0] == 2:
                    p2_quantity_purchased += round((Constants.total_share - cumulative_quantity_above_market_price) * (i[3]/total_at_market_price))
                elif i[0] == 3:
                    p3_quantity_purchased += round((Constants.total_share - cumulative_quantity_above_market_price) * (i[3]/total_at_market_price))
                elif i[0] == 4:
                    p4_quantity_purchased += round((Constants.total_share - cumulative_quantity_above_market_price) * (i[3]/total_at_market_price))
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p3 = group.get_player_by_id(3)
            p4 = group.get_player_by_id(4)
            p1.player_quantity_purchased = p1_quantity_purchased
            p2.player_quantity_purchased = p2_quantity_purchased
            p3.player_quantity_purchased = p3_quantity_purchased
            p4.player_quantity_purchased = p4_quantity_purchased

        # penalty for bidding more than 100,000
        p1 = p1.group.get_player_by_id(1)
        p2 = p2.group.get_player_by_id(2)
        p3 = p2.group.get_player_by_id(3)
        p4 = p2.group.get_player_by_id(4)
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

        if p3.player_total_bid_number > 100000:
            p3.additional_cost = 5000
        else:
            p3.additional_cost = 0
        p3.player_point_earning = round(group.point_for_earning * p3_quantity_purchased - p3.additional_cost, 2)

        if p4.player_total_bid_number > 100000:
            p4.additional_cost = 5000
        else:
            p4.additional_cost = 0
        p4.player_point_earning = round(group.point_for_earning * p4_quantity_purchased - p4.additional_cost, 2)


class ResultsWaitPageFixed(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        if player.task_type == "Fixed":
            return True

    @staticmethod
    def after_all_players_arrive(group: Group):
        # Initial variable settings
        total_bid_number = 0
        market_value = 1
        market_price = Constants.fixed_market_price

        # Get each player information (responses)
        for player in group.get_players():
            # Total submitted quantity at the market price in the group
            total_bid_number += player.fixed_quantity
            # Calculate Market Value
            if player.market_signal == "High":
                market_value += 1
        group.market_value = market_value
        group.market_price = market_price
        group.total_bid_number = total_bid_number
        quantity_above_total_share = total_bid_number - Constants.total_share
        point_for_earning = market_value - market_price
        group.point_for_earning = point_for_earning


        for player in group.get_players():
            if player.group.total_bid_number <= Constants.total_share:
                player.player_quantity_purchased = player.fixed_quantity
                if player.fixed_quantity > 100000:
                    player.additional_cost = 5000
                else:
                    player.additional_cost = 0
            elif player.group.total_bid_number > Constants.total_share:
                player.player_quantity_purchased = round(Constants.total_share * (player.fixed_quantity / total_bid_number))
                if player.fixed_quantity > 100000:
                    player.additional_cost = 5000
                else:
                    player.additional_cost = 0

            # Point Earning
            player.player_point_earning = (player.player_quantity_purchased * point_for_earning) - player.additional_cost


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




page_sequence = [Instructions, FixedBid, UniformBid, ResultsWaitPageUniform, ResultsWaitPageFixed, Results, CombinedResults]
