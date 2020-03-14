import pulsar


class PulsarStore:

    def __init__(self, ip, port):
        self.url = "pulsar://%s:%s" % (ip, port)

    def getClient(self):
        return pulsar.Client(self.url)

    def createProcuder(self, client, topic_name):
        return client.create_producer(topic_name)

    def createConsumer(self, client, topic_name, sub):
        return client.subscribe(topic_name, sub)


    def test(self):
        cl = self.getClient()
        pro = self.createProcuder(cl, "newspaper")
        for i in range(50):
            print("send ...")
            pro.send(('Hello-%d' % i).encode('utf-8'))
        cl.close()


    def test2(self):
        cl = self.getClient()
        consumer = self.createConsumer(cl, "newspaper", "news")
        while True:
            msg = consumer.receive()
            try:
                print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
                # Acknowledge successful processing of the message
                consumer.acknowledge(msg)
            except:
                # Message failed to be processed
                consumer.negative_acknowledge(msg)
        cl.close()

    def test3(self):
        rp = open("./test.jsonl", 'r')
        cl = self.getClient()
        pro = self.createProcuder(cl, "newspaper")
        for v in rp:
            print(v)
            pro.send(v.encode('utf-8'))
        rp.close()
        cl.close()
        
        



if __name__ == "__main__":
    rr = PulsarStore("localhost", 6650)
    rr.test3()

        
