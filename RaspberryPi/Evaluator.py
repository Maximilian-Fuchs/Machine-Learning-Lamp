from DataCollector import *
from LampControl import *
import threading
import random
import pickle

# START CONFIGURATION

sampleTimeInSeconds = 5

# END CONFIGURATION
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def iot_features(rawdata):
    datapoints = rawdata.split('\n')[:-1]
    datapoints = [datapoint.split('\t') for datapoint in datapoints]
    datapoints = [[(entry.split(' ')[0], entry.split(' ')[1]) for entry in datapoint if len(entry.split(' ')) == 2] for datapoint in datapoints]
    datapoint_dicts = [dict(datapoint) for datapoint in datapoints]
    return removekey(datapoint_dicts[0], 'Lamp')

collector = DataCollector()
lamp = LampControl()

#load model
f = open('model/decisiontree_classifier.pickle', 'rb')
model = pickle.load(f)
f.close()

def evalModelAndReact():
	def evalModel():
		# todo query model with current DataCollector values
		data = collector.getLatestDecisionTreeValuesString()
		data_dict = iot_features(data)
		desired_state = model.classify(data)
		boolstate = False
		if desired_state == 'On':
			boolstate = True

		return boolstate

	if evalModel():
		print ("Lamp should be ON. Lamp Status: {}".format(lamp.statusReadable()))
		if not lamp.is_lamp_on():
			lamp.turnOn()
	else:
		print ("Lamp should be OFF. Lamp Status: {}".format(lamp.statusReadable()))
		if lamp.is_lamp_on():
			lamp.turnOff()

	threading.Timer(sampleTimeInSeconds, evalModelAndReact).start()


evalModelAndReact()
collector.startMQTTLoop()
