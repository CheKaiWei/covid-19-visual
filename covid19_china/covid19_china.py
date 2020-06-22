import time 
import json
import requests
from datetime import datetime
import pandas as pd 
import numpy as np

def catch_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    reponse = requests.get(url=url).json()
    data = json.loads(reponse['data'])
    return data

# run
data = catch_data()
dict_keys = data.keys()
print(dict_keys)
#旧的数据集dict_keys = (['chinaTotal', 'chinaAdd', 'lastUpdateTime', 'areaTree', 'chinaDayList', 'chinaDayAddList'])
#新的数据集dict_keys(['lastUpdateTime', 'chinaTotal', 'chinaAdd', 'isShowAdd', 'showAddSwitch', 'areaTree'])



# China
lastUpdateTime = data['lastUpdateTime']
chinaTotal = data['chinaTotal']
chinaAdd = data['chinaAdd']
#结果{'confirm': 84970, 'heal': 79963, 'dead': 4645, 'nowConfirm': 362, 'suspect': 11, 
#'nowSevere': 13, 'importedCase': 1868, 'noInfect': 108}
areaTree = data['areaTree']
china_data = areaTree[0]['children']
china_list = []
for a in range(len(china_data)):
    province = china_data[a]['name']
    province_list = china_data[a]['children']
    for b in range(len(province_list)):
        city = province_list[b]['name']
        total = province_list[b]['total']
        today = province_list[b]['today']
        china_dict = {}
        china_dict['province'] = province
        china_dict['city'] = city
        china_dict['total'] = total
        china_dict['today'] = today
        china_list.append(china_dict)
china_data = pd.DataFrame(china_list)
china_data.head()

# 定义数据处理函数
def confirm(x):
    confirm = eval(str(x))['confirm']
    return confirm
def suspect(x):
    suspect = eval(str(x))['suspect']
    return suspect
def dead(x):
    dead = eval(str(x))['dead']
    return dead
def heal(x):
    heal =  eval(str(x))['heal']
    return heal
# 函数映射
china_data['confirm'] = china_data['total'].map(confirm)
china_data['suspect'] = china_data['total'].map(suspect)
china_data['dead'] = china_data['total'].map(dead)
china_data['heal'] = china_data['total'].map(heal)
china_data['addconfirm'] = china_data['today'].map(confirm)
#['addsuspect'] = china_data['today'].map(suspect)
#china_data['adddead'] = china_data['today'].map(dead)
#china_data['addheal'] = china_data['today'].map(heal)
china_data = china_data[["province","city","confirm","suspect","dead","heal","addconfirm"]]
china_data.head()







from pyecharts.charts import * #导入所有图表
from pyecharts import options as opts
#导入pyecharts的主题（如果不使用可以跳过）
from pyecharts.globals import ThemeType

total_pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,width = '900px',height ='350px'))  #设置主题，和画布大小
total_pie.add("",[list(z) for z in zip(chinaTotal.keys(), chinaTotal.values())],
            center=["50%", "70%"], #图的位置
            radius=[50, 80])   #内外径大小
total_pie.set_global_opts(
            title_opts=opts.TitleOpts(title="全国总量",subtitle=("截止"+lastUpdateTime)))
total_pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{c}"))  #标签格式
total_pie.render_notebook()

totaladd_pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,width = '900px',height ='350px'))  #设置主题，和画布大小
totaladd_pie.add("",[list(z) for z in zip(chinaAdd.keys(), chinaAdd.values())],
            center=["50%", "50%"],
            radius=[50, 80])
totaladd_pie.set_global_opts(
            title_opts=opts.TitleOpts(title="昨日新增"))
totaladd_pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{c}"))  #标签格式
totaladd_pie.render_notebook()

area_data = china_data.groupby("province")["confirm"].sum().reset_index()
area_data.columns = ["province","confirm"]
area_map = Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
area_map.add("",[list(z) for z in zip(list(area_data["province"]), list(area_data["confirm"]))], "china",is_map_symbol_show=False)
area_map.set_global_opts(title_opts=opts.TitleOpts(title="2019_nCoV中国疫情地图"),visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                pieces = [
                        {"min": 1001 , "label": '>1000',"color": "#893448"}, #不指定 max，表示 max 为无限大
                        {"min": 500, "max": 1000, "label": '500-1000',"color": "#ff585e"},
                        {"min": 101, "max": 499, "label": '101-499',"color": "#fb8146"},
                        {"min": 10, "max": 100, "label": '10-100',"color": "#ffb248"},
                        {"min": 0, "max": 9, "label": '0-9',"color" : "#fff2d1" }]))
area_map.render_notebook()


page = Page()
page.add(total_pie)
page.add(totaladd_pie)
page.add(area_map)
page.render("2019_nCoV 中国数据可视化.html")