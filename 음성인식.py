import speech_recognition as sr
import webbrowser
import os
#pip install SpeechRecognition
#pip install PyAudio

Recognizer = sr.Recognizer()  # 인스턴스 생성
mic = sr.Microphone()

while True:
    with mic as source:
        audio = Recognizer.listen(source, phrase_time_limit=5)
    try:
        data = Recognizer.recognize_google(audio, language="ko")
    except:
        print("이해하지 못했음")
        continue
    print(data)
    if "두더지" in data:
        #웹이여서 일단 경찰청신고 홈페이지로 연결
        url = "https://www.police.go.kr/www/security/report/report01.jsp"
        webbrowser.open(url)
        break
    else:
        print("다시 말해주세요.")
