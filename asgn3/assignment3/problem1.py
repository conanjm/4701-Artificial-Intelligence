import csv, sys, numpy as np, matplotlib.pyplot as plt

if __name__=="__main__":
	data, labels = [], []
	with open(sys.argv[1], 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			tmp = [float(i) for i in row[:-1]]
			tmp.append(1)
			data.append(tmp)
			labels.append(float(row[-1]))

	data, labels, w = np.array(data), np.array(labels), np.zeros(len(data[0]))
	error = True
	with open(sys.argv[2], 'wb') as f:
		writer = csv.writer(f, delimiter=',')
		while error:
			error = False
			for x, y in zip(data, labels):
				if np.dot(x, w) * y <= 0:
					error = True
					w += y * x
			writer.writerow(w)
