import glob
import pandas as pd
import time
import tqdm
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
from model_methods import model_methods
start = time.time()

my_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# Label (0 = Bug, 1 = Feature Request, 2 = Not 1 or 0)
labeled_data_path_1 = os.path.join(my_path, 'SSL1.xlsx')

all_files = pd.read_excel(labeled_data_path_1)

all_files.reset_index(inplace = True, drop = True)
all_files.sample(frac=1).reset_index(drop=True)

#for x in range(1,5):
	# .6, .6, .57, .5
data = model_methods(all_files)
X_train, X_test, y_train, y_test = data.process_data()

filename = 'finalized_model.pickle'

retrain = input("Do you want to retrain or use the saved file? (y/n) ")

if (retrain == "y"):
	classifier = OneVsRestClassifier(SVC(class_weight='balanced')).fit(X_train, y_train)

	parameters = {
		"estimator__C": [0.1, 1, 10, 100, 1000],
		"estimator__kernel": ["linear", "rbf"], #"poly",
		"estimator__degree":[0, 1, 2, 3, 4, 5, 6],
		"estimator__gamma":[0.1, 1, 10, 100]
	}

	final_model = tqdm(GridSearchCV(classifier, param_grid=parameters, verbose=4))

	final_model.fit(X_train, y_train)

	pickle.dump(final_model, open(filename, 'wb'))

else:
	final_model = pickle.load(open(filename, 'rb'))

predictions = final_model.predict(X_test)

print(predictions)

accuracy_scores = accuracy_score(y_test, predictions)

print("Accuracy: " + str(accuracy_scores))

end = time.time()

print("Run Time: " + str(end-start))