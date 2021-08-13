import random
from otree.api import *
import numpy as np
import random
import math
random.seed(2021)
c = cu

doc = ''
class Constants(BaseConstants):
    players_per_group = 4
    num_rounds = 3
    name_in_url = 'IPO_Study'
    total_share = 100000
    fixed_market_price = 1.94
    uniform_informed_endowment = 350000
    uniform_uninformed_endowment = 400000
    fixed_informed_endowment = 100000
    fixed_uninformed_endowment = 150000
    uniform_uninformed_max = 80000
    uniform_informed_max = 150000
    fixed_uninformed_max = 80000
    fixed_informed_max = 150000
    task_list = ["Uniform", "Uniform"]
    signal_list = [
        # Set 1
        [random.choices(["Low", "High"], [20,20], k=20),
        random.choices(["Low", "High"], [20,20], k=20),
        random.choices(["Low", "High"], [20,20], k=20),
        ['Uninformed']*20],
        # Set 2
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20],
        # Set 3
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20]
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
    attention_value_question = models.IntegerField(label =  "If the number of good signals in this round is 2, what is the market value of each unit of the good?", blank=True)
    attention_price_question = models.IntegerField(label="If in this round the players' bids are as those in the table below, what is the market price?", blank=True)
    attention_allocation_question = models.IntegerField(label="If in this round the players' bids are as those in the table below, how many units player A will be allocated?", blank=True)
    attention_earning_question = models.IntegerField(label="Suppose the value of each unit of the goods is 3, how many point earnings does Player A will obtain?", blan=True)
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
    round_end_budget_left = models.FloatField()
    final_dollar_amount = models.FloatField()


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
        if player.task_type == "Uniform":
            if values["attention_value_question"] == 3 and values["attention_price_question"] == 0 and values["attention_allocation_question"] == 15 and values["attention_earning_question"] == 45:
                pass
            else:
                return "You submitted wrong answers or did not complete all questions. Please provide correct answers. If you want to read the instructions again, please go back to the previou spage"
        elif player.task_type == "Fixed":
            if values["attention_value_question"] == 3 and values["attention_allocation_question"] == 25 and values["attention_earning_question"] == 20:
                pass
            else:
                return "You submitted wrong answers or did not complete all questions. Please provide correct answers. If you want to read the instructions again, please go back to the previou spage"



class WaitForOtherPlayer(WaitPage):
    group_by_arrival_time = True


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
        if player.round_number == 1: # First Round
            if player.id_in_group == 4: # UNINFORMED condition
                player.starting_budget = Constants.fixed_uninformed_endowment
                player.current_budget = Constants.fixed_uninformed_endowment
                player.max_quantity = Constants.fixed_uninformed_max
            else: # INFORMED condition
                player.starting_budget = Constants.fixed_informed_endowment
                player.current_budget = Constants.fixed_informed_endowment
                player.max_quantity = Constants.fixed_informed_max
        elif player.round_number != 1: # Other Rounds
            player.task_type = player.in_round(1).task_type
            previous_round = player.in_round(player.round_number - 1)
            player.current_budget = previous_round.current_budget + previous_round.player_point_earning
            if player.id_in_group == 4: # UNINFORMED condition
                player.max_quantity = Constants.fixed_uninformed_max
                player.starting_budget = Constants.fixed_uninformed_endowment
            else: # INFORMED condition
                player.max_quantity = Constants.fixed_informed_max
                player.starting_budget = Constants.fixed_informed_endowment

        # MARKET SIGNAL OF THE PLAYER IN THE ROUND
        signal_list_index = player.group.id_in_subsession % 10
        player.market_signal = Constants.signal_list[signal_list_index][player.id_in_group - 1][player.round_number - 1]


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

        if player.round_number == 1:
            if player.id_in_group == 4:
                player.starting_budget = Constants.uniform_uninformed_endowment
                player.current_budget = Constants.uniform_uninformed_endowment
                player.max_quantity = Constants.uniform_uninformed_max
            else:
                player.starting_budget = Constants.uniform_informed_endowment
                player.current_budget = Constants.uniform_informed_endowment
                player.max_quantity = Constants.uniform_informed_max
        elif player.round_number != 1:
            player.task_type = player.in_round(1).task_type
            previous_round = player.in_round(player.round_number-1)
            player.current_budget = previous_round.current_budget + previous_round.player_point_earning
            if player.id_in_group == 4:
                player.max_quantity = Constants.uniform_uninformed_max
                player.starting_budget = Constants.uniform_uninformed_endowment
            else:
                player.max_quantity = Constants.uniform_informed_max
                player.starting_budget = Constants.uniform_informed_endowment

        # MARKET SIGNAL OF THE PLAYER IN THE ROUND
        signal_list_index = player.group.id_in_subsession % 10
        player.market_signal = Constants.signal_list[signal_list_index-1][player.id_in_group - 1][player.round_number - 1]


    # Custom Validation
    @staticmethod
    def error_message(player: Player, values):
        signal_list_index = player.group.id_in_subsession % 10
        player_signal_in_game = Constants.signal_list[signal_list_index-1][player.id_in_group-1][player.round_number-1]
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
            player_response_set_clean = [pairs for pairs in player_response_set if -99 not in pairs]
            player_response_set_sorted = sorted(player_response_set_clean, key=lambda x: x[2], reverse=True)


            # Combining All Players' Cleaned Response Sets
            full_response_set.extend(player_response_set_sorted)

            # Total Bid Quantity and Amount of Each Player
            player_total_bid_number = int(0)
            player_total_bid_amount = 0
            for i in player_response_set_clean:
                player_total_bid_number += int(i[3])
                player_total_bid_amount += i[2] * i[3]
            player.player_total_bid_number = player_total_bid_number
            player.player_total_bid_amount = player_total_bid_amount

            # Total Bid Quantity and Amount of the Group
            total_bid_number += player_total_bid_number
            total_bidding += player_total_bid_amount
            if player.market_signal == 'High':
                market_value += 1

        # GROUP-LEVEL CALCULATION
        # Get MARKET PRICE of each round
        full_response_set_sorted = sorted(full_response_set, key=lambda x: x[2], reverse=True) # Sort the combined (all players in the group) dataset
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

        # GET PURCHASED QUANTITY OF EACH PLAYER IN THE ROUND
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
            p1.player_quantity_purchased = int(p1_quantity_purchased)
            p2.player_quantity_purchased = int(p2_quantity_purchased)
            p3.player_quantity_purchased = p3_quantity_purchased
            p4.player_quantity_purchased = p4_quantity_purchased

        # Penalty for bidding more than 100,000 and Purchased Quantity and Amount
        for player in group.get_players():
            if player.player_total_bid_number > 100000:
                player.additional_cost = 5000
            else:
                player.additional_cost = 0
            player.player_point_earning = round(group.point_for_earning * player.player_quantity_purchased - player.additional_cost, 2)
            player.round_end_budget_left = player.current_budget + player.player_point_earning



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
        group.point_for_earning = round(market_value - market_price, 2) # POINTS for earning calculatino

        for player in group.get_players():
            if player.group.total_bid_number <= Constants.total_share:
                player.player_quantity_purchased = player.fixed_quantity
                if player.fixed_quantity > 100000:
                    player.additional_cost = 5000
                else:
                    player.additional_cost = 0
            elif player.group.total_bid_number > Constants.total_share:
                player.player_quantity_purchased = int(round(Constants.total_share * (player.fixed_quantity / total_bid_number)))
                if player.fixed_quantity > 100000:
                    player.additional_cost = 5000
                else:
                    player.additional_cost = 0

            # Point Earning
            player.player_point_earning = round((player.player_quantity_purchased * group.point_for_earning) - player.additional_cost, 2)
            player.round_end_budget_left = player.current_budget + player.player_point_earning


class Results(Page):
    timeout_seconds = 30
    timer_text = 'You will be automatically forwarded to the next page in'

    @staticmethod
    def js_vars(player: Player):
        player_responses_so_far = [i.player_point_earning for i in player.in_all_rounds()]
        all_round_numbers = [i.round_number for i in player.in_all_rounds()]
        uniform_ins_file = open("uniform_instruction.txt", "r")
        fixed_ins_file = open("uniform_instruction.txt", "r")
        return dict(player_results_so_far = player_responses_so_far,
                    all_round_numbers_so_far = all_round_numbers,
                    uniform_ins_text = uniform_ins_file.read(),
                    fixed_ins_text = fixed_ins_file.read(),
                    task_of_player = player.task_type)



class CombinedResults(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        #all_rounds = player.in_all_rounds()
        combined_payoff = 0
        #final_points = all_rounds[-1].current_budget + all_rounds[-1].player_point_earning
        final_points = player.round_end_budget_left
        final_dollar_amount_temp = math.ceil(final_points / 250)

        #FINAL DOLLAR AMOUNT ===============================
        if final_dollar_amount_temp > 3:
            player.final_dollar_amount = final_dollar_amount_temp
        elif final_dollar_amount_temp <= 3:
            player.final_dollar_amount = 3
        return {
            "combined_payoff": player.final_dollar_amount
        }




page_sequence = [Instructions, UniformBid, ResultsWaitPageUniform, Results, CombinedResults]
