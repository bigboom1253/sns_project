from sklearn.svm import SVC

import matplotlib.pyplot as plt
import numpy as np
import pickle

def train(X, y, line_type = 'rbf', const=1.0, verbose=True):
    svm = SVC(kernel=line_type, C=const, random_state=0, max_iter=10, cache_size=4000, shrinking=0, verbose=verbose)
    svm.fit(X, y)
    with open(r'.\Insta\Model\SVM\model.bin', 'wb') as f:
        pickle.dump(svm, f)
    print('Accuracy: %.2f' % svm.score(X, y))

def predict(X, change_path='.'):
    # 모델 로드
    print('SVM 모델 로드')
    with open(r'{}\Model\SVM\model.bin'.format(change_path), 'rb') as f:
        svm = pickle.load(f)
    return svm.predict(X)
