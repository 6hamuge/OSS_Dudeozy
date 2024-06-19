import os
import numpy as np
import soundfile as sf
import librosa

def extract_feature(file_name):
    print(f'Extracting {file_name}')
    X, sample_rate = sf.read(file_name, dtype='float32')
    if X.ndim > 1:
        X = X[:, 0]
    X = X.T

    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)  # 수정된 부분
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
    return np.hstack([mfccs, chroma, mel, contrast, tonnetz])

def parse_audio_files(parent_dir):
    features, labels = np.empty((0, 193)), np.empty(0)
    for subdir, _, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.wav'):
                label = os.path.basename(subdir)
                file_path = os.path.join(subdir, file)
                feature = extract_feature(file_path)
                features = np.vstack([features, feature])
                labels = np.append(labels, 1 if label == 'scream' else 0)
    return np.array(features), np.array(labels, dtype=int)

def main():
    features, labels = parse_audio_files('data')
    np.save('data/feat.npy', features)
    np.save('data/label.npy', labels)
    print(f'Features and labels saved to data/feat.npy and data/label.npy')

if __name__ == '__main__':
    main()
