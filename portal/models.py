from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager,PermissionsMixin
from datetime import *
from django.utils import timezone
from django_resized import ResizedImageField
from django.core.validators import MinValueValidator
# Create your models here.
class AluminiDetails(models.Model):
        id=models.AutoField(primary_key=True)
        email=models.EmailField(max_length=50,unique=True)
	firstName=models.CharField(max_length=40)
	lastName=models.CharField(max_length=40)
	gender=models.CharField(max_length=10)
	register=models.IntegerField(default=0)	
	branch=models.CharField(max_length=80)
	course=models.CharField(max_length=80)
	year=models.IntegerField()
	dob=models.DateField()
	designation=models.CharField(max_length=60,blank=True)
	organisation=models.CharField(max_length=60,blank=True)
	mobile=models.CharField(max_length=40)
	address_permanent=models.CharField(max_length=200,blank=True)
	city_permanent=models.CharField(max_length=80,blank=True)
	zip_permanent=models.CharField(max_length=10,blank=True)
	state_permanent=models.CharField(max_length=50,blank=True)
	country_permanent=models.CharField(max_length=50,blank=True)
        privacy_PAddress=models.CharField(max_length=20,default="Only Me")
        privacy_CAddress=models.CharField(max_length=20,default="Only Me")
        privacy_Mobile=models.CharField(max_length=20,default="Only Me")
        privacy_Email=models.CharField(max_length=20,default="Only Me")        
        roll=models.CharField(max_length=50,blank=True)
	address_present=models.CharField(max_length=200)
	city_present=models.CharField(max_length=80)
	zip_present=models.CharField(max_length=10)
	state_present=models.CharField(max_length=50)
	country_present=models.CharField(max_length=50)
	last_activity=models.DateTimeField(default=timezone.now)
	verified=models.IntegerField(default=0,blank=True)

	photo=ResizedImageField(size=[600, 600], quality=95,upload_to='')
	#photo=models.FileField(upload_to="")
	def __unicode__(self):              # __unicode__ on Python 2
			return '%s' % (self.email)	

class StudentDetails(models.Model):
        id=models.AutoField(primary_key=True)
        email=models.EmailField(max_length=50,unique=True)
	firstName=models.CharField(max_length=40)
	lastName=models.CharField(max_length=40)
	gender=models.CharField(max_length=10)
	register=models.IntegerField(default=0)	
	branch=models.CharField(max_length=80)
	course=models.CharField(max_length=80)
	year=models.IntegerField()
	dob=models.DateField()
	organisation=models.CharField(max_length=60,blank=True)
	mobile=models.CharField(max_length=40)
	address_permanent=models.CharField(max_length=200,blank=True)
	city_permanent=models.CharField(max_length=80,blank=True)
	zip_permanent=models.CharField(max_length=10,blank=True)
	state_permanent=models.CharField(max_length=50,blank=True)
	country_permanent=models.CharField(max_length=50,blank=True)
        privacy_PAddress=models.CharField(max_length=20,default="Only Me")
        privacy_CAddress=models.CharField(max_length=20,default="Only Me")
        privacy_Mobile=models.CharField(max_length=20,default="Only Me")
        privacy_Email=models.CharField(max_length=20,default="Only Me")        
        roll=models.CharField(max_length=50)
	address_present=models.CharField(max_length=200)
	city_present=models.CharField(max_length=80)
	zip_present=models.CharField(max_length=10)
	state_present=models.CharField(max_length=50)
	country_present=models.CharField(max_length=50)
	last_activity=models.DateTimeField(default=timezone.now)

	photo=ResizedImageField(size=[600, 600], quality=95,upload_to='')
	#photo=models.FileField(upload_to="")
	def __unicode__(self):              # __unicode__ on Python 2
			return '%s' % (self.email)
class FacultyDetails(models.Model):
        id=models.AutoField(primary_key=True)
        email=models.EmailField(max_length=50,unique=True)
	firstName=models.CharField(max_length=40)
	lastName=models.CharField(max_length=40)
	gender=models.CharField(max_length=10)
	year=models.IntegerField()
	register=models.IntegerField(default=0)	
	dob=models.DateField()
	mobile=models.CharField(max_length=40)
	address_permanent=models.CharField(max_length=200,blank=True)
	city_permanent=models.CharField(max_length=80,blank=True)
	zip_permanent=models.CharField(max_length=10,blank=True)
	state_permanent=models.CharField(max_length=50,blank=True)
	country_permanent=models.CharField(max_length=50,blank=True)
        privacy_PAddress=models.CharField(max_length=20,default="Only Me")
        privacy_CAddress=models.CharField(max_length=20,default="Only Me")
        privacy_Mobile=models.CharField(max_length=20,default="Only Me")
        privacy_Email=models.CharField(max_length=20,default="Only Me")        
	designation=models.CharField(max_length=60)
	address_present=models.CharField(max_length=200)
	city_present=models.CharField(max_length=80)
	zip_present=models.CharField(max_length=10)
	state_present=models.CharField(max_length=50)
	country_present=models.CharField(max_length=50)
	branch=models.CharField(max_length=80)
	last_activity=models.DateTimeField(default=timezone.now)

	photo=ResizedImageField(size=[600, 600], quality=95,upload_to='')
	#photo=models.FileField(upload_to="")
	def __unicode__(self):              # __unicode__ on Python 2
			return '%s' % (self.email)
class Verification(models.Model):
	hash_value=models.CharField(max_length=200)
	email=models.EmailField(unique=True)
	password=models.CharField(max_length=50)
	def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.email)
class Notifications(models.Model):
	notification=models.CharField(max_length=1000)
	new=models.IntegerField(default=1)
	date_time=models.DateTimeField( auto_now_add=True)

class AuthUserManager(BaseUserManager):	
	def create_user(self,username,email,category,password=None,):
		if not username:
			raise ValueError("User must have a username")

		user=self.model(username=self.normalize_email(username),)
		user.is_active=True
		user.set_password(password)
		user.email = email
		user.category=category
		
		user.save(using=self._db)
		return user	
	def create_superuser(self,username,email,category,password,):
		user=self.create_user(username=username,email=email,category=category,password=password,)
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user	


class MyUser(AbstractBaseUser,PermissionsMixin):
	username=models.EmailField(unique=True)
	email = models.EmailField(unique=True)
	category=models.CharField(max_length=20)   # 0 for Alumni 1 for Student 2 for Faculty
	objects=AuthUserManager()
	is_active = models.BooleanField(default=True, null=False)
	is_staff = models.BooleanField(default=False, null=False)
	date_joined=models.DateTimeField(null=True,blank=True)
	USERNAME_FIELD='username'

	REQUIRED_FIELDS = ['email','category']
	
	def get_full_name(self):
		user=self.username
		return user

	def get_short_name(self):
		return self.username
	
	def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.username)	


class Question(models.Model):
	heading_story = models.CharField(max_length=200)
	content_story = models.CharField(max_length=6500)
	date_story = models.DateTimeField(default=timezone.now)
	who_posted = models.EmailField(unique=False, default=True, null=False)
	category=models.CharField(max_length=20)
	author_id=models.IntegerField(default=0)
	author_name=models.CharField(max_length=200)
class Interest(models.Model):
        id=models.AutoField(primary_key=True)
	heading_interest = models.CharField(max_length=200)
	content_interest = models.CharField(max_length=600)
	date_interest = models.DateTimeField(default=timezone.now)
	who_posted = models.EmailField(unique=False, default=True, null=False)
class Broadcast(models.Model):
        id=models.AutoField(primary_key=True)
        heading_broadcast=models.CharField(max_length=50)
        content_broadcast=models.CharField(max_length=600)
        date_broadcast=models.DateTimeField(default=timezone.now)
        def __unicode__(self):              # __unicode__ on Python 2
		return '%s %s' % (self.heading_broadcast,self.content_broadcast)
class RequestForContact(models.Model):
        id=models.AutoField(primary_key=True)
        who_requested=models.EmailField(unique=False, default=False)
        requestercategory=models.CharField(max_length=20)
        requestedcategory=models.CharField(max_length=20)
        whom_requested=models.EmailField(unique=False, default=False)
        #Request is : 0 for Not Requested ,1 For requested. 2 for accepted, 3 for decline
        mobile_requested=models.CharField(default='notrequested',max_length=20)
        email_requested=models.CharField(default='notrequested',max_length=20)
        date_request=models.DateTimeField(default=timezone.now)
        def __unicode__(self):              # __unicode__ on Python 2
			return '%s' % (self.who_requested)
class GuestHouse(models.Model):
        id=models.AutoField(primary_key=True)
        email=models.EmailField(unique=False)
        rooms=models.PositiveIntegerField(validators=[MinValueValidator(1)])
        attendees=models.PositiveIntegerField(validators=[MinValueValidator(1)])
        date_start=models.DateField()
        date_end=models.DateField()
        comments=models.CharField(max_length=250,null=True,blank=True)
        mobile=models.CharField(max_length=40)
        def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.email)
class GeneralNotifications(models.Model):
        id=models.AutoField(primary_key=True)
        who_requested=models.EmailField(unique=False, default=False)
        requestercategory=models.CharField(max_length=20)
        requestedcategory=models.CharField(max_length=20)
        whom_requested=models.EmailField(unique=False, default=False)
        notification_content=models.CharField(max_length=200)
        notification_type=models.CharField(default='1',max_length=20)
        date_response=models.DateTimeField(default=timezone.now)
        def __unicode__(self):              # __unicode__ on Python 2
			return '%s' % (self.who_requested)
class IIT_Activities(models.Model):
	id=models.AutoField(primary_key=True)
	heading=models.CharField(max_length=80,blank=False)
	content=models.CharField(max_length=5000,blank=True)
	date_time=models.DateTimeField(default=timezone.now)
	dataid=models.CharField(max_length=500,blank=True)
	videosrc=models.URLField(blank=True,max_length=200)
	photo=models.FileField(upload_to='',blank=True)
class AsmpAlumniResponse(models.Model):
        email=models.EmailField(primary_key=True)
        mentor_max=models.PositiveIntegerField(validators=[MinValueValidator(0)],default=0)
        areas_mentor=models.CharField(max_length=600,blank=False)
        last_response_date=models.DateTimeField(default=timezone.now)
        def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.email)
class AsmpStudentResponse(models.Model):
        email=models.EmailField(primary_key=True)
        career_interest=models.CharField(max_length=100,blank=False)
        guidance_type=models.CharField(max_length=600,blank=False)
        last_response=models.DateTimeField(default=timezone.now)
        def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.email)
class blackList(models.Model):
        id=models.AutoField(primary_key=True)
        email=models.EmailField(unique=True,default=False)
        def __unicode__(self):              # __unicode__ on Python 2
			return '%s' % (self.email)
class Chronicle(models.Model):
        id=models.AutoField(primary_key=True)
	content=models.CharField(max_length=5000,blank=True)
	date_from=models.DateTimeField(default=timezone.now)
        pdf=models.FileField(upload_to="chronicles/",blank=True)

class ReferenceNumber(models.Model):
	number=models.IntegerField(default=0)
class AlumniMeetMembers(models.Model):
	email=models.EmailField(max_length=50,primary_key=True)
	delegate=models.CharField(max_length=30)
	person_count=models.CharField(max_length=2)
	person1=models.CharField(max_length=50)
	person2=models.CharField(max_length=50,blank=True)
	person3=models.CharField(max_length=50,blank=True)
	person4=models.CharField(max_length=50,blank=True)
	person5=models.CharField(max_length=50,blank=True)
	person6=models.CharField(max_length=50,blank=True)
	def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.email)

class PaymentDetails(models.Model):
	email=models.EmailField(max_length=50,primary_key=True)
	mihpayid=models.CharField(max_length=100)
	mode=models.CharField(max_length=10)
	txnid=models.CharField(max_length=10)
	amount=models.CharField(max_length=10)
	cc=models.CharField(max_length=2)
	timestamp=models.DateTimeField(default=timezone.now)
	def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.email + "  "+ self.txnid)
class travelDetail(models.Model):
	email=models.EmailField(max_length=50,primary_key=True)
	arrival_mode=models.CharField(max_length=20)
	arrival_number=models.CharField(max_length=10,blank=True,null=True)
	arrival_time=models.CharField(max_length=10)
	arrival_date=models.CharField(max_length=20)
	pickup=models.CharField(max_length=40,blank=True,null=True)
	drop=models.CharField(max_length=40,blank=True,null=True)
	departure_mode=models.CharField(max_length=20,blank=True,null=True)
	departure_time=models.CharField(max_length=20,blank=True,null=True)
	departure_date=models.CharField(max_length=20,blank=True,null=True)
	def __unicode__(self):              # __unicode__ on Python 2
		return '%s' % (self.email)
