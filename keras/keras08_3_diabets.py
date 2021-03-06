# 0.62이상

from sklearn. datasets import load_diabetes   
import numpy as np 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense 
from sklearn.model_selection import train_test_split

#1. 데이터
datasets = load_diabetes()

x = datasets.data
y = datasets.target

print(x)
print(y)
print(x.shape)     # (442, 10) # 값 찾기. 
print(y.shape)     # (442,)
 
 
x_train, x_test, y_train, y_test = train_test_split(
    x,y, train_size =0.7,                                
    shuffle=True, 
    random_state =52585)
 
#2. 모델구성
model = Sequential()
model.add(Dense(10, input_dim=10))
model.add(Dense(100))
model.add(Dense(80))
model.add(Dense(60))
model.add(Dense(20))
model.add(Dense(1))

#3 컴파일, 훈련
model.compile(loss ='mae', optimizer='adam')
model.fit(x_train, y_train, epochs =600, batch_size = 3)

#4 평가 예측
loss = model.evaluate(x_test, y_test)
print("loss : ", loss)

y_predict = model.predict(x_test)

from sklearn.metrics import r2_score
r2 = r2_score(y_test,y_predict)

print('r2 스코어 :', r2)

# loss :  38.2158203125
# r2 스코어 : 0.6074803349862943

# x_train, x_test, y_train, y_test = train_test_split(
#     x,y, train_size =0.7,                                
#     shuffle=True, 
#     random_state =52585)
 
# #2. 모델구성
# model = Sequential()
# model.add(Dense(10, input_dim=10))
# model.add(Dense(100))
# model.add(Dense(80))
# model.add(Dense(60))
# model.add(Dense(20))
# model.add(Dense(1))

# #3 컴파일, 훈련
# model.compile(loss ='mae', optimizer='adam')
# model.fit(x_train, y_train, epochs =80, batch_size = 15)

