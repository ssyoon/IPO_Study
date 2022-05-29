from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ipo_instruction'
    players_per_group = None
    num_rounds = 1
    task_list = ["Uniform", "Uniform"]  # we only run the Uniform condition


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    task_type = models.StringField()


class Player(BasePlayer):
    attention_value_question = models.IntegerField(
        label="If the number of good signals in this round is 2, what is the market value of each unit of the good?",
        blank=True)
    attention_price_question = models.IntegerField(
        label="If in this round the players' bids are as those in the table below, what is the market price?",
        blank=True)
    attention_allocation_question = models.IntegerField(
        label="If in this round the players' bids are as those in the table below, how many units player A will be allocated?",
        blank=True)
    attention_earning_question = models.IntegerField(
        label="Suppose the value of each unit of the goods is 3, how many point earnings does Player A will obtain?",
        blan=True)
    task_type = models.StringField()


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
        player.participant.task_type = player.task_type


    @staticmethod
    def error_message(player: Player, values):
        if player.task_type == "Uniform":
            if values["attention_value_question"] == 2 and values["attention_price_question"] == 1 and values["attention_allocation_question"] == 50 and values["attention_earning_question"] == 50:
                pass
            elif values["attention_value_question"] != 2:
                return "You provided a wrong answer to Question 1. Please provide correct answer to proceed. Market value is the number of High value signal + 1"
            elif values["attention_price_question"] != 1:
                return "You provided a wrong answer to Question 2. Please provide correct answer to proceed. If the total quantity bid for in your group is less than the total number of units for sale, the market price will be 0. " \
                       "If the total quantity bid for in your group is greater than the total number of units for sale, the market price will be set as the highest bidding price where the cumulated units bid for exceed the quantity for sale."
            elif values["attention_allocation_question"] != 50:
                return "You provided a wrong answer to Question 3. Please provide correct answer to proceed. If the total quantity bid for in your group exceeds the quantity for sale, the goods will be allotted from the highest bidding price to lower prices until all the units are allocated. " \
                       "The quantity you have bid for above the market price will be fully allocated, those below the market price will be ignored, and those at the market price will be allocated proportionately to fully sell the goods (always rounded to integer)."
            elif values["attention_earning_question"] != 50:
                return "You provided a wrong answer to Question 4. Please provide correct answer to proceed. Points earnings = (the per unit market value - the market price) x the number of units allocated"
            else:
                return "You submitted wrong answers or did not complete all questions. Please provide correct answers. If you need, please carefully read the instructions one more time."
        elif player.task_type == "Fixed":
            if values["attention_value_question"] == 3 and values["attention_allocation_question"] == 25 and values["attention_earning_question"] == 20:
                pass
            else:
                return "You submitted wrong answers or did not complete all questions. Please provide correct answers. If you need, please carefully read the instructions one more time."



page_sequence = [Instructions]
