import json
import requests


resove_8400 = ["8437", "8439", "8465",
             "8446", "8463", "8401",
             "8429", "8444", "8473",
             "8451", "8453", "8242"]  # 坚决绿

inspiration_8300 = ["8351", "8360", "8358",
                  "8306", "8304", "8313",
                  "8321", "8316", "8345",
                  "8347", "8410", "8352"]  # 启迪蓝

sorcery_8200 = ["8214", "8229", "8230",
              "8224", "8226", "8275",
              "8210", "8234", "8233",
              "8237", "8232", "8236"]  # 巫术紫

domination_8100 = ["8112", "8124", "8128", "9923",
                 "8126", "8139", "8143",
                 "8136", "8120", "8138",
                 "8135", "8134", "8105", "8106"]  # 主宰红

precision_8000 = ["9101", "9111", "8009",
                "9104", "9105", "9103",
                "8014", "8017", "8299"]  # 精密黄

rune_listname = ['resove_8400','inspiration_8300','sorcery_8200','domination_8100','precision_8000']

def runeIDs(championName ='Fizz'):
    summoner_info = requests.get("http://opgg.dispnt.com/api?championName="+championName).json()
    selectedId = summoner_info[1]['1']
    print(selectedPerkId)
    for list_name in rune_listname:
        if summoner_info[1]['1'][1] in globals()[list_name]:
            print("主系ID:"+list_name.split('_')[1])
            primaryId = list_name.split('_')[1]
        if summoner_info[1]['1'][4] in globals()[list_name]:
            print("副系ID:"+list_name.split('_')[1])
            subId = list_name.split('_')[1]
    return selectedPerkId,subId,primaryId


python2json = {}
selectedPerkIdSecondPart = ['5008','5008','5003']
(selectedPerkId,primaryStyleId,subStyleId) = runeIDs('Fizz')
selectedPerkId.extend(selectedPerkIdSecondPart)
print(selectedPerkId)
python2json['current'] = True
python2json["name"] = "Test"
python2json["primaryStyleId"] = primaryStyleId
python2json["selectedPerkIds"] = selectedPerkId
python2json["subStyleId"] = subStyleId

json_str = json.dumps(python2json)
print(json_str)