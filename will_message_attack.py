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
    print('Admin ID:0')
    print('device1 ID:1')
    print('device2 ID:2')
    print('user ID:3')
    print('adversary ID:4')

    print('Connect them to the IoT Cloud:')
    admin.connect(admin, cloud)
    device1.connect(device1, cloud)
    device2.connect(device2, cloud)
    user.connect(user, cloud)
    adversary.connect(adversary, cloud, will_message=True, content='Some malicious commands')
    print("The adversary has a will message 'Some malicious commands'")

    print('Initialize the reference monitor:')
    reference_monitor_initialization(cloud, [device1, device2, user, adversary], admin)

    print('Firstly the admin put these four subjects into one group:')
    admin.add_user(device1, 'test_group')
    admin.add_user(device2, 'test_group')
    admin.add_user(user, 'test_group')
    admin.add_user(adversary, 'test_group')

    print('Subscription: device 1 -> 1/cmd \n admin -> 1/status \n user -> 1/status \n adversary -> 1/cmd')
    device1.subscribe(device1, '{}/cmd'.format(device1.id), cloud)
    admin.subscribe(admin, '{}/status'.format(device1.id), cloud)
    user.subscribe(user, '{}/status'.format(device1.id), cloud)
    adversary.subscribe(adversary, '{}/cmd'.format(device1.id), cloud)

    print('Subscription: device 2 -> 2/cmd \n admin -> 2/status \n user -> 2/status \n adversary -> 2/cmd')
    device2.subscribe(device2, '{}/cmd'.format(device2.id), cloud)
    admin.subscribe(admin, '{}/status'.format(device2.id), cloud)
    user.subscribe(user, '{}/status'.format(device2.id), cloud)
    adversary.subscribe(adversary, '{}/cmd'.format(device2.id), cloud)

    print('Then both users publish commands to both devices')
    message1 = Message(user, '{}/cmd'.format(device1.id), 'Start1 from user')
    message2 = Message(user, '{}/cmd'.format(device2.id), 'Start2 from user')
    message3 = Message(adversary, '{}/cmd'.format(device1.id), 'Start1 from adversary')
    message4 = Message(adversary, '{}/cmd'.format(device2.id), 'Start2 from adversary')
    print('User ------Start1 from user------> 1/cmd')
    print('User ------Start2 from user------> 2/cmd')
    print('Adversary ------Start1 from adversary------> 1/cmd')
    print('Adversary ------Start2 from adversary------> 2/cmd')
    user.publish(message1, cloud)
    user.publish(message2, cloud)
    adversary.publish(message3, cloud)
    adversary.publish(message4, cloud)

    received1 = device1.get_all_message('{}/cmd'.format(device1.id))
    received2 = device2.get_all_message('{}/cmd'.format(device2.id))

    print('What device1 get until now:', received1)
    print('What device2 get until now:', received2)

    print('Then the admin remove the adversary from the group')
    admin.remove_user(adversary, 'test_group')

    print('After that, the adversary tries to purposefully disconnect from the cloud, triggering the will message')
    adversary.accident_disconnect(cloud)

    received1 = device1.get_all_message('{}/cmd'.format(device1.id))
    received2 = device2.get_all_message('{}/cmd'.format(device2.id))

    print('What device1 get after disconnection of adversary:', received1)
    print('What device2 get after disconnection of adversary:', received2)
