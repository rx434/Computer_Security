from server import Cloud
from subject_device import Device
from subject_user import User, Admin
from object import Message
from reference_monitor import reference_monitor_initialization

if __name__ == '__main__':
    print('Initilization IoT environment...')
    cloud = Cloud()
    admin = Admin(0)
    device1 = Device(1, admin)
    device2 = Device(3, admin)
    user = User(2)
    print('Build 1 admin, 1 user and 2 devices.')

    print('Connect them to the IoT Cloud:')
    admin.connect(admin, cloud)
    device1.connect(device1, cloud)
    device2.connect(device2, cloud)
    user.connect(user, cloud)

    print('Initialize the reference monitor:')
    reference_monitor_initialization(cloud, device1, admin)
    reference_monitor_initialization(cloud, device2, admin)

    print('Subscription: device 1 -> 1/cmd \n admin -> 1/status \n user -> 1/status')
    device1.subscribe(device1, '{}/cmd'.format(device1.deviceid), cloud)
    admin.subscribe(admin, '{}/status'.format(device1.deviceid), cloud)
    user.subscribe(user, '{}/status'.format(device1.deviceid), cloud)

    print('Subscription: device 2 -> 2/cmd \n admin -> 2/status \n user -> 2/status')
    device2.subscribe(device2, '{}/cmd'.format(device2.deviceid), cloud)
    admin.subscribe(admin, '{}/status'.format(device2.deviceid), cloud)
    user.subscribe(user, '{}/status'.format(device2.deviceid), cloud)

    message1 = Message(admin, '{}/cmd'.format(device1.deviceid), 'Start')
    message2 = Message(admin, '{}/cmd'.format(device2.deviceid), 'Close')
    message3 = Message(admin, '{}/cmd'.format(device1.deviceid), 'turn temperature to 72')
    message4 = Message(admin, '{}/cmd'.format(device2.deviceid), 'Start when the time is 9:00 a.m.')
    print('Admin starts to send message to both devices')
    print('Admin ------Start------> 1/cmd')
    print('Admin ------Close------> 2/cmd')
    print('Admin ------turn temperature to 72------> 1/cmd')
    print('Admin ------Start when the time is 9:00 a.m.------> 2/cmd')
    admin.publish(message1, cloud)
    admin.publish(message2, cloud)
    admin.publish(message3, cloud)
    admin.publish(message4, cloud)

    received1 = device1.get_all_message('{}/cmd'.format(device1.deviceid))
    received2 = device2.get_all_message('{}/cmd'.format(device2.deviceid))

    print('What device1 get:', received1)
    print('What device2 get:', received2)
