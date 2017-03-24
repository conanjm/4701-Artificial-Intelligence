import numpy as np, scipy, sklearn, csv, sys
from sklearn.model_selection import train_test_split




if __name__ == '__main__':
	data, labels = [], []
	with open(sys.argv[1], 'rU') as csvfile:
		csvfile.readline()
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data.append([float(i) for i in row[:-1]])
			labels.append(float(row[-1]))

		data, labels = np.array(data), np.array(labels)	
		
		data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.4, stratify=labels)