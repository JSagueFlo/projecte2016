from django.db import models

# Create your models here.
class Centre(models.Model):
	name = models.CharField(max_length=100, unique=True)
	nif = models.CharField(max_length=8, unique=True)
	description = models.CharField(max_length=5000)
	lat = models.DecimalField(max_digits=9, decimal_places=6, default=None)
	lng = models.DecimalField(max_digits=9, decimal_places=6, default=None)
	img = models.URLField()

	class Meta:
		db_table = "centres"

	def __unicode__(self):
		return self.name

class Boia(models.Model):
	centre = models.ForeignKey(Centre, default=None)
	lat = models.DecimalField(max_digits=9, decimal_places=6)
	lng = models.DecimalField(max_digits=9, decimal_places=6)
	is_public = models.BooleanField(default=False)
	has_cam = models.BooleanField(default=True)
	location_img = models.URLField()
	location_name = models.CharField(max_length=200)

	class Meta:
		db_table = "boies"

	def __unicode__(self):
		return self.location_name