import json
from math import floor
from GameDataLogger import print_game_data_2

filename = "GameRunLogs/GameRunLog-2207-110959"
gameJsonData = ""
gameTextData = ""


with open(filename + ".txt", "r") as read_file:
    gameTextData = read_file.readlines()

with open(filename + ".json", "r") as read_file:
    gameJsonData = json.load(read_file)
print(len(gameJsonData))
succ_saves = []

# Find games where goalie saved the goal
for i in range(floor(len(gameTextData)/7)):
    ents = gameTextData[7*i+4].strip('\n').split(':')
    if ents[0] == "Saved" and ents[1].strip(' ') == "True":
        gameId = gameTextData[7*i].split(':')[1]
        succ_saves.append(int(gameId))
print(succ_saves, len(succ_saves))

# succ_saves = range(3600, 3700)


succ_save_data = list(filter(lambda x: x["GameId"] in succ_saves, gameJsonData))

# print_game_data_2(succ_save_data, "GameRunLogs/GameRunLog-2207-110959-Saved-Goals.json")

