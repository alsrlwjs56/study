
from tabnanny import verbose
from sklearn. datasets import load_diabetes    
import numpy as np 
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from sklearn.model_selection import train_test_split

#1. 데이터
datasets = load_diabetes()

x = datasets.data
y = datasets.target

     
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size =0.2,                                
    shuffle=True, random_state =58525)
 
#2. 모델구성
model = Sequential()
model.add(Dense(10, input_dim=10))
model.add(Dense(80))
model.add(Dense(100))
model.add(Dense(15))
model.add(Dense(80))
model.add(Dense(70))
model.add(Dense(15))
model.add(Dense(1))


import time

#3 컴파일, 훈련
model.compile(loss ='mae', optimizer='adam')

start_time = time.time()

hist = model.fit(x_train, y_train, epochs =500, batch_size = 15, verbose=1, validation_split = 0.2)     

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

import matplotlib.pyplot as plt

from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

plt.figure(figsize=(9,6))
plt.plot(hist.history['loss'], marker = '.', c ='red', label= 'loss')   # x빼고 y만 넣어주면 됨(순차적).
plt.plot(hist.history['val_loss'], marker = '.', c ='blue', label= 'val_loss')  
plt.grid()
plt.title('제목')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend(loc='upper right')
plt.show()

# loss와 val_loss의 차이가 적을수록 좋은 값. loss가 적어도 val_loss와의 차이가 많이나면 좋지 않은 것. 

