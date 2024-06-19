from main.models import Alltimeshop
from django.db import connection

cursor = connection.cursor()
cursor.execute("SELET name FROM sqlite_master WHERE type='table';")
print(cursor.fetcahll())