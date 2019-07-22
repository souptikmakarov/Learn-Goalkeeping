from Football_With_Goalie import Game
import json


saved_goals = "GameRunLogs/GameRunLog-2207-110959-Saved-Goals.json"
# last_100 = "GameRunLogs/GameRunLog-2007-182634-Last-100.json"
with open(saved_goals, "r") as read_file:
    gameJsonData = json.load(read_file)

for record in gameJsonData:
    g = Game(graphics=True)

    g.football.ROIx = record['BallROI'][0]
    g.football.ROIy = record['BallROI'][1]
    g.football.ROIz = 0.11

    for move in record['Goalie_Coords']:
        g.goalie.move_to_pos(move[0], move[1])
        g.render_next_frame()

    g.wait_after_complete()


    # print(g.isGameEnd)
    # if g.on_target:
    #     if g.saved:
    #         print("Saved by the goalie!!")
    #     else:
    #         print("Scored!!")
    # else:
    #     print("Missed!!")