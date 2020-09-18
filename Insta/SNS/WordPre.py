# TEXT 전처리 패키지
# Cleasing - 등장 빈도가 적은 단어

## Mecab
# pip install -v python-mecab-ko
## KOMORAN
# pip install konlpy

import re
import numpy as np
import pandas as pd
# import mecab
# from konlpy.tag import Komoran
from pykospacing import spacing
from soynlp.utils import DoublespaceLineCorpus
from soynlp.noun import LRNounExtractor_v2
from soynlp.tokenizer import LTokenizer
from soynlp.vectorizer import BaseVectorizer
from soynlp.word import WordExtractor

# 문장 토큰화, Escape Code 있는 상태에서 - \n 기준으로 나눔
def sent_tokenize(datas):
    return [d.split('\n') for d in datas]

# Escape Code 처리
escape_code = ['\n', '\xa0', '\"', '\'', '\t', '\r', '\$', '\\', '\u200d']
def del_escape(sents):
    for e in escape_code:
        sents = sents.replace(e, ' ')
    return sents

# 한글 단어 토큰화 (단어 길이 1일 경우 제거)
def word_tokenize(self, datas):
    if type(datas) != list:
        datas = [datas]
    return reg_search('[가-힣]{2,}', datas)

# 불용어 처리
def get_stop():
    with open ('kor_stopwords.txt', 'r') as f:
        stopwords = f.readlines()
    return list(map(lambda i : i.replace('\n', ''), stopwords))

def del_stopword(token_datas):
    if type(token_datas) != list:
        token_datas = [token_datas]

    return [list(filter(lambda i : True if i not in get_stop() else False, d)) for d in token_datas]

# 정규표현식 Functions (finditer, sub) - return = list
def reg_search(reg, datas):
    if type(datas) != list:
        datas = [datas]
    result = list(filter(lambda i : i if i else None, [list(re.finditer(reg, d)) for d in datas]))
    return [' '.join(list(map(lambda i : i.group(), r))) for r in result]

def substr(reg, datas, space=True):
    if type(datas) != list:
        datas = [datas]
    return [re.sub(reg, ' ', d) if space==True else re.sub(reg, '', d) for d in datas]

def sent_spacing(datas):
    if type(datas) != list:
        datas = [datas]
    print(datas)
    return [spacing(d) for d in datas]

import math
def word_score(score):
    return (score.cohesion_forward * math.exp(score.right_branching_entropy))

def word_extract(datas):
    we = WordExtractor(
    min_frequency=10,
    min_cohesion_forward=0.05,
    min_right_branching_entropy=0.0
    )
    we.train(datas)
    words = we.extract()
    print('단어   (빈도수, cohesion, branching entropy)\n')
    for word, score in sorted(words.items(), key=lambda x:word_score(x[1]), reverse=True)[:10]:
        print('%s     (%d, %.3f, %.3f)' % (
            word, 
            score.leftside_frequency, 
            score.cohesion_forward,
            score.right_branching_entropy
            )
         )
    return 

def noun_extract(datas):
    ne = LRNounExtractor_v2(verbose=True)
    nouns = ne.train_extract(datas)
    print(list(ne._compounds_components.items())[:5])
    return nouns

import pickle
def soy_tokenizer(ext_type = 'noun'):
    # 파일 불러오기
    with open(r'.\Model\Extractor\nouns.bin', 'rb') as f:
        nouns = pickle.load(f)
    with open(r'.\Model\Extractor\words.bin', 'rb') as f:
        words = pickle.load(f)

    noun_scores = {noun:score.score for noun, score in nouns.items()}
    cohesion_score = {word:score.cohesion_forward for word, score in words.items()}
    combined_scores = {noun:score + cohesion_score.get(noun, 0)
        for noun, score in noun_scores.items()}
    combined_scores.update(
        {subword:cohesion for subword, cohesion in cohesion_score.items()
        if not (subword in combined_scores)}
    )
    if ext_type == 'noun':
        return LTokenizer(scores = noun_scores)
    elif ext_type == 'word':
        return LTokenizer(scores = cohesion_score)
    elif ext_type == 'comb':
        return LTokenizer(scores = combined_scores)

def vectorizer(datas):
    with open(r'.\Insta\Model\Tokenizer\tokenizer.bin', 'rb') as f:
        tokenizer = pickle.load(f)
    for d in datas[:10]:
        print(tokenizer.tokenize(d))

    vectorizing = BaseVectorizer(
        tokenizer = tokenizer,
        min_tf = 0,
        max_tf = 10000,
        min_df = 0,
        max_df = 1.0,
        stopwords=None,
        lowercase=True,
        verbose=True
    )
    vectorizing.fit(datas)
    with open(r'.\Insta\Model\Vectorizer\vectorizer.bin', 'wb') as f:
        pickle.dump(vectorizing, f)

def embedding_datas(datas, TARGET_ID, change_path='.', max_length = 128):
    with open(r'{}\Model\Vectorizer\vectorizer.bin'.format(change_path), 'rb') as f:
        vectorizer = pickle.load(f)
    temp = pd.DataFrame([vectorizer.encode_a_doc_to_list(d) for d in datas]).fillna(0).astype(int)
    now_columns = len(temp.columns)
    if now_columns < max_length:
        for i in range(now_columns, max_length):
            temp[i] = 0
    co = temp.columns[:max_length]
    temp = temp[co]
    temp.to_csv(r'{}\Target_Data\{}\Result.txt'.format(change_path, TARGET_ID))
    

# POS Tagging
# Mecab 1순위, KOMORAN 2순위 사용 고려
# 안쓰는 품사는 제거하거나 쓸 품사만 가져오기
# def pos_tag(self, datas, pack = 'mecab'):
#     if pack == 'mecab':
#         # Mecab
#         mecab = mecab.MeCab()
#         return [mecab.pos(d) for d in datas]

#     elif pack=='komoran':
#         # KOMORAN
#         komoran = Komoran()
#         return [komoran.pos(d) for d in datas]

#     else:
#         return