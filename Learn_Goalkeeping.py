from Goalkeeper_Agent import GameLearner
from Football_With_Goalie import Game
from GameRecordDataModel import GameRecordData
from random import randrange, randint
from GameDataLogger import print_game_data_1, print_game_data_2
from datetime import datetime
from math import floor
import numpy as np

def run():
    agent = GameLearner()
    filename = "GameRunLogs/GameRunLog-{}".format(datetime.now().strftime("%d%m-%H%M%S"))
    # print(agent.model.summary())
    counter_games = 0
    gameRunData = []
    while True:
        #Init Game Classes
        game = Game(graphics=False)
        game.animation_delay = 50
        game.football.ROIx = randrange(-35, 35) / 1000
        game.football.ROIy = randrange(0, 23) / 1000

        gameData = GameRecordData()
        gameData.BallROI = [game.football.ROIx, game.football.ROIy]
        gameData.GameId = counter_games
        reward = 0
        agent.model_save_file = "SavedWeights/model_weight_{}.h5".format(floor(counter_games/100))
        while not game.isGameEnd:
            # agent.epsilon is set to give randomness to actions
            agent.epsilon = 80 - counter_games

            # get old state
            state_old = agent.get_state(game)

            # perform random actions based on agent.epsilon, or choose the action
            if randint(0, 200) < agent.epsilon:
                goalie_to = randint(0, 3)
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old.reshape((1, agent.state_len)))
                # take the floor value for which predicted reward is highest
                goalie_to = np.argmax(prediction[0])

            # perform new move and get new state
            if goalie_to == 0:
                game.goalie.move_by_unit(0, 0.2)
            elif goalie_to == 1:
                game.goalie.move_by_unit(-0.2, 0)
            elif goalie_to == 2:
                game.goalie.move_by_unit(0, -0.2)
            elif goalie_to == 3:
                game.goalie.move_by_unit(0.2, 0)

            game.next_state()
            state_new = agent.get_state(game)

            # set reward for the new state
            reward = agent.set_reward(game)

            gameData.Goalie_Coords.append([game.goalie.Center[0], game.goalie.Center[1], reward])

            # train short memory base on the new action and state
            agent.train_short_memory(state_old, goalie_to, reward, state_new, game.isGameEnd)

            # store the new data into a long term memory
            agent.remember(state_old, goalie_to, reward, state_new, game.isGameEnd)

        gameData.FinalBallCoords = [game.football.X, game.football.Y]
        gameData.Reward = reward
        gameData.Goal_Saved = game.saved
        gameData.On_Target = game.on_target
        gameRunData.append(gameData)
        print_game_data_1(gameData, filename + ".txt")
        print_game_data_2(gameRunData, filename + ".json")

        agent.replay_new(agent.memory)
        if floor(counter_games % 100) == 0:
            agent.save_weights()
        counter_games += 1


run()
