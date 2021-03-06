from tensorflow.python.keras.models import Sequential, Model, load_model
from tensorflow.python.keras.layers import Dense, Input

from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np
from sklearn import datasets
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
# from sqlalchemy import true
from tensorflow.python.keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score, accuracy_score
import time
import tensorflow as tf
from sklearn.preprocessing import MaxAbsScaler, RobustScaler 


#1. 데이터

datasets = load_digits()
x = datasets.data
y = datasets.target

print (x.shape, y.shape)                        # (1797 ,64)
print ( np.unique(y,return_counts=True))        # [0,1,2,3,4,5,6,7,8,9]

from tensorflow.keras.utils import to_categorical
y = to_categorical(y)

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    test_size=0.2,
                                                    shuffle=True,
                                                    random_state=58525
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
# model.add(Dense(10, input_dim=64, activation='relu')) #sigmoid : 이진분류일때 아웃풋에 activation = 'sigmoid' 라고 넣어줘서 아웃풋 값 범위를 0에서 1로 제한해줌
# model.add(Dense(100, activation='relu'))               # 출력이 0 or 1으로 나와야되기 때문, 그리고 최종으로 나온 값에 반올림을 해주면 0 or 1 완성
# model.add(Dense(80, activation='relu'))               # relu : 히든에서만 쓸수있음, 요즘에 성능 젤좋음
# model.add(Dense(15, activation='relu'))               
# model.add(Dense(10, activation='softmax'))             # softmax : 다중분류일때 아웃풋에 활성화함수로 넣어줌, 아웃풋에서 소프트맥스 활성화 함수를 씌워 주면 그 합은 무조건 1로 변함
                                                                 # ex 70, 20, 10 -> 0.7, 0.2, 0.1
                                                                 
                                                                 
# input1 = Input(shape=(64,))          # 컬럼3개를 받아드린다.
# dense1 = Dense(10)(input1)          # Dense 뒤에 input 부분을 붙여넣는다.
# dense2 = Dense(100, activation='relu')(dense1)
# dense3 = Dense(80, activation='relu')(dense2)
# dense4 = Dense(15, activation='relu')(dense3)
# output1 = Dense(10, activation='softmax')(dense4)
# model = Model(inputs = input1, outputs = output1)

# model.summary()                       
# Total params: 11,205          
            
                                          
start_time = time.time()
#3. 컴파일 훈련

# model.compile(loss='categorical_crossentropy', optimizer='adam', # 다중 분류에서는 로스함수를 'categorical_crossentropy' 로 써준다 (99퍼센트로)
#               metrics=['accuracy'])

# earlyStopping = EarlyStopping(monitor='val_loss', patience=80, mode='auto', verbose=1, 
#                               restore_best_weights=True)   

# model.fit(x_train, y_train, epochs=500, batch_size=32,
#                  validation_split=0.2,
#                  callbacks=[earlyStopping],
#                  verbose=1)


end_time = time.time() - start_time

#  model.save("./_save/keras23_12_load_wine.h5")
model = load_model("./_save/keras23_12_load_wine.h5")

#4. 평가, 예측
# loss, acc= model.evaluate(x_test, y_test)
# print('loss : ', loss)
# print('accuracy : ', acc)

results= model.evaluate(x_test, y_test)
print('loss : ', results[0])
print('accuracy : ', results[1])

y_predict = model.predict(x_test)

print(y_predict)
y_predict = np.argmax(y_predict, axis= 1)
print(y_predict)
y_predict = to_categorical(y_predict)


acc= accuracy_score(y_test, y_predict) 
print('acc : ', acc) 
print("걸린시간 :",end_time)

#전 
# acc :  0.9166666666666666
# 걸린시간 : 16.56109356880188
# loss :  0.27097490429878235

#후
# acc :  0.9166666666666666
# 걸린시간 : 0.0
# loss :  0.27097490429878235