import csv, glob, pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import numpy as np

train_path = "./aclImdb/train/" # Change your path accordingly.
test_path = "./imdb_te.csv" # test data for grade evaluation. Change your path accordingly.


'''
Implement this module to extract
and combine text files under train_path directory into 
imdb_tr.csv. Each text file in train_path should be stored 
as a row in imdb_tr.csv. And imdb_tr.csv should have three 
columns, "row_number", "text" and label
'''
def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
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


def unigram(df_train, df_test):

    Y = df_train.polarity

    # train a SGD classifier using unigram representation, 
    # predict sentiments on imdb_te.csv, 
    # and write output to unigram.output.txt
    count_vect = CountVectorizer(decode_error='ignore')
    X_train_counts = count_vect.fit_transform(df_train.text)
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(X_train_counts, Y)
    prediction = clf.predict(count_vect.transform(df_test.text))
    np.savetxt('unigram.output.txt', prediction, fmt='%.0f')
        

    # train a SGD classifier using unigram representation with tf-idf, 
    # predict sentiments on imdb_te.csv, and write 
    # output to unigramtfidf.output.txt
    vectorizer = TfidfVectorizer(decode_error='ignore')
    X_train_tfidf = vectorizer.fit_transform(df_train.text)
    clf.fit(X_train_tfidf, Y)
    prediction = clf.predict(vectorizer.transform(df_test.text))
    np.savetxt('unigramtfidf.output.txt', prediction, fmt='%.0f')



def bigram(df_train, df_test):  

    Y = df_train.polarity

    # train a SGD classifier using bigram representation,
    # predict sentiments on imdb_te.csv, and write output to
    # bigram.output.txt
    count_vect = CountVectorizer(decode_error='ignore',ngram_range=(2, 2))
    X_train_counts = count_vect.fit_transform(df_train.text)
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(X_train_counts, Y)
    prediction = clf.predict(count_vect.transform(df_test.text))
    np.savetxt('bigram.output.txt', prediction, fmt='%.0f')


    # train a SGD classifier using bigram representation with tf-idf, 
    # predict sentiments on imdb_te.csv, and write 
    # output to bigramtfidf.output.txt
    vectorizer = TfidfVectorizer(decode_error='ignore')
    X_train_tfidf = vectorizer.fit_transform(df_train.text)
    clf.fit(X_train_tfidf, Y)
    prediction = clf.predict(vectorizer.transform(df_test.text))
    np.savetxt('bigramtfidf.output.txt', prediction, fmt='%.0f')

  
if __name__ == "__main__":

    # imdb_data_preprocess(train_path)
    df_train, df_test = pd.read_csv('./imdb_tr.csv', delimiter=','), pd.read_csv(test_path, delimiter=',')
    # print df.iloc[0]
    # print df.text 

    unigram(df_train, df_test)

    bigram(df_train, df_test)

