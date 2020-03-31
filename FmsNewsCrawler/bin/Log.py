
from datetime import datetime

class Log:

    def __init__(self, ltype="", key="", msg=""):
        self.log_time = str(datetime.now())
        self.log_type = ltype
        self.log_key = key
        self.log_msg = msg 


    def toDic(self):
        dic = {}
        dic['time'] = self.log_time
        dic['type'] = self.log_type
        dic['key'] = self.log_key
        dic['msg'] = self.log_msg
        return dic

    def parseDic(self, dic):
        self.log_time = dic['time']
        self.log_type = dic['type']
        self.log_key = dic['key']
        self.log_msg = dic['msg']


    def toInflux(self):
        dic = {
            "measurement": "log", 
            "time": self.log_time, 
            "fields": {
                "type":self.log_type, 
                "key": self.log_key, 
                "msg": self.log_msg
            }
        }
        return dic
        