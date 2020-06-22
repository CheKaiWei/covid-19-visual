import time 
import json
import requests
from datetime import datetime
import pandas as pd 
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import *
import pandas as pd
from pyecharts.globals import ThemeType

nameMap = {
        'Singapore Rep.':'新加坡',
        'Dominican Rep.':'多米尼加',
        'Palestine':'巴勒斯坦',
        'Bahamas':'巴哈马',
        'Timor-Leste':'东帝汶',
        'Afghanistan':'阿富汗',
        'Guinea-Bissau':'几内亚比绍',
        "Côte d'Ivoire":'科特迪瓦',
        'Siachen Glacier':'锡亚琴冰川',
        "Br. Indian Ocean Ter.":'英属印度洋领土',
        'Angola':'安哥拉',
        'Albania':'阿尔巴尼亚',
        'United Arab Emirates':'阿联酋',
        'Argentina':'阿根廷',
        'Armenia':'亚美尼亚',
        'French Southern and Antarctic Lands':'法属南半球和南极领地',
        'Australia':'澳大利亚',
        'Austria':'奥地利',
        'Azerbaijan':'阿塞拜疆',
        'Burundi':'布隆迪',
        'Belgium':'比利时',
        'Benin':'贝宁',
        'Burkina Faso':'布基纳法索',
        'Bangladesh':'孟加拉',
        'Bulgaria':'保加利亚',
        'The Bahamas':'巴哈马',
        'Bosnia and Herz.':'波斯尼亚和黑塞哥维那',
        'Belarus':'白俄罗斯',
        'Belize':'伯利兹',
        'Bermuda':'百慕大',
        'Bolivia':'玻利维亚',
        'Brazil':'巴西',
        'Brunei':'文莱',
        'Bhutan':'不丹',
        'Botswana':'博茨瓦纳',
        'Central African Rep.':'中非',
        'Canada':'加拿大',
        'Switzerland':'瑞士',
        'Chile':'智利',
        'China':'中国',
        'Ivory Coast':'象牙海岸',
        'Cameroon':'喀麦隆',
        'Dem. Rep. Congo':'刚果民主共和国',
        'Congo':'刚果',
        'Colombia':'哥伦比亚',
        'Costa Rica':'哥斯达黎加',
        'Cuba':'古巴',
        'N. Cyprus':'北塞浦路斯',
        'Cyprus':'塞浦路斯',
        'Czech Rep.':'捷克',
        'Germany':'德国',
        'Djibouti':'吉布提',
        'Denmark':'丹麦',
        'Algeria':'阿尔及利亚',
        'Ecuador':'厄瓜多尔',
        'Egypt':'埃及',
        'Eritrea':'厄立特里亚',
        'Spain':'西班牙',
        'Estonia':'爱沙尼亚',
        'Ethiopia':'埃塞俄比亚',
        'Finland':'芬兰',
        'Fiji':'斐济',
        'Falkland Islands':'福克兰群岛',
        'France':'法国',
        'Gabon':'加蓬',
        'United Kingdom':'英国',
        'Georgia':'格鲁吉亚',
        'Ghana':'加纳',
        'Guinea':'几内亚',
        'Gambia':'冈比亚',
        'Guinea Bissau':'几内亚比绍',
        'Eq. Guinea':'赤道几内亚',
        'Greece':'希腊',
        'Greenland':'格陵兰',
        'Guatemala':'危地马拉',
        'French Guiana':'法属圭亚那',
        'Guyana':'圭亚那',
        'Honduras':'洪都拉斯',
        'Croatia':'克罗地亚',
        'Haiti':'海地',
        'Hungary':'匈牙利',
        'Indonesia':'印度尼西亚',
        'India':'印度',
        'Ireland':'爱尔兰',
        'Iran':'伊朗',
        'Iraq':'伊拉克',
        'Iceland':'冰岛',
        'Israel':'以色列',
        'Italy':'意大利',
        'Jamaica':'牙买加',
        'Jordan':'约旦',
        'Japan':'日本',
        'Japan':'日本本土',
        'Kazakhstan':'哈萨克斯坦',
        'Kenya':'肯尼亚',
        'Kyrgyzstan':'吉尔吉斯斯坦',
        'Cambodia':'柬埔寨',
        'Korea':'韩国',
        'Kosovo':'科索沃',
        'Kuwait':'科威特',
        'Lao PDR':'老挝',
        'Lebanon':'黎巴嫩',
        'Liberia':'利比里亚',
        'Libya':'利比亚',
        'Sri Lanka':'斯里兰卡',
        'Lesotho':'莱索托',
        'Lithuania':'立陶宛',
        'Luxembourg':'卢森堡',
        'Latvia':'拉脱维亚',
        'Morocco':'摩洛哥',
        'Moldova':'摩尔多瓦',
        'Madagascar':'马达加斯加',
        'Mexico':'墨西哥',
        'Macedonia':'马其顿',
        'Mali':'马里',
        'Myanmar':'缅甸',
        'Montenegro':'黑山',
        'Mongolia':'蒙古',
        'Mozambique':'莫桑比克',
        'Mauritania':'毛里塔尼亚',
        'Malawi':'马拉维',
        'Malaysia':'马来西亚',
        'Namibia':'纳米比亚',
        'New Caledonia':'新喀里多尼亚',
        'Niger':'尼日尔',
        'Nigeria':'尼日利亚',
        'Nicaragua':'尼加拉瓜',
        'Netherlands':'荷兰',
        'Norway':'挪威',
        'Nepal':'尼泊尔',
        'New Zealand':'新西兰',
        'Oman':'阿曼',
        'Pakistan':'巴基斯坦',
        'Panama':'巴拿马',
        'Peru':'秘鲁',
        'Philippines':'菲律宾',
        'Papua New Guinea':'巴布亚新几内亚',
        'Poland':'波兰',
        'Puerto Rico':'波多黎各',
        'Dem. Rep. Korea':'朝鲜',
        'Portugal':'葡萄牙',
        'Paraguay':'巴拉圭',
        'Qatar':'卡塔尔',
        'Romania':'罗马尼亚',
        'Russia':'俄罗斯',
        'Rwanda':'卢旺达',
        'W. Sahara':'西撒哈拉',
        'Saudi Arabia':'沙特阿拉伯',
        'Sudan':'苏丹',
        'S. Sudan':'南苏丹',
        'Senegal':'塞内加尔',
        'Solomon Is.':'所罗门群岛',
        'Sierra Leone':'塞拉利昂',
        'El Salvador':'萨尔瓦多',
        'Somaliland':'索马里兰',
        'Somalia':'索马里',
        'Serbia':'塞尔维亚',
        'Suriname':'苏里南',
        'Slovakia':'斯洛伐克',
        'Slovenia':'斯洛文尼亚',
        'Sweden':'瑞典',
        'Swaziland':'斯威士兰',
        'Syria':'叙利亚',
        'Chad':'乍得',
        'Togo':'多哥',
        'Thailand':'泰国',
        'Tajikistan':'塔吉克斯坦',
        'Turkmenistan':'土库曼斯坦',
        'East Timor':'东帝汶',
        'Trinidad and Tobago':'特里尼达和多巴哥',
        'Tunisia':'突尼斯',
        'Turkey':'土耳其',
        'Tanzania':'坦桑尼亚',
        'Uganda':'乌干达',
        'Ukraine':'乌克兰',
        'Uruguay':'乌拉圭',
        'United States':'美国',
        'Uzbekistan':'乌兹别克斯坦',
        'Venezuela':'委内瑞拉',
        'Vietnam':'越南',
        'Vanuatu':'瓦努阿图',
        'West Bank':'西岸',
        'Yemen':'也门',
        'South Africa':'南非',
        'Zambia':'赞比亚',
        'Zimbabwe':'津巴布韦'
    }


def catch_global_data():
    """
    抓取当前实时数据，并返回 国家、大洲、确诊、疑似、死亡、治愈 列表
    :return:
    """
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    data = requests.post(url).json()['data']

    date_list = list()  # 日期
    name_list = list() # 国家
    continent_list = list() # 大洲
    confirm_list = list()  # 确诊
    suspect_list = list()  # 疑似
    dead_list = list()  # 死亡
    heal_list = list()  # 治愈

    for item in data:
        month, day = item['date'].split('.')
        date_list.append(datetime.strptime('2020-%s-%s' % (month, day), '%Y-%m-%d'))
        name_list.append(item['name'])
        continent_list.append(item['continent'])
        confirm_list.append(int(item['confirm']))
        suspect_list.append(int(item['suspect']))
        dead_list.append(int(item['dead']))
        heal_list.append(int(item['heal']))

    return date_list, name_list, continent_list, confirm_list, suspect_list, dead_list, heal_list


def save_csv():
    """
    将数据存入 csv 文件
    :return:
    """
    date_list, name_list, continent_list, confirm_list, suspect_list, dead_list, heal_list = catch_global_data()
    fw = open('2019-nCoV.csv', 'w', encoding='utf-8')
    fw.write('date,name,continent,confirm,suspect,dead,heal\n')

    i = 0
    while i < len(date_list):
        date = str(date_list[i].strftime("%Y-%m-%d"))
        fw.write(date + ',' + str(name_list[i]) + ',' + str(continent_list[i]) + ',' + str(confirm_list[i]) + ',' + str(suspect_list[i]) + ',' + str(dead_list[i]) + ',' + str(heal_list[i]) + '\n')
        i = i + 1
    else:
        print("csv 写入完成")
        fw.close()


def catch_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    reponse = requests.get(url=url).json()
    data = json.loads(reponse['data'])
    return data




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

def read_country_code():
    """
    获取国家中英文字典
    :return:
    """
    country_dict = {}
    for key, val in nameMap.items():  # 将 nameMap 列表里面键值互换
        country_dict[val] = key
    return country_dict

def read_csv():
    """
    读取数据，返回国家英文名称列表和累计确诊数列表
    :return:
    """
    country_dict = read_country_code()
    data = pd.read_csv("2019-nCoV.csv", index_col=False)

    countrys_names = list()
    confirmed_count = list()

    for x in range(len(data.index)):
        if data['name'].iloc[x] in country_dict.keys():
            countrys_names.append(country_dict[data['name'].iloc[x]])
            confirmed_count.append(data['confirm'].iloc[x])
        else:
            print(data['name'].iloc[x])

    return countrys_names, confirmed_count

def draw_map():
    """
    china!
    """
    data = catch_data()
    dict_keys = data.keys()
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


    """
    绘制世界地图
    遇到一个很神奇的问题：
    两个列表必须写死数据地图才会渲染数据，如果数据是从方法中获得，则地图不渲染数据
    :return:
    """

    # 修复注释中的问题，原因是 confirmed_count 中的 int 是 numpy 的 int ，需转化为 python 中的 int
    # 感谢公众号的 @李康伟 同学提出
    countrys_names, confirmed_count = read_csv()
    confirmed_count_list = []
    for item in confirmed_count:
        confirmed_count_list.append(int(item))

    # countrys_names = ['United States', 'Brazil', 'Russia', 'Spain', 'United Kingdom', 'Italy', 'France', 'Germany', 'Turkey', 'Iran', 'India', 'Peru', 'Canada', 'Saudi Arabia', 'Mexico', 'Chile', 'Belgium', 'Pakistan', 'Netherlands', 'Qatar', 'Ecuador', 'Belarus', 'Sweden', 'Bangladesh', 'Singapore Rep.', 'Switzerland', 'Portugal', 'United Arab Emirates', 'Ireland', 'Indonesia', 'South Africa', 'Poland', 'Ukraine', 'Kuwait', 'Colombia', 'Romania', 'Israel', 'Japan', 'Egypt', 'Austria', 'Dominican Rep.', 'Philippines', 'Denmark', 'Argentina', 'Korea', 'Serbia', 'Panama', 'Afghanistan', 'Czech Rep.', 'Norway', 'Kazakhstan', 'Algeria', 'Nigeria', 'Morocco', 'Oman', 'Malaysia', 'Australia', 'Moldova', 'Ghana', 'Finland', 'Armenia', 'Bolivia', 'Cameroon', 'Iraq', 'Luxembourg', 'Azerbaijan', 'Honduras', 'Hungary', 'Sudan', 'Guinea', 'Uzbekistan', 'Guatemala', 'Thailand', 'Senegal', 'Greece', 'Tajikistan', 'Bulgaria', "Côte d'Ivoire", 'Djibouti', 'Croatia', 'Gabon', 'Cuba', 'Estonia', 'El Salvador', 'Iceland', 'Lithuania', 'Somalia', 'New Zealand', 'Slovakia', 'Slovenia', 'Kyrgyzstan', 'Kenya', 'Guinea Bissau', 'Lebanon', 'Sri Lanka', 'Tunisia', 'Latvia', 'Mali', 'Venezuela', 'Albania', 'Eq. Guinea', 'Niger', 'Cyprus', 'Zambia', 'Costa Rica', 'Haiti', 'Paraguay', 'Burkina Faso', 'Uruguay', 'Georgia', 'Jordan', 'Chad', 'Sierra Leone', 'Nepal', 'Jamaica', 'Tanzania', 'Ethiopia', 'Madagascar', 'Palestine', 'Togo', 'Vietnam', 'Rwanda', 'Montenegro', 'Nicaragua', 'Liberia', 'Swaziland', 'Mauritania', 'Yemen', 'Myanmar', 'Uganda', 'Mozambique', 'Mongolia', 'Brunei', 'Benin', 'Guyana', 'Cambodia', 'The Bahamas', 'Malawi', 'Libya', 'Syria', 'Angola', 'Zimbabwe', 'Burundi', 'Eritrea', 'Botswana', 'Gambia', 'Bhutan', 'East Timor', 'Namibia', 'Lao PDR', 'Fiji', 'Belize', 'Suriname', 'Papua New Guinea', 'Lesotho']
    # 
    # confirmed_count = [1666828, 347398, 335882, 281904, 258504, 229327, 182036, 179986, 155686, 133521, 131920, 115754, 85151, 70161, 65856, 65393, 56810, 54601, 45265, 42213, 36258, 35244, 33188, 32078, 31068, 30725, 30471, 28704, 24582, 21745, 21343, 20931, 20580, 20464, 20177, 17857, 16712, 16536, 16513, 16486, 14422, 13777, 11487, 11353, 11190, 11092, 10577, 9998, 8890, 8346, 8322, 8113, 7526, 7406, 7257, 7185, 7114, 6994, 6617, 6568, 6302, 5915, 4400, 4272, 3990, 3982, 3743, 3741, 3628, 3176, 3132, 3054, 3040, 2976, 2876, 2738, 2427, 2366, 2270, 2243, 1934, 1931, 1821, 1819, 1804, 1616, 1594, 1504, 1504, 1468, 1403, 1192, 1114, 1097, 1089, 1048, 1046, 1015, 1010, 989, 960, 943, 927, 920, 918, 865, 850, 814, 764, 728, 704, 648, 621, 584, 550, 509, 494, 488, 423, 373, 325, 325, 324, 279, 255, 238, 227, 212, 201, 198, 168, 141, 141, 135, 127, 124, 100, 82, 75, 70, 61, 56, 42, 39, 30, 25, 24, 24, 20, 19, 18, 18, 11, 8, 2]


    c = (
        Map()
        .add(
            "确诊人数",
            [list(z) for z in zip(countrys_names, confirmed_count_list)],
            is_map_symbol_show=False,
            maptype="world",
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color="rgb(49,60,72)")
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全球 2019-nCoV 地图"),
            visualmap_opts=opts.VisualMapOpts(max_=1700000),
        )
        #.render("map_world.html")
    )
    page.add(c)
    page.render('covid-19可视化.html')
    
    

if __name__ == '__main__':
    save_csv()
    draw_map()