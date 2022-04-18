class User:
    def __init__(self, userid):
        self.userid = userid
        self.topic_dic = {}

    def connect(self, user, cloud):
        cloud.handle_user_connect(user)
        self.connect_cloud = cloud

    def subscribe(self, user, topic, cloud):
        cloud.handle_subscribtion(user, topic)

    def publish(self, message, cloud):
        cloud.handle_publish(message)

    def receive(self, message):
        self.topic_dic[message.topic].append(message)

    def get_latest_message(self, topic):
        return self.topic_dic[topic][-1].owner, self.topic_dic[topic][-1].topic, self.topic_dic[topic][-1].content

    def get_all_message(self, topic):
        message_list = []
        for message in self.topic_dic[topic]:
            message_list.append( (message.owner, message.topic, message.content,) )
        return message_list

class Admin(User):
    def __init__(self, userid):
        User.__init__(self, userid)
        self.authorized_users = []

    def append_users(self, user):
        self.authorized_users.append(user)

    def remove_users(self, user):
        self.authorized_users.remove(user)
