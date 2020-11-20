import re
import sys
import urllib3
from champid import *
from time import sleep
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getChampName(champ_id):
    d2 = json.load(open('./champid', 'r'))
    return d2[champ_id]


def getRuneIDs(champion_name):
    if champion_name is not None:
        print(f"Loading {champion_name}'s Rune...")
        if usingApi is True:
            summoner_info = requests.get("http://opgg.dispnt.com/api?championName=" + champion_name).json()
        else:
            summoner_info = genRuneJson(champion_name)
    else:
        pass
    rune_selected = summoner_info[1]['1']
    for list_name in rune_listname:
        if rune_selected[1] in globals()[list_name]:
            print(f"\n---主系---  {list_name.split('_')[2]} ")
            for primary_rune in summoner_info[0]['1'][:4]:
                print(f"{primary_rune}",
                      end="  ")
            primary_id = list_name.split('_')[1]
        if rune_selected[4] in globals()[list_name]:
            print(f"\n---副系---  {list_name.split('_')[2]}")
            for sub_rune in summoner_info[0]['1'][4:]:
                print(f"{sub_rune}", end="  ")
            sub_id = list_name.split('_')[1]
    print('\n')
    return rune_selected, sub_id, primary_id


def genRuneJson(champion_name):
    rune_name = {}
    rune_link = []
    rune_id = {}
    url = "http://www.op.gg/champion/" + champion_name + "/statistics/"
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    RuneHtml = soup.find('div', {'class': 'rune-setting'})
    SelectedRuneHtml = RuneHtml.find_all(class_='perk-page__item--active')
    key_and_count = [1, 1]
    for SelectedRune in SelectedRuneHtml:
        rune_link.append(SelectedRune.find('img')['src'])
        if key_and_count[1] <= 6:
            rune_name.setdefault(str(key_and_count[0]), []).append(SelectedRune.find('img')['alt'])
        else:
            key_and_count = [key_and_count[0] + 1, 1]
            rune_name.setdefault(str(key_and_count[0]), []).append(SelectedRune.find('img')['alt'])
        key_and_count[1] = key_and_count[1] + 1
    key_and_count = [1, 1]
    for SelectedRune in rune_link:
        if key_and_count[1] <= 6:
            rune_id.setdefault(str(key_and_count[0]), []).append(re.findall(r"\d\d\d\d", SelectedRune)[0])
        else:
            key_and_count = [key_and_count[0] + 1, 1]
            rune_id.setdefault(str(key_and_count[0]), []).append(re.findall(r"\d\d\d\d", SelectedRune)[0])
        key_and_count[1] = key_and_count[1] + 1
    return rune_name, rune_id


def genRunePost(champion_name):
    rune_str = {}
    selectedPerkIdSecondPart = ['5008', '5008', '5003']
    (selectedPerkId, subStyleId, primaryStyleId) = getRuneIDs(champion_name)
    selectedPerkId.extend(selectedPerkIdSecondPart)
    rune_str['current'] = True
    rune_str["name"] = "AutoRune：" + champion_name
    rune_str["primaryStyleId"] = primaryStyleId
    rune_str["selectedPerkIds"] = selectedPerkId
    rune_str["subStyleId"] = subStyleId
    rune_json = json.dumps(rune_str)
    return rune_json


def getSelectChampName():
    try:
        champ_select_info = requests.get(server_url + "/lol-champ-select/v1/session",
                                         auth=HTTPBasicAuth('riot', server_pwd),
                                         verify=False).json()
        champ_id = champ_select_info['actions'][0][0]['championId']
        return getChampName(str(champ_id))
    except:
        pass


def delRunePg():
    champ_current_rune_page = requests.get(server_url + "/lol-perks/v1/currentpage",
                                           auth=HTTPBasicAuth('riot', server_pwd),
                                           verify=False).json()
    champ_current_rune_page_id = champ_current_rune_page['id']
    if int(champ_current_rune_page_id) > 100:
        requests.delete(server_url + "/lol-perks/v1/pages/" + str(champ_current_rune_page_id),
                        auth=HTTPBasicAuth('riot', server_pwd), verify=False).json()


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
    print(server_url, server_pwd,'\nUsing API =',str(usingApi))

if __name__ == "__main__":
    while True:
        sleep(0.5)
        try:
            champName = getSelectChampName()
            champ_current_rune_page = requests.get(server_url + "/lol-perks/v1/currentpage",
                                                   auth=HTTPBasicAuth('riot', server_pwd),
                                                   verify=False).json()
            champ_current_rune_page_name = champ_current_rune_page['name']
            if champ_current_rune_page_name.split ('：')[1] == champName:
                pass
            else:
                delRunePg()
                rune_json = genRunePost(champName)
                champ_select_info = requests.post(server_url + "/lol-perks/v1/pages", data=rune_json,
                                                  auth=HTTPBasicAuth('riot', server_pwd),
                                                  verify=False).json()
        except:
            print('Waiting...')
