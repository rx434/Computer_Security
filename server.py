class Cloud:
    def __init__(self):
        self.subscribtion_dic = {}
        self.connected_devices = []
        self.connected_users = []

    def handle_device_connect(self, device):
        self.connected_devices.append(device)

    def handle_user_connect(self, user):
        self.connected_users.append(user)

    def handle_subscribtion(self, client, topic):
        existing_topic = self.subscribtion_dic.get(topic, [])
        existing_topic.append(client)
        if client.topic_dic.get(topic, None) is None:
            client.topic_dic[topic] = []
        self.subscribtion_dic[topic] = existing_topic

    def handle_publish(self, message):
        message_topic = message.topic
        topic_clients = self.subscribtion_dic[message_topic]
        for client in topic_clients:
            client.receive(message)




