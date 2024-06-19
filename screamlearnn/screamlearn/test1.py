import subprocess

# 첫 번째 코드 실행: feature 추출
subprocess.run(["python", "feat_extract.py"])

# 두 번째 코드 실행: SVM을 사용한 학습
subprocess.run(["python", "svm.py"])

# 세 번째 코드 실행: 신경망을 사용한 학습
subprocess.run(["python", "nn.py"])

# 네 번째 코드 실행: 신경망을 사용한 학습과 예측
subprocess.run(["python", "cnn.py"])

# 다섯 번째 코드 실행: 신경망을 통한 실시간 예측
subprocess.run(["python", "screampredict.py"])

# 여섯 번째 코드 실행: train.py 실행
subprocess.run(["python", "train.py"])
