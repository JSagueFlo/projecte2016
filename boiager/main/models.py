from django.db import models
from django.contrib.auth.models import User

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
		db_table = "centres"

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
		return ''

	class Meta:
		db_table = "boies"

class Registre_boia(models.Model):
	boia = models.ForeignKey(Boia, default=None)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return u''+str(self.timestamp)

	def __str__(self):
		return str(self.timestamp)

	class Meta:
		db_table = "registre_boia"