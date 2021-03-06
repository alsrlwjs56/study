from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

import numpy as np
from sklearn.model_selection import train_test_split

#1.데이터

x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
y = np.array([1,2,3,4,6,7,9,10,13,14,15,17,8,16,23,24,26,29,27,30])

from sklearn.model_selection import train_test_split     
x_train, x_test, y_train, y_test = train_test_split(
    x,y, train_size =0.7,                                
    shuffle=True, 
    random_state =66)

#2. 모델구성
model = Sequential()
model.add(Dense(64, input_dim=13))
model.add(Dense(32, activation= 'relu'))
model.add(Dense(16, activation= 'relu'))
model.add(Dense(8, activation= 'relu'))
model.add(Dense(1))

#3 컴파일, 훈련
model.compile(loss ='mse', optimizer='adam')
model.fit(x_train, y_train, epochs =200, batch_size = 2)

#4 평가 예측
loss = model.evaluate(x_test, y_test)
print("loss : ", loss)

y_predict = model.predict(x)

from sklearn.metrics import r2_score
r2 = r2_score(y,y_predict)

print('r2 스코어 :', r2)


# loss :  1.758468508720398
# r2 스코어 : 0.9130251249876765

# loss :  0.7509753108024597
# r2 스코어 : 0.9185493263854302



# import matplotlib.pyplot as plt

# plt.scatter(x, y)
# plt.plot(x, y_predict, color ="red")
# plt.show()





#predict는 아직. 
