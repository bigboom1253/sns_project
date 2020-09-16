from SNS import WordPre
import pandas as pd
import pickle

# 모델 학습용 나중에 삭제

# temp = pd.read_csv(r'C:\Users\svsta\Desktop\result.txt')
# datas = list(temp['text'])

# # Word Extractor 학습
# words = WordPre.word_extract(datas)
# import pickle
# with open(r'.\Insta\Model\Extractor\words.bin', 'wb') as f:
#     pickle.dump(words, f)

# # Noun Extractor 학습
# nouns = WordPre.noun_extract(datas)
# import pickle
# with open(r'C:\Users\svsta\Desktop\nouns.bin', 'wb') as f:
#     pickle.dump(nouns, f)

# # Tokenizer 학습
# tokenizer = WordPre.soy_tokenizer('noun')
# import pickle
# with open(r'.\Insta\Model\Tokenizer\tokenizer.bin', 'wb') as f:
#     pickle.dump(tokenizer, f)

# Vectorizer 저장
# WordPre.vectorizer(datas)

# Vector화
# WordPre.embedding_datas(datas, 'testing')

with open(r'.\Insta\Target_Data\testing\Result.bin', 'rb') as f:
    x_datas = pickle.load(f)
with open (r'Insta\Target_Data\testing\y_datas.bin', 'rb') as f:
    y_datas = pickle.load(f)
from Model import SVM
SVM.train(x_datas, y_datas)

