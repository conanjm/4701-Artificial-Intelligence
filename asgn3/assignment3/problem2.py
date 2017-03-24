import csv, sys, numpy as np

def gd(data, labels, alpha, betas):
	for i in xrange(100):
		risk = np.sum(np.square( np.dot(data, betas) - labels )) / (2 * len(labels))
		betas -= alpha * np.sum( np.transpose(( np.dot(data, betas) - labels ) * np.transpose(data)), 0 )/ len(labels)


def lr(data, labels):
	data, labels, betas = np.array(data), np.array(labels), np.zeros(len(data[0])+1)
	data = (data-np.mean(data, axis=0)) / np.std(data, axis=0)
	data = np.c_[np.ones(len(labels)), data]
	for i in xrange(100):
		betas -= 0.5 * np.sum( np.transpose(( np.dot(data, betas) - labels ) * np.transpose(data)), 0 )/ len(labels)
	print betas



if __name__ == '__main__':
	age, weight, height = [], [], []
	data, labels = [], []
	with open(sys.argv[1], 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data.append([float(i) for i in row[:-1]])
			labels.append(float(row[-1]))

	lr(data, labels)


