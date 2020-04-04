
from InfluxStore import InfluxStore
from Log import Log


class InfluxLogger:

    def __init__(self, store):
        self.influx = store

    def info(self, key, msg):
        log = Log(ltype="INFO", key = key, msg=msg)
        self.influx.write(log.toInflux())

    def debug(self, key, msg):
        log = Log(ltype="DEBUG", key = key, msg=msg)
        self.influx.write(log.toInflux())

    def error(self, key, msg):
        log = Log(ltype="ERROR", key = key, msg=msg)
        self.influx.write(log.toInflux())

if __name__ == '__main__':
    hh = "localhost"
    port = 28086
    dbname = "NewsCrawlerLog"
    store = InfluxStore(hh, port)
    store.switchDB(dbname)
    logger = InfluxLogger(store)
    logger.info("Test1", "우하하 테스트 하자 ")