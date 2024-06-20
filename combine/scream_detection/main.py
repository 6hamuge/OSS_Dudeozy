import subprocess
import webbrowser
import os

def run_script(script_name, args=[]):
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, script_name)

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
                process.terminate()  # 비명이 감지되면 프로세스를 종료합니다.

    rc = process.poll()  # 프로세스의 종료 코드를 얻습니다.
    return rc


def run_test_scripts():
    # 각 스크립트 파일의 경로를 절대 경로로 지정합니다.
    base_dir = os.path.dirname(__file__)

    # 첫 번째 코드 실행: feature 추출
    subprocess.run(["python", os.path.join(base_dir, 'feat_extract.py')])

    # 두 번째 코드 실행: 신경망 학습
    subprocess.run(["python", os.path.join(base_dir, 'nn.py')])

    # 세 번째 코드 실행: 신경망을 통한 실시간 예측
    run_script(os.path.join(base_dir, 'predict.py'))



if __name__ == "__main__":
    run_test_scripts()
