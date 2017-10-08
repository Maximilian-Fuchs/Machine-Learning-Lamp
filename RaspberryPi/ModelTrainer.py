import nltk
import pickle

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

#load set of data
f = open('decision_tree_data', 'r')
rawdata = f.read()
f.close()

#extract features:
def iot_features(rawdata):
    datapoints = rawdata.split('\n')[:-1]
    datapoints = [datapoint.split('\t') for datapoint in datapoints]
    datapoints = [[(entry.split(' ')[0], entry.split(' ')[1]) for entry in datapoint if len(entry.split(' ')) == 2] for datapoint in datapoints]
    datapoint_dicts = [dict(datapoint) for datapoint in datapoints]
    return datapoint_dicts

#build train and test set
data_dicts = iot_features(rawdata)
feature_sets = [(removekey(data_dict, 'Lamp'), data_dict['Lamp']) for data_dict in data_dicts]
size = int(len(feature_sets) * 0.5)
train_set, test_set = feature_sets[size:], feature_sets[:size]

#train classifier
classifier = nltk.DecisionTreeClassifier.train(train_set)
#print classifier
print(classifier.pseudocode(depth=4))

#store the classifier in /model
f = open('model/decisiontree_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()
