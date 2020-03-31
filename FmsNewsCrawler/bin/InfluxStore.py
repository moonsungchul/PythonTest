

from influxdb import InfluxDBClient
from Log import Log

class InfluxStore:

    def __init__(self, host, port):
        self.host = host
        self.port = port 
        self.client = InfluxDBClient(host=self.host, port=self.port) 
    

    def createDB(self, dbname):
        self.client.create_database(dbname)


    def switchDB(self, dbname):
        self.client.switch_database(dbname)


    def openDB(self, dbname, host, port):
        self.client = InfluxDBClient(database=dbname, host=host, port=port)
        return self.client


    def getLogs(self):
        sql = "select * from log"
        rs = self.client.query(sql)
        buf = []
        for po in rs.get_points():
            log = Log()
            log.parseDic(po)
            buf.append(log)
        return buf

    def test(self):
        hh = "localhost"
        port = 28086
        dbname = "NewsCrawlerLog"
        cl = self.openDB(dbname, hh, port)

        buf = []
        for v in range(100):
            ss = "Test msg %d" % (v)
            log = Log("DEBUG", "TEST", ss)
            #print(log.toInflux())
            buf.append(log.toInflux())

        cl.write_points(buf)

        sql = "select * from log"
        rs = cl.query(sql)
        for po in rs.get_points():
            print(po)

        rs = self.getLogs()
        for v in rs:
            print(v.toDic())


if __name__ == '__main__':
    hh = "localhost"
    port = 28086
    dbname = "NewsCrawlerLog"
    store = InfluxStore(hh, port)
    #store.createDB(dbname)
    #store.switchDB(dbname)
    #store.openDB(dbname, hh, port)
    store.test()
    
