from object import Message


def reference_monitor_initialization(cloud, subject_list, admin):
    for subject in subject_list:
        subject.subscribe(subject, '{}/{}/trusted'.format(admin.id, subject.id), cloud)
        admin.subscribe(admin, '{}/{}/request'.format(admin.id, subject.id), cloud)


def reference_monitor_check(cloud, subject, admin, message_owner):
    message = Message(subject, '{}/{}/request'.format(admin.id, subject.id), message_owner)
    subject.publish(message, cloud)
    request = admin.topic_dic['{}/{}/request'.format(admin.id, subject.id)][-1].content

    subject_group = admin.groups.get(subject, [])
    request_group = admin.groups.get(request, [])

    if list(set(subject_group) & set(request_group)) == []:
        result = 0
    else:
        result = 1

    back_message = Message(admin, '{}/{}/trusted'.format(admin.id, subject.id), result)
    admin.publish(back_message, cloud)
    trusted = subject.topic_dic['{}/{}/trusted'.format(admin.id, subject.id)][-1].content
    return trusted


