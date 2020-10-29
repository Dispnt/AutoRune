import sys
from time import sleep

from champid import *
from requests.auth import HTTPBasicAuth

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

resove_8400 = ["8437", "8439", "8465",
               "8446", "8463", "8401",
               "8429", "8444", "8473",
               "8451", "8453", "8242"]

inspiration_8300 = ["8351", "8360", "8358",
                    "8306", "8304", "8313",
                    "8321", "8316", "8345",
                    "8347", "8410", "8352"]

sorcery_8200 = ["8214", "8229", "8230",
                "8224", "8226", "8275",
                "8210", "8234", "8233",
                "8237", "8232", "8236"]

domination_8100 = ["8112", "8124", "8128", "9923",
                   "8126", "8139", "8143",
                   "8136", "8120", "8138",
                   "8135", "8134", "8105", "8106"]

precision_8000 = ["9101", "9111", "8009",
                  "9104", "9105", "9103",
                  "8014", "8017", "8299"]

rune_listname = ['resove_8400', 'inspiration_8300', 'sorcery_8200', 'domination_8100', 'precision_8000']

game_path = 'E:\\IdiotGame\\LeagueofLegends\\英雄联盟\\LeagueClient'

try:
    server_info = open(game_path + "\\lockfile", "r").read().split(':')
except IOError:
    sys.exit('Launch Your Game First')
else:
    global server_url, server_pwd
    server_port = server_info[2]
    server_pwd = server_info[3]
    server_protocol = server_info[4]
    # ProcessName:PID:WebServerPort:WebServerPwd:Protocol
    server_url = f"{server_protocol}://127.0.0.1:{server_port}"

    print(server_url, server_port, server_pwd)


# summoner_info = requests.get(server_url + "/lol-summoner/v1/current-summoner",
#                              auth=HTTPBasicAuth('riot', server_pwd),
#                              verify=False).json()
# print(summoner_info['summonerId'])


def runeIDs(championName):
    summoner_info = requests.get("http://opgg.dispnt.com/api?championName=" + championName).json()
    selectedId = summoner_info[1]['1']
    print(selectedId)
    for list_name in rune_listname:
        if selectedId[1] in globals()[list_name]:
            print("主系ID:" + list_name.split('_')[1])
            primaryId = list_name.split('_')[1]
        if selectedId[4] in globals()[list_name]:
            print("副系ID:" + list_name.split('_')[1])
            subId = list_name.split('_')[1]
    return selectedId, subId, primaryId


def runeJson(championName='Fizz'):
    rune_str = {}
    selectedPerkIdSecondPart = ['5008', '5008', '5003']
    (selectedPerkId, subStyleId, primaryStyleId) = runeIDs(championName)
    selectedPerkId.extend(selectedPerkIdSecondPart)
    rune_str['current'] = True
    rune_str["name"] = "自动点的:" + championName
    rune_str["primaryStyleId"] = primaryStyleId
    rune_str["selectedPerkIds"] = selectedPerkId
    rune_str["subStyleId"] = subStyleId
    rune_json = json.dumps(rune_str)
    return rune_json


def champSelect():
    try:
        champ_select_info = requests.get(server_url + "/lol-champ-select/v1/session",
                                         auth=HTTPBasicAuth('riot', server_pwd),
                                         verify=False).json()
        champ_id = champ_select_info['actions'][0][0]['championId']
        return getChampName(str(champ_id))
    except:
        print('Waiting...')

while True:
    sleep(1)
    try:
        post_body = runeJson(champSelect())
        champ_select_info = requests.post(server_url + "/lol-perks/v1/pages", data=post_body,
                                          auth=HTTPBasicAuth('riot', server_pwd),
                                          verify=False).json()
        print(champ_select_info)
    except:
        pass
