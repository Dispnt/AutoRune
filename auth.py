import sys
import requests
from requests.auth import HTTPBasicAuth

game_path = 'E:\\IdiotGame\\LeagueofLegends\\英雄联盟\\LeagueClient'

try:
    server_info = open(game_path + "\\lockfile", "r").read().split(':')
except IOError:
    sys.exit('Launch Your Game First')
else:
    server_port = server_info[2]
    server_pwd = server_info[3]
    server_protocol = server_info[4]
    # ProcessName:PID:WebServerPort:WebServerPwd:Protocol
    server_url = f"{server_protocol}://127.0.0.1:{server_port}"
    print(server_url, server_port, server_pwd)

summoner_info = requests.get(server_url + "/lol-summoner/v1/current-summoner", auth=HTTPBasicAuth('riot', server_pwd),
                             verify=False).json()
print(summoner_info['summonerId'])
