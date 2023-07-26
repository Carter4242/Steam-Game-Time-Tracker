import requests
from decouple import config
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
import os

# Check all all the IDs


def check_IDs(listNewFiles=True, listIDSummaries=True):
    totalNewGames, totalOldGames = 0, 0
    for id in SteamIDs:
        # ensure the current ID folder has been created, if not, create it
        IdFolder = SteamIDFolder + "\\" + id
        if not os.path.exists(IdFolder):
            os.mkdir(IdFolder)

        # ensure the current IDs games folder has been created, if not this is the first run, so check every game
        gamesFolder = IdFolder + "\games"
        if not os.path.exists(gamesFolder):  # check every game
            os.mkdir(gamesFolder)
            slink1 = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
            slink2 = "&steamid=" + \
                id.split()[
                    0] + "&skip_unvetted_apps=false&include_appinfo=1&include_played_free_games=1?include_free_sub=1&format=json"
        else:  # only need to check last two weeks (to get the last day)
            slink1 = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="
            slink2 = "&steamid=" + id.split()[0] + "&format=json"
        gamesFiles = os.listdir(gamesFolder)  # make list of all gameFiles

        slink = slink1 + KEY + slink2  # create the https api link

        # send API Get request and save respond to a variable
        r = requests.get(slink)

        # convert to JSON and save to another variable
        user = r.json()["response"]

        newGames, oldGames = 0, 0  # counts of added/updated games
        for game in user["games"]:  # check every game
            if (game["playtime_forever"]) != 0:  # If never played no need to add
                if (str(game["appid"])) not in gamesFiles:  # file does not exist
                    if listNewFiles:
                        print("\nFor ID: " + id + ". Adding file: " + gamesFolder +
                              "\\" + str(game["appid"]) + " for game " + game["name"])
                        print(
                            "With " + str(game["playtime_forever"]) + " minutes of game time")
                    with open(gamesFolder + "\\" + str(game["appid"]), 'w') as f:
                        # first line of the file is the name of the game
                        f.write(game["name"] + "\n")
                        # then add yesterdays date and the current total playtime
                        f.write(str(yesterday) + " " +
                                str(game["playtime_forever"]))
                    newGames += 1  # added 1 game
                else:  # file exists
                    last_line = ""  # get the last line of the file to see if total playtime has changed since we've last checked
                    with open(gamesFolder + "\\" + str(game["appid"]), 'r') as f:
                        for line in f:
                            pass
                        last_line = line
                    if int(last_line.split()[1]) != game["playtime_forever"]:
                        oldGames += 1  # updated 1 game
                        with open(gamesFolder + "\\" + str(game["appid"]), 'a') as f:
                            # add yesterdays date and the current total playtime
                            f.write("\n" + str(yesterday) + " " +
                                    str(game["playtime_forever"]))
        if listIDSummaries:
            print("\nFor ID:", id + ". Added", newGames,
                  "game(s) and updated", oldGames, "game(s)")
        totalNewGames += newGames
        totalOldGames += oldGames

    print("\n\nIn total, added", totalNewGames,
          "game(s) and updated", totalOldGames, "game(s)\n\n")


# Get steam API key from .env file or the running Github Actions secret
try:  # first try to get it from GitHub Actions
    KEY = os.environ["STEAMAPIKEY"]
    print("Using Repo Secret Successfully")
except:  # if that doesn't work we are hopefully running locally, so try the .env file
    KEY = config("STEAM_API_KEY")


# Create list of SteamIDs to check
SteamIDs = []
with open(os.getcwd() + "\Steam IDs.txt", 'r') as f:
    for line in f:
        SteamIDs.append(str(line).strip())

# get yesterdays date, it should be the early hours of today in EST time (1-4AM)
tz = timezone('EST')
# Date object (so just year month and day, no time)
yesterday = datetime.now(tz).date() - relativedelta(days=1)
print("Yesterday was hopefully: ", yesterday)

# ensure the Steam IDs folder has been created, if not, create it
SteamIDFolder = os.getcwd()+"\Steam IDs"
if not os.path.exists(SteamIDFolder):
    os.mkdir(SteamIDFolder)
    print("\nStarting check 1 of 2\n")
    check_IDs()  # check_IDS twice to get recently played games as well (owned games doesn't include family shared games)
    print("\nStarting check 2 of 2\n")
check_IDs()
