'''import glob
import os
import numpy as np
import soundfile as sf
import librosa

def extract_feature(file_name):
    try:
        X, sample_rate = sf.read(file_name, dtype='float32')
        if X.ndim > 1:
            X = X[:, 0]  # mono 오디오로 변환

        if len(X) < 1024:
            print(f"[경고] {file_name}의 길이가 FFT 길이보다 짧습니다. 길이: {len(X)}")
            return None, None, None, None, None

        # 단기 푸리에 변환 (STFT)
        stft = np.abs(librosa.stft(X, n_fft=1024))

        # MFCC (멜 주파수 켑스트럼 계수)
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)

        # 크로마
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)

        # 멜 스펙트로그램
        mel = np.mean(librosa.feature.melspectrogram(S=stft, sr=sample_rate).T, axis=0)
        mel_db = librosa.power_to_db(mel)  # 스펙트로그램을 데시벨로 변환

        # 스펙트럴 대비
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)

        # 톤넷츠 (조화 오디오의 토날 중심 특징)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
        return mfccs, chroma, mel_db, contrast, tonnetz
    except Exception as e:
        print(f"[오류] 특징 추출 오류: {file_name}, {e}")
        return None, None, None, None, None

def parse_audio_files(parent_dir='data'):
    features, labels = [], []
    for label, sub_dir in enumerate(['scream', 'notscream']):
        full_path = os.path.join(parent_dir, sub_dir)
        for fn in glob.glob(os.path.join(full_path, '*.wav')):  # 파일 확장자를 '.wav'로 변경
            mfccs, chroma, mel, contrast, tonnetz = extract_feature(fn)
            if all(v is not None for v in [mfccs, chroma, mel, contrast, tonnetz]):  # 모든 값이 None이 아니어야 추가
                ext_features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
                features.append(ext_features)
                labels.append(label)
                print(f"[완료] 특징 추출 완료: {fn}")
            else:
                print(f"[오류] 특징 추출 실패: {fn}")
    return np.array(features), np.array(labels)

# 특징과 레이블 저장
features, labels = parse_audio_files()
np.save('feat.npy', features)
np.save('label.npy', labels)
'''

import glob
import os
import numpy as np
import soundfile as sf
import librosa

def extract_feature(file_or_audio_data, sample_rate=None):
    try:
        if isinstance(file_or_audio_data, str):
            # file_or_audio_data가 파일 경로인 경우
            audio_data, sample_rate = sf.read(file_or_audio_data, dtype='float32')
        else:
            # file_or_audio_data가 오디오 데이터인 경우
            audio_data = file_or_audio_data

        if audio_data.ndim > 1:
            audio_data = audio_data[:, 0]  # mono 오디오로 변환

        if len(audio_data) < 1024:
            print(f"[경고] 오디오 데이터의 길이가 FFT 길이보다 짧습니다. 길이: {len(audio_data)}")
            return None, None, None, None, None

        # 단기 푸리에 변환 (STFT)
        stft = np.abs(librosa.stft(audio_data, n_fft=1024))

        # MFCC (멜 주파수 켑스트럼 계수)
        mfccs = np.mean(librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40).T, axis=0)

        # 크로마
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)

        # 멜 스펙트로그램
        mel = np.mean(librosa.feature.melspectrogram(S=stft, sr=sample_rate).T, axis=0)
        mel_db = librosa.power_to_db(mel)  # 스펙트로그램을 데시벨로 변환

        # 스펙트럴 대비
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)

        # 톤넷츠 (조화 오디오의 토날 중심 특징)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio_data), sr=sample_rate).T, axis=0)

        print(f"[특징 추출 완료] MFCCs: {mfccs.shape}, Chroma: {chroma.shape}, Mel: {mel_db.shape}, Contrast: {contrast.shape}, Tonnetz: {tonnetz.shape}")
        return mfccs, chroma, mel_db, contrast, tonnetz
    except Exception as e:
        print(f"[오류] 특징 추출 오류: {e}")
        return None, None, None, None, None

def parse_audio_files(parent_dir='data'):
    features, labels = [], []
    for label, sub_dir in enumerate(['scream', 'notscream']):
        full_path = os.path.join(parent_dir, sub_dir)
        for fn in glob.glob(os.path.join(full_path, '*.wav')):
            mfccs, chroma, mel, contrast, tonnetz = extract_feature(fn)
            if all(x is not None for x in [mfccs, chroma, mel, contrast, tonnetz]):
                ext_features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
                features.append(ext_features)
                labels.append(label)
                print(f"[완료] 특징 추출 완료: {fn}")
            else:
                print(f"[오류] 특징 추출 실패: {fn}")
    return np.array(features), np.array(labels)

# 특징과 레이블 저장
features, labels = parse_audio_files()
np.save('feat.npy', features)
np.save('label.npy', labels)




