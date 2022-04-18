from object import Message


def reference_monitor_initialization(cloud, device, admin):
    device.subscribe(device, '{}/{}/trusted'.format(admin.userid, device.deviceid), cloud)
    admin.subscribe(admin, '{}/{}/request'.format(admin.userid, device.deviceid), cloud)


def reference_monitor_check(cloud, device, admin, message_owner):
    message = Message(device, '{}/{}/request'.format(admin.userid, device.deviceid), message_owner)
    device.publish(message, cloud)
    request = admin.topic_dic['{}/{}/request'.format(admin.userid, device.deviceid)][-1].content
    if request in admin.authorized_users:
        result = 1
    else:
        result = 0

    back_message = Message(admin, '{}/{}/trusted'.format(admin.userid, device.deviceid), result)
    admin.publish(back_message, cloud)
    trusted = device.topic_dic['{}/{}/trusted'.format(admin.userid, device.deviceid)][-1].content
    return trusted


