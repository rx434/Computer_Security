Summary: 
This is the first version of my SWS (shared with security) system to protect security of IoT cloud which is based on MQTT protocol. It simulates the MQTT protocols in Python, and also build an authentication progress into it, which doesn't exist in current MQTT protocols. 

Configuration: 
main language: Python
interpreter: 3.8

Code structure:
|---README.txt
|---object.py
|---subject_device.py
|---subject_user.py
|---server.py
|---reference_monitor.py
|---test1.py
|---test2.py
|---test3.py

Explanation:
object.py: inplement the message class in MQTT protocol
subject_device.py: inplement device class in MQTT protocol, which is allowed to do connect, subscribe, publish and receive messages. 
subject_user.py: inplement user and admin class in MQTT protocol, which is allowed to do connect, subscribe, publish and receive messages. Moreover, the admin class is inherited from user class, which has the authorties to add or remove users into or from the trust lists. 
server.py: simulate the IoT cloud based on MQTT protocol, which is used to handle messages from subjects. 
reference_monitor.py: inplement a reference monitor based on MQTT protocol. It will check whether an object's owner is in the trusted list stored in admin's local enviorment. 
test1.py: test what happens when the admin publish the messages to devices. 
test2.py: test what happens when a user, who is not in admin's trusted list yet, publish the messages to devices. 
test3.py: test what happens when a user, who is now in admin's trusted list, publish the message to devices. 

Installation and run (On Windows):
1. get the zip code and unzip it.
2. In your Anaconda Prompt, create a new enviornment by using the following command:
conda create -n (your enviornment name) python=3.8
3. In your Anaconda Prompt, activate the enviornment by using the following command:
activate (your enviornment name)
4. Go to the path of this system and type:
python test1.py
then you can see the details of the corresponding test. 
