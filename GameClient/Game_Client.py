from AI_Goalie import AI_Goalie
from Game import Game
from datetime import datetime

class Game_Client:
    def __init__(self):
        self.agent = AI_Goalie()
        self.filename = "GameRunLogs/GameRunLog-{}".format(datetime.now().strftime("%d%m-%H%M%S"))

    def play(self):
        gameRunData = []
        counter_games = 0
        while True:
            game = Game(graphics=True)
            game.animation_delay = 50
            game.get_user_inputs()