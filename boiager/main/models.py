from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Centre(models.Model):
	name = models.CharField(max_length=100, unique=True)
	nie = models.CharField(max_length=10, unique=True, null=True)
	description = models.CharField(max_length=5000, blank=True)
	is_public = models.BooleanField(default=False)
	lat = models.DecimalField(max_digits=9, decimal_places=6, default=None)
	lng = models.DecimalField(max_digits=9, decimal_places=6, default=None)
	img = models.CharField(max_length=100, blank=True)
	user = models.ManyToManyField(User)


	def __unicode__(self):
		return u'%s' % self.name

	def __str__(self):
		return self.name

	class Meta:
		db_table = "centres"

	

class Boia(models.Model):
	centre = models.ForeignKey(Centre, default=None)
	lat = models.DecimalField(max_digits=9, decimal_places=6)
	lng = models.DecimalField(max_digits=9, decimal_places=6)
	has_cam = models.BooleanField(default=True)
	location_img = models.CharField(max_length=100, blank=True)
	location_name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.location_name

	def __str__(self):
		return self.location_name

	class Meta:
		db_table = "boies"
