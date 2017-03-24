import numpy as np, scipy, sklearn, csv, sys





if __name__ == '__main__':
	data, labels = [], []
	with open(sys.argv[1], 'rU') as csvfile:
		csvfile.readline()
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data.append([float(i) for i in row[:-1]])
			labels.append(row[-1])
		