# PRODIGY 使用文档

本项目是在对 [EXPLOSION prodigy](https://prodi.gy/) 逆向工程的基础上增添若干功能实现。

![readme_1.png](https://i.loli.net/2019/06/21/5d0c1c0b19eea52775.png)

## 使用文档

工具分左右视图，左侧为信息栏，右侧为工作区，右侧下方是标记工具栏。

### 信息栏

 - __`NEW ENTITIES`__ 为当前批次标记中新增的实体。
 - __`HISTORY`__ 为当前批次标记中已完成标记的文档。记录上单击可以将记录重新放回工作区。

__注意：__ 一旦提交，此两栏将清空。

### 工具栏

 - __`Accept`__ 认定当前新闻标记完毕，放入 `HISTORY` 等待上传，，`revise='accept'`；
 - __`Ignore`__ 跳过当前新闻，放入 `HISTORY`，`revise='ignore'`；
 - __`Undo`__ 将上一条标记内容取回工作区；
 - __`Submit`__ 将 `HISTORY` 中的新闻和 `NEW ENTITIES` 中的实体上传到服务器。

__注意：__ 如果关闭浏览器，未上传（`Submit`）的标记记录将无法恢复!

### 工作区

__已知词自动高亮__

加载时所有已知词会自动被标记。

__防无意操作__

任何时刻有且仅有一篇新闻被激活（可以标记），防止无意识的错误点击。

> “被激活”体现在：新闻上方出现蓝色的标签框、新闻正文不再半透明、新闻可以标记。

__标记和取消标记__

当某个标签（示例图中，共有三个标签：“关键词”、“公司”、“垃圾”）被选中后，之后所有的标记将被认定为该标签类下的实体。

鼠标选中一段文字后松开即可完成标记。

单击已标记区域即可取消该区域的标记。

__新闻溯源__

每条新闻右下角有该新闻来源和ID，点击该区域可以访问新闻原网页。

__批量标记__

右上角的开关状态为`BATCH`时，每次标记会使当前页面上（之后的新闻需要提交后才生效）所有新闻的相关词被标记；反之为`SINGLE`时，只有当前新闻的当前词被标记。取消标记亦然。

__无限滚动__

当滚动到页面底端的时候会自动拉取下一批的新闻。

### 快捷键

- __`A`__   ：   `Accept`
- __`Space`__   ：   `Ignore`
- __`Backspace`/`Delete`__   ：   `Undo`
- __`Tab`__   ：   `BATCH`状态改变
- __`1` ~ `9`__   ：   不同`label`之间切换

----------


## 接口文档

### GET /api/news?n=\<number\>

#### 格式

json

#### requst

null

#### response

```python
{
    'name': <数据名称: str>,
    'items': <新闻列表: list>,
    'labels': [<标签 1: str>, <标签 2: str>, ...],
    'user': <操作员昵称: str>,
    'load_batch': <一次请求获取的新闻数量: int=3>,
    'doc_num': <数据库中所有未标记新闻数量: int>
}
```

其中，`items` 为长度 `number` 的数组，每个元素如下：

```python
{
    'id': <新闻ID: str>,
    'source': <新闻来源: str>,
    'tokens': <新闻正文token列表: list>,
    'link': <原文链接: str>,
    'entities': <已知实体: list>
}
```

`body` 中可以包含回车符 `\n`，`entities` 是可选的，若指定，格式如下：

```python
{
    'text': <实体字符串: str>, 
    'span': <实体起始和结束字符下标: list>,
    'label': <实体类型: str>,
    'source': <实体来源: str>,
    'confidence': <实体可信度: float>
}
```

 - 实体来源可以是 `NER`（命名实体服务自动标注）、`DICT`（术语库匹配）、`Theo`（标记员用户名）等。

 - 实体可信度为`NER`专用的参数，表示每个实体的可信度，在前端展示时会用透明度可视化，色彩越深越可信。


#### 示例 response

```python
{
    "doc_num": 3,
    "items": [
        {
            "entities": [
                {
                    "confidence": 1,
                    "label": 0,
                    "source": "NER",
                    "span": [
                        36,
                        42
                    ],
                    "text": "损害责任追究"
                },
                {
                    "confidence": 1,
                    "label": 0,
                    "source": "NER",
                    "span": [
                        44,
                        46
                    ],
                    "text": "问责"
                },
                {
                    "confidence": 1,
                    "label": 0,
                    "source": "NER",
                    "span": [
                        56,
                        58
                    ],
                    "text": "问责"
                }
            ],
            "id": "472398",
            "link": "http://www.baidu.com",
            "source": "新浪财经",
            "tokens": [
                "3",
                "月",
                "29",
                "日",
                "，",
                "生",
                "态",
                "环",
                "境",
                "部",
                "网",
                "站",
                "发",
                "布",
                "的",
                "《",
                "甘",
                "肃",
                "省",
                "通",
                "报",
                "中",
                "央",
                "环",
                "境",
                "保",
                "护",
                "督",
                "察",
                "移",
                "交",
                "生",
                "态",
                "环",
                "境",
                "损",
                "害",
                "责",
                "任",
                "追",
                "究",
                "问",
                "题",
                "问",
                "责",
                "情",
                "况",
                "》",
                "(",
                "以",
                "下",
                "简",
                "称",
                "“",
                "《",
                "问",
                "责",
                "情",
                "况",
                "》",
                "”",
                ")",
                "显",
                "示",
                "，",
                "白",
                "银",
                "有",
                "色",
                "集",
                "团",
                "股",
                "份",
                "有",
                "限",
                "公",
                "司"
            ]
        }
    ],
    "labels": [
        "关键词",
        "公司",
        "严重度"
    ],
    "load_batch": 1,
    "name": "News",
    "user": "Theo"
}
```

### POST /api/news

#### 格式

json

#### requst

```python
{
    'operator': 'Theo', 
    'items': [
        {
            'id': <新闻唯一id: str>,
            'entities': (同上)
        },
        {...}
    ], 
    'new_hot_words': <标记中新出现的关键词: dict>
}
```

#### 示例 requst

```python
{
    "operator": "Theo",
    "items": [
        {
            "id": "472398",
            "entities": [
                {
                    "text": "罚款",
                    "span": [
                        1044,
                        1046
                    ],
                    "label": "关键词",
                    "source": "NER"
                },
                {
                    "text": "违法",
                    "span": [
                        1102,
                        1104
                    ],
                    "label": "严重度",
                    "source": "NER"
                },
                {
                    "text": "白银有色",
                    "span": [
                        84,
                        88
                    ],
                    "label": "公司",
                    "source": "Theo"
                },
                {
                    "text": "白银有色",
                    "span": [
                        66,
                        70
                    ],
                    "label": "公司",
                    "source": "Theo"
                }
            ]
        }
    ],
    "new_hot_words": {
        "白银有色": "公司"
    }
}
```


#### response

```python
{'status':'success'}
```

__注意：__ 一定要有这个返回，否则前端会报错。

