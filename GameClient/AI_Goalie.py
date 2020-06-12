# Play against an AI Goalie
from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import numpy as np

class AI_Goalie:
    def __init__(self):
        self.model_save_file = "GameRunLog-2207-110959.h5"
        self.learning_rate = 0.0005
        self.state_len = 8
        self.model = self.network(self.model_save_file)

    def get_state(self, game):
        state = [game.football.X,
                 game.football.Y,
                 game.football.Z,
                 game.football.prevX,
                 game.football.prevY,
                 game.football.prevZ,
                 game.goalie.Prev_Pos[0],
                 game.goalie.Prev_Pos[1]]
        return np.asarray(state)

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=self.state_len))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        # output is the x,y coordinates of the goalie
        model.add(Dense(output_dim=4, activation='softmax'))

        opt = RMSprop(lr=self.learning_rate)

        model.compile(loss='mse', optimizer=opt)

        # Load save weights if any
        if weights:
            model.load_weights(weights)
        return model



