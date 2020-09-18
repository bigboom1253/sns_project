from keras.datasets import reuters
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
from keras.preprocessing import sequence
from keras.utils import np_utils
import numpy
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from keras.layers import Bidirectional
import pandas as pd
import pickle
# (X_train, Y_train), (X_test, Y_test) = reuters.load_data(num_words=1000,test_split=0.2)
# X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, shuffle = True)
# x_train = sequence.pad_sequences(X_train, maxlen=100)
# x_test = sequence.pad_sequences(X_test, maxlen=100)
# y_train = np_utils.to_categorical(Y_train)
# y_test = np_utils.to_categorical(Y_test)

# X = np.random.random(size=(2000, 100))
# y = np.random.randint(8, size = (2000,1))

# X = sequence.pad_sequences(X, maxlen=200) # 독립변수 X 크기(열) 동일하게 맞춰주기
X = []
for i in np.asarray(pd.read_csv(r'Insta\Target_Data\testing\Result.txt', index_col=0)):
    X.append(list(i))
with open (r'Insta\Target_Data\testing\oneman_y.bin', 'rb') as f:
    y = pickle.load(f)

model = Sequential()

# model.add(Embedding(1000,200)) # Embedding('불러온 단어의 총 개수', '기사 당 단어수')

model.add(Bidirectional(LSTM(128, return_sequences = True), input_shape = (128,1))) #성능개선을 위해 양방향 LSTM 추가
model.add(LSTM(128, activation='tanh')) # 100은 X 열과 맞춰줘야함 padding 필요 // LSTM(기사당 단어 수, 활성함수)
model.add(Dense(64,activation='tanh')) #Dense layer 입력과 출력을 연결해주는 선. 128은 그 선의 수 이며, 가중치의 수이기도하다.
model.add(Dense(1, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X, y, batch_size=100, epochs=2, validation_data=(X, y))

print("\n 정확도 : %.4f" % (model.evaluate(X, y)[1]))


# ***시각화 참고****
# y_test_loss = history.history['val_loss']
# y_train_loss = history.history['loss']
# x_len = numpy.arange(len(y_test_loss))
# plt.plot (x_len, y_test_loss, marker=',', c='red', label='Testset_loss')
# plt.plot(x_len, y_train_loss, marker=',', c='blue', label='Trainset_loss')
# plt.legend(loc='upper right')
# plt.grid()
# plt.xlabel('epoch')
# plt.ylabel('loss')
# plt.show()