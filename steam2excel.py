import requests
import json
import pandas as pd


def main():
    base_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=4DBADD20D599923D76FA9DFE01DF32F9&steamid={}&include_appinfo=1&include_played_free_games=1&format=json'
    gokurin = '76561198049700950'
    response = requests.get(base_url.format(gokurin))
    parsed = json.loads(response.text)
    games = parsed['response']['games']
    games_df = pd.DataFrame(data=games)
    writer = pd.ExcelWriter('steam.xlsx', engine='xlsxwriter')
    games_df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    main()

