Summary: 
This is the first version of my SWS (shared with security) system to protect security of IoT cloud which is based on MQTT protocol. It simulates the MQTT protocols in Python, and also build an authentication progress into it, which doesn't exist in current MQTT protocols. 

Configuration: 
main language: Python
interpreter: 3.8

Code structure:
|---README.txt
|---README-Attacks.txt
|---object.py
|---subject_device.py
|---subject_user.py
|---server.py
|---reference_monitor.py
|---will_message_attack.py
|---retained_message_attack.py
|---Non_updated_session_lifecycle_state_attack.py

Explanation:
object.py: inplement the message class in MQTT protocol
subject_device.py: inplement device class in MQTT protocol, which is allowed to do connect, subscribe, publish and receive messages. 
subject_user.py: inplement user and admin class in MQTT protocol, which is allowed to do connect, subscribe, publish and receive messages. Moreover, the admin class is inherited from user class, which has the authorties to add or remove users into or from the trust lists. 
server.py: simulate the IoT cloud based on MQTT protocol, which is used to handle messages from subjects. 
reference_monitor.py: inplement a reference monitor based on MQTT protocol. It will check whether an object's owner is in the trusted list stored in admin's local enviorment. 
will_message_attack.py: Demonstrate how will message attack works and how this system prevents it.
retained_message_attack.py: Demonstrate how retained message attack works and how this system prevents it.
Non_updated_session_lifecycle_state_attack.py: Demonstrate how this attack works and how this system prevents it. 
README-Attacks.txt： Detailed information of these three attacks.

Installation and run (On Windows):
1. get the zip code and unzip it.
2. In your Anaconda Prompt, create a new enviornment by using the following command:
conda create -n (your enviornment name) python=3.8
3. In your Anaconda Prompt, activate the enviornment by using the following command:
activate (your enviornment name)
4. Go to the path of this system and type:
python test1.py
then you can see the details of the corresponding test.

New Version of this system:
I improve this system a little bit. One difference is that now all the subjects, no matter it is user or device, use the same class called 'Subject'. As a result, I delete the file of subject_device and change the name of the file 'subject_user.py' as 'subject.py'.
The second difference is that I change the structure of trusted list into a group. Instead of using trusted list of users, the admin now can put any users and devices into the same group. The logic of the reference monitor also changes: It will check whether the owner of the message is in the same group with the receipt. If so, then the receipt can have the right to receive the message. Otherwise, the message will be blocked.
