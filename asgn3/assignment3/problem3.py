import numpy as np, scipy, sklearn, csv, sys
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn import svm, linear_model, tree, datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import time

def svm_linear(data_train, data_test, labels_train, labels_test):
	parameters = {'kernel':['linear'], 'C':[ 0.1, 0.5, 1, 5, 10, 50, 100]}
	svr = svm.SVC()
	clf = GridSearchCV(svr, parameters, cv=5)
	clf.fit(data_train, labels_train)
	print 'svm_linear,{},{}'.format (clf.best_score_, clf.score(data_test, labels_test))

def svm_poly(data_train, data_test, labels_train, labels_test):
	parameters = {'kernel':['poly'], 'C':[ 0.1, 1, 3], 'degree': [4,5,6], 'gamma':[0.1, 1]}
	svr = svm.SVC()
	clf = GridSearchCV(svr, parameters, cv=5)
	clf.fit(data_train, labels_train)
	print 'svm_poly,{},{}'.format (clf.best_score_, clf.score(data_test, labels_test))

def svm_rbf(data_train, data_test, labels_train, labels_test):
	parameters = {'kernel':['rbf'], 'C':[ 0.1, 0.5, 1, 5, 10, 50, 100],'gamma':[0.1, 0.5, 1, 3, 6, 10]}
	svr = svm.SVC()
	clf = GridSearchCV(svr, parameters, cv=5)
	clf.fit(data_train, labels_train)
	print 'svm_rbf,{},{}'.format (clf.best_score_, clf.score(data_test, labels_test))

def logisticRegression(data_train, data_test, labels_train, labels_test):
	parameters = {'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
	logreg = linear_model.LogisticRegression()
	clf = GridSearchCV(logreg, parameters, cv=5)
	clf.fit(data_train, labels_train)
	print 'logistic,{},{}'.format(clf.best_score_, clf.score(data_test, labels_test))

def KNN(data_train, data_test, labels_train, labels_test):
	parameters = {'n_neighbors':range(1, 51), 'leaf_size': range(5, 61, 5)}
	knn = KNeighborsClassifier()
	clf = GridSearchCV(knn, parameters, cv=5)
	clf.fit(data_train, labels_train)
	print 'knn,{},{}'.format(clf.best_score_, clf.score(data_test, labels_test))

def DT(data_train, data_test, labels_train, labels_test):
	parameters = {'max_depth': range(1, 51), 'min_samples_split': range(2,11)}
	dt = tree.DecisionTreeClassifier()
	clf = GridSearchCV(dt, parameters, cv=5)
	clf.fit(data_train, labels_train)
	print 'decision_tree,{},{}'.format(clf.best_score_, clf.score(data_test, labels_test))

def RF(data_train, data_test, labels_train, labels_test):
	parameters = {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}
	rf = RandomForestClassifier()
	clf = GridSearchCV(dt, parameters, cv=5)
	clf.fit(data_train, labels_train)
	print 'random_forest,{},{}'.format(clf.best_score_, clf.score(data_test, labels_test))

if __name__ == '__main__':
	start = time.time()
	data, labels = [], []
	with open(sys.argv[1], 'rU') as csvfile:
		csvfile.readline()
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data.append([float(i) for i in row[:-1]])
			labels.append(int(row[-1]))

		data, labels = np.array(data), np.array(labels)	
		data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.4, stratify=labels)

		# svm_linear(data_train, data_test, labels_train, labels_test)
		# svm_poly(data_train, data_test, labels_train, labels_test)
		# svm_rbf(data_train, data_test, labels_train, labels_test)
		# logisticRegression(data_train, data_test, labels_train, labels_test)
		# KNN(data_train, data_test, labels_train, labels_test)
		DT(data_train, data_test, labels_train, labels_test)
		RF(data_train, data_test, labels_train, labels_test)

		print 'execute time: {}'.format(time.time() - start)


