import code
import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
import queue

def extract_feature(file_name=None):
    if file_name: 
        print('Extracting', file_name)
        X, sample_rate = sf.read(file_name, dtype='float32')
    else:  
        device_info = sd.query_devices(None, 'input')
        sample_rate = int(device_info['default_samplerate'])
        q = queue.Queue()
        def callback(i,f,t,s): q.put(i.copy())
        data = []
        with sd.InputStream(samplerate=sample_rate, callback=callback):
            while True: 
                if len(data) < 100000: data.extend(q.get())
                else: break
        X = np.array(data)

    if X.ndim > 1: X = X[:,0]
    X = X.T

    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast,tonnetz

#def parse_audio_files(parent_dir, file_ext='*.ogg'):
#    sub_dirs = os.listdir(parent_dir)
#    sub_dirs.sort()
#    features, labels = np.empty((0,193)), np.empty(0)
#    for label, sub_dir in enumerate(sub_dirs):
#        if os.path.isdir(os.path.join(parent_dir, sub_dir)):
#            for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
#                try: mfccs, chroma, mel, contrast,tonnetz = extract_feature(fn)
#                except Exception as e:
#                    print("[Error] extract feature error in %s. %s" % (fn,e))
#                    continue
#                ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
#                features = np.vstack([features,ext_features])
#                labels = np.append(labels, label)
#            print("extract %s features done" % (sub_dir))
#    return np.array(features), np.array(labels, dtype = np.int)

def parse_audio_files(parent_dir, file_ext='*.ogg'):
    scream_dir = os.path.join(parent_dir, 'scream')
    non_scream_dir = os.path.join(parent_dir, 'non_scream')

    features_scream, labels_scream = parse_audio_files_in_dir(scream_dir, file_ext)
    features_non_scream, labels_non_scream = parse_audio_files_in_dir(non_scream_dir, file_ext)

    features = np.vstack([features_scream, features_non_scream])
    labels = np.hstack([labels_scream, labels_non_scream])

    return features, labels


def main():
    features, labels = parse_audio_files('data')
    np.save('feat.npy', features)
    np.save('label.npy', labels)

    features, filenames = parse_predict_files('predict')
    np.save('predict_feat.npy', features)
    np.save('predict_filenames.npy', filenames)

if __name__ == '__main__': main()
