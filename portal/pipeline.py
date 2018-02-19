from django.shortcuts import redirect

from social.pipeline.partial import partial

from portal.models import *

import random
import hashlib

@partial
def save_username(strategy, details, user=None, is_new=False, *args, **kwargs):
    # if kwargs.get('ajax') or user and user.email:
    #     return
    # elif is_new and not details.get('email'):
    #     email = strategy.request_data().get('email')
    #     if email:
    #         details['email'] = email
    #     else:
    #         return redirect('require_email')
    if user.username != user.email:
        print "not equal"
        user.username = user.email
        user.save()

@partial
def alumni_form(strategy, backend, details, user=None, is_new=False, *args, **kwargs):
    if user:
        # print "hello"
        email = user.username
        alumni = AluminiDetails.objects.filter(email=email)
        if alumni:
            ### already exists no need to do anything ###
            return
        else:
            ### need to fill up the alumni form ###
            print backend.name
            if backend.name == 'linkedin-oauth2':
                ### hash for linkedin ###
                # q=random.randint(0,1000000)
                string=user.email+"linkedin-oauth2"
                m=hashlib.md5(string)
                hash_value=m.hexdigest()
                print "pipeline" + str(hash_value)
                ### link for verify mail 'portal/verify/hash_value' ###
                x=Verification(email=email,hash_value=hash_value)
                # x.full_clean()                  
                x.save()
                return redirect('/portal/verify/'+ hash_value + '/?backend=linkedin-oauth2')
            elif backend.name == 'google-oauth2':
                string=user.email+"google-oauth2"
                m=hashlib.md5(string)
                hash_value=m.hexdigest()
                print "pipeline" + str(hash_value)
                ### link for verify mail 'portal/verify/hash_value' ###
                x=Verification(email=email,hash_value=hash_value)
                # x.full_clean()                
                x.save()
                return redirect('/portal/verify/'+ hash_value + '/?backend=google-oauth2')
