import json

import requests

champList = requests.post("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()
champidList = {}
for champ in champList['hero']:
    champidList[champ["heroId"]]=champ["alias"]
json.dump(champidList, open("./champid",'w'))
d2 = json.load(open('./champid','r'))
print(d2['2'])