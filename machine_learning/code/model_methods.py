import glob
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
from sklearn.svm import SVC
import re
import os
import numpy as np
import pickle


class model_methods():

    def __init__(self, data):
        self.all_files = data

    def process_data(self):

        all_title_and_body = []
        for title, body in zip(self.all_files['title'], self.all_files['body']):
            all_title_and_body.append(str(title) + " " + str(body))

        # create the transform
        vectorizer = CountVectorizer(stop_words='english', min_df=10, max_df=160)

        # tokenize and build vocab
        vectorizer.fit(all_title_and_body)

        # summarize
        print(vectorizer.vocabulary_)

        # encode document
        vector = vectorizer.transform(all_title_and_body)

        # summarize encoded vector
        X = vector.toarray()

        y = self.all_files['label']

        X_train, X_test, y_train, y_test = train_test_split( X, y, random_state=42)

        return X_train, X_test, y_train, y_test
        

