from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

f = open('/var/www/saic/SAIC/static/scripts/assignedMenteesPhase1.txt', 'r')
l=[]

#image=open('mentorship.jpg','r')
subject, from_email = 'Greetings from IIT (BHU) !', 'alumnicell@itbhu.ac.in'

html_content = render_to_string('MenteeFeedBackMail.html') # ...
text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

failed=open('/var/www/saic/SAIC/static/scripts/failed.txt','w')
count=1
for line in f:
    try:
        x=line.split('\n')
        #print x
        l.append(x[0])
        p=[]
        x[0]=x[0].strip()
        p.append(x[0])
        msg = EmailMultiAlternatives(subject, text_content, from_email,p)
        msg.attach_alternative(html_content, "text/html")
        #msg.attach_file('mentorship.jpg')
        msg.send()
        print count
        count+=1
    except:
        failed.write(line+'\n')
failed.close()
f.close()
# create the email, and attach the HTML version as well.
    

