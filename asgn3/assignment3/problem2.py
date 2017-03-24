import csv, sys, numpy as np
from decimal import Decimal

def gd(data, labels, alpha):
	betas = np.zeros(len(data[0]))
	for i in xrange(100):
		# risk = np.sum(np.square( np.dot(data, betas) - labels )) / (2 * len(labels))
		betas -= alpha * np.sum( np.transpose(( np.dot(data, betas) - labels ) * np.transpose(data)), 0 )/ len(labels)
	print '%f,%d,%.6e,%.6e,%.6e' % (alpha, 100, Decimal(betas[0]), Decimal(betas[1]), Decimal(betas[2]))

	# # output the risk value
	# print '%f, %20e' % ( alpha, np.sum(np.square( np.dot(data, betas) - labels )) / (2 * len(labels)) )


def mygd(data, labels, alpha):
	betas = np.zeros(len(data[0]))
	for i in xrange(90):
		betas -= alpha * np.sum( np.transpose(( np.dot(data, betas) - labels ) * np.transpose(data)), 0 )/ len(labels)
	print '%f,%d,%.6e,%.6e,%.6e' % (alpha, 90, Decimal(betas[0]), Decimal(betas[1]), Decimal(betas[2]))

	# # output the risk value
	# print '%f, %20e' % ( alpha, np.sum(np.square( np.dot(data, betas) - labels )) / (2 * len(labels)) )


def lr(data, labels):
	data, labels, alphas = np.array(data), np.array(labels), [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
	data = (data-np.mean(data, axis=0)) / np.std(data, axis=0)
	data = np.c_[np.ones(len(labels)), data]
	for alpha in alphas:
		gd(data, labels, alpha)

	mygd(data, labels, 1.1)


if __name__ == '__main__':
	age, weight, height = [], [], []
	data, labels = [], []
	with open(sys.argv[1], 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data.append([float(i) for i in row[:-1]])
			labels.append(float(row[-1]))

	lr(data, labels)


