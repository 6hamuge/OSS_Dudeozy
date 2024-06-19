import os
import django

# 현재 파일의 위치를 기준으로 프로젝트 루트 디렉토리를 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safetymap.settings')
os.environ.setdefault('PYTHONPATH', BASE_DIR)

django.setup()

import csv
from main.models import Cctv

CSV_PATH = os.path.join(BASE_DIR, 'main', 'data', 'cctv.csv')

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    data_reader = csv.reader(csvfile)
    for row in data_reader:
        if row[0] != 'lon':
            cctv = Cctv(lon=row[0], lat=row[1])
            cctv.save()
