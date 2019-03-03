from datetime import datetime
import argparse
import os
import sys
import requests
import json
import pandas as pd


def resolve_vanity_url(vanity_url):
    response = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=' + os.getenv('STEAM_API_KEY') + '&vanityurl=' + vanity_url)
    loaded_response = json.loads(response.content)
    if 'steamid' in loaded_response['response']:
        return loaded_response['response']['steamid']
    return ''

def main():
    parser = argparse.ArgumentParser(description='Steam2Excel, written by Ellis Madagan. This is free software! If you paid for it, you''re a sucker!')
    parser.add_argument('--id')
    args = parser.parse_args()
    base_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + os.getenv('STEAM_API_KEY') + '&steamid={}&include_appinfo=1&include_played_free_games=1&format=json'
    response = requests.get(base_url.format(resolve_vanity_url(args.id)))
    if response.status_code != 200:
        print('Please enter a valid Steam ID.')
        exit()
    parsed = json.loads(response.text)
    games = parsed['response']['games']
    games_df = pd.DataFrame(data=games)
    writer = pd.ExcelWriter(os.getcwd() + '/Steam ' + datetime.strftime(datetime.now(), '%d-%m-%Y %H%M%S') + '.xlsx', engine='xlsxwriter')
    games_df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    main()