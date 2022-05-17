from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(
        verbose_name="I provide consent",
        choices=[
            [1, 'Yes, I understand the explanation provided and agree to participate'],
            [0, 'No, I do not want to participate']
        ]
    )


# T1: Consent Form - Rutgers
class Consent_Rutgers(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['consent']


class Consent_Disagree(Page):
    @staticmethod
    def is_displayed(player): # Display this page only if paricipant disagrees with the terms.
        if player.consent == 0:
            return True




page_sequence = [Consent_Rutgers, Consent_Disagree]
