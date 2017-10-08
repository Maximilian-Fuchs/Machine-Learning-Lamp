import paho.mqtt.client as mqtt
from nltk.collections import defaultdict
import time
import datetime
from astral import Astral
import pytz
from LampControl import *

class DataCollector:
	"""Collects current MQTT Values and serializes for usage in NLTK"""

	# Returns plain current values dictionary
	def getLatestDecisionTreeValuesDict(self):
		# Can be used to augment dict with time, sunrise, sundown etc.
		decision_tree_values_dict = self.getLatestRawValuesDict()

		#assign connection state of wlan devices
		devices = [attribute for attribute in self.data_attributes if 'tk3iot' in attribute]
		for device in devices:
			connection_state = float(decision_tree_values_dict[device])
			if connection_state == 0:
				decision_tree_values_dict[device] = 'DISCONNECTED'
			else:
				decision_tree_values_dict[device] = 'CONNECTED'

		#assign approximate daytime
		daytime_hour = (1/60)*decision_tree_values_dict['Daytime']
		daytime = ''
		if daytime_hour < 6 or daytime_hour > 23:
			daytime = 'NIGHT'
		elif daytime_hour < 9:
		    daytime = 'EARLY_MORNING'
		elif daytime_hour < 12:
		    daytime = 'MORNING'
		elif daytime_hour < 15:
		    daytime = 'EARLY_AFTERNOON'
		elif daytime_hour < 18:
		    daytime = 'LATE_AFTERNOON'
		elif daytime_hour < 21:
		    daytime = 'EVENING'
		elif daytime_hour <= 23:
		    daytime = 'LATE_EVENING'
		decision_tree_values_dict['Daytime'] = daytime

		return decision_tree_values_dict

	def getLatestRawValuesDict(self):
		# Can be used to augment dict with time, sunrise, sundown etc.
		raw_values_dict = {}
		#make sure every attribute is assigned a value. (Defaultdict Value = 0.0)
		for attribute in self.data_attributes:
			raw_values_dict[attribute] = self.latest_sensor_values[attribute]

	    #get Weekday
		datetime_object = time.strptime(time.ctime(), '%a %b %d %H:%M:%S %Y')
		weekday = datetime_object.tm_wday
		raw_values_dict['Weekday'] = weekday

		#get Daytime
		minutes_since_midnight = datetime_object.tm_hour*60 + datetime_object.tm_min
		raw_values_dict['Daytime'] = minutes_since_midnight

		#get Sunlight
		a = Astral()
		a.solar_depression = 'civil'
		city = a['Berlin']
		sun = city.sun(local=True)
		dto = datetime.datetime.now(pytz.timezone('Europe/Amsterdam'))
		if dto > sun['sunrise'] and dto <= sun['sunset']:
		    daylight = True
		else:
		    daylight = False
		raw_values_dict['Daylight'] = daylight

		#get Lamp State
		if self.lamp.is_lamp_on():
			lampstate = 'On'
		else:
			lampstate = 'Off'
		raw_values_dict['Lamp'] = lampstate

		#return
		return raw_values_dict

	# Returns serialized version of dictionary
	def getLatestRawValuesString(self):
		sensor_data_touples = list(self.getLatestRawValuesDict().items())
		tab = '\t'
		values_string = tab.join([str(topic)+' '+str(payload) for (topic, payload) in sensor_data_touples])
		return values_string

	def getLatestDecisionTreeValuesString(self):
		sensor_data_touples = list(self.getLatestDecisionTreeValuesDict().items())
		tab = '\t'
		values_string = tab.join([str(topic)+' '+str(payload) for (topic, payload) in sensor_data_touples])
		return values_string


	# The callback for when the client receives a CONNACK response from the server.
	def on_connect(self, client, userdata, flags, rc):
	    print("Connected with result code "+str(rc))
	    client.subscribe("tk3iot/#")

	# The callback for when a PUBLISH message is received from the server.
	def on_message(self, client, userdata, msg):
	    self.latest_sensor_values[msg.topic] = msg.payload

	# Initalize MQTT CLient and values dictionary
	def __init__(self):
		self.lamp = LampControl()
		self.latest_sensor_values = defaultdict(float)
		self.data_attributes = ['Weekday', 'Daytime', 'Daylight', 'tk3iot/PC', 'tk3iot/iPhone', 'tk3iot/iPad', 'tk3iot/android', 'tk3iot/esp1', 'tk3iot/esp2', 'tk3iot/kindle', 'Lamp']
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		# 192.168.1.226
		self.client.connect("192.168.1.226", 1883, 60)

	# Method blocks; enabled constant receiving of mqtt events
	def startMQTTLoop(self):
		self.client.loop_forever()
