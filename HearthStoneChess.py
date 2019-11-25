from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Scatter, Pie, Page

import requests
import os
import json
import codecs
import re

cateGoryDict = {
    "鱼人": 14,
    "恶魔": 15,
    "机械": 17,
    "野兽": 20,
    "无种类": None
}

effectPatternDict = {
    "战吼": "BattleCry",
    "嘲讽": "Taunt",
    "圣盾": "DivineShield",
    "磁力": "Magnetic",
    "亡语": "DeathRattle", 
    "剧毒": "Poisonous",
    "超杀": "Overkill",
    "风怒": "WindFury",
    "复生": "Reborn",

    "冲锋": "Rush",
    "突袭": "Lifesteal",
    "过载": "Overload",
}

def getHeroList(map):
    heroMap = []
    for hero in map:
        battlegrounds = hero["battlegrounds"]
        if battlegrounds["hero"] == True:
            heroMap.append(hero)
    return heroMap


def getSlaveList(map):
    slaveMap = []
    for hero in map:
        battlegrounds = hero["battlegrounds"]
        if battlegrounds["hero"] == False:
            slaveMap.append(hero)
    return slaveMap


def getListByCategory(map, category):
    cateGoryList = []
    for card in map:
        if card["minionTypeId"] == category:
            card["category"] = "None" if category == None else category
            cateGoryList.append(card)
    return cateGoryList

def getTierList(map, cost):
    cateGoryList = []
    for card in map:
        battlegrounds = card["battlegrounds"]
        if battlegrounds["tier"] == cost:
            cateGoryList.append(card)
    return cateGoryList

def getEffectList(map, effect):
    EffectWithDesciptionList = []
    for card in map:
        text = card["text"]
        result = re.match(".*" + effect, text)
        if result != None:
            card["effect"] = effect
            EffectWithDesciptionList.append(card)
    return EffectWithDesciptionList

def count_charts(murlocList, mechList, demonList, beastList, nullList):
    bar = (Bar()
    .add_xaxis(list(cateGoryDict.keys()))
    .add_yaxis(
        "数量", [
            len(murlocList),
            len(mechList),
            len(demonList),
            len(beastList),
            len(nullList),
            
        ],
        color=Faker.rand_color()).set_global_opts(title_opts=opts.TitleOpts(title="数量分布情况")))
    return bar


def tier_charts(slaveList):
    bar = (Bar()
    .add_xaxis(["一星怪", "二星怪", "三星怪", "四星怪", "五星怪", "六星怪"])
    .add_yaxis(
        "数量", [
            len(getTierList(slaveList, 1)),
            len(getTierList(slaveList, 2)),
            len(getTierList(slaveList, 3)),
            len(getTierList(slaveList, 4)),
            len(getTierList(slaveList, 5)),
            len(getTierList(slaveList, 6)),
        ],
        color = '#FAD860'
        ).set_global_opts(title_opts=opts.TitleOpts(title="费用分布情况")))
    return bar


def count_pie(slaveList) -> Pie:
    countList = []
    for cateGory in cateGoryDict.keys() :
         countList.append(len(getListByCategory(slaveList, cateGoryDict[cateGory])))

    c = (
        Pie()
        .add("", [list(z) for z in zip(cateGoryDict.keys() , countList)])
        .set_global_opts(title_opts=opts.TitleOpts(title="各种类数量分布情况"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:  {c}"))
    )
    return c

def effect_pie(slaveList) -> Pie:
    countList = []
    for effect in effectPatternDict.keys() :
         countList.append(len(getEffectList(slaveList, effect)))

    c = (
        Pie()
        .add("", [list(z) for z in zip(effectPatternDict.keys() , countList)])
        # .set_global_opts(title_opts=opts.TitleOpts(title="各种特效数量分布情况"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:  {c}"))
    )
    return c

def invert_dict(m):
    return dict(zip(m.values(), m.keys()))


def downLoadPage():
    # 下载最新的炉石战旗数据并保存到本地
    url = "http://hs.blizzard.cn/action/hs/cards/battleround?sort=tier&order=asc&type=hero%2Cminion&tier=all&viewMode=table&collectible=0%2C1&pageSize=200&locale=zh_cn"
    jsonContent = requests.get(url).content.decode("utf-8")
    save_path = u"战棋"
    filename = u"英雄及卡牌全数据"
    jsonContent = jsonContent.encode("utf-8")
    StringListSave(save_path, filename, jsonContent)
    # print(json)
    dict = json.loads(s=jsonContent)
    list = dict["cards"]
    # python的json.dumps方法默认会输出成这种格式"\u535a\u5ba2\u56ed",。
    # 要输出中文需要指定ensure_ascii参数为False，如下代码片段：
    # json.dumps({'text':"中文"},ensure_ascii=False)
    cards = json.dumps(list, ensure_ascii=False).encode("utf-8")
    filename = u"卡牌全数据"
    StringListSave(save_path, filename, cards)
    # print(map)

    # 解析战旗卡牌并分类
    AnalyzeJsonDataAndDraw(list)

def AnalyzeJsonDataAndDraw(list):

    # 解析英雄卡牌列表
    # heroList = getHeroList(list)

    slaveList = getSlaveList(list)
    murlocList = getListByCategory(slaveList, cateGoryDict["鱼人"])
    demonList = getListByCategory(slaveList, cateGoryDict["恶魔"])
    mechList = getListByCategory(slaveList, cateGoryDict["机械"])
    beastList = getListByCategory(slaveList, cateGoryDict["野兽"])
    nullList = getListByCategory(slaveList, cateGoryDict["无种类"])

    # 解析卡牌星级
    # murlocTierList = getTierList(slaveList, 1)
    # print(len(murlocTierList))

    # # 解析卡牌特效
    # # 匹配 战吼 嘲讽 等
    BattleCryList = getEffectList(slaveList, "战吼")
    print(len(BattleCryList))
    for z in BattleCryList:
        print(z["name"])
    TauntList = getEffectList(slaveList, "嘲讽") 
    print(len(TauntList))
    for z in TauntList:
        print(z["name"])
    DivineShieldList = getEffectList(slaveList, "圣盾")
    print(len(DivineShieldList))
    for z in DivineShieldList:
        print(z["name"])
    MagneticList = getEffectList(slaveList, "磁力")
    print(len(MagneticList))
    for z in MagneticList:
        print(z["name"])
    DeathRattleList = getEffectList(slaveList, "亡语")
    print(len(DeathRattleList))
    for z in DeathRattleList:
        print(z["name"])
    PoisonousList = getEffectList(slaveList, "剧毒")
    print(len(PoisonousList))
    for z in PoisonousList:
        print(z["name"])
    OverkillList = getEffectList(slaveList, "超杀")
    print(len(OverkillList))
    for z in OverkillList:
        print(z["name"])
    WindFuryList = getEffectList(slaveList, "风怒")
    print(len(WindFuryList))
    for z in WindFuryList:
        print(z["name"])

    # 绘制图表
    countBar = count_charts(murlocList, demonList, mechList, beastList, nullList)
    tierBar = tier_charts(slaveList)
    countPie = count_pie(slaveList)
    effectPie = effect_pie(slaveList)

    page = Page(layout=Page.SimplePageLayout)
    page.add(countBar, tierBar, countPie, effectPie)
    page.render()

    # grid = (Grid()
    # .add(countBar, grid_opts=opts.GridOpts(pos_top="60%"))
    # .add(tierBar, grid_opts=opts.GridOpts(pos_top="60%"))
    # .add(countPie, grid_opts=opts.GridOpts(pos_top="60%")))
    

    # grid.render()
    # grid_vertical().render()


def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename + ".json"
    with open(path, "wb") as fp:
        fp.write(slist)

if __name__ == "__main__":
    
    # 远程调试
    downLoadPage()


    # 本地调试
    # with open('战棋/英雄及卡牌全数据.json', 'rb') as f:
    #     jsonContent = json.load(f) 
    # cardlist = jsonContent["cards"]
    # AnalyzeJsonDataAndDraw(cardlist)

