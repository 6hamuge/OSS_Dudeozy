##test1.py
import subprocess
import webbrowser

def run_script(script_name, args=[]):
    result = subprocess.run(["python", script_name] + args, capture_output=True, text=True)
    if "Scream detected!" in result.stdout:
        webbrowser.open("https://www.police.go.kr/index.do")
        print("Scream detected! Opening police website.")
        exit()

# 첫 번째 코드 실행: feature 추출
subprocess.run(["python", "feat_extract.py"])

# 두 번째 코드 실행: 신경망을 사용한 학습과 예측
subprocess.run(["python", "cnn.py"])

subprocess.run(["python", "svm.py"])
###subprocess.run(["python", "nn.py"])

# 세 번째 코드 실행: 신경망을 통한 실시간 예측
run_script("screampredict.py", ["-P"])

# 네 번째 코드 실행: train.py 실행
subprocess.run(["python", "train.py"])
