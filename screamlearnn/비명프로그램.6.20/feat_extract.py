import os
import numpy as np
import soundfile as sf
import librosa

def extract_feature(data, sample_rate):
    if isinstance(data, str):
        print(f'Extracting {data}')
        X, sample_rate = sf.read(data, dtype='float32')
    else:
        X = data

    if X.ndim > 1:
        X = X[:, 0]
    X = X.T

    # n_fft 값을 데이터 길이에 따라 동적으로 조정
    n_fft = min(1024, len(X))

    # NaN 및 무한대 값 처리
    X = np.nan_to_num(X)

    try:
        stft = np.abs(librosa.stft(X, n_fft=n_fft))
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate, n_fft=n_fft).T, axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
        return np.hstack([mfccs, chroma, mel, contrast, tonnetz])
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None


def parse_audio_files(parent_dir):
    features, labels = np.empty((0, 193)), np.empty(0)
    for subdir, _, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.wav'):
                label = os.path.basename(subdir)
                file_path = os.path.join(subdir, file)
                feature = extract_feature(file_path, None)
                if feature is not None:
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
