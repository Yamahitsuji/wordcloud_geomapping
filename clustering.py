from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
from gensim.models.doc2vec import Doc2Vec
import numpy as np
import csv
from sklearn import svm
from sklearn.model_selection import train_test_split


def get_noun_list(text):
    token_filters = [
        POSKeepFilter(['名詞'])
    ]
    analyzer = Analyzer(token_filters=token_filters)
    return [v.surface for v in analyzer.analyze(text)]


INDOOR_LABEL = 0
OUTDOOR_LABEL = 1


def main():
    noun_lists = []
    labels = []
    with open('data/new_indoor.csv') as f:
        for line in csv.reader(f):
            noun_lists.append(get_noun_list(line[1]))
            labels.append(INDOOR_LABEL)
    with open('data/new_outdoor.csv') as f:
        for line in csv.reader(f):
            noun_lists.append(get_noun_list(line[1]))
            labels.append(OUTDOOR_LABEL)

    model = Doc2Vec.load("model/jawiki.doc2vec.dbow300d.model")
    data = []
    for nouns in noun_lists:
        data.append(model.infer_vector(nouns))
    train_data, test_data, train_label, test_label = train_test_split(data, labels, test_size=0.3)
    clf = svm.SVC(kernel='rbf')
    clf.fit(train_data, train_label)
    result = clf.predict(test_data)
    accuracy = np.sum(np.array(test_label) == result) / len(test_label)
    print("accuracy :", accuracy)


if __name__ == '__main__':
    main()
