
class GameRecordData:
    def __init__(self):
        self.GameId = -1
        self.Goalie_Coords = []
        self.FinalBallCoords = None
        self.Reward = 0
        self.On_Target = False
        self.Goal_Saved = None
        self.BallROI = []

# class Prediction:
#     def __init__(self):
#         self.Id = -1
#         self.Floor = -1
#         self.EggsLeft = -1
#         self.Reward = -1