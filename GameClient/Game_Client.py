from AI_Goalie import AI_Goalie
from Game import Game
from datetime import datetime
import numpy as np

class Game_Client:
    def __init__(self):
        self.agent = AI_Goalie()
        self.game = Game()

        # self.filename = "GameRunLogs/GameRunLog-{}".format(datetime.now().strftime("%d%m-%H%M%S"))

    def play(self):
        gameRunData = []
        counter_games = 0
        goals_saved = 0
        on_target = 0
        while True:
            self.game.reset_game()
            self.game.animation_delay = 100
            roi = self.game.get_user_input()
            self.game.football.ROIx = roi[1]
            self.game.football.ROIy = roi[2]
            self.game.football.ROIz = roi[0]
            while not self.game.isGameEnd:
                state_old = self.agent.get_state(self.game)
                prediction = self.agent.model.predict(state_old.reshape((1, self.agent.state_len)))
                goalie_to = np.argmax(prediction[0])

                # perform new move and get new state
                if goalie_to == 0:
                    self.game.goalie.move_by_unit(0, 0.2)
                elif goalie_to == 1:
                    self.game.goalie.move_by_unit(-0.2, 0)
                elif goalie_to == 2:
                    self.game.goalie.move_by_unit(0, -0.2)
                elif goalie_to == 3:
                    self.game.goalie.move_by_unit(0.2, 0)

                self.game.render_next_frame(goals_saved)
            counter_games += 1
            if self.game.on_target is not None:
                if self.game.on_target:
                    on_target += 1
                    if self.game.saved:
                        goals_saved += 1
            print("Shots Taken: {}, On Target: {}, Scored: {}".format(counter_games, on_target, on_target - goals_saved))
            self.game.wait_after_complete()


gc = Game_Client()
gc.play()
