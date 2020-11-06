import json
import requests

game_path = 'E:\\IdiotGame\\LeagueofLegends\\英雄联盟\\LeagueClient'
usingApi = True

class RuneColor:
    resove = '\033[32m'
    inspiration = '\033[34m'
    sorcery = '\033[35m'
    domination = '\033[31m'
    precision = '\033[33m'
    WARNING = '\033[93m'


header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; R8207 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36; OP.GG Mobile Android (4.8.0); X-DEVICE-WIDTH=540',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}


def champIDInit():
    champ_list = requests.post("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()
    champ_id_list = {}
    for champ in champ_list['hero']:
        champ_id_list[champ["heroId"]] = champ["alias"]
    json.dump(champ_id_list, open("./champid", 'w'))


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

champIDInit()
