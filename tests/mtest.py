import paho.mqtt.publish as publish

publish.single("gateway/", "request", hostname="192.168.1.8", qos=0)
