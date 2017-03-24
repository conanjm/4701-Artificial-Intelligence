import csv, sys, numpy as np

def pla(data, labels):
	data, labels, w = np.array(data), np.array(labels), np.zeros(len(data[0]))

	error = True
	while error:
		error = False
		for x, y in zip(data, labels):
			if np.sign(np.dot(x, w)) * y <= 0:
				error = True
				w += y * x

		print w


if __name__=="__main__":
	data, labels = [], []
	with open(sys.argv[1], 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			tmp = [float(i) for i in row[:-1]]
			tmp.append(1)
			data.append(tmp)
			labels.append(float(row[-1]))

	pla(data, labels)


