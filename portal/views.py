from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from portal.models import *
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from portal.forms import *
import string,re
from django.http import HttpResponse
from django.db.models import Q
from django.core.files import File
from django.conf import settings
from django.templatetags.static import static
from django.core import serializers
import json
from django.http import JsonResponse
import os
import hashlib
from datetime import datetime
import requests
import datetime
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from recaptcha.client import captcha
from portal.mailid import *
from el_pagination.decorators import page_template

from django.http import Http404
import time
from django.core.urlresolvers import reverse

#pdf
from reportlab.pdfgen import canvas
#import Image
########
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
# from payu.forms import PayUForm
# from payu.utils import verify_hash
# from portal.forms import OrderForm

#from django.contrib.webdesign.lorem_ipsum import sentence as lorem_ipsum
from uuid import uuid4
from random import randint
import logging


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@login_required
@page_template('portal/story_paginate.html')
@page_template('portal/iitbhu_paginate.html')
def portal_main_page(request,template='portal/forum.html', extra_context=None):
	# Render list page with the documents and the form
	email=request.user
	category=request.user.category
	context_dict={}
	if extra_context is not None:
                context_dict.update(extra_context)
	if category == 'alumni' :
                author_detail=AluminiDetails.objects.get(email=email)
                author_id=author_detail.id
                author_name=author_detail.firstName
        elif category == 'student' :
                author_detail=StudentDetails.objects.get(email=email)
                author_id=author_detail.id
                author_name=author_detail.firstName
        elif category == 'faculty' :
                author_detail=FacultyDetails.objects.get(email=email)
                author_id=author_detail.id
                author_name=author_detail.firstName
	if request.method == 'POST' and request.method:
                        heading_story=request.POST.get("heading_story")
                        content_story=request.POST.get("content_story")
                        date_story=timezone.now()
                        who_posted=email
                        try:
                                x=Question(heading_story=heading_story,content_story=content_story,date_story=date_story,who_posted=who_posted,category=category,author_id=author_id,author_name=author_name)
                                x.full_clean()
                                x.save()
                        except:
                                None
        try:
                Storyinfo=Question.objects.all().order_by("-date_story")
                iitbhu_data=IIT_Activities.objects.all().order_by("-date_time")
        except:
                None
        just_registered=False
        if not request.user.date_joined:
                just_registered=True
                user=MyUser.objects.get(username=email)
                user.date_joined=timezone.now()
                user.save()
        context_dict["just_registered"]=just_registered			
	context_dict["profile_data"]=author_detail
	context_dict["story_data"]=Storyinfo
	context_dict["iit_bhu_data"]=iitbhu_data
    	get_notification(request,context_dict,category)
	return render(request, template, context_dict)
@login_required
def setting_page_data(request):
	email=request.user
	category=request.user.category
	context_dict={}
	context_dict["category"]=category
	try:
                if category == 'alumni':
                        context_dict["profile_data"] = AluminiDetails.objects.get(email=email)
                elif category == 'student':
                        context_dict["profile_data"] = StudentDetails.objects.get(email=email)
                elif category == 'faculty':
                        context_dict["profile_data"] = FacultyDetails.objects.get(email=email)
	except :
		render(request,"portal/error.html")
	get_notification(request,context_dict,category)
	return render_to_response("portal/setting.html",context_dict,context_instance=RequestContext(request))
def verify_page(request,hash):
	try:
		hash_temp=Verification.objects.get(hash_value=hash)
		email=hash_temp.email
		password=hash_temp.password
	except:
		return render(request,"portal/error.html")

	### backend to tell which social auth is being used ###
	backend = []
	if ('backend' in request.GET) and request.GET['backend'].strip():
			backend = request.GET.getlist('backend')
 
	print backend

	if 'backend' in request.GET:
		return render(request, 'portal/form.html', {'hash':hash,'backend': backend[0]})
	else:
		return render(request, 'portal/form.html', {'hash':hash,})
def verify_alumni(request,hash):
	try:
		hash_temp=Verification.objects.get(hash_value=hash)
		email=hash_temp.email
		password=hash_temp.password
	except:
                return render(request,"portal/error.html")

	### backend to tell which social auth is being used ###
	backend = []
	if ('backend' in request.GET) and request.GET['backend'].strip():
			backend = request.GET.getlist('backend')
	else:
			backend="manual" 
	print backend

	if request.method == 'POST':
			### a hidden input field tells which social auth is being used ###
			# backend = []
			# backend.append(request.POST['backend'])
			form = AluminiForm(request.POST)
			addPermanent=AddressForm(request.POST)
			addPresent=AddressFormPresent(request.POST)
		# check whether it's valid:
			if form.is_valid() and addPermanent.is_valid() and addPresent.is_valid():
				# process the data in form.cleaned_data as required
				# ...
				# redirect to a new URL:
				firstname=form.cleaned_data["firstName"]
				lastname=form.cleaned_data["lastName"]
				gender=form.cleaned_data["gender"]
				course=form.cleaned_data["course"]
				degrees=""
				for x in course:
					degrees=degrees+x+"/"    #There will be a forward slash at the end of string.Keep in mind when breaking string by delimiter.It will produce an empty string too.

				dob=form.cleaned_data["dob"]
				addressPermanent=addPermanent.cleaned_data["address"]
				cityPermanent=addPermanent.cleaned_data["city"]
				zipPermanent=addPermanent.cleaned_data["zipCode"]
				statePermanent=addPermanent.cleaned_data["state"]
				countryPermanent=addPermanent.cleaned_data["country"]

				addressPresent=addPresent.cleaned_data["addressPresent"]
				cityPresent=addPresent.cleaned_data["cityPresent"]
				zipPresent=addPresent.cleaned_data["zipCodePresent"]
				statePresent=addPresent.cleaned_data["statePresent"]
				countryPresent=addPresent.cleaned_data["countryPresent"]

				designation=form.cleaned_data["designation"]
				organisation=form.cleaned_data["organisation"]
				branch=form.cleaned_data["branch"]
				mobile=form.cleaned_data["mobile"]
				year=form.cleaned_data["year"]
				if firstname.strip()=="" or lastname.strip()=="" or gender.strip()=="" or degrees.strip()=="" or addressPermanent.strip()=="" or cityPermanent.strip()=="" or zipPermanent.strip()=="" or addressPresent.strip()=="" or cityPresent.strip()=="" or zipPresent.strip()=="" or statePresent.strip()=="" or countryPresent.strip()=="" or statePermanent.strip()=="" or countryPermanent.strip()==""  or branch.strip()=="" or mobile.strip()=="" or year.strip()=="" or organisation.strip()=="" or designation.strip()=="" :
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Fields cannot be left empty",'hash':hash}) 

				if gender=="Male":
					f = open(BASE_DIR+'/static/defaultImage/male.jpg','r')
					# f = open('/media/tanay/7E3BCE16663C8E73/saic/static/defaultImage/male.jpg', 'r')
					photo=File(f)
				elif gender=="Female":
					f = open(BASE_DIR+'/static/defaultImage/female.jpg','r')
					# f = open('/media/tanay/7E3BCE16663C8E73/saic/static/defaultImage/female.jpg', 'r')
					photo=File(f)
                                #Category Checking Whether the User is Alumni or Student or Other
				if not re.match("^[a-zA-Z\s]*$", firstname):                
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Firstname should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", lastname):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Lastname should contain only characters and whitespace",'hash':hash})
                                if not re.match("^[a-zA-Z\s]*$", gender):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Select any one Gender",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", organisation):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Organisation should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", designation):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Designation should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", cityPermanent):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent City should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", cityPresent):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present City should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", statePresent):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present state contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", statePermanent):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent state contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", countryPresent):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present Country should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", countryPermanent):             
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent Country contain only characters and whitespace",'hash':hash})
                                try:
                                        temp=blackList.objects.get(email=email)
                                except:
                                        temp=False
                                if not temp:
                                        x=AluminiDetails(firstName=firstname,lastName=lastname,gender=gender,email=email,address_permanent=addressPermanent,city_permanent=cityPermanent,state_permanent=statePermanent,country_permanent=countryPermanent,zip_permanent=zipPermanent,address_present=addressPresent,city_present=cityPresent,state_present=statePresent,country_present=countryPresent,zip_present=zipPresent,mobile=mobile,course=degrees,branch=branch,year=year,designation=designation,organisation=organisation,dob=dob,photo=photo)
                                else:
                                        return HttpResponse("You Have been blacklisted by the administrator.If you see this message then please contact the web administrator")
				#if not re.match("^[a-zA-Z\s]*$", mothername):               
				#	return render(request, 'portal/form.html',{'form': form,'error':"Mothername should contain only characters and whitespace",'hash':hash})
				#if not re.match("^[a-zA-Z\s]*$", fathername):               
				#	return render(request, 'portal/form.html',{'form': form,'error':"Fathername should contain only characters and whitespace",'hash':hash})
				#if len(mobile)!=10 or not mobile.isdigit():
				#	return render(request, 'portal/form.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Invalid mobile number",'hash':hash})
				
				try:
					x.full_clean()
					x.save()
					#y=Batch(roll_no=Student.objects.get(roll_no=username),year=year,department=department)          
					
					# try:
					if password != "":
						user=MyUser.objects.create_user(username=email,email=email,category='alumni',password=password)
						user.save()        
						userLog=authenticate(username=email, password=password)
						login(request,userLog)
					z=Verification.objects.get(hash_value=hash)
					z.delete()
					if password != "":
						return HttpResponseRedirect('/portal/')
					else:
						backend_url = str(backend[0])
						print backend_url
						return redirect(reverse('social:complete', args=(backend_url,)))
					
					# except:
					# 	return render(request,'portal/success.html')
				except ValidationError:
					return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Database Error",'hash':hash, 'backend': backend[0]})

			else:
				return render(request, 'portal/formalumni.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Invalid Details",'hash':hash, 'backend': backend[0]})


					#return render(request,'portal/success.html')       
				#return render(request, 'portal/form.html',{'form': form,'error':e.message_dict,'hash':hash})
	# if a GET (or any other method) we'll create a blank form
	else:
		form = AluminiForm()
		addPermanent=AddressForm()
		addPresent=AddressFormPresent()

	if 'backend' in request.GET:
		return render(request, 'portal/formalumni.html', {'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'hash':hash,'backend': backend[0]})
	else:
		return render(request, 'portal/formalumni.html', {'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'hash':hash,})

def verify_student(request,hash):
	try:
		hash_temp=Verification.objects.get(hash_value=hash)
		email=hash_temp.email
		password=hash_temp.password
	except:
		return render(request,"portal/error.html")

	### backend to tell which social auth is being used ###
	backend = []
	if ('backend' in request.GET) and request.GET['backend'].strip():
			backend = request.GET.getlist('backend')
 	else:
			backend="manual" 
	print backend

	if request.method == 'POST':
			### a hidden input field tells which social auth is being used ###
			# backend = []
			# backend.append(request.POST['backend'])
			form = StudentForm(request.POST)
			addPermanent=AddressForm(request.POST)
			addPresent=AddressFormPresent(request.POST)
		# check whether it's valid:
			if form.is_valid() and addPermanent.is_valid() and addPresent.is_valid():
				# process the data in form.cleaned_data as required
				# ...
				# redirect to a new URL:
				firstname=form.cleaned_data["firstName"]
				lastname=form.cleaned_data["lastName"]
				gender=form.cleaned_data["gender"]
				course=form.cleaned_data["course"]
				degrees=""
				for x in course:
					degrees=degrees+x+"/"    #There will be a forward slash at the end of string.Keep in mind when breaking string by delimiter.It will produce an empty string too.

				dob=form.cleaned_data["dob"]
				addressPermanent=addPermanent.cleaned_data["address"]
				cityPermanent=addPermanent.cleaned_data["city"]
				zipPermanent=addPermanent.cleaned_data["zipCode"]
				statePermanent=addPermanent.cleaned_data["state"]
				countryPermanent=addPermanent.cleaned_data["country"]

				addressPresent=addPresent.cleaned_data["addressPresent"]
				cityPresent=addPresent.cleaned_data["cityPresent"]
				zipPresent=addPresent.cleaned_data["zipCodePresent"]
				statePresent=addPresent.cleaned_data["statePresent"]
				countryPresent=addPresent.cleaned_data["countryPresent"]
                                roll=form.cleaned_data["roll"]
				branch=form.cleaned_data["branch"]
				mobile=form.cleaned_data["mobile"]
				year=form.cleaned_data["year"]
				if firstname.strip()=="" or lastname.strip()=="" or gender.strip()=="" or degrees.strip()=="" or addressPermanent.strip()=="" or cityPermanent.strip()=="" or zipPermanent.strip()=="" or addressPresent.strip()=="" or cityPresent.strip()=="" or zipPresent.strip()=="" or statePresent.strip()=="" or countryPresent.strip()=="" or statePermanent.strip()=="" or countryPermanent.strip()==""  or branch.strip()=="" or mobile.strip()=="" or year.strip()=="" or roll.strip()=="":
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Fields cannot be left empty",'hash':hash}) 

				if gender=="Male":
					f = open(BASE_DIR+'/static/defaultImage/male.jpg','r')
					# f = open('/media/tanay/7E3BCE16663C8E73/saic/static/defaultImage/male.jpg', 'r')
					photo=File(f)
				elif gender=="Female":
					f = open(BASE_DIR+'/static/defaultImage/female.jpg','r')
					# f = open('/media/tanay/7E3BCE16663C8E73/saic/static/defaultImage/female.jpg', 'r')
					photo=File(f)
                                #Category Checking Whether the User is Alumni or Student or Other
                                if not re.match("^[a-zA-Z\s]*$", firstname):                
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Firstname should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", lastname):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Lastname should contain only characters and whitespace",'hash':hash})
                                if not re.match("^[a-zA-Z\s]*$", gender):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Select any one Gender",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", cityPermanent):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent City should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", cityPresent):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present City should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", statePresent):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present state contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", statePermanent):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent state contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", countryPresent):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present Country should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", countryPermanent):             
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent Country contain only characters and whitespace",'hash':hash})
                                x=StudentDetails(firstName=firstname,lastName=lastname,gender=gender,email=email,address_permanent=addressPermanent,city_permanent=cityPermanent,state_permanent=statePermanent,country_permanent=countryPermanent,zip_permanent=zipPermanent,address_present=addressPresent,city_present=cityPresent,state_present=statePresent,country_present=countryPresent,zip_present=zipPresent,mobile=mobile,course=degrees,branch=branch,year=year,roll=roll,dob=dob,photo=photo)
				try:
					x.full_clean()
					x.save()
					#y=Batch(roll_no=Student.objects.get(roll_no=username),year=year,department=department)          
					
					# try:
					if password != "":
						user=MyUser.objects.create_user(username=email,email=email,category='student',password=password)
						user.save()        
						userLog=authenticate(username=email, password=password)
						login(request,userLog)
					z=Verification.objects.get(hash_value=hash)
					z.delete()
					if password != "":
						return HttpResponseRedirect('/portal/')
					else:
						backend_url = str(backend[0])
						print backend_url
						return redirect(reverse('social:complete', args=(backend_url,)))
					
					# except:
					# 	return render(request,'portal/success.html')
				except ValidationError:
					return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Database Error",'hash':hash, 'backend': backend[0]})

			else:
				return render(request, 'portal/formstudent.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Invalid Details",'hash':hash, 'backend': backend[0]})


					#return render(request,'portal/success.html')       
				#return render(request, 'portal/form.html',{'form': form,'error':e.message_dict,'hash':hash})
	# if a GET (or any other method) we'll create a blank form
	else:
		form = StudentForm()
		addPermanent=AddressForm()
		addPresent=AddressFormPresent()

	if 'backend' in request.GET:
		return render(request, 'portal/formstudent.html', {'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'hash':hash,'backend': backend[0]})
	else:
		return render(request, 'portal/formstudent.html', {'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'hash':hash,})

def verify_faculty(request,hash):
	try:
		hash_temp=Verification.objects.get(hash_value=hash)
		email=hash_temp.email
		password=hash_temp.password
	except:
		return render(request,"portal/error.html")

	### backend to tell which social auth is being used ###
	backend = []
	if ('backend' in request.GET) and request.GET['backend'].strip():
			backend = request.GET.getlist('backend')
 	else:
			backend="manual" 
	print backend

	if request.method == 'POST':
			### a hidden input field tells which social auth is being used ###
			# backend = []
			# backend.append(request.POST['backend'])
			form = FacultyForm(request.POST)
			addPermanent=AddressForm(request.POST)
			addPresent=AddressFormPresent(request.POST)
		# check whether it's valid:
			if form.is_valid() and addPermanent.is_valid() and addPresent.is_valid():
				# process the data in form.cleaned_data as required
				# ...
				# redirect to a new URL:
				firstname=form.cleaned_data["firstName"]
				lastname=form.cleaned_data["lastName"]
				gender=form.cleaned_data["gender"]
				dob=form.cleaned_data["dob"]
				addressPermanent=addPermanent.cleaned_data["address"]
				cityPermanent=addPermanent.cleaned_data["city"]
				zipPermanent=addPermanent.cleaned_data["zipCode"]
				statePermanent=addPermanent.cleaned_data["state"]
				countryPermanent=addPermanent.cleaned_data["country"]
                                designation=form.cleaned_data["designation"]
				addressPresent=addPresent.cleaned_data["addressPresent"]
				cityPresent=addPresent.cleaned_data["cityPresent"]
				zipPresent=addPresent.cleaned_data["zipCodePresent"]
				statePresent=addPresent.cleaned_data["statePresent"]
				countryPresent=addPresent.cleaned_data["countryPresent"]
				branch=form.cleaned_data["branch"]
				mobile=form.cleaned_data["mobile"]
				year=form.cleaned_data["year"]
				if firstname.strip()=="" or lastname.strip()=="" or gender.strip()=="" or addressPermanent.strip()=="" or cityPermanent.strip()=="" or zipPermanent.strip()=="" or addressPresent.strip()=="" or cityPresent.strip()=="" or zipPresent.strip()=="" or statePresent.strip()=="" or countryPresent.strip()=="" or statePermanent.strip()=="" or countryPermanent.strip()==""  or branch.strip()=="" or mobile.strip()=="" or year.strip()=="" or designation.strip()=="":
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Fields cannot be left empty",'hash':hash}) 

				if gender=="Male":
					f = open(BASE_DIR+'/static/defaultImage/male.jpg','r')
					# f = open('/media/tanay/7E3BCE16663C8E73/saic/static/defaultImage/male.jpg', 'r')
					photo=File(f)
				elif gender=="Female":
					f = open(BASE_DIR+'/static/defaultImage/female.jpg','r')
					# f = open('/media/tanay/7E3BCE16663C8E73/saic/static/defaultImage/female.jpg', 'r')
					photo=File(f)
                                #Category Checking Whether the User is Alumni or Student or Other
				if not re.match("^[a-zA-Z\s]*$", firstname):                
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Firstname should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", lastname):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Lastname should contain only characters and whitespace",'hash':hash})
                                if not re.match("^[a-zA-Z\s]*$", gender):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Select any one Gender",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", designation):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Designation should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", cityPermanent):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent City should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", cityPresent):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present City should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", statePresent):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present state contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", statePermanent):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent state contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", countryPresent):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Present Country should contain only characters and whitespace",'hash':hash})
				if not re.match("^[a-zA-Z\s]*$", countryPermanent):             
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Permanent Country contain only characters and whitespace",'hash':hash})
				x=FacultyDetails(firstName=firstname,lastName=lastname,gender=gender,email=email,address_permanent=addressPermanent,city_permanent=cityPermanent,state_permanent=statePermanent,country_permanent=countryPermanent,zip_permanent=zipPermanent,address_present=addressPresent,city_present=cityPresent,state_present=statePresent,country_present=countryPresent,zip_present=zipPresent,mobile=mobile,branch=branch,year=year,designation=designation,dob=dob,photo=photo)
				try:
					x.full_clean()
					x.save()
					#y=Batch(roll_no=Student.objects.get(roll_no=username),year=year,department=department)          
					
					# try:
					if password != "":
						user=MyUser.objects.create_user(username=email,email=email,category='faculty',password=password)
						user.save()        
						userLog=authenticate(username=email, password=password)
						login(request,userLog)
					z=Verification.objects.get(hash_value=hash)
					z.delete()
					if password != "":
						return HttpResponseRedirect('/portal/')
					else:
						backend_url = str(backend[0])
						print backend_url
						return redirect(reverse('social:complete', args=(backend_url,)))
					
					# except:
					# 	return render(request,'portal/success.html')
				except ValidationError:
					return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Database Error",'hash':hash, 'backend': backend[0]})

			else:
				return render(request, 'portal/formfaculty.html',{'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'error':"Invalid Details",'hash':hash, 'backend': backend[0]})


					#return render(request,'portal/success.html')       
				#return render(request, 'portal/form.html',{'form': form,'error':e.message_dict,'hash':hash})
	# if a GET (or any other method) we'll create a blank form
	else:
		form = FacultyForm()
		addPermanent=AddressForm()
		addPresent=AddressFormPresent()

	if 'backend' in request.GET:
		return render(request, 'portal/formfaculty.html', {'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'hash':hash,'backend': backend[0]})
	else:
		return render(request, 'portal/formfaculty.html', {'form': form,'formAddPermanent':addPermanent,'formAddPresent':addPresent,'hash':hash,})
@login_required
@page_template('portal/profile_story_paginate.html')
def profile_page(request,template='portal/profile.html',extra_context=None):
		#Get the context from the request
		email=request.user
                category=request.user.category
                context_dict={}
                context_dict["profile_edit_success"]=False
                interest_post_success=False
		if category == 'alumni' :
                        p = AluminiDetails.objects.get(email=email)
                elif category == 'student' :
                        p = StudentDetails.objects.get(email=email)
                elif category == 'faculty' :
                        p=FacultyDetails.objects.get(email=email)
                # Code Below is to recieve Edit Profile Code
		if request.method == 'POST' and request.method and "editprofile_form" in request.POST:
                        try:
				p.firstName=request.POST.get('profilefirstName')
				p.lastName=request.POST.get('profilelastName')
				p.gender=request.POST.get('profileGender')
				if category  == 'student' or category == 'alumni':
                                        p.year=request.POST.get('profileBatch')
                                        p.roll=request.POST.get('profileRoll')
                                        p.course=request.POST.get('profileCourse')
				p.branch=request.POST.get('profileBranch')				
				if category == 'alumni':
                                        p.organisation=request.POST.get('profileCurrent')
                                if category == 'alumni' or category == 'faculty':
                                        p.designation=request.POST.get('profileDesignation')
				p.address_present=request.POST.get('profileCAddress')
				p.city_present=request.POST.get('profileCCity')
				p.state_present=request.POST.get('profileCState')
				p.zip_present=request.POST.get('profileCZip')
				p.country_present=request.POST.get('profileCCountry')
				p.address_permanent=request.POST.get('profilePAddress')
				p.city_permanent=request.POST.get('profilePCity')
				p.state_permanent=request.POST.get('profilePState')
				p.zip_permanent=request.POST.get('profilePZip')
				p.country_permanent=request.POST.get('profilePCountry')
				p.mobile=request.POST.get('profileMobile')
				p.year=request.POST.get('profileBatch')
				p.save()
				context_dict["profile_edit_success"]=True
			except:
				context_dict["profile_edit_success"]=False
		#COde Below is to submit an interest i.e. post an interest
		if request.method == 'POST' and request.method and "interestpost_form" in request.POST:
                        heading_interest=request.POST.get("heading_interest")
                        content_interest=request.POST.get("content_interest")
                        date_interest=timezone.now()
                        who_posted=email
                        try:
                                x=Interest(heading_interest=heading_interest,content_interest=content_interest,date_interest=date_interest,who_posted=who_posted)
                                x.full_clean()
                                x.save()
                                context_dict["interest_post_success"]=True
                        except:
                                context_dict["interest_post_success"]=False
                                None    
                #Code For interest Post ends
                #Code Below is to generate Information and context dictionaries
		try:
			if category == 'alumni':
                                Profinfo=AluminiDetails.objects.get(email=email)
                        elif category == 'student':
                                Profinfo=StudentDetails.objects.get(email=email)
                        elif category == 'faculty':
                                Profinfo=FacultyDetails.objects.get(email=email)
		except :
			Profinfo=None
			return render(request,"portal/error.html")
		try:
                        story_data=Question.objects.filter(who_posted=email).order_by("-date_story")
                        interest_data=Interest.objects.filter(who_posted=email).order_by("-date_interest")
                        context_dict["story_data"]=story_data
                        context_dict["interest_data"]=interest_data
                except:
                        None
                upload_form=DocumentForm()
                get_notification(request,context_dict,category)
                context_dict["profile_data"]=Profinfo
                context_dict["category"]=category
                context_dict["delete_success"]=False
                context_dict["upload_form"]=upload_form
                if extra_context is not None:
                        context_dict.update(extra_context)
		return render_to_response(template,context_dict,context_instance=RequestContext(request))
@login_required
def photo(request):
		#Get the context from the request
	email=request.user
	category=request.user.category
	files_list=set([".jpg", ".jpeg", ".png",])
	# Handle file upload
	context_dict={}
	if request.method=="POST":
		form = DocumentForm(request.POST, request.FILES)
		c=0
		
		if form.is_valid():
                        if category == 'alumni' :
                                user=AluminiDetails.objects.get(email=request.user)
                        elif category == 'student' :
                                user=StudentDetails.objects.get(email=request.user)
                        elif category == 'faculty' :
                                user=FacultyDetails.objects.get(email=request.user)
			temp=request.FILES['photo']
			for word in files_list:
				if word in temp.name.lower():
					if temp.size<=5242880:
						deleteTemp=user.photo.path
						user.photo=temp
						user.save()
						os.remove(deleteTemp)
						c=1
						context_dict["status"]="success"
						context_dict["image_url"]=user.photo.url         
						return JsonResponse(context_dict)
						
					else:
						c=2	
						temp=""
						
					break
			if c==0:
				context_dict["status"]="failure"
				context_dict["error"]="Invalid File Format"
				return JsonResponse(context_dict)	
			elif c==2:
				context_dict["status"]="failure"
				context_dict["error"]="Image should be less than 5 Mb"
				return JsonResponse(context_dict)		
		
	
	else:
		return render_to_response("portal/failed_verify.html",context_dict,context_instance=RequestContext(request))
@login_required	
def deletePhoto(request):
	# Handle file upload
	category=request.user.category
	if request.method=="GET":
	#	try:
                if category == 'alumni' :
                        user=AluminiDetails.objects.get(email=MyUser.objects.get(username=request.user))
                elif category == 'student' :
                        user=StudentDetails.objects.get(email=MyUser.objects.get(username=request.user))
                elif category == 'faculty' :
                        user=FacultyDetails.objects.get(email=MyUser.objects.get(username=request.user))
		if user.gender=="Male":
			f = open('/var/www/saic/SAIC/static/defaultImage/male.jpg', 'r')
			photo=File(f)
		elif user.gender=="Female":
			f = open('/var/www/saic/SAIC/static/defaultImage/female.jpg', 'r')
			photo=File(f)
		os.remove(user.photo.path)
        user.photo=photo
        user.save()
        return HttpResponse("success")
    
@login_required
def setting_page(request):
		#Get the context from the request
	context_instance=RequestContext(request)
	email=request.user
	category=request.user.category
	context_dict={}
	try:
                if category == 'alumni':
                        Privinfo=AluminiDetails.objects.get(email=email)
                elif category == 'student':
                        Privinfo=StudentDetails.objects.get(email=email)
                elif category == 'faculty':
                        Privinfo=FacultyDetails.objects.get(email=email)
                else:
                        Privinfo=None
                #Hello
		if request.method and request.method == 'POST':
			Privinfo.privacy_PAddress=request.POST.get("privacy_paddress")
			Privinfo.privacy_CAddress=request.POST.get("privacy_caddress")
			Privinfo.privacy_Email=request.POST.get("privacy_email")
			Privinfo.privacy_Mobile=request.POST.get("privacy_mobile")
			Privinfo.save()                  
	except :
		Privinfo=None
		return render(request,"portal/error.html")
	get_notification(request,context_dict,category)
	context_dict["profile_data"]=Privinfo
	context_dict["category"]=category
	return render_to_response("portal/setting.html",context_dict,context_instance)	
@login_required
def search_page(request):
	context_dict={}
	yearRangeLow=1920
	yearRangeHigh=2020
	category=request.user.category
	try:
                if category == 'alumni':
                        context_dict["profile_data"]=AluminiDetails.objects.get(email=request.user)
                elif category == 'student':
                        context_dict["profile_data"]=StudentDetails.objects.get(email=request.user)
                elif category == 'faculty':
                        context_dict["profile_data"]=FacultyDetails.objects.get(email=request.user)
        except:
                render(request,"portal/error.html")
	if request.method=="POST":
		form = searchForm(request.POST)
		c=0
		
		if form.is_valid():
			firstName=form.cleaned_data["search_byName"]
			year=form.cleaned_data["search_byYear"]
			branch=form.cleaned_data["search_byDepartment"]
			if not year and not branch and not firstName:
                                return render(request,"portal/search.html",{'search_form':form,'error':"Input atleast one Search Field",'category_to_check_mentorship':category,"profile_data":context_dict["profile_data"]})
                                
			nameList=[]
			context_dict["year"]=year
			checkParameters={}
			search_results_alumni=None
			search_results_student=None
			search_results_faculty=None
			query=Q()
			if year:
                                query &=Q(year__icontains=year)
                        if firstName:
                                query &=Q(firstName__icontains=firstName)
                        if branch:
                                query &=Q(branch__icontains=branch)
                        search_results_alumni=AluminiDetails.objects.filter(query).order_by("firstName")
                        search_results_student=StudentDetails.objects.filter(query).order_by("firstName")
                        search_results_faculty=FacultyDetails.objects.filter(query).order_by("firstName")
			context_dict["search_results_alumni"]=search_results_alumni
			context_dict["search_results_faculty"]=search_results_faculty
			context_dict["search_results_student"]=search_results_student
			count_alumni=0
			count_student=0
			count_faculty=0
			for alumni in search_results_alumni:
                                count_alumni+=1
                        for student in search_results_student:
                                count_student+=1
                        for faculty in search_results_faculty:
                                count_faculty+=1                        
                        context_dict["count_alumni"]=count_alumni
                        context_dict["count_student"]=count_student
                        context_dict["count_faculty"]=count_faculty
                        context_dict["count_total"]=count_alumni+count_student+count_faculty
                        # Following Block of code is for gettingthe Search results id
                        context_dict["alumni_id"]={}
                        context_dict["student_id"]={}
                        context_dict["faculty_id"]={}
                                               
		else:
			context_dict["error"]=form.errors
		context_dict["search_form"]=form
		#context_dict["broadcasts"]=broadcast
                get_notification(request,context_dict,category)
		return render_to_response("portal/search.html",context_dict,context_instance=RequestContext(request))
	else:
		search_form=searchForm()
		context_dict["search_form"]=search_form
	get_notification(request,context_dict,category)
	return render_to_response("portal/search.html",context_dict,context_instance=RequestContext(request))
@login_required
@page_template('portal/profile_story_paginate.html')
def user_detail(request,userid,categorypass,template="portal/profiledisplay.html",extra_context=None):
        email=request.user
        #category_current_user is for the user being searched
        category_current_user=request.user.category
        context_dict={}
        try:
                if categorypass == 'alumni':
                        userinfo=AluminiDetails.objects.get(id=userid)
                        category_searched="alumni"
                        context_dict["profilesearch"] = AluminiDetails.objects.get(email=userinfo.email)
                elif categorypass == 'student':
                        userinfo=StudentDetails.objects.get(id=userid)
                        category_searched="student"
                        context_dict["profilesearch"] = StudentDetails.objects.get(email=userinfo.email)
                elif categorypass == 'faculty':
                        userinfo=FacultyDetails.objects.get(id=userid)
                        category_searched="faculty"
                        context_dict["profilesearch"] = FacultyDetails.objects.get(email=userinfo.email)
        except:
                return render(request,"portal/error.html")
        if userinfo.email == request.user.email and category_searched == request.user.category :
                return HttpResponseRedirect("../../../../portal/profile")
        else:
                #category is for the user being searched
                context_dict["category_current_user"]=category_current_user
                context_dict["categorysearch"]=category_searched
                try:
                        if category_current_user == 'alumni':
                                context_dict["profile_data"]=AluminiDetails.objects.get(email=request.user)
                        elif category_current_user == 'student':
                                context_dict["profile_data"]=StudentDetails.objects.get(email=request.user)
                        elif category_current_user == 'faculty':
                                context_dict["profile_data"]=FacultyDetails.objects.get(email=request.user)
                except:
                        return render(request,"portal/error.html")
                try:
                        tmp_request=RequestForContact.objects.get(whom_requested=userinfo.email,who_requested=request.user)
                        context_dict["contacts_data"]=tmp_request
                except:
                        tmp_request=None
                context_dict["story_data"]=Question.objects.filter(who_posted=userinfo.email)
                context_dict["interest_data"]=Interest.objects.filter(who_posted=userinfo.email).order_by("-date_interest")
                context_dict["story_data"]=Question.objects.filter(who_posted=userinfo.email).order_by("-date_story")
                context_dict["profile_edit_success"]=False
                context_dict["upload_form"]=DocumentForm()
                context_dict["delete_success"]=False
                get_notification(request,context_dict,category_current_user)
                if extra_context is not None:
                        context_dict.update(extra_context)
                return render(request, template,context_dict)
@login_required
def delete_interest(request,interestid):
        email=request.user
        category=request.user.category
        context_dict={}
        context_dict["delete_success"]=False
        context_dict["story_data"]=Question.objects.filter(who_posted=email).order_by("-date_story")
        try:
                content_to_delete=Interest.objects.get(id=interestid)
                content_to_delete.delete()
                context_dict["delete_success"]=True
        except:
                context_dict["delete_success"]=False
                None  
        context_dict["interest_data"]=Interest.objects.filter(who_posted=email).order_by("-date_interest")
        context_dict["category"]=category
        if category == 'alumni' :
                context_dict["profile_data"] = AluminiDetails.objects.get(email=email)
        elif category == 'student' :
                context_dict["profile_data"] = StudentDetails.objects.get(email=email)
        elif category == 'faculty' :
                context_dict["profile_data"]=FacultyDetails.objects.get(email=email)
        upload_form=DocumentForm()
        context_dict["upload_form"]=DocumentForm()
        get_notification(request,context_dict,category)
	return render_to_response("portal/profile.html",context_dict,context_instance=RequestContext(request))        
@login_required
def guestHouse_page(request):
	context_dict={}
	category=request.user.category
	get_notification(request,context_dict,category)
	if request.method=="POST":
		form=guestHouse(request.POST)
		context_dict["form"]=form
		if form.is_valid():
                 
				#url = "https://www.google.com/recaptcha/api/siteverify"
				#params = {'secret': settings.RECAPTCHA_SECRET_KEY,'response': request.POST.get('g-recaptcha-response'),'remoteip': request.META['REMOTE_ADDR']}
				#verify_rs = requests.get(url, params=params, verify=True)
				#verify_rs = verify_rs.json()
				#response={}
				#response["status"] = verify_rs.get("success", False)
				#response['message'] = verify_rs.get('error-codes', None) or "Unspecified error."
				#return HttpRespon
				response = captcha.submit(request.POST.get('recaptcha_challenge_field'),request.POST.get('recaptcha_response_field'),settings.RECAPTCHA_SECRET_KEY,request.META['REMOTE_ADDR'],)
				if response.is_valid:
					rooms=form.cleaned_data["no_of_rooms"]
					attendees=form.cleaned_data["no_of_attendees"]
					sDate=form.cleaned_data["date_start"]
					eDate=form.cleaned_data["date_end"]
					mobile=form.cleaned_data["mobile"]
					#date_start=datetime.datetime.strptime(sDate , '%Y-%d-%m')
					#date_end=datetime.datetime.strptime(eDate , '%Y-%d-%m')
					comments=form.cleaned_data["comments"]
					if eDate < sDate:
                                                msg = u"Check-Out date should be greater than Check-In date."
                                                context_dict["errors"] = msg
                                                return render_to_response("portal/guestHouse.html",context_dict,context_instance=RequestContext(request))
					try:
                                                x=GuestHouse(email=request.user,rooms=rooms,attendees=attendees,date_start=sDate,date_end=eDate,comments=comments,mobile=mobile)
                                                x.full_clean()
                                                x.save()
                                                context_dict["successBooking"]="1"
                                                try:	
                                                        message="Thank you for choosing to stay with us.\n\nYour request is being currently processed.\nOur team will get back to you with confirmation shortly."
                                                        send_mail('Guest House Booking',message,SUPPORT_TEAM,[request.user],fail_silently=False)
                                                        message_team="Details:\n"+"No. of rooms: "+ str(rooms)+"\nNo. of guests: "+ str(attendees)+"\nCheck In Date: " +str(sDate)+"\nCheckout Date: " +str(eDate)+"\nComments: "+comments+"\nMobile: " +str(mobile)  
                                                        send_mail('Guest House Booking',message_team,SUPPORT_TEAM,[CORE_TEAM_1],fail_silently=False)
                                                except ValidationError,e:
                                                        context_dict["error"]=e.message_dict
                                                return render_to_response("portal/guestHouse.html",context_dict,context_instance=RequestContext(request))
					except:
                                                context_dict["errors"]="Database Format Error"
					#context_dict["date"]=sDate
					return render_to_response("portal/guestHouse.html",context_dict,context_instance=RequestContext(request))
				else:
					context_dict["errors"]="Try right captcha"
					return render_to_response("portal/guestHouse.html",context_dict,context_instance=RequestContext(request))
	
				context_dict["errors"]="Please check your internet connection"
				return render_to_response("portal/guestHouse.html",context_dict,context_instance=RequestContext(request))
			
		else:
			context_dict["errors"]=form.errors
			return render_to_response("portal/guestHouse.html",context_dict,context_instance=RequestContext(request))


	else:
		form=guestHouse()
		context_dict["form"]=form

	return render_to_response("portal/guestHouse.html",context_dict,context_instance=RequestContext(request))        
@login_required
def requestcontact(request,category,contacttype,userid):
        emailrequester=request.user.email
        categoryrequester=request.user.category
        categoryrequest=category
        typerequest=contacttype
        idrequest=userid
        if categoryrequest == 'alumni':
                        tmp=AluminiDetails.objects.get(id=idrequest)
        elif categoryrequest == 'student':
                        tmp=StudentDetails.objects.get(id=idrequest)
        elif categoryrequest == 'faculty':
                        tmp=FacultyDetails.objects.get(id=idrequest)
        if typerequest == '0':
                try:
                        tmpcheck=RequestForContact.objects.get(who_requested=emailrequester,whom_requested=tmp.email)
                        tmpcheck.email_requested='requested'
                        tmpcheck.date_request=timezone.now()
                        tmpcheck.save()
                except:
                        p=RequestForContact(who_requested=emailrequester,requestercategory=categoryrequester,requestedcategory=categoryrequest,whom_requested=tmp.email,email_requested='requested')                    
                        p.save()
        elif typerequest == '1':
                try:
                        tmpcheck=RequestForContact.objects.get(who_requested=emailrequester,whom_requested=tmp.email)
                        tmpcheck.mobile_requested='requested'
                        tmpcheck.date_request=timezone.now()
                        tmpcheck.save()
                except:
                        p=RequestForContact(who_requested=emailrequester,requestercategory=categoryrequester,requestedcategory=categoryrequest,whom_requested=tmp.email,mobile_requested='requested')                    
                        p.save()
        return HttpResponseRedirect("../../../../../portal/user_detail/"+idrequest+"/"+categoryrequest+"/")
@login_required
def get_notification(request,context_dict,category):
        if category == 'alumni' :
                lastactivity=AluminiDetails.objects.get(email=request.user)
                
        elif category == 'student' :
                lastactivity=StudentDetails.objects.get(email=request.user)
        elif category == 'faculty' :
                lastactivity=FacultyDetails.objects.get(email=request.user)
        context_dict["profile_data"]=lastactivity
        total_count=0
        try:
                #FOllowing checks for the confirmed requests only and sends them as a deictionary, This block was for if no one requested and also to send all requests
                confirm="requested"
                query=Q(email_requested=confirm)|Q(mobile_requested=confirm)
                tmp=RequestForContact.objects.filter(query,whom_requested=request.user,requestedcategory=category)
                context_dict["contact_requests"]=tmp
                context_dict["count_request"]=tmp.count()
                total_count+=tmp.count()
        except:
                tmp=None
        #Following is for general notifications
        try:
                gen_temp=GeneralNotifications.objects.filter(who_requested=request.user).order_by("date_response")
                gen_query=Q(notification_type="requestemail")|Q(notification_type="requestmobile")
                gen_request_notifications_new=GeneralNotifications.objects.filter(gen_query,who_requested=request.user,date_response__gte=lastactivity.last_activity).order_by("date_response")
                gen_request_notifications_old=GeneralNotifications.objects.filter(gen_query,who_requested=request.user,date_response__lte=lastactivity.last_activity).order_by("date_response")
                context_dict["contact_requests_response_new"]=gen_request_notifications_new
                context_dict["contact_requests_response_old"]=gen_request_notifications_old
                context_dict["count_gen_request"]=gen_request_notifications_new.count()
                total_count+=gen_request_notifications_new.count()
        except:
                gen_temp=None
        #Following is to send broadcast messages
        current_time=timezone.now()
        try:
                broadcast=Broadcast.objects.filter(date_broadcast__gte=lastactivity.last_activity).order_by("-date_broadcast")
                broadcast_old=Broadcast.objects.filter(date_broadcast__lte=lastactivity.last_activity).order_by("-date_broadcast")
                context_dict["broadcasts"]=broadcast
                context_dict["broadcasts_old"]=broadcast_old
                context_dict["count_broadcast"]=broadcast.count()
                total_count+=broadcast.count()
        except:
                broadcast=None
        context_dict["category_to_check_mentorship"]= category
        context_dict["total_count_notification"]=total_count    
	return
def notification_read(request):
        category=request.user.category
        context_dict={}
        if category == 'alumni' :
                lastactivity=AluminiDetails.objects.get(email=request.user)
        elif category == 'student' :
                lastactivity=StudentDetails.objects.get(email=request.user)
        elif category == 'faculty' :
                lastactivity=FacultyDetails.objects.get(email=request.user)
        context_dict["profile_data"]=lastactivity
        try:
                #FOllowing checks for the confirmed requests only and sends them as a deictionary, This block was for if no one requested and also to send all requests
                confirm="requested"
                query=Q(email_requested=confirm)|Q(mobile_requested=confirm)
                tmp=RequestForContact.objects.filter(query,whom_requested=request.user,requestedcategory=category)
                context_dict["contact_requests"]=tmp
                context_dict["count_request"]=tmp.count()
        except:
                tmp=None
        #Following is for general notifications
        try:
                gen_temp=GeneralNotifications.objects.filter(who_requested=request.user).order_by("date_response")
                gen_query=Q(notification_type="requestemail")|Q(notification_type="requestmobile")
                gen_request_notifications_new=GeneralNotifications.objects.filter(gen_query,who_requested=request.user,date_response__gte=lastactivity.last_activity).order_by("date_response")
                gen_request_notifications_old=GeneralNotifications.objects.filter(gen_query,who_requested=request.user,date_response__lte=lastactivity.last_activity).order_by("date_response")
                context_dict["contact_requests_response_new"]=gen_request_notifications_new
                context_dict["contact_requests_response_old"]=gen_request_notifications_old
                context_dict["count_gen_request"]=gen_request_notifications_new.count()
        except:
                gen_temp=None
        #Following is to send broadcast messages
        current_time=timezone.now()
        try:
                broadcast=Broadcast.objects.filter(date_broadcast__gte=lastactivity.last_activity).order_by("-date_broadcast")
                broadcast_old=Broadcast.objects.filter(date_broadcast__lte=lastactivity.last_activity).order_by("-date_broadcast")
                context_dict["broadcasts"]=broadcast
                context_dict["broadcasts_old"]=broadcast_old
                context_dict["count_broadcast"]=broadcast.count()
                #since all notifications being displayed, therefore setting count_broadcast=0
                lastactivity.last_activity=current_time
                lastactivity.save()
        except:
                broadcast=None
        context_dict["category_to_check_mentorship"]= category
        return render_to_response("portal/notification.html",context_dict,context_instance=RequestContext(request))
@login_required
def request_update(request,reqtype,reqid,reqresponse):
        # reqtpe is whether user has responded to email request or mobile request i.e. reqtype=0 for email and reqtype=1 for mobile
        # reqresponse is whether user has accepted the request or not.. i.e. 2 for accept , 3 for decline , 1 for still pending
        #reqid is the id of the queryset being executed from the requestcontact model class
        email=request.user
	category=request.user.category	
	context_dict={}
        request_type=reqtype
        response=reqresponse
        request_id=reqid
        try:
                temp_obj=RequestForContact.objects.get(id=request_id)
                #four lines below are for general notifications
                gen_who_requested=temp_obj.who_requested
                gen_whom_requested=temp_obj.whom_requested
                gen_requestercategory=temp_obj.requestercategory
                gen_requestedcategory=temp_obj.requestedcategory
                gen_date_response=timezone.now()
                if request_type == '0':
                        #this is for email request responses
                        if response == 'accepted':
                                #This means the request for email has been accepted
                                temp_obj.email_requested = 'accepted'
                                temp_obj.save()
                                #General Notifcation Block Starts
                                gen_noti_type="requestemail"
                                gen_noti_content="Accepted your request for email."
                                #General Notification Block Ends
                        elif response == 'declined':
                                #This means the request for email has been rejected
                                temp_obj.email_requested = 'notrequested'
                                temp_obj.save()
                                #General Notifcation Block Starts
                                gen_noti_type="requestemail"
                                gen_noti_content="Declined your request for email."
                                #General Notification Block Ends
                elif request_type == '1':
                        #this is for email request responses
                        if response == 'accepted':
                                #This means the request for email has been accepted
                                temp_obj.mobile_requested = 'accepted'
                                temp_obj.save()
                                #General Notifcation Block Starts
                                gen_noti_type="requestmobile"
                                gen_noti_content="Accepted your request for mobile."
                                #General Notification Block Ends
                        elif response == 'declined':
                                #This means the request for email has been rejected
                                temp_obj.mobile_requested= 'notrequested'
                                temp_obj.save()
                                #General Notifcation Block Starts
                                gen_noti_type="requestmobile"
                                gen_noti_content="Declined your request for mobile."
                                #General Notification Block Ends
                else:
                        return render(request,"portal/error.html")
                try:
                        x=GeneralNotifications(who_requested=gen_who_requested,whom_requested=gen_whom_requested,requestercategory=gen_requestercategory,requestedcategory=gen_requestedcategory,notification_type=gen_noti_type,notification_content=gen_noti_content,date_response=gen_date_response)
                        x.save()
                except:
                        return render(request,"portal/error.html")
        except:
                return render(request,"portal/error.html")
        return HttpResponseRedirect("../../../../../portal/notification_read/")
def contactUs(request):
        category=request.user.category
        context_dict={}
        if request.POST and request.method == "POST" and "contact_form" in request.POST:
                try:
                        subject_contact=request.POST.get('subject_contact')
                        message_contact=request.POST.get('message_contact')
                        message_contact=message_contact+"\nSent by:"+str(request.user)
                        try:	
                                send_mail(subject_contact,message_contact,SUPPORT_TEAM,[SUPPORT_TEAM_1],fail_silently=False)
                                context_dict["success_mail"]='1'
                                context_dict["send_error"]='0'
                        except:
                                context_dict["success_mail"]='0'
                                context_dict["send_error"]='1'
                except:
                        context_dict["success_mail"]='0'
                        context_dict["send_error"]='1'
        get_notification(request,context_dict,category)
        return render_to_response("portal/contactus.html",context_dict,context_instance=RequestContext(request))
def mentor_response(request):
        category=request.user.category
        context_dict={}
        contact=""
        if category=="student":
                contact="alumnus/alumna"
        else:
                contact="student"
        context_dict["category"]=category
        salutation=category.capitalize()
        messageAlumnus="Dear "+"Alumnus/Alumna"+"\nThank you for being a part of Student Alumni Mentorship Programme.\n\nWe are currently matching your field of expertise against the respective students. You will hear from us as soon as the process is completed.\nHope that you will have fruitful interaction with the "+contact+"."
        messageStudent="Dear "+"Alumnus/Alumna"+"\nThank you for being a part of Student Alumni Mentorship Programme.\n\nWe are currently matching your areas of interest against the respective alumni. You will hear from us as soon as the process is completed.\nHope that you will have fruitful interaction with the "+contact+"."           
        get_notification(request,context_dict,category)
        #Alumni Response Recorder
        if request.POST and request.method == "POST" and "alumni_mentor_form" in request.POST:
                        mentor_max=request.POST.get('mentor_max')
                        areas_mentor=request.POST.getlist('areas_mentor')
                        #otherValue="others : "+request.POST.get('others_check')
                        #areas_mentor.append(otherValue)
                        #context_dict["areas"]=areas_mentor
                        #return render_to_response("portal/mentorship.html",context_dict,context_instance=RequestContext(request))
                        if areas_mentor == None or len(areas_mentor)==0:
                                context_dict["errors"]="Selest atleast one area of interest"
                                return render_to_response('portal/mentorship.html',context_dict,context_instance=RequestContext(request))
                        try:
                                p1=AsmpAlumniResponse.objects.get(email=request.user)
                                p1.mentor_max=mentor_max
                                p1.areas_mentor=areas_mentor
                                p1.last_response_date=timezone.now()
                                p1.save()
                        except:
                                p1=AsmpAlumniResponse(mentor_max=mentor_max,areas_mentor=areas_mentor,email=request.user,last_response_date=timezone.now())
                                p1.save()
			ASMP_ALUMNI_MAIL="Hey,I " + str(request.user) + " am willing to opt for the mentorship form.\n\nDetails:\n" + "Max No. of students opted: " + str(mentor_max) + "\nAreas of Interest: " + str(areas_mentor) + '\nThankyou'
			send_mail("Student Alumni Mentorship Programme",ASMP_ALUMNI_MAIL,SUPPORT_TEAM,[CORE_TEAM_1,CORE_TEAM_2,CORE_TEAM_3],fail_silently=False)
                        send_mail("Student Alumni Mentorship Programme",messageAlumnus,SUPPORT_TEAM,[request.user],fail_silently=False)

                        context_dict["success_mail"]='success'
                        context_dict["send_error"]='0'
        #Student Response Recorder
        if request.POST and request.method == "POST" and "student_mentor_form" in request.POST:
                        context_dict["error"]="Initiated"
                        career_interest_pref_1=request.POST.get('career_interest_pref_1')
                        career_interest_pref_2=request.POST.get('career_interest_pref_2')
                        guidance_type=request.POST.get('guidance_type')
                        try:
                                #context_dict["error"]="Try Block"
                                if request.POST.get('career_interest_other_pref_1'):
                                       career_interest_pref_1=request.POST.get('career_interest_other_pref_1')
                                #context_dict["error"]="Try Block 2"
                                if request.POST.get('career_interest_other_pref_2'):
                                       career_interest_pref_2=request.POST.get('career_interest_other_pref_2')
                        except:
                                pass
                        career_interest=career_interest_pref_1+","+career_interest_pref_2
                        try:
                                #context_dict["error"]="Try Block 3"
                                #if Response already Exists
                                p=AsmpStudentResponse.objects.get(email=request.user)
                                p.career_interest=career_interest
                                p.guidance_type=guidance_type
                                p.last_response=timezone.now()
                                p.save()
                                context_dict["success_mail"]='success'
                                context_dict["send_error"]='0'
                        except:
                                #context_dict["error"]="Except"
                                #if Responded for the first Time
                                q=AsmpStudentResponse(email=request.user,career_interest=career_interest,guidance_type=guidance_type,last_response=timezone.now())
                                q.save()
                                context_dict["success_mail"]='success'
                                context_dict["send_error"]='0'
                        ASMP_STUDENT_MAIL="Hey,I " + str(request.user) + " am willing to opt for the mentorship form.\n\nDetails:\n" + "Career Interest: " + str(career_interest) + "\nGuidance Type: " + str(guidance_type) + '\nThankyou'
			send_mail("Student Alumni Mentorship Programme",ASMP_STUDENT_MAIL,SUPPORT_TEAM,[CORE_TEAM_1,CORE_TEAM_2,CORE_TEAM_3],fail_silently=False)
                        send_mail("Student Alumni Mentorship Programme",messageStudent,SUPPORT_TEAM,[request.user],fail_silently=False)

        get_notification(request,context_dict,category)
        return render_to_response("portal/mentorship.html",context_dict,context_instance=RequestContext(request))

def pass_change(request,hash):
	
	try:
		hash_temp=Verification.objects.get(hash_value=hash)
		
		email=hash_temp.email
		password=hash_temp.password
	except:
	
		return render(request,'portal/error.html')
	if request.method == 'POST':
		form = PassRecoveryForm(request.POST)
		if form.is_valid():
			Pass=form.cleaned_data["password"]
			PassC=form.cleaned_data["passwordC"]
			if Pass==PassC:
				if len(Pass)>=8:

					try:
						x=MyUser.objects.get(username=email)
						x.set_password(Pass)
						x.save()
						hash_temp.delete()
						
						return render(request, 'portal/pass_success.html')
					except:
						return render(request, 'portal/pass_recovery.html', {'form': form,'hash':hash,'error':"Error in connection"})
				else:
					return render(request, 'portal/pass_recovery.html', {'form': form,'hash':hash,'error':"Password should be greater than 8 characters"})      
			else:
				return render(request, 'portal/pass_recovery.html', {'form': form,'hash':hash,'error':"Password Doesnot match"})
	else:
		form = PassRecoveryForm()
	return render(request, 'portal/pass_recovery.html', {'form': form,'hash':hash})
      
				
logger = logging.getLogger('django')
loggerPay = logging.getLogger('payment.log')
loggerCheckout=logging.getLogger('checkout.log')
def checkout(request):
	if request.method == 'POST':

		try:
			userDetails=AluminiDetails.objects.get(email=request.user)
			if userDetails.register==1:
				return render(request, 'payment/errorMessage.html', {'error':"You are already registered for the meet"})
		except:
			return render(request, 'payment/errorMessage.html', {'error':"Unrecognized Request"})
		order_form = OrderForm(request.POST)
		
		person_details=paymentForm(request.POST)
	   # try:
		number_of_person=request.POST['persons_count']
		delegate=request.POST['delegate']
		
		if delegate=="Indian Delegate":
			amount=((int(number_of_person)-1)*500)+5000
			cc="rupee"
			merchant_key=settings.PAYU_INFO['merchant_key_rupee']
			salt=settings.PAYU_INFO['salt_rupee']
		elif delegate=="Foreign Delegate":
			amount=((int(number_of_person)-1)*25)+100
			cc="dollar"
			merchant_key=settings.PAYU_INFO['merchant_key_usd']
			salt=settings.PAYU_INFO['salt_usd']        
		#except:
			#return render(request, 'failure.html', {'error':"Invalid Inputs"})

		try:
			person={"person1":request.POST['person1'],"person2":request.POST['person2'],"person3":request.POST['person3'],"person4":request.POST['person4'],"person5":request.POST['person5'],"person6":request.POST['person6']}
			count=0
			for key, value in person.iteritems():
				if not value.strip()=="":
					count+=1
			if not str(count)==number_of_person:
				return render(request, 'payment/errorMessage.html', {'error':"Person count does not match",'personCount':number_of_person,'count':count,'person':person})
			
		except:
			return render(request, 'payment/errorMessage.html', {'error':"Error occured while matching the person count",'personCount':number_of_person,'count':count,'person':person})

		count=ReferenceNumber.objects.get(id=1)

		value=str(count.number)
		count.number+=1
		count.save()
		txnid="AM"+"0"*(5-len(value))+value

		#order_form.txnid=txnid
		if order_form.is_valid():
			initial = order_form.cleaned_data

			if not initial['amount']==(amount):
				return render(request, 'payment/errorMessage.html', {'error':"Amount does not match"})
			initial.update({'key': merchant_key,
							'surl': request.build_absolute_uri(reverse('order.success')),
							'furl': request.build_absolute_uri(reverse('order.failure')),
							'udf1':person['person1']+"|"+person['person2']+"|"+person['person3'],'udf2':person['person4']+"|"+person['person5']+"|"+person['person6'],'udf3':number_of_person,'udf4':delegate,
							})
			# Once you have all the information that you need to submit to payu
			# create a payu_form, validate it and render response using
			# template provided by PayU.
			initial['txnid']=txnid
			payu_form = PayUForm(initial)
			if payu_form.is_valid():
				payuForm=payu_form.cleaned_data
				payu_form_final=PayUForm(payuForm)
				#return render(request, 'payment/errorMessage.html', {'error':payuForm["hash"]+" "+payuForm["udf4"]+" "+payuForm["txnid"]})
				context = {'form': payu_form_final,
						   'action': "%s" % settings.PAYU_INFO['payment_url']}
				ts=time.time()

				loggerCheckout.info(txnid+"  "+initial['email']+"  "+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))		   
				return render(request, 'payment/paymentForm.html', context)
			else:
				loggerPay.error('Something went wrong! Looks like initial data\
						used for payu_form is failing validation')
				return render(request, 'payment/errorMessage.html', {'error':"Code:410 ."})
		else:
			return render(request, 'payment/errorMessage.html', {'error':"Code: 409"})
	else:
	   
		return render(request, 'payment/errorMessage.html', {'error':"Request is not POST"})
#@csrf_protect
@csrf_exempt
def success(request):
	if request.method == 'POST':
		ts=time.time()
		timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		try:
			txnid=request.POST.get('txnid')
			mihpayid=request.POST.get('mihpayid')
			email=request.POST.get('email')
			amount=request.POST.get('amount')
			error_Message=request.POST.get('error_Message')
			status=request.POST.get('status')
			mode=request.POST.get('mode')
			group1=request.POST.get('udf1').split("|")
			group2=request.POST.get('udf2').split("|")
			personCount=request.POST.get('udf3')
			delegate=request.POST.get('udf4')

			#timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		except:
			loggerPay.error("Parameters are not in response")
		
		if delegate=="Indian Delegate":
			#amount=((int(number_of_person)-1)*3000)+5000
			cc="rupee"
			merchant_key=settings.PAYU_INFO['merchant_key_rupee']
			salt=settings.PAYU_INFO['salt_rupee']
		elif delegate=="Foreign Delegate":
			#amount=int(number_of_person)*100
			cc="dollar"
			merchant_key=settings.PAYU_INFO['merchant_key_usd']
			salt=settings.PAYU_INFO['salt_usd']

		if not verify_hash(request.POST,salt):
			return redirect('order.failure')
		else:
			loggerPay.info(mihpayid+"\t"+txnid+'\t'+email+"\t"+amount+"\t"+cc+"\t"+timestamp+"\t"+error_Message+"\t"+status)
			#try:
			payment=PaymentDetails(email=email,txnid=txnid,mihpayid=mihpayid,timestamp=datetime.datetime.now(),amount=amount,mode=mode)
			members=AlumniMeetMembers(email=email,delegate=delegate,person_count=personCount,person1=group1[0],person2=group1[1],person3=group1[2],person4=group2[0],person5=group2[1],person6=group2[2])
			payment.save()
			members.save()
			user=AluminiDetails.objects.get(email=request.POST.get('email'))
			user.register=1
			user.save()
			return render(request, 'payment/success.html',{'request':request.POST})
			#except:
				#return render(request, 'errorMessage.html', {'error':"Database Error"}) 
			
	else:
                return render_to_response('portal/error.html')
@csrf_exempt
def failure(request):
	context_dict={}
	if request.method == 'POST':
		
		ts=time.time()
		try:
			txnid=request.POST.get('txnid')
			mihpayid=request.POST.get('mihpayid')
			email=request.POST.get('email')
			amount=request.POST.get('amount')
			error_Message=request.POST.get('error_Message')
			status=request.POST.get('status')
			timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			delegate=request.POST.get('udf4')
		except:
			loggerPay.error("Parameters are not in response")
		
		if delegate=="Indian Delegate":
			#amount=((int(number_of_person)-1)*3000)+5000
			cc="rupee"
			merchant_key=settings.PAYU_INFO['merchant_key_rupee']
			salt=settings.PAYU_INFO['salt_rupee']
		elif delegate=="Foreign Delegate":
			#amount=int(number_of_person)*100
			cc="dollar"
			merchant_key=settings.PAYU_INFO['merchant_key_usd']
			salt=settings.PAYU_INFO['salt_usd']

		context_dict["email"]=email
		context_dict['timestamp']=timestamp    
		context_dict['txnid']=txnid  
		if not verify_hash(request.POST,salt):
			loggerPay.warning("Response data for order (txnid: %s) has been "
						   "tampered. Confirm payment with PayU." %
						   request.POST.get('txnid'))
			
			context_dict['reason']="Response data for payment has been tampered"

			return render(request, 'payment/failure.html', context_dict)
		else:
			loggerPay.info(mihpayid+"\t"+txnid+'\t'+email+"\t"+amount+"\t"+cc+"\t"+timestamp+"\t"+error_Message+"\t"+status)
			context_dict['reason']=request.POST.get('error_Message')
			return render(request, 'payment/failure.html', context_dict)
	 
	else:
		raise Http404("Unauthorized request") 

def pdfGenerate(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	c=0
	try:
		user=AluminiDetails.objects.get(email=request.user)
		if user.register==1:
			c=1
		else:
			c=0
	except:
		raise Http404("Unauthorized Request")
	if c==1:
		payment=PaymentDetails.objects.get(email=request.user)
		members=AlumniMeetMembers.objects.get(email=request.user)

		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] ='attachment; filename="receipt.pdf"'
		#response['pagesize']="A4"
		# Create the PDF object, using the response object as its "file."
		p = canvas.Canvas(response)
		width,height=595,842
		margin=50
		width_rect=width-2*margin
		heigth_rect=height-2*margin
		insideMargin=20
		labelHeight=50
		rectX,rectY=margin,margin
		formX_Left=rectX+insideMargin
		formY_Left=rectY+heigth_rect-140-labelHeight-10

		formX_Right=rectX+insideMargin+(width_rect-2*insideMargin)*0.6
		formY_Right=rectY+heigth_rect-140-labelHeight-10

		lineSpace=20

		#image=Image.open("./static/images/IITBHULogo.jpg")
		#
		# Draw things on the PDF. Here's where the PDF generation happens.
		# See the ReportLab documentation for the full list of functionality.
		
		p.rect(margin,margin,width-2*margin,height-2*margin, fill=0)
		#p.drawString(100, 100, "Hello world.")
		logoFile=os.path.join(BASE_DIR,"static/images/IITBHULogo.jpg")
		p.drawInlineImage(logoFile,margin+40,margin+heigth_rect-145, width=100,height=100) #LOGO

		p.drawString(formX_Left,formY_Left ,"Reference No.")
		p.drawString(formX_Left+250,formY_Left ,":")
		p.drawString(formX_Right,formY_Right ,payment.txnid)

		p.setFont("Helvetica", 18)
		p.drawString(formX_Left+240,margin+heigth_rect-85 ,"IIT (BHU) Alumni Meet")
		p.setFont("Helvetica", 15)
		p.drawString(formX_Left+width_rect/2-100,formY_Left+30 ,"E-Reciept of Registration")

		p.setFont("Helvetica", 12)
		p.drawString(formX_Left+260,margin+heigth_rect-100 ,"(27 Feb ,2017 - March 1,2017)")
		#Date
		p.drawString(formX_Left,formY_Left- lineSpace ,"Date/Time of Transaction")
		p.drawString(formX_Left+250,formY_Left -lineSpace ,":")
		p.drawString(formX_Right,formY_Right -lineSpace,str(payment.timestamp.strftime('%d-%m-%Y %H:%M:%S')))


		#Alumni
		p.drawString(formX_Left,formY_Left- 2*lineSpace-20 ,"Name of the Alumnus/Alumna")
		p.drawString(formX_Left+250,formY_Left- 2*lineSpace-20 ,":")
		p.drawString(formX_Right,formY_Right -2*lineSpace-20,members.person1)
		#Delegate
		p.drawString(formX_Left,formY_Left- 3*lineSpace -20,"Delegate")
		p.drawString(formX_Left+250,formY_Left- 3*lineSpace-20 ,":")
		p.drawString(formX_Right,formY_Right -3*lineSpace-20,members.delegate)

		#Payment
		p.drawString(formX_Left,formY_Left- 4*lineSpace -20,"Payment Status")
		p.drawString(formX_Left+250,formY_Left- 4*lineSpace-20 ,":")
		p.setFillColorRGB(0,1,0)

		p.drawString(formX_Right,formY_Right -4*lineSpace-20,"PAID")
		p.setFillColorRGB(0,0,0)
		#attendees
		p.setFont("Helvetica", 14)
		p.drawString(formX_Left,formY_Left- 5*lineSpace -30,"Names of the Attendees")
		p.setFont("Helvetica", 12)
		
                count=members.person_count
                mult=6
		#members_new=members.values()
		#member_dict=dict(members_new.iterlists())
		#for key,value in members_new[0].iteritems():
			
		 #   y="person"
		 #       if value!="":
		  #          p.drawString(formX_Left+50,formY_Left- mult*lineSpace -40,str(count)+". "+value)
		   #         count+=1
			#        mult+=1
		#p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,payment.person1)
		#if payment.person2!=""
		 #   p.drawString(formX_Left+50,formY_Left- 7*lineSpace -40,str(count)+payment.person2)
		 #   count+=1
		#p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,members.person1+members.person1+members.person2+members.person3+members.person4)
		if count=="1":
			p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,"1."+members.person1)
		elif count=="2":
			p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,"1."+members.person1)
			p.drawString(formX_Left+50,formY_Left- 7*lineSpace -40,"2."+members.person2)
		elif count=="3":
			p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,"1."+members.person1)
			p.drawString(formX_Left+50,formY_Left- 7*lineSpace -40,"2."+members.person2)
			p.drawString(formX_Left+50,formY_Left- 8*lineSpace -40,"3."+members.person3)
		elif count=="4":
			p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,"1."+members.person1)
			p.drawString(formX_Left+50,formY_Left- 7*lineSpace -40,"2."+members.person2)
			p.drawString(formX_Left+50,formY_Left- 8*lineSpace -40,"3."+members.person3)
			p.drawString(formX_Left+50,formY_Left- 9*lineSpace -40,"4."+members.person4)
		elif count=="5":
			p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,"1."+members.person1)
			p.drawString(formX_Left+50,formY_Left- 7*lineSpace -40,"2."+members.person2)
			p.drawString(formX_Left+50,formY_Left- 8*lineSpace -40,"3."+members.person3)
			p.drawString(formX_Left+50,formY_Left- 9*lineSpace -40,"4."+members.person4)
			p.drawString(formX_Left+50,formY_Left- 10*lineSpace -40,"5."+members.person5)
		elif count=="6":
			p.drawString(formX_Left+50,formY_Left- 6*lineSpace -40,"1."+members.person1)
			p.drawString(formX_Left+50,formY_Left- 7*lineSpace -40,"2."+members.person2)
			p.drawString(formX_Left+50,formY_Left- 8*lineSpace -40,"3."+members.person3)
			p.drawString(formX_Left+50,formY_Left- 9*lineSpace -40,"4."+members.person4)
			p.drawString(formX_Left+50,formY_Left- 10*lineSpace -40,"5."+members.person5)
			p.drawString(formX_Left+50,formY_Left- 11*lineSpace -40,"6."+members.person6)
			
		#p.drawString(formX_Left+50,formY_Left- 8*lineSpace -40,"3. Tanay Sharma")
		#p.drawString(formX_Left+50,formY_Left- 9*lineSpace -40,"4. Tanay Sharma")
		if "Indian" in members.delegate:
			perAlum="5000"
			cc="Rs."
			perAcc="500"
			total=str(payment.amount)
		else:
			perAlum="100"
			cc="$ "
			perAcc="25"
			total=str(payment.amount)   
		p.setFont("Helvetica", 14)
		p.drawString(formX_Left,formY_Left- 10*lineSpace -60,"Payment Details")
		p.setFont("Helvetica", 12)
		
		p.drawString(formX_Left,formY_Left- 11*lineSpace -70,"Registration Amount (per alumni)")
		p.drawString(formX_Left+260,formY_Left- 11*lineSpace-70 ,":")
		p.drawString(formX_Right,formY_Right -11*lineSpace-70,cc+perAlum)
		
		p.drawString(formX_Left,formY_Left- 12*lineSpace -70,"Registration Amount (per accompanying person)")
		p.drawString(formX_Left+260,formY_Left- 12*lineSpace-70 ,":")
		p.drawString(formX_Right,formY_Right -12*lineSpace-70,cc+perAcc)
		
		p.drawString(formX_Left,formY_Left- 13*lineSpace -70,"Total attendees")
		p.drawString(formX_Left+260,formY_Left- 13*lineSpace-70 ,":")
		p.drawString(formX_Right,formY_Right -13*lineSpace-70,members.person_count)

		p.drawString(formX_Left,formY_Left- 14*lineSpace -70,"Total Amount")
		p.drawString(formX_Left+260,formY_Left- 14*lineSpace-70 ,":")
		p.drawString(formX_Right,formY_Right -14*lineSpace-70,cc+total)
		
		

		p.setFont("Helvetica", 11)
		p.drawString(margin+20,margin+20,"Note: Delegates are required to submit a hard copy of this e-reciept at the time of registration.")
		# Close the PDF object cleanly, and we're done.
		p.showPage()
		p.save()
		p.showPage()
		return response
	else:
		raise Http404("Unauthorized Request")

def validate_phone(x):
	t=string.maketrans('','')
	nodigs=t.translate(t, string.digits)
	return x.encode("utf-8").translate(t, nodigs)

@login_required
def travelUpdate(request):
	if request.method=="POST":
		email=request.user
		arrival_mode=request.POST.get('arrival_mode')
		arrival_number=request.POST.get('arrival_number')
		arrival_time=request.POST.get('arrival_time')
		arrival_date=request.POST.get('arrival_date')
		pickup=request.POST.get('pickup')
		drop=request.POST.get('drop')
		departure_mode=request.POST.get('departure_mode')
		departure_time=request.POST.get('departure_time')
		departure_date=request.POST.get('departure_date')
		c=0
		try:
			exist=travelDetail.objects.get(email=email)
			c=1
		except:
			c=2
		if c==1:
			try:
				exist.arrival_mode=arrival_mode
				exist.arrival_number=arrival_number
				exist.arrival_time=arrival_time
				exist.arrival_date=arrival_date
				exist.pickup=pickup
				exist.drop=drop
				exist.departure_mode=departure_mode
				exist.departure_time=departure_time
				exist.departure_date=departure_date
				exist.save()
				return HttpResponse("success")
			except:
				return HttpResponse("Database Error")
		elif c==2:
			#try:

			travel=travelDetail(email=email,arrival_mode=arrival_mode,arrival_number=arrival_number,arrival_time=arrival_time,arrival_date=arrival_date,pickup=pickup,drop=drop,departure_date=departure_date,departure_time=departure_time,departure_mode=departure_mode)  
			travel.full_clean()
			travel.save()
				# HttpResponse("success")
			#except:
			return HttpResponse("success")
	else:
		return HttpResponse("Request is not Post")

				
@login_required				
def AlumniMeet(request):
        email=request.user
        category=request.user.category
        context_dict={}
        try:
                alumni_details=AluminiDetails.objects.get(email=email)
        except:
                context_dict["error"]="Only Alumni are authorized to view this page"
                return render_to_response('payment/errorMessage.html',context_dict,context_instance=RequestContext(request)) 

	members=AluminiDetails.objects.values('firstName','lastName','year','branch','register').order_by('year', 'branch', 'firstName','lastName')
	context_dict["alumniDetails"]=alumni_details
	context_dict["members"]=members
	context_dict['payForm']=paymentForm(initial={'person1':alumni_details.firstName+" "+alumni_details.lastName})
	context_dict['orderForm']=OrderForm(initial={'firstname':alumni_details.firstName,'phone':validate_phone(alumni_details.mobile),'email':alumni_details.email,'txnid':uuid4().hex,'productinfo': "Alumni Meet Registration Amount",})
	context_dict["date"]=alumni_details.dob.strftime('%Y-%d-%m')
	context_dict['amount_india']=5000
	context_dict['amount_foreign']=100
	context_dict['amount_foreign_accomp']=25
	context_dict['amount_india_accomp']=500
	try:
		travel=travelDetail.objects.get(email=email)
		
	except:
		travel=None 
	context_dict['travel']=travel
	get_notification(request,context_dict,category)
	# Render list page with the documents and the form
	return render_to_response('portal/alumniMeet.html',context_dict,context_instance=RequestContext(request))

