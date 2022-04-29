from server import Cloud
from subject_device import Device
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

    print('Firstly the admin put these four subjects into one group:')
    admin.add_user(device1, 'test_group')
    admin.add_user(device2, 'test_group')
    admin.add_user(user, 'test_group')
    admin.add_user(adversary, 'test_group')

    print("Then the adversary publish a retained message to a topic 1/cmd and 2/cmd with the content 'Malicious retained message'. ")
    message1 = Message(adversary, '{}/cmd'.format(device1.id), 'Malicious retained message')
    message2 = Message(adversary, '{}/cmd'.format(device2.id), 'Malicious retained message')
    adversary.publish(message1, cloud, retained=True)
    adversary.publish(message2, cloud, retained=True)

    print('Then device1 subscribe to topic 1/cmd')
    device1.subscribe(device1, '{}/cmd'.format(device1.id), cloud)

    received1 = device1.get_all_message('{}/cmd'.format(device1.id))
    print('Now device1 receives:', received1)

    print('Then the admin remove the adversary from the group')
    admin.remove_user(adversary, 'test_group')

    print('Then device2 subscribe to topic 2/cmd')
    device2.subscribe(device2, '{}/cmd'.format(device2.id), cloud)

    received2 = device2.get_all_message('{}/cmd'.format(device2.id))
    print('Now device2 receives:', received2)
