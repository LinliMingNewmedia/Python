from flask import Flask, render_template, request
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map,Tab
from pyecharts.globals import ChartType, SymbolType
import plotly as py
import plotly.graph_objs as go
import plotly.express as px

app = Flask(__name__)

df = pd.read_csv('suicide1.csv', encoding='gbk')
regions_available_loaded = list(df.year.dropna().unique())


df1 = pd.read_csv('自杀率.csv')

dfe=pd.read_csv('高低自杀率国家.csv')
dfe

# 自杀率
自杀率 = list(zip(list(df1.国家), list(df1.总自杀率)))

def map_world() -> Map:
    c = (
        Map()
            .add("2016年总自杀率（每10万人）", [list(z) for z in zip(df1["国家"], df1["总自杀率"])], "world")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2016年总自杀率"),
            visualmap_opts=opts.VisualMapOpts(min_=0, max_=30),
        )
    )
    return c

map_world().render()

自杀率二 = list(zip(list(df1.国家), list(df1.男性自杀率)))

def map_world1() -> Map:
    c = (
        Map()
            .add("2016年男性自杀率（每10万人）", [list(z) for z in zip(df1["国家"], df1["男性自杀率"])], "world")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2016年男性自杀率"),
            visualmap_opts=opts.VisualMapOpts(min_=0, max_=30),
        )
    )
    return c

map_world1().render()

自杀率三 = list(zip(list(df1.国家), list(df1.女性自杀率)))

def map_world2() -> Map:
    c = (
        Map()
            .add("2016年女性性自杀率（每10万人）", [list(z) for z in zip(df1["国家"], df1["女性自杀率"])], "world")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2016年女性自杀率"),
            visualmap_opts=opts.VisualMapOpts(min_=0, max_=30),
        )
    )
    return c

map_world2().render()

tab = Tab()
tab.add(map_world(), "2016年总自杀率")
tab.add(map_world1(), "2016年男性自杀率")
tab.add(map_world2(), "2016年女性自杀率")
tab.render('p2.html')




@app.route('/', methods=['GET'])
def get_out():
    data_str = df.to_html()

    regions_available = regions_available_loaded  # 下拉选单有内容
    return render_template('p1.html',
                           the_res=data_str,  # 表
                           the_select_region=regions_available)


@app.route('/suicide1', methods=['POST'])
def get_in() -> 'html':
    the_region = request.form["the_region_selected"]  ## 取得用户交互输入
    print(the_region)  ## 检查用户输入, 在后台
    fig = px.scatter(df, x="country", y="suicides_rate")
    fig.show()
    dfs = df.query("year=='{}'".format(the_region))  ## 使用df.query()方法. 按用户交互输入the_region过滤

    data_str = dfs.to_html()  # 数据产出dfs, 完成互动过滤呢

    regions_available = regions_available_loaded  # 下拉选单有内容

    py.offline.plot(fig, filename="p1.html", auto_open=False)  # 備出"成果.html"檔案之交互圖
    with open("p1.html", encoding="utf8", mode="r") as k:  # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(k.readlines())

    return render_template('p1.html',
                           the_plot_all_3=plot_all,
                           the_res=data_str,
                           the_select_region=regions_available
                           )
    # return render_template('p1.html',
    #                        the_res=data_str,
    #                        the_select_region=regions_available,
    #                        )
    #




@app.route('/p2.html', methods=['POST'])
def get_mo() -> 'html':
    with open("p2.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())


    return render_template('p2.html',
                           the_plot_all=plot_all
                           )


@app.route('/p3.html', methods=['POST'])
def get_you() -> 'html':
    trace1 = go.Bar(
        x=["Guyana", "Lesotho", "Lithuania", "Republic of Korea", "Russian Federation", "Suriname", "Uganda",
           "Zimbabwe"],
        y=[1, 1, 1, 1, 1, 1, 1, 1, ],
        name='Independent mental health regulations')
    trace2 = go.Bar(
        x=["Guyana", "Lesotho", "Lithuania", "Republic of Korea", "Russian Federation", "Suriname", "Uganda",
           "Zimbabwe"],
        y=[1, 0, 1, 1, 1, 1, 1, 1],
        name='Independent mental health plan')
    trace3 = go.Bar(
        x=["Azerbaijan", "Barbados", "Grenada", "Guatemala", "Jamaica", "Kuwait", "Maldives",
           "Saint Vincent and the Grenadines", "Syrian Arab Republic", "United Arab Emirates"],
        y=[1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        name='Independent mental health regulations')
    trace4 = go.Bar(
        x=["Azerbaijan", "Barbados", "Grenada", "Guatemala", "Jamaica", "Kuwait", "Maldives",
           "Saint Vincent and the Grenadines", "Syrian Arab Republic", "United Arab Emirates"],
        y=[1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
        name='Independent mental health plan'
    )

    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        title='自杀率高低不同的国家政策制定情况(左边为自杀率高的国家，右边为自杀率低的国家)',
        barmode='stack',
        paper_bgcolor='rgb(233,233,233)',
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()

    py.offline.plot(fig, filename="p3.html", auto_open=False)  # 備出"成果.html"檔案之交互圖
    with open("p3.html", encoding="utf8", mode="r") as g:  # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(g.readlines())

    return render_template('p3.html',
                           the_plot_all_1=plot_all)

@app.route('/p4.html',methods=['POST'])

def get_xi() -> 'html':
    return render_template('p4.html')

if __name__ == '__main__':
    app.run(port = 3020)
