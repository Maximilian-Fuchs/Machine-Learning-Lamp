from DataCollector import *
import threading


# START CONFIGURATION

sampleTimeInSeconds = 10


## END CONFIGURATION


collector = DataCollector()


def writeFrame():
    raw_data_string = collector.getLatestRawValuesString()
    decisiontree_data_string = collector.getLatestDecisionTreeValuesString()
    f = open('raw', 'a')
    f.write(raw_data_string + '\n')  # python will convert \n to os.linesep
    f.close()
    f = open('decision_tree_data', 'a')
    f.write(decisiontree_data_string + '\n')  # python will convert \n to os.linesep
    f.close()
    #f = open('data/decision_tree_formatted', 'a')
    #f.write('hi theredsfsf\n')  # python will convert \n to os.linesep
    #f.close()

    print(raw_data_string + '\n' + decisiontree_data_string + '\n\n')
    threading.Timer(sampleTimeInSeconds, writeFrame).start()




# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

writeFrame()
collector.startMQTTLoop()
