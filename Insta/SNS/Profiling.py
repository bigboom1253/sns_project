import os, sys
from SNS import WordPre, FileSearch
import pandas as pd
from sklearn.svm import SVC
import numpy as np
from Model import SVM
import pickle

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
    WordPre.embedding_datas(datas, TARGET_ID)
    print('Target : {} 전처리 완료'.format(TARGET_ID))
    SVM_Predict(TARGET_ID)

# SVM 결과 도출
def SVM_Predict(TARGET_ID):
    # 데이터 로드
    print('Target : {} 데이터 로드'.format(TARGET_ID))
    with open(r'.\Insta\Target_Data\{}\Result.bin'.format(TARGET_ID), 'rb') as f:
        datas = pickle.load(f)

    cate = {'스포츠': 0, '카페': 1, '여행': 2, '패션': 3, '맛집': 4, '반려동물': 5, '게임': 6, '미디어감상': 7}
    print('유저 Profiling 결과 : ', end='\t')
    print(cate.keys()[SVM.predict(datas)])

# if __name__ == '__main__':
#     main()
