# rasp-arduino-mqtt-highcharts
communication among raspberry pi / arduino / mqtt broker / mqtt subscriber / higcharts visualizsation

Led_Arduino_Raspberry.py -> Sets up the broker and request value from Arduino

Potiauslesen.ino -> Arduino File with logic and providing value

subscriber.py -> Example for a mqtt subscriber in python

get.js -> Example for a mqtt subscriber in javascript (requieres npm install mqtt)

index.html -> Visualize data from the mqtt broker (requieres mqttws31.js)

mqttws31.js -> Requirement for index.html
