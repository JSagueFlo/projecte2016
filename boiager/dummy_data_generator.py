#encoding: utf-8
'''
	IMPORTS - NO EDITIS AQUESTES LÍNIES
'''
from main.models import Boia, Registre_boia, Centre
import random
import time
from datetime import datetime, date, timedelta
'''
	FI IMPORTS
'''

'''
	DEFINEIX ELS PARÀMETERS AQUÍ
'''
boies = Boia.objects.all()

data_inici = datetime(2015, 5, 23)
data_final = datetime(2016, 5, 23)
'''
	FI DEFINICIÓ DELS PARÀMETRES
'''

'''
	NO EDITIS LES SEGÜENTS LÍNIES
'''
print('Creant registres des de ' + str(data_inici) + ' fins ' + str(data_final))
#python3 manage.py shell < helloworld.py 


current_datetime = data_inici
increment = 3600 #segons
segonsTotals = (data_final - data_inici).days * ( 60 * 60 * 24)

for boia in boies:
	for i in range(0, segonsTotals+1, increment):
		timestamp = current_datetime
		tmpAir = random.uniform(-5.0, 40.0)
		tmpWater = random.uniform(5.0, 25.0)
		windSpeed = random.uniform(0.0, 60.0)
		nou_registre = Registre_boia(boia=boia, timestamp=timestamp, tmp_air=tmpAir, tmp_water=tmpWater, wind_speed=windSpeed)
		nou_registre.save()
		current_datetime = current_datetime + timedelta(seconds=increment) # days, seconds, then other fields.

print('end')