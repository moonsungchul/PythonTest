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
        for i in range(10):
            pro.send(('Hello-%d' % i).encode('utf-8'))
        cl.close()

        '''
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
        '''



if __name__ == "__main__":
    rr = PulsarStore("172.17.0.5", 6650)
    rr.test()

        