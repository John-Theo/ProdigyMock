from flask import Flask, send_from_directory, request
from flask_json import as_json
import os, re

app = Flask(__name__)
app.config['JSON_ADD_STATUS'] = False


DEV_LABELS = [
    "关键词",
    "公司",
    "严重度"
]

DEV_TEXT = '''
原标题：十二年跌幅八成！中国石油股价逼近历史新低，股东成功减持30亿元 来源：丁蜀农业信息网
周五沪指跌破2900点，其中 中国石油 跌幅2.01%为沪指贡献了-1.78个点数，盘中最低跌至6.31元，离历史新低6.04元仅一步之遥。
a股市场上市公司大股东减持股票的问题，一直是证券投资者尤其是散户们重点关注的事情，料哥和大家分享一个当前正在逐渐被广泛采取的减持股票招式，可以做到在股价持续下跌的背景下，减持资产几乎毫发无伤甚至还可能获得额外盈余，非常高明！
2019年4月17日，沪交所上市公司中国石油天然气股份有限公司（以下采用其股票简称：中国石油）发布了一则重磅公告：《关于控股股东认购证券投资基金计划公告》。
'''.strip()

DEV_TEXTS = [DEV_TEXT]*200

DEV_HOT_REGEXES = {
    '中国石油': '公司',
    '(大?股东(减持|增持))': '关键词'
}

# *** IMPLEMENT THIS *** #
def get_record_from_db(limit=3):
    return zip(range(limit), DEV_TEXTS[:limit])

# *** IMPLEMENT THIS *** #
def text_tokenization(text):
    return list(text)

# *** IMPLEMENT THIS *** #
def extract_entities_from_text(text):
    entities = []
    for regex, label in DEV_HOT_REGEXES.items():
        for hit in re.finditer(regex, DEV_TEXT, flags=re.S):
            ent_text = hit.group()
            start = hit.start()
            entities.append({
                "confidence": 1,
                "label": DEV_LABELS.index(label),
                "source": "DICT",
                "span": [
                    start,
                    start+len(ent_text)
                ],
                "text": ent_text
            })
    return entities


@app.route('/')
def interface():
    return send_from_directory('./', 'index.html')

@app.route('/api/news', methods=['GET'])
@as_json
def serve_data():
    number = int(request.args.get('n'))
    records = get_record_from_db(limit=number)
    items = [{
        'tokens': text_tokenization(rec_text),
        'id': rec_id,
        'link': 'http://new_source.url/',
        'source': '新浪财经',
        'entities': extract_entities_from_text(rec_text)
    } for rec_id, rec_text in records]

    return {
        'name': '数据集名称',
        'items': items,
        'labels': DEV_LABELS,
        'user': '操作员昵称',
        'load_batch': 10,  # 一次请求获取的新闻数量
        'doc_num': 200  # 数据库中所有未标记新闻数量
    }


@app.route('/api/news', methods=['POST'])
@as_json
def recieve_annotated():
    data = request.json
    print('新出现的关键词：', data['new_hot_words'])
    print('标注员：', data['operator'])
    for annotation in data['items']:
        print('  ', '新闻id：', annotation['id'])
        print('  ', '出现实体：')
        for entity in annotation['entities']:
            print(' '*4, '文本：', entity['text'])
            print(' '*4, '文本位置：', entity['span'])
            print(' '*4, '标注类型：', entity['label'])
            print(' '*4, '来源：', entity['source'])
            print(' '*4, '-'*20)
    return {'status': 'success'}


if __name__ == '__main__':
    app.run(debug=True)
