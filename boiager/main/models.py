from django.db import models, connection
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg
from django.utils.timezone import localtime, now
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from datetime import datetime, date, timedelta as td
from dateutil.relativedelta import relativedelta
from uuid import uuid4
import calendar
import locale
from django.db.models.signals import post_save
from django.dispatch import receiver

locale.setlocale(locale.LC_ALL, 'ca_ES')



# Create your models here.
class Centre(models.Model):
	name = models.CharField(max_length=100, unique=True)
	nie = models.CharField(max_length=10, unique=True, null=True, default=None)
	description = models.CharField(max_length=5000, blank=True, null=True)
	is_public = models.BooleanField(default=False)
	lat = models.DecimalField(max_digits=10, decimal_places=7, default=None)
	lng = models.DecimalField(max_digits=10, decimal_places=7, default=None)
	img = models.CharField(max_length=1000, blank=True, null=True)
	user = models.ManyToManyField(User, blank=True, null=True, default=None)
	email = models.EmailField(max_length=100, default='jordi.martyn1@gmail.com')
	site = models.URLField(max_length=200, default='http://www.boiager.cat')

	def __unicode__(self):
		return u'%s' % self.name

	def __str__(self):
		return str(self.id) + ' - ' + self.name

	def get_boies(self):
		"""
		Retorna la llista de boies del centre
		:return: llista de boies
		"""
		return Boia.objects.filter(centre=self)

	def get_boies_count(self):
		"""
		Retorna el número de boies del centre
		:return: número de boies del centre
		"""
		return len(Boia.objects.filter(centre=self))

	def get_map_coords(self):
		"""
		Retorna el centre de coordenades en funció de la distancia entre boies del centre, si no hi ha boies, retorna les coordenades del centre
		:return: diccionari amb la latitud i longitud del centre
		"""
		try:
			boies = self.get_boies()
			coords = boies.aggregate(max_lat=Max('lat'), max_lng=Max('lng'), min_lat=Min('lat'), min_lng=Min('lng'))
			if self.lat > coords['max_lat']:
				coords['max_lat'] = self.lat
			elif self.lat < coords['min_lat']:
				coords['min_lat'] = self.lat
			if self.lng > coords['max_lng']:
				coords['max_lng'] = self.lng
			elif self.lng < coords['min_lng']:
				coords['min_lng'] = self.lng
			lat = (coords['max_lat'] + coords['min_lat'])/2
			lng = (coords['max_lng'] + coords['min_lng'])/2
		except:
			lat = self.lat
			lng = self.lng
		map_centre = {'lat': lat, 'lng': lng}
		return map_centre

	def generate_tokens(self, num):
		"""
		Genera tokens vinculats al centre i envia un correu al administrador amb la informació generada
		:param num: número de tokens a generar
		:return: void
		"""
		if not self.is_public:
			email_body = 'Nous codis d\'accés generats' + self.name + '\n\n'
			for i in range(num):
				token = str(uuid4())
				email_body += '\n' + token
				token_obj = Token(centre=self, token=token)
				token_obj.save()
			try:
				email = EmailMessage('Nous codis d\'accés generats', email_body, to=[self.email])
				email.send()
			except:
				pass

	class Meta:
		db_table = "centre"



@receiver(post_save, sender=Centre)
def after_Centre_save(sender, instance, **kwargs):
	"""
	Després de guardar un centre, executa el mètode generate_tokens d'aquell centre
	:param sender: indica el model que envia l'event
	:param instance: indica l'objecte sobre el qual s'ha de treballar
	:return: void
	"""
	instance.generate_tokens(10)


class Boia(models.Model):
	centre = models.ForeignKey(Centre, default=None)
	lat = models.DecimalField(max_digits=10, decimal_places=7)
	lng = models.DecimalField(max_digits=10, decimal_places=7)
	has_cam = models.BooleanField(default=True)
	location_img = models.CharField(max_length=100, blank=True, null=True)
	location_name = models.CharField(max_length=200)
	ip = models.CharField(max_length=20, blank=True, null=True, default='80.174.145.128:8080')

	def __unicode__(self):
		return self.location_name

	def __str__(self):
		return self.location_name

	# def get_anys(self):
	# 	arrayDades = Registre_boia.objects.filter(boia=self).values('timestamp')
	# 	arrayYears = []
	# 	for date in arrayDades:
	# 		arrayYears.append( int(date['timestamp'].year) )
	# 	arrayYears = list(set(arrayYears))
	# 	arrayYears.sort(reverse=True)
	# 	return arrayYears
    #
	# def get_mesos(self, anyy):
	# 	arrayDades = Registre_boia.objects.filter(boia=self).filter(timestamp__year=anyy).values('timestamp')
	# 	arrayMesos = []
	# 	for date in arrayDades:
	# 		arrayMesos.append( int(date['timestamp'].month) )
	# 	arrayMesos = list(set(arrayMesos))
	# 	arrayMesos.sort(reverse=True)
	# 	return arrayMesos
	#
	# def get_dies(self, anyy, mes):
	# 	arrayDades = Registre_boia.objects.filter(boia=self).filter(timestamp__year=anyy).values('timestamp')
	# 	arrayDies = []
	# 	for date in arrayDades:
	# 		if mes == int(date['timestamp'].month):
	# 			arrayDies.append( int(date['timestamp'].day) )
	# 	arrayDies = list(set(arrayDies))
	# 	arrayDies.sort(reverse=True)
	# 	return arrayDies

	def get_dates_min_max(self):
		"""
		Retorna la primera i última data en que hi ha registres de la boia
		:return: array primera i ultima data
		"""
		d1 = Registre_boia.objects.first().timestamp.date()
		d2 = Registre_boia.objects.last().timestamp.date()
		return [d1,d2]

	def get_dates(self):
		"""
		Retorna un diccionari de diccionaris que conté l'estructura temporal en el qual hi ha dades d'una boia (any, mes, dia)
		:return: diccionari
		"""
		d1 = Registre_boia.objects.filter(boia=self).first().timestamp.date()
		d2 = Registre_boia.objects.filter(boia=self).last().timestamp.date()
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

	def get_registre_actual(self):
		"""
		Retorna l'últim registre de la boia
		:return: últim registre
		"""
		return Registre_boia.objects.filter(boia=self).last()


	def get_latest_registres(self):
		"""
		Retorna els últims 10 registres de la boia
		:return: llista dels últims 10 registres
		"""
		ultims = Registre_boia.objects.filter(boia=self).order_by('-id')[:10]
		return reversed(ultims)

	def get_registres_anuals(self, year):
		"""
		Retorna les mitjanes dels registres mensuals de la boia durant un any en concret, de gener a desembre
		:param year: any
		:return: array de mitjanes mensuals
		"""
		month = connection.ops.date_trunc_sql('month', 'timestamp')
		registres_year = Registre_boia.objects.filter(boia=self).filter(timestamp__contains=year)
		registres = registres_year.extra({'month': month}).values('month').annotate(\
																		tmp_aigua=Avg('tmp_water'),\
																		tmp_aire=Avg('tmp_air'),\
																		wind_speed=Avg('wind_speed')\
																	   )
		reg = []
		for registre in registres:
			reg.append({
				'mes': calendar.month_abbr[registre['month'].month],
				'tmp_aigua': registre['tmp_aigua'],
				'tmp_aire': registre['tmp_aire'],
				'wind_speed': registre['wind_speed']
			})

		return reg


	def get_registres_mensuals(self, year, month):
		"""
		Retorna les mitjanes del registres diaris de la boia durant un mes i any concret, del 1 al últim dia del mes
		:param year: any
		:param month: mes
		:return: array de mitjanes diàries
		"""
		month = str(month) if month >= 10 else '0' + str(month)
		day = connection.ops.date_trunc_sql('day', 'timestamp')
		registres_month = Registre_boia.objects.filter(boia=self).filter(timestamp__contains=str(year)+'-'+str(month))
		registres = registres_month.extra({'day': day}).values('day').annotate(\
																			tmp_aigua=Avg('tmp_water'),\
																			tmp_aire=Avg('tmp_air'),\
																			wind_speed=Avg('wind_speed')\
																		)
		reg = []
		for registre in registres:
			reg.append({
				'dia': registre['day'].day,
				'tmp_aigua': registre['tmp_aigua'],
				'tmp_aire': registre['tmp_aire'],
				'wind_speed': registre['wind_speed']
			})

		return reg


	def get_registres_diaris(self, year, month, day):
		"""
		Retorna les mitjanes del registres horaris de la boia durant un dia, mes i any concret, de les 00:00 a les 23:00
		:param year: any
		:param month: mes
		:param day: dia
		:return: array de mitjanes horaries
		"""
		month = str(month) if month >= 10 else '0' + str(month)
		day = str(day) if day >= 10 else '0' + str(day)
		registres_month = Registre_boia.objects.filter(boia=self).filter(timestamp__contains=str(year) + '-' + str(month))
		registres =  registres_month.extra({'hour': 'HOUR(timestamp)'}).values('hour').annotate(\
																						tmp_aigua=Avg('tmp_water'),\
																						tmp_aire=Avg('tmp_air'),\
																						wind_speed=Avg('wind_speed')\
																						)
		reg = []
		for registre in registres:
			reg.append({
				'hora': registre['hour'],
				'tmp_aigua': registre['tmp_aigua'],
				'tmp_aire': registre['tmp_aire'],
				'wind_speed': registre['wind_speed']
			})

		return reg


	def get_registres_max_min_today(self):
		"""
		Retorna un diccionari amb els valors màxims i mínims d'avui
		:return: diccionari de valors màxims i mínims
		"""
		today = localtime(now()).date()
		return Registre_boia.objects.filter(boia=self)\
									.filter(timestamp__contains=today)\
		                            .aggregate( tmp_aigua_maxima=Max('tmp_water'),\
		                            			tmp_aigua_minima=Min('tmp_water'),\
		                            			tmp_aire_maxima=Max('tmp_air'),\
		                            			tmp_aire_minima=Min('tmp_air'),\
		                            			wind_speed_maxima=Max('wind_speed'),\
		                            			wind_speed_minima=Min('wind_speed')
		                            )


	def get_registres_max_min_avg(self, year=None, month=None, day=None):
		"""
		Retorna un diccionari amb els valors màxims mínims i mitjans d'un dia, mes o any en concret
		:param year: any
		:param month: mes, opcional
		:param day: dia, opcional
		:return:
		"""
		string_data = ''
		if year is not None:
			string_data += str(year)
			if month is not None:
				string_data += '-' + (str(month) if month >= 10 else '0' + str(month))
				if day is not None:
					string_data += '-' + (str(day) if day >= 10 else '0' + str(day))

		return Registre_boia.objects.filter(boia=self)\
			.filter(timestamp__contains=string_data) \
			.aggregate(tmp_aigua_maxima=Max('tmp_water'),\
					   tmp_aigua_minima=Min('tmp_water'),\
					   tmp_aigua_mitjana=Avg('tmp_water'),\
					   tmp_aire_maxima=Max('tmp_air'),\
					   tmp_aire_minima=Min('tmp_air'),\
					   tmp_aire_mitjana=Avg('tmp_air'),\
					   wind_speed_maxima=Max('wind_speed'),\
					   wind_speed_minima=Min('wind_speed'),\
					   wind_speed_mitjana=Avg('wind_speed')
					   )


	class Meta:
		db_table = "boia"


class Registre_boia(models.Model):
	boia = models.ForeignKey(Boia, default=None)
	#
	# Important canviar auto_now en mode de produccio
	#
	timestamp = models.DateTimeField()
	tmp_air = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
	tmp_water = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
	wind_speed = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
	humiext = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)

	def __unicode__(self):
		return u''+str(self.timestamp)

	def __str__(self):
		return str(self.timestamp)

	class Meta:
		db_table = "registre_boia"


class Token(models.Model):
	centre = models.ForeignKey(Centre, default=None)
	user = models.ForeignKey(User, default=None, null=True, blank=True)
	token = models.CharField(max_length=36, unique=True)
	used = models.BooleanField(default=False)
	being_used = models.BooleanField(default=False)
	expire_date = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return u''+self.token

	def __str__(self):
		return self.token

	def use(self, user):
		"""
		Vincula un usuari amb un token, actualitza la data d'expiració perqué caduqui al cap de 3 mesos, i canvia l'estat del token a used
		:param user: usuari
		:return: void
		"""
		self.used = 1
		self.expire_date = datetime.now() + relativedelta(months=3)
		self.user = user
		self.save()

	class Meta:
		db_table = "token"

class Slider(models.Model):
	title = models.CharField(max_length=100, default='Title')
	img = models.CharField(max_length=100, null=True, blank=True)
	synopsis = models.CharField(max_length=1000, null=True, blank=True)
	href = models.CharField(max_length=100, unique=True, default='/')
	btn = models.CharField(max_length=100, default='Més informació')

	def __unicode__(self):
		return u''+self.title

	def __str__(self):
		return self.title

	class Meta:
		db_table = "slider"
