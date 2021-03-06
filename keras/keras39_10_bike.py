from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.layers import Dense, Input, LSTM
import numpy as np
import pandas as pd
from sqlalchemy import true #pandas : 엑셀땡겨올때 씀
from keras.layers.recurrent import  SimpleRNN
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import datetime as dt
from sklearn.preprocessing import MaxAbsScaler, RobustScaler 
from sklearn.preprocessing import MinMaxScaler, StandardScaler  

#1. 데이터
path = './_data/bike/'
train_set = pd.read_csv(path + 'train.csv') # + 명령어는 문자를 앞문자와 더해줌  index_col=n n번째 컬럼을 인덱스로 인식
            
test_set = pd.read_csv(path + 'test.csv') # 예측에서 쓸거임        

'''                        
print(train_set)
print(train_set.shape) # (10886, 12)
                  
print(test_set)
print(test_set.shape) # (6493, 9)
print(test_set.info()) # (715, 9)
print(train_set.columns)
print(train_set.info()) # info 정보출력
print(train_set.describe()) # describe 평균치, 중간값, 최소값 등등 출력
'''


######## 년, 월 ,일 ,시간 분리 ############

train_set["hour"] = [t.hour for t in pd.DatetimeIndex(train_set.datetime)]
train_set["day"] = [t.dayofweek for t in pd.DatetimeIndex(train_set.datetime)]
train_set["month"] = [t.month for t in pd.DatetimeIndex(train_set.datetime)]
train_set['year'] = [t.year for t in pd.DatetimeIndex(train_set.datetime)]
train_set['year'] = train_set['year'].map({2011:0, 2012:1})

test_set["hour"] = [t.hour for t in pd.DatetimeIndex(test_set.datetime)]
test_set["day"] = [t.dayofweek for t in pd.DatetimeIndex(test_set.datetime)]
test_set["month"] = [t.month for t in pd.DatetimeIndex(test_set.datetime)]
test_set['year'] = [t.year for t in pd.DatetimeIndex(test_set.datetime)]
test_set['year'] = test_set['year'].map({2011:0, 2012:1})

train_set.drop('datetime',axis=1,inplace=True) # 트레인 세트에서 데이트타임 드랍
train_set.drop('casual',axis=1,inplace=True) # 트레인 세트에서 캐주얼 레지스터드 드랍
train_set.drop('registered',axis=1,inplace=True)

test_set.drop('datetime',axis=1,inplace=True) # 트레인 세트에서 데이트타임 드랍

print(train_set)# [10886 rows x 13 columns]
print(test_set)# [6493 rows x 12 columns]

##########################################


x = train_set.drop(['count'], axis=1)  # drop 데이터에서 ''사이 값 빼기
print(x)
print(x.columns)
print(x.shape) # (10886, 12)
y = train_set['count'] 
print(y)
print(y.shape) # (10886,)
x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    train_size=0.75,
                                                    random_state=31
                                                    )
print(train_set)# [10886 rows x 13 columns]
print(test_set)# [6493 rows x 12 columns]


#scaler = MaxAbsScaler()
scaler = RobustScaler()
# scaler = MinMaxScaler()
# scaler = StandardScaler()
scaler.fit(x_train)
x_test = scaler.transform(x_test)
x_train = scaler.transform(x_train)
print(np.min(x_train))      # 0   알아서 컬럼별로 나눠준다. 
print(np.max(x_train))      # 1
print(np.min(x_test))      # 0   알아서 컬럼별로 나눠준다. 
print(np.max(x_test))

print(x_test,y_test)

print(x_train.shape,x_test.shape)  #(8164, 12) (2722, 12)
print(x_train.shape,x_test.shape)
x_train = x_train.reshape(8164, 12,1)
x_test = x_test.reshape(2722, 12,1)



#2. 모델구성
model = Sequential()
model.add(LSTM(350, input_shape=(12,1)))      # [batch, timesteps(몇개씩 자르는지), feature=1(input_dim)]
model.add(Dense(128, activation='swish'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='swish'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='swish'))
model.add(Dense(4, activation='swish'))
model.add(Dense(1))
model.summary()

#3. 컴파일, 훈련
from tensorflow.python.keras.callbacks import EarlyStopping
earlystopping =EarlyStopping(monitor='loss', patience=100, mode='min', 
              verbose=1, restore_best_weights = True)     
        
model.compile(loss='mse', optimizer='adam')

hist = model.fit(x_train, y_train, epochs=200, batch_size=1500, verbose=1,
          validation_split=0.2, callbacks=[earlystopping])

test_set = np.array(test_set)

test_set = test_set.reshape(6493,12,1)
print(test_set)

#4. 평가, 예측
loss = model.evaluate(x_test, y_test) 
print('loss : ', loss)

y_predict = model.predict(x_test)
def RMSE(a, b): 
    return np.sqrt(mean_squared_error(a, b))
rmse = RMSE(y_test, y_predict)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print('loss : ', loss)
print("RMSE : ", rmse)
print('r2스코어 : ', r2)


y_summit = model.predict(test_set)

print(y_summit)
print(y_summit.shape) # (6493, 1)
submission_set = pd.read_csv(path + 'Submission.csv', # + 명령어는 문자를 앞문자와 더해줌
                             index_col=0) # index_col=n n번째 컬럼을 인덱스로 인식
print(submission_set)
submission_set['count'] = y_summit
print(submission_set)
submission_set.to_csv(path + 'submission.csv', index = True)


#6. model
# loss: 69619.0469
# r2스코어 :  0.9447082024123568
# 걸린시간 :  90.73648834228516

# LSTM
# loss :  32741.541015625
# RMSE :  180.94623188280528
# r2스코어 :  -0.001026005307254163