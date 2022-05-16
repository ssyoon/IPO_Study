from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    NAME_IN_URL = 'ipo_instruction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
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
            if values["attention_value_question"] == 3 and values["attention_price_question"] == 0 and values["attention_allocation_question"] == 15 and values["attention_earning_question"] == 45:
                pass
            else:
                return "You submitted wrong answers or did not complete all questions. Please provide correct answers. If you want to read the instructions again, please go back to the previou spage"
        elif player.task_type == "Fixed":
            if values["attention_value_question"] == 3 and values["attention_allocation_question"] == 25 and values["attention_earning_question"] == 20:
                pass
            else:
                return "You submitted wrong answers or did not complete all questions. Please provide correct answers. If you want to read the instructions again, please go back to the previou spage"



page_sequence = [Instructions]
