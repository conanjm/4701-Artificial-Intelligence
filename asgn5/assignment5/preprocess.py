import csv, glob

if __name__ == '__main__':

	stopwords = set()
	with open('stopwords.en.txt', 'rb') as ifile:
		for line in ifile:
			stopwords.add(line.split()[0])

	fieldnames = ['row_number', 'text', 'polarity']

	posfiles = glob.glob("aclImdb/train/pos/*.txt")
	negfiles = glob.glob("aclImdb/train/neg/*.txt")
	
	i=0

	with open('imdb_tr.csv', 'wb') as ofile:
		writer = csv.DictWriter(ofile, fieldnames=fieldnames, delimiter=',')
		writer.writeheader()
		for f in posfiles:
			with open(f, 'rb') as ifile:
				# get a list of words in the raw review data
				words = ifile.readline().replace('<br />', '').split()
				text = [word for word in words if word not in stopwords]
				text = ' '.join(text)
				writer.writerow({'row_number': i, 'text': text, 'polarity': 1})
				i += 1

		for f in negfiles:
			with open(f, 'rb') as ifile:
				words = ifile.readline().replace('<br />', '').split()
				text = [word for word in words if word not in stopwords]
				text = ' '.join(text)
				writer.writerow({'row_number': i, 'text': text, 'polarity': 0})
				i += 1



	# print files
