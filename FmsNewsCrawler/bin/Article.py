
import json


class Article:
    """
    news 기사를 저장한다. 
    """

    def __init__(self, title, stext,  company):
        self.title = title
        self.text = stext
        self.company = company

    def toDic(self):
        dic = {}
        dic['title'] = self.title
        dic['text'] = self.text
        dic['company'] = self.company
        return dic

    def toJson(self):
        return json.dumps(self.toDic())
