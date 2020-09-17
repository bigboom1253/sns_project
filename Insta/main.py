from SNS import WordPre
import pandas as pd
import pickle
import numpy as np

# 모델 학습용 나중에 삭제

# temp = pd.read_csv(r'C:\Users\svsta\Desktop\final_data_900.txt')
# datas = list(temp['text'])

# # Word Extractor 학습
# import pickle
# with open(r'.\Insta\Model\Extractor\words.bin', 'wb') as f:
#     pickle.dump(WordPre.word_extract(datas), f)

# # Noun Extractor 학습
# import pickle
# with open(r'.\Insta\Model\Extractor\nouns.bin', 'wb') as f:
#     pickle.dump(WordPre.noun_extract(datas), f)

# # Tokenizer 학습
# import pickle
# with open(r'.\Insta\Model\Tokenizer\tokenizer.bin', 'wb') as f:
#     pickle.dump(WordPre.soy_tokenizer('comb'), f)

# # Vectorizer 저장
# with open(r'.\Insta\Model\Vectorizer\vectorizer.bin', 'wb') as f:
#     pickle.dump(WordPre.vectorizer(datas), f)

# # Vector화
# WordPre.embedding_datas(datas, 'testing')

# # Y_DATA 추출
# with open(r'.\Insta\Target_Data\testing\y_datas.bin', 'wb') as f:
#     pickle.dump(list(temp['target']), f)

from libsvm.svmutil import *

# 모델 학습
x_datas = np.matrix(pd.read_csv(r'.\Insta\Target_Data\testing\Result.txt', index_col=0))

with open (r'Insta\Target_Data\testing\y_datas.bin', 'rb') as f:
    y_datas = pickle.load(f)

print(x_datas.shape, len(y_datas))
m = svm_train(y_datas, x_datas, '-c 4')
with open(r'.\Insta\Model\SVM\model.bin', 'wb') as f:
    pickle.dump(m, f)

# from Model import SVM
# SVM.train(x_datas, y_datas)
