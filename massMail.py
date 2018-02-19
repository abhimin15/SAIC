from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from portal.models import *
#f = open('mailList.csv', 'r')
l=[]
f=AluminiDetails.objects.all()
#image=open('mentorship.jpg','r')
#subject, from_email = 'IIT (BHU) Varanasi requests your presence in the SECOND ALUMNI MEET, 2017', 'ajamal.min@itbhu.ac.in'
subject, from_email = 'Greetings from IIT (BHU) Varanasi on Holi', 'alumnicell@iitbhu.ac.in'

html_content = render_to_string('holi.html') # ...
text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

failed=open('failed.txt','w')
count=1
for line in f:
    try:
        x=line.email.split('\n')
        l.append(x[0])
        p=[]
        x[0]=x[0].strip()
        #print x[0]
        p.append(x[0])
        ccEmail=[]
        #ccEmail.append("shah.yash.bce12@iitbhu.ac.in")
        #ccEmail.append("shashank.agarwal.met14@itbhu.ac.in")
        #ccEmail.append("neha.gupta.mec13@itbhu.ac.in")
        #ccEmail.append("tanay.sharma.cse12@iitbhu.ac.in")
        msg = EmailMultiAlternatives(subject, text_content, from_email,p,cc=ccEmail)
        msg.attach_alternative(html_content, "text/html")
        msg.attach_file('HappyHoli.jpg')
        msg.send()
        print count
        count+=1
    except:
        failed.write(line.email+'\n')
failed.close()
#f.close()
# create the email, and attach the HTML version as well.
    

