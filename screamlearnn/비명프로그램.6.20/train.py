import sounddevice as sd
import numpy as np
import queue
import webbrowser
from keras.models import load_model
from feat_extract import extract_feature

def real_time_predict(model_path):
    model = load_model(model_path)
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
                    continue
                features = extract_feature(data, 44100)
                if features is not None:
                    features = np.expand_dims(features, axis=0)
                    features = np.expand_dims(features, axis=2)
                    predictions = model.predict(features)
                    if np.argmax(predictions) == 1:
                        print("Scream detected!")
                        webbrowser.open("https://www.police.go.kr/index.do")
                        return  # 감지 후 함수 종료
                    else:
                        print("No scream detected.")
        except KeyboardInterrupt:
            print("Recording stopped.")
        except Exception as e:
            print("Error:", e)

model_path = 'trained_model.keras'
real_time_predict(model_path)
