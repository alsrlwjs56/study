
from gc import callbacks
from tabnanny import verbose
from sklearn. datasets import   fetch_california_housing  
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import MaxAbsScaler, RobustScaler 
from sklearn import datasets
from sklearn.metrics import r2_score, mean_squared_error
from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.layers import Dense, Input


#1. 데이터
datasets =  fetch_california_housing ()

x = datasets.data
y = datasets.target


x_train, x_test, y_train, y_test = train_test_split(
    x, y,train_size=0.7,random_state=66
    )

# scaler = MinMaxScaler()
scaler = RobustScaler()
scaler.fit(x_train)
# scaler.transform(x_test)
x_test =scaler.transform(x_test)
x_train = scaler.transform(x_train)
print(np.min(x_train))      # 0   알아서 컬럼별로 나눠준다. 
print(np.max(x_train))      # 1
print(np.min(x_test))      # 0   알아서 컬럼별로 나눠준다. 
print(np.max(x_test))


#2. 모델구성
# model = Sequential()
# model.add(Dense(10, input_dim=8))
# model.add(Dense(120))
# model.add(Dense(80))
# model.add(Dense(25))
# model.add(Dense(1))

input1 = Input(shape=(8,))          # 컬럼3개를 받아드린다.
dense1 = Dense(100)(input1)          # Dense 뒤에 input 부분을 붙여넣는다.
dense2 = Dense(50, activation='relu')(dense1)
dense3 = Dense(30, activation='sigmoid')(dense2)
output1 = Dense(1)(dense3)

model = Model(inputs = input1, outputs = output1)


import time

#3 컴파일, 훈련
model.compile(loss ='mse', optimizer='adam')

from tensorflow.python.keras.callbacks import EarlyStopping
earlystopping =EarlyStopping(monitor='loss', patience=100, mode='min', 
              verbose=1, restore_best_weights = True)     
   
   
   
   
# EarlyStopping 일찍멈추겠다. (monitor-보겠다.='val_loss', patience=10-참겠다., 
# mode=(min)최소값)-(max)최대값 auto(자동), verbose=1 - 0으로 지정하면 10뒤에 값을 가져오게됨.)         

start_time = time.time()

hist = model.fit(x_train, y_train, epochs =100, batch_size = 32, 
                 verbose=1, validation_split = 0.2,
                 callbacks = [earlystopping])      # callbacks으로 불러온다 erlystopping   

end_time = time.time() - start_time

# loss = model.evaluate(x_test, y_test)
# print('loss : ', loss)

#4 평가 예측
loss = model.evaluate(x_test, y_test)
print("loss : ", loss)

print('====================')
print(hist)                         #<keras.callbacks.History object at 0x0000013FEE7CFDC0>
print('====================')
print(hist.history)  
print('====================')
print(hist.history['loss'])         # 키 벨류 안에 있는    loss로 양쪽에 '' 을 포함 시킨다. 
print('====================')
print(hist.history['val_loss'])  

print("걸린시간 : ", end_time)

y_predict = model.predict(x_test)

from sklearn.metrics import r2_score
r2 = r2_score(y_test,y_predict)

print('r2 스코어 :', r2)

# import matplotlib.pyplot as plt

# plt.figure(figsize=(9,6))
# plt.plot(hist.history['loss'], marker = '.', c ='red', label= 'loss')   # x빼고 y만 넣어주면 됨(순차적).
# plt.plot(hist.history['val_loss'], marker = '.', c ='blue', label= 'val_loss')  
# plt.grid()
# plt.title('제목')
# plt.ylabel('loss')
# plt.xlabel('epochs')
# plt.legend(loc='upper right')
# plt.show()




#1. scaler 하기전 
# 걸린시간 :  5.952741384506226
# r2 스코어 : 0.04069687405033395

#2. minmaxscaler
# 걸린시간 :  5.26584005355835
# r2 스코어 : 0.6037828875202791

#3. standardscaler 
# 걸린시간 :  5.23887038230896
# r2 스코어 : 0.6055634093852085

#4. MaxAbsScaler
# 걸린시간 :  118.99500775337219
# r2 스코어 : 0.5367446038096855
# loss :  0.635665237903595

#5. RobustScaler
# 걸린시간 :  123.04301404953003
# r2 스코어 : 0.5050329074235778
# loss :  0.6791790127754211

#6.
# loss :  0.27558133006095886
# 걸린시간 :  105.35696721076965
# r2 스코어 : 0.7991639182619943