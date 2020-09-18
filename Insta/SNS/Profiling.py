import os, sys
from SNS import WordPre, FileSearch
import pandas as pd
import numpy as np
from Model import SVM
import pickle

# 최초 호출
def Predict(TARGET_ID):
    try:
        fl = FileSearch.JsonSearch().search(r'Insta\Target_Data\{}'.format(TARGET_ID))
    except:
        fl = None

    if fl:
        # 전처리 실행
        Text_Pre(TARGET_ID, 'Insta')
    else:
        # 크롤링 실행
        crawling = "cd Insta && scrapy crawl target_post -a TARGET_ID={}".format(TARGET_ID)
        print('Target : {} 크롤링 시작'.format(TARGET_ID))
        os.system(crawling)

# 벡터라이징
def Text_Pre(TARGET_ID, change_path = '.'):
    print('Target : {} 전처리 시작'.format(TARGET_ID))
    PATH = r'{}\Target_Data\{}'.format(change_path, TARGET_ID)
    datas = []
    for f in FileSearch.JsonSearch().search(PATH):
        datas.extend(list(pd.read_json(f)['content']))
    datas = WordPre.sent_spacing(WordPre.reg_search('(?<=#)[가-힣ㄱ-ㅎㅏ-ㅣ]+', datas))
    WordPre.embedding_datas(datas, TARGET_ID, change_path=change_path)
    print('Target : {} 전처리 완료'.format(TARGET_ID))
    SVM_Predict(TARGET_ID, change_path)

from collections import Counter
# SVM 결과 도출
def SVM_Predict(TARGET_ID, change_path='.'):
    # 데이터 로드
    print('Target : {} 데이터 로드'.format(TARGET_ID))
    datas = np.asarray(pd.read_csv(r'{}\Target_Data\{}\Result.txt'.format(change_path, TARGET_ID), index_col=0))

    cate = {'스포츠': 0, '카페': 1, '여행': 2, '패션': 3, '맛집': 4, '반려동물': 5, '게임': 6, '미디어감상': 7}
    score = SVM.predict(datas, change_path)
    labels = Counter(score).most_common()
    cate = list(cate.keys())
    for l in labels:
        label = cate[l[0]]
        print('{} : {}'.format(label, l[1]), end = ' ')

    label = cate[labels[0][0]]
    print('\n유저 Profiling 결과 : {}'.format(label))
    with open(r'{}\Target_Data\{}\label.txt'.format(change_path, TARGET_ID), 'w', encoding='utf-8') as f:
        f.write(label)
