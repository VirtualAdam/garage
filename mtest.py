import paho.mqtt.publish as publish

publish.single("lex/garage1/", "mqtt test", hostname="192.168.1.4", qos=1)
