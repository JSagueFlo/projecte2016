#encoding: utf-8
from main.models import Boia, Registre_boia, Centre
import random
import time
from datetime import datetime, date, timedelta

boies = Boia.objects.all()
data_inici = datetime(2014, 5, 23)
data_final = datetime(2016, 5, 23)

print('Creant registres des de ' + str(data_inici) + ' fins ' + str(data_final))

current_datetime = data_inici
increment = 3600
segonsTotals = (data_final - data_inici).days * ( 60 * 60 * 24)

for i in range(0, segonsTotals+1, increment):
	for boia in boies:
		timestamp = current_datetime
		tmpAir = random.uniform(-5.0, 40.0)
		tmpWater = random.uniform(5.0, 25.0)
		windSpeed = random.uniform(0.0, 60.0)
		nou_registre = Registre_boia(boia=boia, timestamp=timestamp, tmp_air=tmpAir, tmp_water=tmpWater, wind_speed=windSpeed)
		nou_registre.save()
	current_datetime = current_datetime + timedelta(seconds=increment)

print('end')