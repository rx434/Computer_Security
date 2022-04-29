from reference_monitor import reference_monitor_check


class Device:
    def __init__(self, deviceid, admin):
        self.id = deviceid
        self.topic_dic = {}
        self.admin = admin

    def connect(self, device, cloud):
        cloud.handle_device_connect(device)
        self.connected_cloud = cloud

    def subscribe(self, device, topic, cloud):
        cloud.handle_subscribtion(device, topic)

    def publish(self, message, cloud, retained=False):
        cloud.handle_publish(message, retained)

    def receive(self, message):
        if message.owner == self.admin:
            self.topic_dic[message.topic].append(message)
        else:
            trusted = reference_monitor_check(self.connected_cloud, self, self.admin, message.owner)
            if trusted:
                self.topic_dic[message.topic].append(message)
            else:
                rejected_message = message
                rejected_message.content = 'You are not allowed to receive this message'
                self.topic_dic[message.topic].append(rejected_message)

    def get_latest_message(self, topic):
        return self.topic_dic[topic][-1].owner, self.topic_dic[topic][-1].topic, self.topic_dic[topic][-1].content

    def get_all_message(self, topic):
        message_list = []
        for message in self.topic_dic[topic]:
            message_list.append( (message.owner, message.topic, message.content,) )
        return message_list