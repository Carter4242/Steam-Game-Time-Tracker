# Steam-Game-Time-Tracker
Tracks a list of Steam users' daily game time using GitHub actions.

### Install requirements with:
    pip install -r requirements.txt

If running locally, put your Steam API key (https://steamcommunity.com/dev/registerkey) in the .env file. If using Github Actions, create a repo secret called STEAMAPIKEY with your API key.

Put some SteamID64(s) in Steam IDs.txt.

A SteamID can be found as the default profile link or using a username (https://www.steamidfinder.com/ or https://steamid.io)

#### Note that only the first word of each line is used as the actual ID, so the following is acceptable:
    0123456789 my friend
    1234567890 me
#### But these wouldn't be:
    0123456789my friend
    12345 67890 me
