from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core import serializers
import random
import hashlib
from os import *
from portal.models import *
from portal.mailid import *
import datetime
#import urllib2
import requests
import json
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import render
import string,re
from recaptcha.client import captcha  
#from portal.forms import Registration_Form
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def ValuesQuerySetToDict(vqs):
	return [item for item in vqs]

def has_special(pw):
	'Password must contain a special character'
	return len(set(string.punctuation).intersection(pw)) > 0

def has_numeric(pw):
	'Password must contain a digit'
	return len(set(string.digits).intersection(pw)) > 0

def login_page(request):
	if request.method == 'POST':
		email=request.POST.get('email_id')
		password=request.POST.get('password')
		user = authenticate(username=email, password=password)	
		if user is not None:
			login(request,user)
			return HttpResponse("success")

		else:
			return HttpResponse("Your username and password were incorrect.")	
	else:
		return HttpResponseRedirect('../')		

def main_page(request):
	# Render list page with the documents and the form
	context = RequestContext(request)   
	try:
		
		context_dict=None
				# Add category to the context so that we can access the id and likes
				
	
	except Category.DoesNotExist:
		pass

	  
	return render(request, 'index.html', context_dict, context)

def logout_page(request):
	logout(request)
	#   
	return HttpResponseRedirect('../')



def gallery(request):
	context = RequestContext(request)   
	context_dict={}
	galleryPath=settings.GALLERY_PATH
	fileList=[]
	fileDirectories=[]
	temp_dict={}
	for (dirpath, dirnames, filenames) in walk(galleryPath):
                fileList.append(filenames)
                fileDirectories.extend(dirnames)
        for i in range(1,len(fileList)):
                temp_dict[fileDirectories[i-1]]=fileList[i]
        context_dict["folders"]=fileDirectories
        context_dict["all_files"]=temp_dict
        context_dict["base_path"]="/static/gallery/"
	return render_to_response('gallery.html',context_dict,context)

def signup_page(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		AddEmail=request.POST.get('email')          
		Pass=request.POST.get('pass')
		CPass=request.POST.get('cpass')
		#branchName=request.POST.get('branchname')
		#gender=request.POST.get('gender')
		#name=request.POST.get('name')
		#yearOfPassing=request.POST.get('year')
		#dob=request.POST.get('dob')
		#course=request.POST.get("course")
		context_dict={} 
		context_dict["email"]=AddEmail
		
		#context_dict["course"]=course
		#context_dict["dob"]=dob
		#context_dict["year"]=yearOfPassing
		#form=Registration_Form(request.POST)       
		
		# see if the user correctly entered CAPTCHA information
		# and handle it accordingly.
					

		if (AddEmail.strip()!="" and Pass.strip()!="" and CPass.strip()!=""):
			try:
				validate_email( AddEmail )
					
			except ValidationError:
				#context_dict["error"]="Please Enter A valid Email ID" 
				return HttpResponse("Please Enter a valid Email Id")

			if len(Pass)<8 :
					#context_dict["error"]="Password should be minimum 8 characters long,a special character and a number"
					#context_dict["check"]="1"   
					return HttpResponse("Password should be minimum 8 characters long")
			#return HttpResponse(request.POST.get('recaptcha_challenge_field')+request.POST.get('recaptcha_response_field'))
		
			#------------------------------------------------------------captcha verification-------------------------------------------

			#response = captcha.submit(request.POST.get('recaptcha_response_field'),'6LclNAsTAAAAAKXM2_TU7PXZTk-TuvZSW6cuLeVy',request.META['REMOTE_ADDR'],)
			#url = "https://www.google.com/recaptcha/api/siteverify"
			#params = {'secret': settings.RECAPTCHA_SECRET_KEY,'response': request.POST.get('recaptcha_response_field'),'remoteip': request.META['REMOTE_ADDR']}
			#verify_rs = requests.get(url, params=params, verify=True)
			#verify_rs = verify_rs.json()
			#response={}
			#response["status"] = verify_rs.get("success", False)
			#response['message'] = verify_rs.get('error-codes', None) or "Unspecified error."
			#return HttpResponse()
			response = captcha.submit(request.POST.get('recaptcha_challenge_field'),request.POST.get('recaptcha_response_field'),settings.RECAPTCHA_SECRET_KEY,request.META['REMOTE_ADDR'],)

			if response.is_valid:
				captcha_response = "YOU ARE HUMAN:"
				if(Pass==CPass):
					try:
						exist=MyUser.objects.get(username=AddEmail)
						#context_dict["error"]="You are already signed up with this email"
						#context_dict["check"]="1"   
						#c = RequestContext(request,context_dict)            
						#return render_to_response('login.html',c )
						return HttpResponse("You are already signed up with this email")
					except MyUser.DoesNotExist:
						pass
					
					q=random.randint(0,1000000)
					string=str(q)+AddEmail
					m=hashlib.md5(string)
					hash_value=m.hexdigest()                    
					try:
						check=Verification.objects.get(email=AddEmail)
						#context_dict["error"]="A mail has been sent to you already"
						#context_dict["check"]="1"                    
						return HttpResponse("A mail has been sent to you already")
					except:
						pass
					
					
					try:	
						message="Welcome to the fraternity of IIT(BHU)!!.\nThanks for signing up in the Alumni Portal , IIT (BHU).\n\nPlease click on the link below to authenticate yourself and proceed to the registration with Alumni Portal"+"\n\n\n"+"http://"+settings.HOST+"/portal/verify/"+hash_value+"/"+"\n"+"Please do not reply to this email. For any assistance please contact support@itbhualumni.net.\n\n-----\nAdministrator\nAlumni Portal\nIIT (BHU) Varanasi."
						send_mail('Verification Mail',message,ADMIN,[AddEmail],fail_silently=False)
						x=Verification(email=AddEmail,password=Pass,hash_value=hash_value)
						x.full_clean()                  
						x.save()
									
						return HttpResponse("success")
					except ValidationError,e:
						#context_dict["error"]=e.message_dict
						return HttpResponse(e.message_dict)


				else:
			#context_dict["error"]="Password Doesnot Match"
					return HttpResponse("Password Doesnot Match")

			else:
				#context_dict["error"]="Type right captcha"
				#context_dict["check"]="1"   
				return HttpResponse("Type right captcha")
			#except:
			#	return HttpResponse("Captcha can not be loaded")




			
				#if not re.match("[\d]*\dEN\d[\d]*", roll):
				#	context_dict["error"]="Wrong Roll no"
				#	c = RequestContext(request, context_dict)           
				#	return render_to_response('login.html',c )
				


				
	
					
			
		else:
			#context_dict["error"]="Field Cannot Be Empty"           
			return HttpResponse("Field Cannot Be Empty")
			
	#   if form.is_valid():
		#try:       
			#user=User.objects.create_user(username=AddEmail,password=AddPass)
			#user.save()        
			#userLog=authenticate(username=AddEmail, password=AddPass,email=AddEmail)       
			#login(request,userLog) 
			
				
		#   return HttpResponseRedirect('/portal/')     
		#except:
		#   c = RequestContext(request, {'error': "SignUp unsuccessfull:username may have already taken"})          
		#   return render_to_response('login.html',c )
				
def team_page(request):
	context = RequestContext(request)   
	context_dict={}
	return render_to_response('team.html',context_dict,context)



def pass_recovery(request):
    context_dict={}
    email=None   
    if request.method == 'POST':

        email=request.POST.get('emailId')     
                        
    try:
        x=MyUser.objects.get(username=email)
        category=x.category
        password="#"                
        try:
            q=random.randint(0,1000000)
            string=str(q)+email
            m=hashlib.md5(string)
            hash_value=m.hexdigest()                    
            try:
                check=Verification.objects.get(email=email)
                return HttpResponse( "A mail has been sent to you already")
            except:
                pass    
            message="This is the Password Recovery email. Please click on the link below to reset your password"+"\n\n\n"+"https://"+settings.HOST+"/portal/pass_change/"+hash_value+"/"
            send_mail('Password Recovery Mail',message,ADMIN,[email],fail_silently=False)
            x=Verification(email=email,hash_value=hash_value,password=password)
            x.full_clean()                  
            x.save()                
            return HttpResponse("A link for resetting the password has been sent to your registered email id.")
        except ValidationError,e:
            #context_dict["message"]=e.message_dict                  
            #c = RequestContext(request,context_dict)            
            return HttpResponse("Message cannot be sent. Server Error")
    except MyUser.DoesNotExist:
        #context_dict["message"]="This emailId doesnot exist.Please enter valid emailId"                   
        #c = RequestContext(request,context_dict)            
        return HttpResponse("This Email Id does not exist. Please enter a valid Email Id")
    
    return HttpResponse("Something wrong. Please retry again.")
def chronicles(request):
	# Render list page with the documents and the form
	context = RequestContext(request)   
	context_dict={}
	chk_val=0
                #get all file fields
	try:
                chronicle_data=Chronicle.objects.all()
                context_dict['chronicles']=chronicle_data
                context_dict['chronicle_count']=len(chronicle_data)
        except:
                context_dict['chronicle_count']=0
	return render_to_response('chronicle.html',context_dict,context)

def abtinstitute(request):
	return render(request,'institute.html',{})
def abtcentenary(request):
	return render(request,'centenary.html',{})