import random
from otree.api import *
import numpy as np
import random
import math
random.seed(2021) # Seed Number for Randomization
c = cu

doc = ''
class Constants(BaseConstants):
    players_per_group = 4
    num_rounds = 20
    name_in_url = 'IPO_Study'
    total_share = 100000
    fixed_market_price = 1.94
    uniform_informed_endowment = 350000
    uniform_uninformed_endowment = 400000
    uniform_uninformed_max = 80000
    uniform_informed_max = 150000
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
         ['Uninformed'] * 20],
        # Set 4
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20],
        # Set 5
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20],
        # Set 6
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20],
        # Set 7
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20],
        # Set 8
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20],
        # Set 9
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20],
        # Set 10
        [random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         random.choices(["Low", "High"], [20, 20], k=20),
         ['Uninformed'] * 20]
    ] # a set of list of signals (10 sets)


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
    task_type = models.StringField()
    fixed_quantity = models.IntegerField(min=0)
    price1 = models.FloatField()
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
    is_default = models.IntegerField() # this variable is to track the player's bankrupcy status
    is_default_next_round = models.IntegerField()



## Page 1: Wait Page for Grouping ==========================================
class WaitForOtherPlayer(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player):
        player.task_type = player.participant.task_type


## Page 2: Initiating a round ==============================================
class RoundStart(Page):
    form_model = 'player'
    timeout_seconds = 5
    timer_text = 'The next round will start in '

    @staticmethod
    def vars_for_template(player: Player):
        player.task_type = player.participant.task_type
        if player.round_number == 1:
            player.is_default = 0
        else:
            previous_round = player.in_round(player.round_number - 1)
            player.current_budget = previous_round.current_budget + previous_round.player_point_earning
            if player.current_budget > 0:
                player.is_default = 0
            elif player.current_budget <= 0:
                player.is_default = 1



## Page3A: Uniform Condition Bidding ===============================================
class UniformBid(Page):
    form_model = 'player'
    form_fields = ['price1', 'quantity1', 'price2', 'quantity2', 'price3', 'quantity3', 'price4', 'quantity4', 'price5', 'quantity5', 'price6', 'quantity6']

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).task_type == "Uniform" and player.is_default == 0:
            return True

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == 1:
            player.is_default = 0
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

            # Set the max quantity and initial budget
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
        if total_submitted_quantity > player.current_budget:
            return "You submitted a higher total quantity than your current budget. Please double check whether your total submitted bid quantity does not exceed your current budget."
        if sum([i[0] > 6 or i[0] < 0 for i in all_response_list if None not in i]) != 0:
            return "Price can be from 0 to 6 with 0.01 increment."

    @staticmethod
    def js_vars(player: Player): # Creating Variables for the JavaScript in the Page
        if player.round_number == 1:
            player_responses_so_far = ["This is Round 1"]
        else:
            player_responses_so_far = [i.player_point_earning for i in player.in_previous_rounds()]
        all_round_numbers = [i.round_number for i in player.in_all_rounds()]
        uniform_ins_file = open("uniform_instruction.txt", "r")
        fixed_ins_file = open("uniform_instruction.txt", "r")
        return dict(player_results_so_far=player_responses_so_far,
                    all_round_numbers_so_far=all_round_numbers,
                    uniform_ins_text=uniform_ins_file.read(),
                    fixed_ins_text=fixed_ins_file.read(),
                    task_of_player=player.task_type,
                    this_round_number = player.round_number)


# Page2B: Page for Bankrupt Players ================================================================
class BankruptBid(Page):
    form_model = 'player'
    timeout_seconds = 10
    timer_text = 'You will be automatically forwarded to the next page in'

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number != 1 and player.is_default == 1:
            return True

    @staticmethod
    def vars_for_template(player: Player):
        player.task_type = player.in_round(1).task_type
        price_list = [2, 3, 4, 5]
        quantity_list = [3000, 5000, 7000, 10000]
        market_signal_list = ["Low", "High"]
        player.price1 = random.choice(price_list) # we assume that this player bids at a random price (from 2 to 5)
        player.quantity1 = random.choice(quantity_list) # we assume that this player bids a random quantity at the random price
        player.market_signal = random.choice(market_signal_list)


# Page3: Result Page =======================================================================
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
            p3.player_quantity_purchased = int(p3_quantity_purchased)
            p4.player_quantity_purchased = int(p4_quantity_purchased)

        # Penalty for bidding more than 100,000 and Purchased Quantity and Amount
        for player in group.get_players():
            if player.player_total_bid_number > 100000:
                player.additional_cost = 5000
            else:
                player.additional_cost = 0

            # Points earning and end round budget left
            if player.is_default == 0:
                player.player_point_earning = round(group.point_for_earning * player.player_quantity_purchased - player.additional_cost, 2)
                player.round_end_budget_left = player.current_budget + player.player_point_earning
            elif player.is_default == 1:
                player.player_point_earning = 0
                player.round_end_budget_left = 0

            # whether this player is bankrupt after this round
            if player.round_end_budget_left <= 0:
                player.is_default_next_round = 1
            else:
                player.is_default_next_round = 0


class Results(Page):
    timeout_seconds = 30
    timer_text = 'You will be automatically forwarded to the next page in'

    @staticmethod
    def js_vars(player: Player):
        player_responses_so_far = [i.player_point_earning for i in player.in_all_rounds()]
        player_price1_so_far = [i.price1 for i in player.in_all_rounds()]
        player_quantity1_so_far = [i.quantity1 for i in player.in_all_rounds()]
        all_round_numbers = [i.round_number for i in player.in_all_rounds()]
        uniform_ins_file = open("uniform_instruction.txt", "r")
        fixed_ins_file = open("fixed_instruction.txt", "r")
        return dict(player_results_so_far = player_responses_so_far,
                    all_round_numbers_so_far = all_round_numbers,
                    uniform_ins_text = uniform_ins_file.read(),
                    fixed_ins_text = fixed_ins_file.read(),
                    task_of_player = player.task_type,
                    player_price1_so_far = player_price1_so_far,
                    player_quantity1_so_far = player_quantity1_so_far)




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
        final_dollar_amount_temp = round(final_points / 17500, 2) # The exchange rate is 175 points to 1 cent (17500 points to 1 dollar).

        #FINAL DOLLAR AMOUNT ===============================
        if final_dollar_amount_temp > 3:
            player.final_dollar_amount = final_dollar_amount_temp
        elif final_dollar_amount_temp <= 3:
            player.final_dollar_amount = 3
        return {
            "combined_payoff": player.final_dollar_amount
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == Constants.num_rounds:
            player.participant.finished = True
            player.finished = 'True'


page_sequence = [WaitForOtherPlayer, RoundStart, UniformBid, BankruptBid, ResultsWaitPageUniform, Results, CombinedResults]
