import subprocess
import webbrowser

def run_script(script_name, args=[]):
    result = subprocess.run(["python", script_name] + args, capture_output=True, text=True)
    print(result.stdout)  # 실행 결과 출력
    if "비명이 감지되었습니다." in result.stdout:
        webbrowser.open("https://www.police.go.kr/index.do")
        print("Scream detected! Opening police website.")
        exit()

# 첫 번째 코드 실행: feature 추출
subprocess.run(["python", "feat_extract.py"])

# 두 번째 코드 실행: 신경망 학습
subprocess.run(["python", "nn.py"])

# 세 번째 코드 실행: 신경망을 통한 실시간 예측
run_script("predict.py")
