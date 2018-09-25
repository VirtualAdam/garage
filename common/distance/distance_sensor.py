#!/usr/bin/python
from gpiozero import DistanceSensor
import time
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.1, max_distance=3)
while True:
      print(ultrasonic.distance)
      time.sleep(1)