# Project : 여성 안전 귀가 프로그램

## 목차
1. 소개
2. 개발 기간
3. 프로젝트 설명
4. 시연 영상
5. 기술 스택
6. 라이선스

## 소개
#### 안전한 귀갓길을 만드는 웹 서비스 "여성 안전 귀가 프로그램"
귀갓길의 위험 요소들로 인해 불안한 사람들을 위해 안전한 길을 안내하고, 비상 시에 자동으로 도움을 요청할 수 있는 프로그램을 만들고자 하였습니다.
- 안전 귀가를 위해 방범율을 높이거나 도움을 요청할 수 있는 CCTV, 가로등, 경찰서, 안전상비의약품 판매업소, 안전비상벨의 위치를 고려한 경로를 안내합니다.
- 비명이나 사용자가 미리 설정한 암호 음성을 인식하여 비상 상황 시 대처 수단으로 활용 가능합니다.

## 개발 기간
2024.05.18~2024.06.21

## 프로젝트 설명

#### 주요 기능
1. 길찾기 기능
   - 사용자가 설정한 출발지와 도착지를 바탕으로, 가장빠르게 갈 수 있는 최단 경로와 가까운 안전 요소의 가중치가 높은 안전 경로를 추천하여 지도 위에 표시 및 거리와 시간을 알려준다.
   - 가중치를 매길 안전요소: CCTV, 가로등, 안전비상벨, 경찰서 및 지구대, 안전비상의약품판매업소
2. 비명 인식 기능
   - 실시간으로 소리를 분석하여, 비명소리가 들린다면 바로 경찰청 홈페이지로 넘어갈 수 있게 함.
   
#### 각 페이지 설명 
#### API 사용
1. Daum Map Open API 활용 (길찾기 기능)
   - 지도 표시 및 시각화
   - 경로 표시를 위해 폴리라인과 같은 그래픽 요소를 추가하여 제공된 UI에 표시
   - 입력된 주소를 기반으로 해당 주소의 좌표를 가져옴.
#### AI 활용
2. 비명 인식 기능
   - 비명과 비명이 아닌 여러 소리를 구분하여 학습.
   - 우선적으로 데이터들의 특징들을 추출함. 그후, 신경망학습을 통하여 비명과 비명이 아닌 소리를 구분 할 수 있도록 하였음.
   - 마지막으로, 실시간으로 소리를 수집하여 특징을 추출하고, 학습된 것에 적용시켜 비명을 판단함.
## 실행 방법
safetymap폴더의 manage.py실행
(주의) pip install django==2.2.24
로 설치할 것 (최신 버전이 아니라)
- python manage.py runserver

## 시연 영상

## 기술 스택
1. 길찾기 기능
   - Django 사용: Python으로 구축된 고수준 웹 프레임워크로, 웹 애플리케이션의 백엔드 구축을 하는 데 사용됨.
   - 사용한 라이브러리: geocoder(위치 좌표 변환), leaflet.js(지도 프레임워크), haversine(좌표 간 거리 측정)
2. 비명 인식 기능
   *screamlearn 내부의 파일과 폴더가 비명 인식 기능에 관한 프로그램입니다.
   
   - feat_extract.py는 소리 데이터의 특징들을 추출합니다.
   - extract_feature 함수는 특징을 추출하는 함수이며, parse_audio_files함수는 extract_feature함수를 통해 추출한 특징을 저장합니다.
  
   - nn.py는 신경망 학습을 진행합니다. feat_extract.py 에서 미리 뽑아둔 특징을 통하여 학습을 시킵니다. 두 개의 은닉층을 사용하였습니다.
  
   - predict.py는 실시간으로 소리를 감지하여 비명인지 아닌지, 위에서 미리 학습한 결과를 통하여 판단해 줍니다. 
  
   - test1.py는 위의 과정을 모두 하나로 모은 파일입니다. 비명소리가 감지된다면, 바로 경찰청 웹페이지로 넘어가게 설정해 두었습니다.
  
   *이 프로그램은 wav 형식의 음성 데이터를 사용해야 합니다.


## 라이선스
*참고 오픈소스
- https://github.com/imfing/audio-classification/tree/master
