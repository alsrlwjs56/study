import numpy as np


# 1. 데이터
x = np.array([[1,2,3,4,5,6,7,8,9,10],
             [1,1,1,1,2,1.3,1.4,1.5,1.6,1.4]
             ,[9,8,7,6,5,4,3,2,1,0]])   # -> y= w1x1 + w2x2 +b
y = np.array([11,12,13,14,15,16,17,18,19,20])    # (10,)
print (x.shape)  #(3,10)    # x = 행3, 열,10 
print (y.shape)  #(10,)

# x = x.transpose()                     # transpose 행과열의 위치변경 방법1 
x = x.T                                 # transpose 행과열의 위치변경 방법2

print(x.shape)   #(10, 3) (10,)



#2. 모델구성
from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.layers import Dense, Input

# model = Sequential()
# # model.add(Dense(10, input_dim=3))
# model.add(Dense(10, input_shape=(3,)))
# model.add(Dense(5, activation='relu'))
# model.add(Dense(3, activation='sigmoid'))
# model.add(Dense(1))

input1 = Input(shape=(3,))          # 컬럼3개를 받아드린다.
dense1 = Dense(10)(input1)          # Dense 뒤에 input 부분을 붙여넣는다.
dense2 = Dense(100, activation='relu')(dense1)
dense3 = Dense(80, activation='relu')(dense2)
dense4 = Dense(50, activation='relu')(dense3)
dense5 = Dense(15, activation='relu')(dense4)
dense6 = Dense(10, activation='relu')(dense5)
output1 = Dense(1)(dense6)

model = Model(inputs = input1, outputs = output1)

model.summary()         # Total params: 117

# Model: "model"
# _________________________________________________________________
# Layer (type)                 Output Shape              Param #
# =================================================================
# input_1 (InputLayer)         [(None, 3)]               0              # <<< Sequential() 과 다른부분.
# _________________________________________________________________
# dense (Dense)                (None, 10)                40
# _________________________________________________________________
# dense_1 (Dense)              (None, 5)                 55
# _________________________________________________________________
# dense_2 (Dense)              (None, 3)                 18
# _________________________________________________________________
# dense_3 (Dense)              (None, 1)                 4
# =================================================================
# Total params: 117
# Trainable params: 117
# Non-trainable params: 0

#3. 컴파일
model.compile(loss='mse', optimizer='adam')
model.fit(x,y,epochs=10, batch_size=1)





