import json
from json import JSONEncoder
from GameRecordDataModel import GameRecordData


class GameRecordEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, GameRecordData):
            return {
                "GameId": o.GameId,
                "Goalie_Coords": o.Goalie_Coords,
                "FinalBallCoords": o.FinalBallCoords,
                "Reward": o.Reward,
                "On_Target": o.On_Target,
                "Goal_Saved": o.Goal_Saved,
                "BallROI": o.BallROI
            }
        else:
            return super().default(o)


# Print goalie_coords for each frame and final ball coords
def print_game_data_1(data, filename):

    log_msg = "Game:{}\nBall loc: [{},{}]\nGoalie Final Coords: [{},{},{}]\nOn Target: {}\nSaved: {}\nReward: {}\n\n".format(
            data.GameId,
            data.FinalBallCoords[0], data.FinalBallCoords[1],
            data.Goalie_Coords[-1][0], data.Goalie_Coords[-1][1], data.Goalie_Coords[-1][2],
            data.On_Target,
            data.Goal_Saved,
            data.Reward)

    print(log_msg)

    with open(filename, 'a') as f:
        f.write(log_msg)


def print_game_data_2(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, cls=GameRecordEncoder)
