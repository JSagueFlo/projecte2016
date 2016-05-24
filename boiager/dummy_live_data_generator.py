#encoding: utf-8

from main.models import Boia, Registre_boia, Centre
import random
import time
from datetime import datetime

boies = Boia.objects.all()

while True:
    for boia in boies:
        timestamp = datetime.now()
        tmpAir = random.uniform(-5.0, 40.0)
        tmpWater = random.uniform(5.0, 25.0)
        windSpeed = random.uniform(0.0, 60.0)
        nou_registre = Registre_boia(boia=boia, timestamp=timestamp, tmp_air=tmpAir, tmp_water=tmpWater,wind_speed=windSpeed)
        nou_registre.save()
    time.sleep(5)

