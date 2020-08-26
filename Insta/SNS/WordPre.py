# TEXT 전처리 패키지
# Cleasing - 등장 빈도가 적은 단어

# Stemming - ?
# Lemmatization - ?

## Mecab
# pip install -v python-mecab-ko
## KOMORAN
# pip install konlpy

import re
import mecab
from konlpy.tag import Komoran


class Pre():

    # 문장 토큰화, Escape Code 있는 상태에서 - \n 기준으로 나눔
    def sent_tokenize(self, datas):
        return [d.split('\n') for d in datas]

    # Escape Code 처리
    escape_code = ['\n', '\xa0', '\"', '\'', '\t', '\r', '\$', '\\', '\u200d']
    def del_escape(self, datas):
        for e in self.escape_code:
            datas = datas.replace(e, ' ')
        return datas

    # 한글 단어 토큰화 (단어 길이 1일 경우 제거)
    def word_tokenize(self, datas):
        if type(datas) != list:
            datas = [datas]
        return list(filter(lambda i : i if len(i) > 1 else False, self.search('(?<!가-힣)[가-힣]+(?!가-힣)', datas)))

    # 불용어 처리
    def get_stop(self):
        with open ('kor_stopwords.txt', 'r') as f:
            stopwords = f.readlines()
        return list(map(lambda i : i.replace('\n', ''), stopwords))

    def del_stopword(self, token_datas):
        stopwords = self.get_stop()
        if type(token_datas) != list:
            token_datas = [token_datas]
        
        return [list(filter(lambda i : True if i not in stopwords else False, d)) for d in token_datas]

    # 정규표현식 Functions (finditer, sub) - return = list
    def search(self, reg, datas):
        if type(datas) != list:
            datas = [datas]
        result = [list(re.finditer(reg, d)) for d in datas]
        features = []
        for r in result:
            features.extend(list(map(lambda i : i.group(), r)))
        return features
    
    def substr(self, reg, datas):
        if type(datas) != list:
            datas = [datas]
        return [re.sub(reg, ' ', d) for d in datas]

    # POS Tagging
    # Mecab 1순위, KOMORAN 2순위 사용 고려
    # 안쓰는 품사는 제거하거나 쓸 품사만 가져오기
    def pos_tag(self, datas, pack = 'mecab'):
        if pack == 'mecab':
            # Mecab
            mecab = mecab.MeCab()
            return [mecab.pos(d) for d in datas]

        elif pack=='komoran':
            # KOMORAN
            komoran = Komoran()
            return [komoran.pos(d) for d in datas]

        else:
            return

    # Tokenizing

# Ngram화
