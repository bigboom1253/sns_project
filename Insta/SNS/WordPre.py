# TEXT 전처리 패키지
# Cleasing - 등장 빈도가 적은 단어

## Mecab
# pip install -v python-mecab-ko
## KOMORAN
# pip install konlpy

import re
# import mecab
# from konlpy.tag import Komoran
from pykospacing import spacing
from soynlp.utils import DoublespaceLineCorpus
from soynlp.noun import LRNounExtractor_v2
from soynlp.tokenizer import LTokenizer
from soynlp.vectorizer import BaseVectorizer

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
    result = [list(re.finditer(reg, d)) for d in datas]
    return [list(map(lambda i : i.group(), r)) for r in result]

def substr(reg, datas, space=True):
    if type(datas) != list:
        datas = [datas]
    return [re.sub(reg, ' ', d) if space==True else re.sub(reg, '', d) for d in datas]

def sent_spacing(datas):
    if type(datas) != list:
        datas = [datas]
    return [spacing(d) for d in datas]

def noun_extract(datas):
    ne = LRNounExtractor_v2(verbose=True)
    return ne.train_extract(datas)

def soy_tokenizer(datas):
    ns = {noun:score.score for noun, score in noun_extract(datas).items()}
    return LTokenizer(scores = ns)

def vectorizer(datas, TARGET_ID):
    vectorizing = BaseVectorizer(
        tokenizer = soy_tokenizer(datas),
        min_tf = 0,
        max_tf = 10000,
        min_df = 0,
        max_df = 1.0,
        stopwords=None,
        lowercase=True,
        verbose=True
    )
    FILE_PATH = './Insta/TARGET_DATA/{}/Result'.format(str(TARGET_ID))
    vectorizing.fit_to_file(datas, FILE_PATH)


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