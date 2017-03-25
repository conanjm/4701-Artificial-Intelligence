import numpy as np, scipy, sklearn, csv, sys
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.svm import SVC
from sklearn import datasets


# iris = datasets.load_iris()
# print iris.target
# parameters = {'kernel':['linear'], 'C':[0.1, 0.5, 1, 5, 10, 50, 10]}
# svr = SVC()
# clf = GridSearchCV(svr, parameters, cv=5)
# clf.fit(iris.data, iris.target)
# print clf.cv_results_

	
if __name__ == '__main__':
	data, labels = [], []
	with open(sys.argv[1], 'rU') as csvfile:
		csvfile.readline()
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data.append([float(i) for i in row[:-1]])
			labels.append(float(row[-1]))

		data, labels = np.array(data), np.array(labels)	
		data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.1, stratify=labels)

		parameters = {'kernel': ['linear'], 'C': [0.01, 100]}#0.5, 1, 5, 10, 50,100 10000] }

		clf = GridSearchCV(SVC(), parameters)
		clf.fit(data_train, labels_train)
		print clf.cv_results_['std_train_score']
		# print '%.6f' % clf.fit(data_train, labels_train).score(data_test, labels_test)

		# skf = StratifiedKFold(n_splits=5)
		# for foldTrainIdx, foldTestIdx in skf.split(data_train, labels_train):
		# 	svr = svm.SVC()
		# 	clf = GridSearchCV(svr, parameters)
		# 	print clf.fit(data_train[foldTrainIdx], labels_train[foldTrainIdx]).score(data_train[foldTestIdx], labels_train[foldTestIdx])
		# 	print clf.get_params


		

		# clf = SVC(kernel='linear', C=[0.1, 0.5, 1, 5, 10, 50, 100])
		# scores = cross_val_score(clf, data_train, labels_train, cv=5).score()
		# print clf.fit(data_train, labels_train).score(data_train, labels_train)

