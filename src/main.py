import requests
from decouple import config
from datetime import datetime
from pytz import timezone
import os



KEY = config("STEAM_API_KEY")
STEAMID = config("STEAM_ID")

gamesFolder = os.getcwd()+"\games"
if not os.path.exists(gamesFolder):
    os.mkdir(gamesFolder)
    slink1 = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
    slink2 = "&steamid=" + STEAMID + "&skip_unvetted_apps=false&include_appinfo=1&include_played_free_games=1&format=json"
else:
    slink1 = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="
    slink2 = "&steamid=" + STEAMID + "&format=json"
gamesFiles = os.listdir(gamesFolder)

#Steam API link formatting for "GetOwnedGames"
slink = slink1 + KEY + slink2
 
#Sent API Get request and save respond to a variable
r = requests.get(slink)
 
#convert to JSON and save to another variable
user = r.json()
user = user["response"]
 


tz = timezone('EST')
now = datetime.now(tz).date()  # Date object (so just year month and day, no time)
print("Today is hopefully:", now)

newGames = 0
oldGames = 0
for game in user["games"]:
    if (game["playtime_forever"]) != 0:
        if (str(game["appid"])) not in gamesFiles:
            print("\nAddding file: " + gamesFolder + "\\" + str(game["appid"]) + " for game " + game["name"])
            print("With " + str(game["playtime_forever"]) + " minutes of game time")
            with open(gamesFolder + "\\" + str(game["appid"]), 'w') as f:
                f.write(game["name"] + "\n")
                f.write(str(now) + " " + str(game["playtime_forever"]))
            newGames += 1
        else:
            last_line = ""
            with open(gamesFolder + "\\" + str(game["appid"]), 'r') as f:
                for line in f:
                    pass
                last_line = line
            if int(last_line.split()[1]) != game["playtime_forever"]:
                oldGames += 1
                with open(gamesFolder + "\\" + str(game["appid"]), 'a') as f:
                    f.write("\n" + str(now) + " " + str(game["playtime_forever"]))
            
print("\nAdded", newGames, "new game(s) and updated", oldGames, "old game(s)")