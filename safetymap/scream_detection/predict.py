import sounddevice as sd
import numpy as np
import keras
import os
from feat_extract import extract_feature  # 직접 임포트로 변경

def real_time_predict(model_path):
    try:
        if not os.path.exists(model_path):
            print("모델을 찾을 수 없습니다. 먼저 네트워크를 학습하세요.")
            return

        model = keras.models.load_model(model_path)
        sample_rate = 44100  # 샘플링 레이트 설정
        duration = 1  # 오디오 녹음 시간

        print("녹음 시작. 비명이 감지되면 프로그램이 종료됩니다.")
        while True:
            print("소리를 녹음하고 있습니다...")
            audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()  # 녹음이 완료될 때까지 대기
            audio_data = audio_data.flatten()

            if len(audio_data) < 512:
                print(f"[경고] 오디오 데이터의 길이가 FFT 길이보다 짧습니다. 길이: {len(audio_data)}")
                continue  # 다음 반복으로 넘어가기

            if len(audio_data) > 0:
                # 추출된 오디오 데이터와 샘플 레이트를 extract_feature 함수에 전달
                mfccs, chroma, mel, contrast, tonnetz = extract_feature(audio_data, sample_rate)
                if all(x is not None for x in [mfccs, chroma, mel, contrast, tonnetz]):
                    features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
                    features = np.expand_dims(features, axis=0)
                    prediction = model.predict(features)
                    label = '비명' if np.argmax(prediction) == 0 else '비명아님'
                    print(f'예측: {label}')
                    if label == '비명':
                        print("비명이 감지되었습니다.")
                        break
                else:
                    print("오디오 특징 추출 실패")
            else:
                print("녹음된 데이터가 유효하지 않습니다. 다시 시도합니다.")
    except KeyboardInterrupt:
        print("프로그램 종료")
    except Exception as e:
        print(f"오류: {e}")

if __name__ == '__main__':
    model_path = os.path.join(os.path.dirname(__file__), 'trained_model.keras')
    real_time_predict(model_path)
