from sklearn.svm import SVC

import matplotlib.pyplot as plt
import numpy as np
import pickle

# 로지스틱 회귀에서의 C와 반대의 개념. 모델을 조율해주는 값이라고 보면 됨.
def train(X, y, line_type = 'rbf', const=1.0):
    svm = SVC(kernel=line_type, C=const, random_state=0)
    svm.fit(X, y)
    with open(r'.\Insta\Model\SVM\model.bin', 'wb') as f:
        pickle.dump(svm, f)
    print('Accuracy: %.2f' % svm.score(X, y))

def predict(X):
    # 모델 로드
    print('SVM 모델 로드')
    with open(r'.\Insta\Model\SVM\model.bin', 'wb') as f:
        svm = pickle.load(f)
    y_lists = np.mean(svm.predict_proba(X))
    return y_lists.index(max(y_lists))
