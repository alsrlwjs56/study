import numpy as np
import pandas as pd
from tensorflow.python.keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score, accuracy_score
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import MinMaxScaler, StandardScaler  
from sklearn.preprocessing import MaxAbsScaler, RobustScaler 

#1. 데이터
season = np.load('d:/study_data/_save/_npy/personaltest28.npy')
x_train = np.load('d:/study_data/_save/_npy/project_train_x.npy')
y_train = np.load('d:/study_data/_save/_npy/project_train_y.npy')
x_test = np.load('d:/study_data/_save/_npy/project_test_x.npy')
y_test = np.load('d:/study_data/_save/_npy/project_test_y.npy')
            # (550,)

print(x_train.shape)            # (2600, 150, 150, 3)
print(y_train.shape)            # (2600, 7)
print(x_test.shape)             # (700, 150, 150, 3)
print(y_test.shape)             # (700, 7)


x_train = x_train.reshape(2600,150,450)
x_test = x_test.reshape(700,150,450)
print(season.shape)
season = season.reshape(7,150,450)
print(x_train.shape)            # 2600, 150, 450)
print(y_train.shape)            # (2600, 7)
print(x_test.shape)             # (700, 150, 450)
print(y_test.shape)             # (700, 7)



from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten , Dropout,MaxPooling2D,LSTM,Reshape


#2. 모델 
model = Sequential()
model.add(LSTM(64, input_shape = (150,450), activation='relu'))
model.add(Reshape(target_shape=(4,4,4)))
model.add(Conv2D(128,(3,3),activation='relu',padding='same'))
model.add(MaxPooling2D(2,2))
model.add(Conv2D(128,(3,3),activation='relu',padding='same'))
model.add(MaxPooling2D(2,2))
model.add(Conv2D(128,(3,3),activation='relu',padding='same'))
model.add(Flatten())
model.add(Dense(64,activation='relu'))
# model.add(Dropout(0.3))
model.add(Dense(32,activation='relu'))
# model.add(Dropout(0.3))
model.add(Dense(7,activation='softmax'))
model.summary()    

#3. 컴파일.훈련

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics= ['accuracy'])

earlystopping =EarlyStopping(monitor='loss', patience=50, mode='auto', 
              verbose=1, restore_best_weights = True)     

hist = model.fit(x_train,y_train, epochs=30,validation_split=0.3,verbose=2,batch_size=128,
                 callbacks=[earlystopping]) 


#4. 예측
accuracy = hist.history['accuracy']
val_accuracy = hist.history['val_accuracy']
loss = hist.history['loss']
val_loss = hist.history['val_loss']

print('loss : ',loss[-1])
print('accuracy : ', accuracy[-1])

loss = model.evaluate(x_test, y_test)
y_predict = model.predict(season)
print('predict : ',y_predict)


# 1.hail   2.lighting   3.rain   4.rime   5.shine   6.smog   7.snow 

# 1.hail : 3/7
# [[0. 0. 0. 0. 1. 0. 0.]
#  [0. 1. 0. 0. 0. 0. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 1. 0. 0. 0. 0.]
#  [0. 0. 0. 1. 0. 0. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]]

# 2.lighting : 7/7
# [[0. 1. 0. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0. 0. 0.]]

# 3.rain : 4/7
# [[0. 0. 1. 0. 0. 0. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 1. 0. 0. 0. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 1. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 1. 0. 0. 0. 0.]]

# 4.rime : 2/7
# [[0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 1. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 0. 1. 0. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 1. 0. 0.]
#  [0. 0. 0. 1. 0. 0. 0.]]

# 5.sunshine : 6/7
#  [[0. 0. 0. 0. 1. 0. 0.]
#  [0. 0. 0. 1. 0. 0. 0.]
#  [0. 0. 0. 0. 1. 0. 0.]
#  [0. 0. 0. 0. 1. 0. 0.]
#  [0. 0. 0. 0. 1. 0. 0.]
#  [0. 0. 0. 0. 1. 0. 0.]
#  [0. 0. 0. 0. 1. 0. 0.]]

#  6.smog : 3/7
# [[1. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 1. 0.]
#  [0. 0. 0. 0. 0. 1. 0.]
#  [0. 0. 0. 0. 0. 0. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 1. 0.]
#  [1. 0. 0. 0. 0. 0. 0.]]

# 7.snow : 7/7
# [[0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 0. 0. 0. 1.]
#  [0. 0. 0. 0. 0. 0. 1.]]

