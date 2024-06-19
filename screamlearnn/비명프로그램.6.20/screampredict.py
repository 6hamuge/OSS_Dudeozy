'''import sounddevice as sd
import queue
import numpy as np
from keras.models import load_model
import sys
from feat_extract import extract_feature

def real_time_predict(args):
    if op.exists(args.model):
        model = load_model(args.model)
        q = queue.Queue()

        def callback(indata, frames, time, status):
            q.put(indata.copy())

        with sd.InputStream(callback=callback, channels=1, samplerate=44100):
            print("Recording... Press Ctrl+C to stop.")
            while True:
                try:
                    data = q.get()
                    data = data.flatten()
                    sample_rate = 44100

                    if np.isfinite(data).all():
                        data = np.nan_to_num(data)
                        feature = extract_feature(data, sample_rate)
                        if feature is not None:
                            features = np.expand_dims(feature, axis=0)
                            features = np.expand_dims(features, axis=2)
                            predictions = model.predict(features)
                            pred_class = np.argmax(predictions, axis=1)
                            if pred_class[0] == 1:
                                print("Scream detected!")
                                webbrowser.open("https://www.police.go.kr/index.do")
                            else:
                                print("No scream detected.")
                    else:
                        print("Invalid audio buffer detected. Skipping...")
                except KeyboardInterrupt:
                    print("Stopped.")
                    break
                except Exception as e:
                    print(type(e).__name__, ":", e)
                    break
    else:
        print("Model not found. Train network first.")
        if input('Train network first? (y/N)').lower() in ['y', 'yes']:
            from train import train
            args.batch_size = 64  # Default settings
            args.epochs = 500  # Default settings
            train(args)
            real_time_predict(args)


def main(args):
    if args.real_time_predict:
        real_time_predict(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Real-time scream detection")
    parser.add_argument('-P', '--real-time-predict', action='store_true', help='predict sound in real time')
    parser.add_argument('-m', '--model', metavar='path', default='trained_model.keras', help='use this model path on train and predict operations')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose print')
    args = parser.parse_args()
    main(args)
'''
##screampredict.py
import sounddevice as sd
import numpy as np
import queue
import webbrowser
from keras.models import load_model
from feat_extract import extract_feature  # 필요한 특성 추출 함수

# 실시간 비명 감지
def real_time_predict(model_path):
    model = load_model(model_path)  # 학습된 모델 로드
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(indata.copy())

    with sd.InputStream(callback=callback, channels=1, samplerate=44100):
        print("Recording... Press Ctrl+C to stop.")
        try:
            while True:
                data = q.get()
                if data is None or not np.isfinite(data).all():
                    continue  # 유효한 데이터가 아니면 무시
                features = extract_feature(data, 44100)  # 특성 추출
                if features is not None:
                    features = np.expand_dims(features, axis=0)
                    features = np.expand_dims(features, axis=2)  # 차원 추가
                    predictions = model.predict(features)
                    if np.argmax(predictions) == 1:  # 비명 클래스의 인덱스가 1일 때
                        print("Scream detected!")
                        webbrowser.open("https://www.police.go.kr/index.do")
                        break  # 감지 후 종료
                    else:
                        print("No scream detected.")
        except KeyboardInterrupt:
            print("Stopped recording.")
        except Exception as e:
            print("Error:", e)

# 모델 경로 설정
model_path = 'trained_model.keras'

# 실행
real_time_predict(model_path)
