import sys
from champid import *
from time import sleep
from requests.auth import HTTPBasicAuth

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



resove_8400_坚决 = ["8437", "8439", "8465",
               "8446", "8463", "8401",
               "8429", "8444", "8473",
               "8451", "8453", "8242"]

inspiration_8300_启迪 = ["8351", "8360", "8358",
                    "8306", "8304", "8313",
                    "8321", "8316", "8345",
                    "8347", "8410", "8352"]

sorcery_8200_巫术 = ["8214", "8229", "8230",
                "8224", "8226", "8275",
                "8210", "8234", "8233",
                "8237", "8232", "8236"]

domination_8100_主宰 = ["8112", "8124", "8128", "9923",
                   "8126", "8139", "8143",
                   "8136", "8120", "8138",
                   "8135", "8134", "8105", "8106"]

precision_8000_精密 = ["9101", "9111", "8009",
                  "9104", "9105", "9103",
                  "8014", "8017", "8299"]

rune_listname = ['resove_8400_坚决', 'inspiration_8300_启迪', 'sorcery_8200_巫术', 'domination_8100_主宰', 'precision_8000_精密']

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

    print(server_url, server_pwd)


# summoner_info = requests.get(server_url + "/lol-summoner/v1/current-summoner",
#                              auth=HTTPBasicAuth('riot', server_pwd),
#                              verify=False).json()
# print(summoner_info['summonerId'])


def runeIDs(championName):
    summoner_info = requests.get("http://opgg.dispnt.com/api?championName=" + championName).json()
    selectedId = summoner_info[1]['1']
    for rune in summoner_info[0]['1']:
        print(rune)
    for list_name in rune_listname:
        if selectedId[1] in globals()[list_name]:
            print("主系:" + list_name.split('_')[2])
            for paimary_rune in summoner_info[0]['1'][:4]:
                print(paimary_rune)
            primaryId = list_name.split('_')[1]
        if selectedId[4] in globals()[list_name]:
            print("副系:" + list_name.split('_')[2])
            for sub_rune in summoner_info[0]['1'][2:]:
                print(rune)
            subId = list_name.split('_')[1]
    return selectedId, subId, primaryId


def runeJson(championName='Fizz'):
    rune_str = {}
    selectedPerkIdSecondPart = ['5008', '5008', '5003']
    (selectedPerkId, subStyleId, primaryStyleId) = runeIDs(championName)
    selectedPerkId.extend(selectedPerkIdSecondPart)
    rune_str['current'] = True
    rune_str["name"] = "自动点的：" + championName
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
        pass


def runeDelete():
    champ_current_rune_page = requests.get(server_url + "/lol-perks/v1/currentpage",
                                           auth=HTTPBasicAuth('riot', server_pwd),
                                           verify=False).json()
    champ_current_rune_page_id = champ_current_rune_page['id']
    if int(champ_current_rune_page_id) > 100:
        requests.delete(server_url + "/lol-perks/v1/pages/" + str(champ_current_rune_page_id),
                        auth=HTTPBasicAuth('riot', server_pwd), verify=False).json()


while True:
    sleep(0.5)
    try:
        champName = champSelect()
        champ_current_rune_page = requests.get(server_url + "/lol-perks/v1/currentpage",
                                               auth=HTTPBasicAuth('riot', server_pwd),
                                               verify=False).json()
        champ_current_rune_page_name = champ_current_rune_page['name']
        if champ_current_rune_page_name.split('：')[1] == champName:
            pass
        else:
            runeDelete()
            rune_json = runeJson(champName)
            champ_select_info = requests.post(server_url + "/lol-perks/v1/pages", data=rune_json,
                                              auth=HTTPBasicAuth('riot', server_pwd),
                                              verify=False).json()
    except:
        print('Waiting...')
