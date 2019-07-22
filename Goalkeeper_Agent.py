import random
import numpy as np
from keras.optimizers import Adam, RMSprop
from keras.models import Sequential
from keras.layers.core import Dense, Dropout

class GameLearner:
    def __init__(self):
        self.reward = 0
        self.gamma = 0.8
        self.alpha = 0.8
        self.short_memory = np.array([])
        self.learning_rate = 0.0005
        self.epsilon = 0
        self.state_len = 8
        self.actual = []
        self.memory = []
        self.model_save_file = "SavedWeights/GameRunLog-2007-223556"
        self.model = self.network()

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

    def set_reward(self, g):
        self.reward = 0
        if g.on_target is not None:
            if g.on_target:
                if g.saved:
                    self.reward = 10
                    print("Saved by the goalie!!")
                else:
                    self.reward = -10
                    print("Scored!!")
            else:
                self.reward = 0
                print("Missed!!")
        else:
            if g.gbd_old > g.gbd_new:
                self.reward = 1
            else:
                self.reward = -1
        return self.reward

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

        # Load save weights if any
        # model.load_weights(self.model_save_file)

        # opt = Adam(self.learning_rate)
        opt = RMSprop(lr=self.learning_rate)

        model.compile(loss='mse', optimizer=opt)

        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, self.state_len)))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][action] = target
            self.model.fit(state.reshape((1, self.state_len)), target_f, epochs=1, verbose=0)

    def save_weights(self):
        self.model.save_weights(self.model_save_file)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            pred = self.model.predict(next_state.reshape((1, self.state_len)))[0]
            #alpha is the learning rate
            target = self.alpha * (reward + self.gamma * np.amax(pred))
        target_f = self.model.predict(state.reshape((1, self.state_len)))
        target_f[0][action] = target
        self.model.fit(state.reshape((1, self.state_len)), target_f, epochs=1, verbose=0)