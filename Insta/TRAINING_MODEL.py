from SNS import WordPre
import pandas as pd
import pickle
import numpy as np

# 모델 학습용

temp = pd.read_csv(r'Insta\Target_Data\testing\test_file.txt')
datas = list(temp['text'])

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

# Vector화
WordPre.embedding_datas(datas, 'testing','Insta')

# # 모델 학습
# x_datas = np.asarray(pd.read_csv(r'.\Insta\Target_Data\testing\Result.txt', index_col=0))

# with open (r'Insta\Target_Data\testing\saman.bin', 'rb') as f:
#     y_datas = pickle.load(f)

# print(x_datas.shape, len(y_datas))

# from Model import SVM
# SVM.train(x_datas, y_datas)
