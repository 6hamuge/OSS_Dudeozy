import sounddevice as sd
import soundfile as sf
import queue
import librosa
import numpy as np
import keras
import sys
import os.path as op
import argparse
from feat_extract import extract_feature

def real_time_predict(args):
    if op.exists(args.model):
        model = keras.models.load_model(args.model)
        while True:
            try:
                features = np.empty((0, 193))
                start = time.time()
                mfccs, chroma, mel, contrast, tonnetz = extract_feature()
                ext_features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
                features = np.vstack([features, ext_features])
                features = np.expand_dims(features, axis=2)
                pred = model.predict_classes(features)
                for p in pred:
                    print(p)
                    if args.verbose:
                        print('Time elapsed in real time feature extraction: ', time.time() - start)
                    sys.stdout.flush()
            except KeyboardInterrupt:
                parser.exit(0)
            except Exception as e:
                parser.exit(type(e).__name__ + ': ' + str(e))
    elif input('Model not found. Train network first? (y/N)').lower() in ['y', 'yes']:
        from train import train
        train(args)
        real_time_predict(args)

def main(args):
    if args.real_time_predict:
        real_time_predict(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-P', '--real-time-predict', action='store_true', help='predict sound in real time')
    parser.add_argument('-m', '--model', metavar='path', default='trained_model.h5', help='use this model path on train and predict operations')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose print')
    args = parser.parse_args()
    main(args)
