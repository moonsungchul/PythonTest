
import json


class Article:
    """
    news 기사를 저장한다. 
    """

    def __init__(self, title, stext):
        self.title = title
        self.text = stext

    def toDic(self):
        dic = {}
        dic['title'] = self.title
        dic['text'] = self.text
        return dic

    def toJson(self):
        return json.dumps(self.toDic())
