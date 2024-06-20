import subprocess
import webbrowser

def run_script(script_name, args=[]):
    # subprocess.Popen을 사용하여 실시간으로 출력을 가져오기 위해 stdout=subprocess.PIPE를 설정합니다.
    process = subprocess.Popen(["python", script_name] + args, stdout=subprocess.PIPE, text=True)
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())  # 출력된 결과를 출력합니다.
            if "비명이 감지되었습니다." in output:
                webbrowser.open("https://www.police.go.kr/index.do")
                print("Scream detected! Opening police website.")
                

    rc = process.poll()  # 프로세스의 종료 코드를 얻습니다.
    return rc

# 첫 번째 코드 실행: feature 추출
subprocess.run(["python", "feat_extract.py"])

# 두 번째 코드 실행: 신경망 학습
subprocess.run(["python", "nn.py"])

# 세 번째 코드 실행: 신경망을 통한 실시간 예측
run_script("predict.py")
