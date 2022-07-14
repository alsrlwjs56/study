from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.layers import Dense, Input, Dropout,LSTM
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np
import pandas as pd
from sqlalchemy import true                                 #pandas : 엑셀땡겨올때 씀
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MaxAbsScaler, RobustScaler 

#1. 데이터
path = './_data/ddarung/'
train_set = pd.read_csv(path + 'train.csv',                 # + 명령어는 문자를 앞문자와 더해줌
                        index_col=0)                        # index_col=n n번째 컬럼을 인덱스로 인식
print(train_set)
print(train_set.shape) # (1459, 10)

test_set = pd.read_csv(path + 'test.csv',                    # 예측에서 쓸거임                
                       index_col=0)
print(test_set)
print(test_set.shape) # (715, 9)

print(train_set.columns)
print(train_set.info())                                     # info 정보출력
print(train_set.describe())                                 # describe 평균치, 중간값, 최소값 등등 출력

# 결측치 처리 1. 제거 #############

print(train_set.isnull().sum())
train_set = train_set.fillna(train_set.mean())       # dropna() : train_set 에서 na, null 값 들어간 행 삭제
test_set = test_set.fillna(test_set.mean()) # test_set 에서 이빨빠진데 바로  ffill : 위에서 가져오기 test_set.mean : 평균값
print(train_set.isnull().sum()) 
print(train_set.shape)   # (1328, 10)

############################            


x = train_set.drop(['count'], axis=1)                    # drop 데이터에서 ''사이 값 빼기
print(x)
print(x.columns)
print(x.shape) # (1459, 9)

y = train_set['count'] 
print(y)
print(y.shape) # (1459,)

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    train_size=0.8,
                                                    random_state=58525
                                                    )
scaler = MaxAbsScaler()
# scaler = StandardScaler()
scaler.fit(x_train)
# scaler.transform(x_test)
x_test =scaler.transform(x_test)
x_train = scaler.transform(x_train)
print(np.min(x_train))      # 0   알아서 컬럼별로 나눠준다. 
print(np.max(x_train))      # 1
print(np.min(x_test))      # 0   알아서 컬럼별로 나눠준다. 
print(np.max(x_test))

print(x_train.shape,x_test.shape)  #(1167, 9) (292, 9)

x_train = x_train.reshape(1167, 9,1)
x_test = x_test.reshape(292, 9,1)

#2. 모델구성
model = Sequential()
# model.add(SimpleRNN(units= 10, input_shape=(3,1)))      # [batch, timesteps(몇개씩 자르는지), feature=1(input_dim)]
# 10 = units, 3 = timesteps , 1 = feature 
# units * (feature +bias +units)                    # units를 한번더 해준다. 
# model.add(SimpleRNN(32))                          # RNN은 2차원으로 인식해서 바로 Dense적용가능.
# model.add(SimpleRNN(units=10, input_length =3, input_dim=1))       
# model.add(SimpleRNN(units=10, input_dim=1, input_length =3))    # 가독성 떨어짐                                                 # RNN은 2차원으로 인식해서 바로 Dense적용가능.  
model.add(LSTM(350, input_shape=(30,1)))      # [batch, timesteps(몇개씩 자르는지), feature=1(input_dim)]
model.add(Dense(128, activation='swish'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='swish'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='swish'))
model.add(Dense(8, activation='swish'))
model.add(Dense(1))
                                         # erorr = ndim=3 3차원으로 바꿔라. 
model.summary()    

# input1 = Input(shape=(9,))          # 컬럼3개를 받아드린다.
# dense1 = Dense(128)(input1)          # Dense 뒤에 input 부분을 붙여넣는다.
# dense2 = Dense(64, activation='relu')(dense1)
# dense3 = Dense(32, activation='relu')(dense2)
# dense4 = Dense(16, activation='relu')(dense3)
# dense5 = Dense(8, activation='relu')(dense4)
# dense6 = Dense(4, activation='relu')(dense5)
# output1 = Dense(1, activation='relu')(dense6)

# model = Model(inputs = input1, outputs = output1)

import time
start_time = time.time()

#3. 컴파일, 훈련

from tensorflow.python.keras.callbacks import EarlyStopping
earlyStopping = EarlyStopping(monitor='val_loss', patience=200, mode='min', verbose=1, 
                              restore_best_weights=True)
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint 
import datetime
date = datetime.datetime.now()
date = date.strftime('%m%d_%H%M') 
filepath = './_ModelCheckPoint/9ddarung/'
filename = '{epoch:04d}-{val_loss:.4f}.hdf5'    # f > 소수점4자리까지 표현.           

earlystopping =EarlyStopping(monitor='loss', patience=50, mode='min', 
              verbose=1, restore_best_weights = True)     
        
mcp = ModelCheckpoint(monitor='val_loss', mode='auto', verbose=1,               # mode acc > max 
                      save_best_only=True,                                      # patience 필요없음.
                      filepath ="".join([filepath,'9ddarung_',date, '_', filename])
                      ) 
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit(x_train, y_train, epochs=200, batch_size=32, 
          verbose=1, validation_split=0.2, callbacks=[earlyStopping, mcp])

end_time = time.time() - start_time

#4. 평가, 예측
loss = model.evaluate(x, y) 


y_predict = model.predict(x_test)

def RMSE(a, b): 
    return np.sqrt(mean_squared_error(a, b))

rmse = RMSE(y_test, y_predict)


from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)

print('loss : ', loss)
print("RMSE : ", rmse)
print('r2스코어 : ', r2)

print("걸린시간 :",end_time)


#4. MaxAbsScaler
# loss :  [2539560448.0, 45863.0859375]
# RMSE :  44.13384823645532
# r2스코어 :  0.6934015870340235
# 걸린시간 : 17.524970531463623

