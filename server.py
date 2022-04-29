class Cloud:
    def __init__(self):
        self.subscribtion_dic = {}
        self.connected_devices = []
        self.connected_users = []
        self.retained_message = {}

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

        if self.retained_message.get(topic) is not None:
            client.receive(self.retained_message[topic])

    def handle_publish(self, message, retained):
        if not retained:
            message_topic = message.topic
            topic_clients = self.subscribtion_dic[message_topic]
            for client in topic_clients:
                client.receive(message)
        else:
            message_topic = message.topic
            self.retained_message[message_topic] = message





