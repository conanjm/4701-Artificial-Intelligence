import csv, glob, pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

train_path = "./aclImdb/train/" # Change your path accordingly.
test_path = "../imdb_te.csv" # test data for grade evaluation. Change your path accordingly.



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


def unigram(train_data_path):

    # construct a dataframe training data
    df = pd.read_csv(train_data_path, delimiter=',')
    # print df.iloc[0]
    # print df.text

    # only unigram count
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(df.text)
    print X_train_counts.shape

    # unigram with tf-idf
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print X_train_tfidf.shape




def bigram(train_data_path):

    # construct a dataframe training data
    df = pd.read_csv(train_data_path, delimiter=',')    


    # only bigram count
    count_vect = CountVectorizer(ngram_range=(2, 2))
    X_train_counts = count_vect.fit_transform(df.text)
    print X_train_counts.shape


    # bigram with tf-idf
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print X_train_tfidf.shape





  
if __name__ == "__main__":

    # imdb_data_preprocess(train_path)

    unigram('./imdb_tr.csv')

    # bigram('./imdb_tr.csv')




'''train a SGD classifier using unigram representation,
predict sentiments on imdb_te.csv, and write output to
unigram.output.txt'''

'''train a SGD classifier using bigram representation,
predict sentiments on imdb_te.csv, and write output to
unigram.output.txt'''

'''train a SGD classifier using unigram representation
with tf-idf, predict sentiments on imdb_te.csv, and write 
output to unigram.output.txt'''

'''train a SGD classifier using bigram representation
with tf-idf, predict sentiments on imdb_te.csv, and write 
output to unigram.output.txt'''
pass