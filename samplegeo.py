from __future__ import print_function
import numpy as np
from scipy.sparse import csc_matrix
from sklearn import metrics
import sys, os
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import json
import operator
from pprint import pprint
import gensim
import re
import codecs
#import io

def get_top_labels_and_feats(top, topinc,filename=""):
    featids = {'content': [], 'name': [], 'tz': [], 'ulang': [], 'uloc': []}
    topcountries = {}
    if os.path.exists('feats/topcountries' + str(top)) and os.path.exists('feats/content' + str(topinc)) and os.path.exists('feats/name' + str(topinc)) and os.path.exists('feats/tz' + str(topinc)) and os.path.exists('feats/ulang' + str(topinc)) and os.path.exists('feats/uloc' + str(topinc)):
        with open('feats/topcountries' + str(top), 'r') as fh:
            for line in fh:
                data = line.strip().split('\t')
                topcountries[data[0]] = int(data[1])
        with open('feats/content' + str(topinc), 'r') as fh:
            featids['content'] = fh.read().splitlines()
        with open('feats/name' + str(topinc), 'r') as fh:
            featids['name'] = fh.read().splitlines()
        with open('feats/tz' + str(topinc), 'r') as fh:
            featids['tz'] = fh.read().splitlines()
        with open('feats/ulang' + str(topinc), 'r') as fh:
            featids['ulang'] = fh.read().splitlines()
        with open('feats/uloc' + str(topinc), 'r') as fh:
            featids['uloc'] = fh.read().splitlines()
    return topcountries, featids

def build_matrix(tweet, featureids, featurelengths, toplabels, istest = 0):
    colcount = featurelengths['content'] + featurelengths['name'] + featurelengths['tz'] + featurelengths['ulang'] + featurelengths['uloc']

    linecount = 0
    rows = []
    cols = []
    gt = []
    values = []

    

    for a in range(1):
            
            if istest == 1 or tweet['location']['address']['country_code'] in toplabels:
                for ctoken in list(set(re.sub(r'([^\s\w]|_)+', '', tweet['text'].lower()).split(' '))):
                     if ctoken in featureids['content']:
                         rows.append(linecount)
                         cols.append(featureids['content'][ctoken])
                         values.append(1)

                for nametoken in list(set(re.sub(r'([^\s\w]|_)+', '', tweet['user']['name'].lower()).split(' '))):
                    if nametoken in featureids['name']:
                        rows.append(linecount)
                        cols.append(featureids['name'][nametoken] + featurelengths['content'])
                        values.append(1)

                if str(tweet['user']['time_zone']) in featureids['tz']:
                    rows.append(linecount)
                    cols.append(featureids['tz'][str(tweet['user']['time_zone'])] + featurelengths['content'] + featurelengths['name'])
                    values.append(1)

                if tweet['user']['lang'] in featureids['ulang']:
                    rows.append(linecount)
                    cols.append(featureids['ulang'][tweet['user']['lang']] + featurelengths['content'] + featurelengths['name'] + featurelengths['tz'])
                    values.append(1)

                for loctoken in list(set(re.sub(r'([^\s\w]|_)+', '', tweet['user']['location'].lower()).split(' '))):
                    if loctoken in featureids['uloc']:
                        rows.append(linecount)
                        cols.append(featureids['uloc'][loctoken] + featurelengths['content'] + featurelengths['name'] + featurelengths['tz'] + featurelengths['ulang'])
                        values.append(1)

                if istest == 0:
                    gt.append(toplabels[tweet['coordinates']['location']['address']['country_code']])
                else:
                    gt.append(0)

                linecount += 1
            sys.stdout.flush()

    # TODO: tlang

    row = np.asarray(rows)
    col = np.asarray(cols)
    data = np.asarray(values)

    return (csc_matrix((data, (row, col)), shape=(linecount, colcount)), gt)

testdata = "t7.txt"
print(testdata)
classifier = "maxent"
output = 'how.txt'
top = int(217)

topinc = int(10000)
print(topinc)


def findCountry(tweets):
    toplabels, featids = get_top_labels_and_feats(top, topinc)
    featureids = {'content': {}, 'name': {}, 'tz': {}, 'ulang': {}, 'uloc': {}}
    featurelengths = {'content': 0, 'name': 0, 'tz': 0, 'ulang': 0, 'uloc': 0}
    for ftype in ['content', 'name', 'tz', 'ulang', 'uloc']:
        fid = 0
        for feat in featids[ftype]:
            featureids[ftype][feat] = fid
            fid = len(featureids[ftype])
        featurelengths[ftype] = len(featureids[ftype])

    cmodel = joblib.load('models/maxent-217-10000.pkl')

    test_data, test_gt = build_matrix(tweets, featureids, featurelengths, toplabels, 1)


    predicted = cmodel.predict(test_data)
    rest=[]
    for conn in predicted:
        rest.append(list(toplabels.keys())[list(toplabels.values()).index(conn)])

    return rest

