from object import Message
from reference_monitor import reference_monitor_check


class Subject:
    def __init__(self, subjectid, admin):
        self.id = subjectid
        self.topic_dic = {}
        self.admin = admin
        self.will = False

    def connect(self, user, cloud, will_message=False, content=None):
        cloud.handle_user_connect(user)
        self.connected_cloud = cloud
        if will_message:
            self.will = True
            self.will_message_list = []
            self.will_message_content = content


    def subscribe(self, user, topic, cloud):
        cloud.handle_subscribtion(user, topic)
        if self.will:
            will_message = Message(self, topic, self.will_message_content)
            self.will_message_list.append(will_message)

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

    def accident_disconnect(self, cloud):
        if self.will:
            for message in self.will_message_list:
                self.publish(message, cloud)


class Admin(Subject):
    def __init__(self, subjectid):
        Subject.__init__(self, subjectid, self)
        self.groups = {}

    def add_user(self, user, group_name):
        group = self.groups.get(user)
        if group is None:
            self.groups[user] = [group_name]
        else:
            self.groups[user].append(group_name)

    def remove_user(self, user, group_name):
        group = self.groups.get(user)
        group.remove(group_name)

    def remove_user_completely(self, user):
        return self.groups.pop(user, "Not Found")

    def receive(self, message):
        self.topic_dic[message.topic].append(message)
