import os, sys
from SNS import WordPre, FileSearch
import pandas as pd
from sklearn.svm import SVC
import numpy as np

# 파이썬 환경 설정 - conda activate base
# 파일 실행 - & ../anaconda3/python.exe ../sns_project/실행 파일

# 최초 호출, 크롤링 시작
def Predict(TARGET_ID):
    crawling = "cd Insta && scrapy crawl target_post -a TARGET_ID={}".format(TARGET_ID)
    print('Target : {} 크롤링 시작'.format(TARGET_ID))
    os.system(crawling)

# 벡터라이징
def Text_Pre(TARGET_ID):
    print('Target : {} 전처리 시작'.format(TARGET_ID))
    PATH = r'.\Insta\Target_Data\{}'.format(TARGET_ID)
    datas = []
    for f in FileSearch.JsonSearch().search(PATH):
        datas.extend(list(pd.read_json(f)['content']))
    datas = WordPre.sent_spacing(WordPre.reg_search('(?<=#)[가-힣ㄱ-ㅎㅏ-ㅣ]+', datas))
    WordPre.vectorizer(datas, TARGET_ID)
    print('Target : {} 크롤링 완료'.format(TARGET_ID))
    SVM_Predict(TARGET_ID)

# SVM 결과 도출
def SVM_Predict(TARGET_ID):
    # 모델 로드
    print('SVM 모델 로드')
    # with open('model-path', 'rb') as f:
    # Model = pickle.load(f)
    # 데이터 로드
    print('Target : {} 데이터 로드'.format(TARGET_ID))
    with open('./Insta/Target_Data/{}'.format(TARGET_ID), 'r') as f:
        datas = list(map(lambda i : list(map(int, i.split())), f.readlines()[2:]))
    datas = np.matrix(pd.DataFrame(datas).fillna(0))
    # 학습한 모델로 예측
    support_vector_machine = SVC(kernel='rbf', C=1.0, random_state=0, gamma=0.1)
    cate = {'스포츠': 0, '카페': 1, '여행': 2, '패션': 3, '맛집': 4, '반려동물': 5, '게임': 6, '미디어감상': 7}
    print('유저 Profiling 결과 : ', end='\t')
    print(cate.keys()[support_vector_machine.predict(datas)])

# if __name__ == '__main__':
#     main()