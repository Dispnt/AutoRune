import json
import requests


def champIDInit():
    champ_list = requests.post("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()
    champ_id_list = {}
    for champ in champ_list['hero']:
        champ_id_list[champ["heroId"]] = champ["alias"]
    json.dump(champ_id_list, open("./champid", 'w'))


def getChampName(champ_id):
    d2 = json.load(open('./champid', 'r'))
    print(d2[champ_id])
    return d2[champ_id]

# champIDInit()
# getChampName('2')
