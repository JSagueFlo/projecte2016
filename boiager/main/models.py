from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Centre(models.Model):
	name = models.CharField(max_length=100, unique=True)
	nie = models.CharField(max_length=10, unique=True, null=True, default=None)
	description = models.CharField(max_length=5000, blank=True, null=True)
	is_public = models.BooleanField(default=False)
	lat = models.DecimalField(max_digits=9, decimal_places=6, default=None)
	lng = models.DecimalField(max_digits=9, decimal_places=6, default=None)
	img = models.CharField(max_length=100, blank=True, null=True)
	user = models.ManyToManyField(User)

	def __unicode__(self):
		return u'%s' % self.name

	def __str__(self):
		return self.name

	def get_boies(self):
		return Boia.objects.filter(centre=self)

	class Meta:
		db_table = "centre"

class Boia(models.Model):
	centre = models.ForeignKey(Centre, default=None)
	lat = models.DecimalField(max_digits=9, decimal_places=6)
	lng = models.DecimalField(max_digits=9, decimal_places=6)
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

	def get_actual(self):
		return Registre_boia.objects.latest('id')

	class Meta:
		db_table = "boia"

class Registre_boia(models.Model):
	boia = models.ForeignKey(Boia, default=None)
	timestamp = models.DateTimeField(auto_now=True)
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