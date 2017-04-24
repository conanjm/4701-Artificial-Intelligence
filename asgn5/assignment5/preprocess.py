import csv, glob, pandas as pd

train_path = 'aclImdb/test/'

def imdb_data_preprocess(inpath, outpath="./", name="mytest.csv", mix=False):
    fieldnames = ['row_number', 'text', 'polarity']
    posfiles, negfiles = glob.glob(train_path + 'pos/*.txt'), glob.glob(train_path + 'neg/*.txt')
    i=0
    with open(outpath+name, 'wb') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for f in posfiles:
            with open(f, 'rb') as ifile:
                # get a list of words in the raw review data
                text = ifile.readline().replace('<br />', '')
                # text = [word for word in words if word not in stopwords]
                # text = ' '.join(text)
                writer.writerow({'row_number': i, 'text': text, 'polarity': 1})
                i += 1

        for f in negfiles:
            with open(f, 'rb') as ifile:
                text = ifile.readline().replace('<br />', '')
                # text = [word for word in words if word not in stopwords]
                # text = ' '.join(text)
                writer.writerow({'row_number': i, 'text': text, 'polarity': 0})
                i += 1


if __name__ == '__main__':
	imdb_data_preprocess(train_path)

