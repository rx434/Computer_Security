from server import Cloud
from subject_user import Subject, Admin
from object import Message
from reference_monitor import reference_monitor_initialization

if __name__ == '__main__':
    print('Initilization IoT environment...')
    cloud = Cloud()
    admin = Admin(0)
    device1 = Subject(1, admin)
    device2 = Subject(2, admin)
    user = Subject(3, admin)
    adversary = Subject(4, admin)
    print('Build 1 admin, 1 user, 1 adversary and 2 devices.')

    print('Connect them to the IoT Cloud:')
    admin.connect(admin, cloud)
    device1.connect(device1, cloud)
    device2.connect(device2, cloud)
    user.connect(user, cloud)
    adversary.connect(adversary, cloud)

    print('Initialize the reference monitor:')
    reference_monitor_initialization(cloud, [device1, device2, user, adversary], admin)

    print('Firstly the admin put these subjects into one group, except the adversary:')
    admin.add_user(device1, 'test_group')
    admin.add_user(device2, 'test_group')
    admin.add_user(user, 'test_group')

    print('Subscription: device 1 -> 1/cmd \n user -> 1/status')
    device1.subscribe(device1, '{}/cmd'.format(device1.id), cloud)
    user.subscribe(user, '{}/status'.format(device1.id), cloud)

    print('Then the user ask the device to close')
    message = Message(user, '{}/cmd'.format(device1.id), 'Close')
    user.publish(message, cloud)

    print("Unfortunately, it fails. So the device plans to respond 'Fail' to the user")
    print("However, the adversary is faster than the device to respond 'Success' to the user")
    message_a = Message(adversary, '{}/status'.format(device1.id), 'Success')
    adversary.publish(message_a, cloud)
    message_d = Message(device1, '{}/status'.format(device1.id), 'Fail')
    device1.publish(message_d, cloud)

    print('Now the user receives:', user.get_all_message('{}/status'.format(device1.id)))
