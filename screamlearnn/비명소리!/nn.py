import numpy as np
import keras
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.optimizers import RMSprop

# 데이터 로드
X = np.load('feat.npy')
y = np.load('label.npy').ravel()

# 데이터를 섞고 학습/테스트 데이터로 분리
X, y = shuffle(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

# 레이블 원-핫 인코딩
num_classes = np.max(y) + 1  # 클래스의 수를 기반으로 설정
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# 모델 아키텍처 설정
input_layer = Input(shape=(X_train.shape[1],))  # 입력 데이터의 형태
x = Dense(512, activation='relu')(input_layer)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
output_layer = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=input_layer, outputs=output_layer)

model.compile(optimizer=RMSprop(), loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 학습
model.fit(X_train, y_train, batch_size=64, epochs=800, validation_split=0.2)

# 테스트 평가
score, acc = model.evaluate(X_test, y_test, batch_size=32)
print('Test score:', score)
print('Test accuracy:', acc)

# 모델 저장 (네이티브 Keras 포맷 사용)
model.save('trained_model.keras')
