import speech_recognition as sr
import webbrowser
import os

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
    if "노래 틀어줘" in data or "노래 켜" in data or "노래 틀어" in data or "노래 틀어 줘" in data:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        webbrowser.open(url)
    elif "노래 꺼줘" in data or "노래 꺼" in data or "노래 꺼 줘" in data:
        os.system('taskkill /f /im chrome.exe')
    elif "앱 꺼줘" in data or "프로그램 종료" in data or "앱 꺼 줘" in data or "앱 꺼" in data:
        break
    else:
        print("다시 말해주세요.")
