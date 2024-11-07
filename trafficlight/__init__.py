from otree.api import *
import json

doc = """
Traffic light norm task from Kimbrough and Vostroknutov (2016)
"""


class C(BaseConstants):
    NAME_IN_URL = 'trafficlight'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
  
    # event log in json format
    eventLog = models.LongStringField(blank=True)



# Define the ExtraModel for event logs
class EventLog(ExtraModel):
    player = models.Link(Player)
    time = models.FloatField()
    event = models.StringField()
    currentlight = models.IntegerField()
    funds = models.StringField()


# custom export of data
def custom_export(players):
    # header row
    yield ['session_code', 'participant_code', 'round', 'time', 'event', 'currentlight', 'funds']

    # vars
    events = EventLog.filter()
    for x in events:
        player = x.player
        if player is not None:  # Check if player is not None
            participant = player.participant
            session = player.session

            yield [session.code, participant.code, player.round_number, x.time, x.event, x.currentlight, x.funds]


# PAGES
class taskPage(Page):
    form_model = 'player'
    form_fields = ['eventLog']
    
    @staticmethod
    def live_method(player: Player, data):
        if 'eventLog' in data:
            output = json.loads(data['eventLog'])
            lastEntry = output[-1]

            # Create a new EventLog object
            EventLog.create(
                player = player,
                time = lastEntry['time'],
                event = lastEntry['event'],
                currentlight = lastEntry['currentlight'],
                funds = lastEntry['funds'],
            )

            # save copy to player vars (optional)
            player.eventLog = json.dumps(output)

            # send to live page if needed            
            return {player.id_in_group: output}  



page_sequence = [
    taskPage,
]
