# unused, using a steam api module, but it didn't have all the features I wanted and was trivial to implement myself
# Is equivalent to the no games folder existing version of main.py
"""
from steam import Steam
from decouple import config
import os

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)
user = steam.users.get_owned_games("76561198262842527")

gamesFolder = os.getcwd()+"\games"
if not os.path.exists(gamesFolder):
    os.mkdir(gamesFolder)
gamesFiles = os.listdir(gamesFolder)

for game in user["games"]:
    #print(game["name"], game["playtime_forever"])
    #print(game)
   # continue
    if (str(game["appid"]) + " - GAMETITLE: " + game["name"]) not in gamesFiles:
        if (game["playtime_forever"]) != 0:
            print("\nAddding file: " + gamesFolder + "\\" + str(game["appid"]) + " for game " + game["name"])
            print("With " + str(game["playtime_forever"]) + " minutes of game time")
            with open(gamesFolder + "\\" + str(game["appid"]), 'w') as f:
                f.write(game["name"] + "\n")
                f.write(str(game["playtime_forever"]))
"""
