from warnings import filters
from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.layers import LSTM, Activation, Dense, Conv2D, Flatten, MaxPooling2D, Input, Dropout, Conv1D
from keras.datasets import mnist, fashion_mnist, cifar10, cifar100
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical # https://wikidocs.net/22647 케라스 원핫인코딩
from sklearn.preprocessing import OneHotEncoder  # https://psystat.tistory.com/136 싸이킷런 원핫인코딩
from sklearn.metrics import r2_score, accuracy_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler
from keras.layers import BatchNormalization


###########################폴더 생성시 현재 파일명으로 자동생성###########################################
import inspect, os
a = inspect.getfile(inspect.currentframe()) #현재 파일이 위치한 경로 + 현재 파일 명
print(a)
print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) #현재 파일이 위치한 경로
print(a.split("\\")[-1]) #현재 파일 명
current_name = a.split("\\")[-1]
##########################밑에 filepath경로에 추가로  + current_name + '/' 삽입해야 돌아감###################


#1. 데이터
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
print(x_train.shape, y_train.shape) #(60000, 28, 28) (60000,)
print(x_test.shape, y_test.shape) #(10000, 28, 28) (10000,)

###################리세이프#######################
x_train = x_train.reshape(60000, 28, 28)
x_test = x_test.reshape(10000, 28, 28)
print(x_train.shape)
print(np.unique(y_train, return_counts=True))
#################################################

#####################XXXXX스케일러XXXXX######################
# scaler = MinMaxScaler()
# scaler = StandardScaler()
# scaler = MaxAbsScaler()
# scaler = RobustScaler()
# x_train = scaler.fit_transform(x_train)
# x_test = scaler.transform(x_test)
#################################################

####################겟더미#######################
# y = pd.get_dummies(y)  #겟더미는 y_predict 할때 np아니고 tf.argmax로 바꾸기
# print(y)
################################################

####################원핫인코더###################
df1 = pd.DataFrame(y_train)
df2 = pd.DataFrame(y_test)
print(df1)
oh = OneHotEncoder(sparse=False) # sparse=true 는 매트릭스반환 False는 array 반환
y_train = oh.fit_transform(df1)
y_test = oh.transform(df2)
print('====================================')
print(y_train.shape)
print('====================================')
print(y_test.shape)
################################################

# ###################케라스########################
# y_train = to_categorical(y_train)
# y_test = to_categorical(y_test)
# print(np.unique(y_train, return_counts=True))
# print(np.unique(y_test, return_counts=True))   # y의 라벨값 :  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# print(x_train.shape, y_train.shape) 
# print(x_test.shape, y_test.shape)
# ################################################
print(x_train.shape,x_test.shape) # (60000, 28, 28) (10000, 28, 28)
# x_train = x_train.reshape(60000, 28, 28)
# x_test = x_test.rashape(10000, 28, 28)


# 맹그러바바바
# acc 0.98이상
# cifar는 칼라 패션은 흑백


#2. 모델구성

model = Sequential()    
model.add(Conv1D(1280, 2, input_shape=(28,28)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(2, activation='relu'))
model.add(Dense(10, activation='softmax')) 


# # (kernel_size * channels +bias) * filters = summary param # (CNN모델)

# x = x.reshape(10,2) 현재 데이터를 순서대로 표기된 행렬로 바꿈

#3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint
import datetime
date = datetime.datetime.now()
date = date.strftime("%m%d_%H%M") # 0707_1723
print(date)

save_filepath = './_ModelCheckPoint/' + current_name + '/'
load_filepath = './_ModelCheckPoint/' + current_name + '/'

###############################로드모델###################################
# model = load_model(load_filepath + '0708_1757_0018-0.2908.hdf5')
#########################################################################

filename = '{epoch:04d}-{val_loss:.4f}.hdf5'

earlyStopping = EarlyStopping(monitor='val_loss', patience=40, mode='auto', verbose=1, 
                              restore_best_weights=True)        

mcp = ModelCheckpoint(monitor='val_loss', mode='auto', verbose=1, save_best_only=True, 
                      filepath= "".join([save_filepath, date, '_', filename])
                      )

hist = model.fit(x_train, y_train, epochs=20, batch_size=128,
                 validation_split=0.3,
                 callbacks=[earlyStopping],
                 verbose=1)

#4. 평가, 예측
loss = model.evaluate(x_test, y_test) 
print('loss : ', loss)

y_predict = model.predict(x_test)
y_predict = np.argmax(y_predict, axis= 1)
df3 = pd.DataFrame(y_predict)
y_predict = oh.transform(df3)


acc = accuracy_score(y_test, y_predict)
print('acc스코어 : ', acc)

# CNN
# loss :  [0.27665308117866516, 0.9068999886512756]
# acc스코어 :  0.9069

# RNN
# loss :  [0.48293060064315796, 0.8213000297546387]
# acc스코어 :  0.8213

# Conv1D
#  accuracy: 0.1000
# loss :  [2.30261492729187, 0.10000000149011612]
# acc스코어 :  0.1