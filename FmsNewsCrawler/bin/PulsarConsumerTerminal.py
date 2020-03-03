import pulsar

from PulsarStore import PulsarStore


class PulsarConsumerterminal:

    def __init__(self, ip, port):
        self.store = PulsarStore(ip, port)


    def startConsumer(self):
        cl = self.store.getClient()
        con = self.store.createConsumer(cl, "newspaper", "news")
        while True:
            msg = con.receive()
            try:
                print("Received message '{}' id='{}'".format(msg.data().decode(), msg.message_id()))
                # Acknowledge successful processing of the message
                con.acknowledge(msg)
            except:
                # Message failed to be processed
                con.negative_acknowledge(msg)
        cl.close()

if __name__ == '__main__':
    rr = PulsarConsumerterminal("172.17.0.5", 6650)
    rr.startConsumer()
