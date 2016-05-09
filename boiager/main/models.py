from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg
from datetime import datetime, date, timedelta as td

# Create your models here.
class Centre(models.Model):
	name = models.CharField(max_length=100, unique=True)
	nie = models.CharField(max_length=10, unique=True, null=True, default=None)
	description = models.CharField(max_length=5000, blank=True, null=True)
	is_public = models.BooleanField(default=False)
	lat = models.DecimalField(max_digits=10, decimal_places=7, default=None)
	lng = models.DecimalField(max_digits=10, decimal_places=7, default=None)
	img = models.CharField(max_length=100, blank=True, null=True)
	user = models.ManyToManyField(User, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.name

	def __str__(self):
		return self.name

	def get_boies(self):
		return Boia.objects.filter(centre=self)

	def get_boies_count(self):
		return len(Boia.objects.filter(centre=self))

	def get_map_coords(self):
		boies = self.get_boies()
		coords = boies.aggregate(max_lat=Max('lat'), max_lng=Max('lng'), min_lat=Min('lat'), min_lng=Min('lng'))
		lat = (coords['max_lat'] + coords['min_lat'])/2
		lng = (coords['max_lng'] + coords['min_lng'])/2
		map_centre = {'lat': lat, 'lng': lng}
		return map_centre

	class Meta:
		db_table = "centre"


class Boia(models.Model):
	centre = models.ForeignKey(Centre, default=None)
	lat = models.DecimalField(max_digits=10, decimal_places=7)
	lng = models.DecimalField(max_digits=10, decimal_places=7)
	has_cam = models.BooleanField(default=True)
	location_img = models.CharField(max_length=100, blank=True, null=True)
	location_name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.location_name

	def __str__(self):
		return self.location_name

	def get_anys(self):
		arrayDades = Registre_boia.objects.filter(boia=self).values('timestamp')
		arrayYears = []
		for date in arrayDades:
			arrayYears.append( int(date['timestamp'].year) )
		arrayYears = list(set(arrayYears))
		arrayYears.sort(reverse=True)
		return arrayYears

	def get_mesos(self, anyy):
		arrayDades = Registre_boia.objects.filter(boia=self).filter(timestamp__year=anyy).values('timestamp')
		arrayMesos = []
		for date in arrayDades:
			arrayMesos.append( int(date['timestamp'].month) )
		arrayMesos = list(set(arrayMesos))
		arrayMesos.sort(reverse=True)
		return arrayMesos
		
	def get_dies(self, anyy, mes):
		arrayDades = Registre_boia.objects.filter(boia=self).filter(timestamp__year=anyy).values('timestamp')
		arrayDies = []
		for date in arrayDades:
			if mes == int(date['timestamp'].month):
				arrayDies.append( int(date['timestamp'].day) )
		arrayDies = list(set(arrayDies))
		arrayDies.sort(reverse=True)
		return arrayDies

	def get_dates(self):
		d1 = Registre_boia.objects.first().date()
		d2 = Registre_boia.objects.last().date()
		delta = d2 - d1
		dates = {}

		for i in range(delta.days + 1):
			dia = (d1 + td(days=i))
			year = dia.year
			month = dia.month
			day = dia.day
			if year not in dates.keys():
				dates[year] = {}
			if month not in dates[year].keys():
				dates[year][month] = {}
			if day not in dates[year][month].keys():
				dates[year][month][day] = {}
		return dates

	def get_registres_actual(self):
		return Registre_boia.objects.filter(boia=self).last()

	def get_registres_max_min_dia(self):
		today = date.today()
		registres_today = Registre_boia.objects.filter(timestamp__contains=today)
		return Registre_boia.objects.filter(boia=self)\
									.filter(timestamp__contains=today)\
		                            .aggregate( tmp_aigua_maxima=Max('tmp_water'),\
		                            			tmp_aigua_minima=Min('tmp_water'),\
		                            			tmp_aire_maxima=Max('tmp_air'),\
		                            			tmp_aire_minima=Min('tmp_air'),\
		                            			wind_speed_maxima=Max('wind_speed'),\
		                            			wind_speed_minima=Min('wind_speed')
		                            )

	class Meta:
		db_table = "boia"


class Registre_boia(models.Model):
	boia = models.ForeignKey(Boia, default=None)
	#
	# Important canviar auto_now en mode de produccio
	#
	timestamp = models.DateTimeField(auto_now=False)
	tmp_air = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
	tmp_water = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
	wind_speed = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)

	def __unicode__(self):
		return u''+str(self.timestamp)

	def __str__(self):
		return str(self.timestamp)

	class Meta:
		db_table = "registre_boia"


class Token(models.Model):
	centre = models.ForeignKey(Centre, default=None)
	token = models.CharField(max_length=36, unique=True)
	used = models.BooleanField(default=False)
	being_used = models.BooleanField(default=False)

	def __unicode__(self):
		return u''+self.token

	def __str__(self):
		return self.token

	class Meta:
		db_table = "token"


class Slider(models.Model):
	title = models.CharField(max_length=100, default='Title')
	img = models.CharField(max_length=100, null=True, blank=True)
	label = models.CharField(max_length=30, unique=True, default='Label')
	synopsis = models.CharField(max_length=1000, null=True, blank=True)
	filename = models.CharField(max_length=100, unique=True, default='index.html')

	def __unicode__(self):
		return u''+self.title

	def __str__(self):
		return self.title

	class Meta:
		db_table = "slider"