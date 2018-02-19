from portal.models import *
import csv
import time

def getMentorsDetails():
    listItem=[None] * 22
    data=AluminiDetails.objects.all()
    f=open('/var/www/saic/SAIC/static/scripts/AlumniDetailsFromFile'+time.strftime("%d-%m-%Y")+'.csv', 'w')
    writer =csv.writer(f, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Email","First Name","Last Name","Gender","Department","Degrees","Year Of Passing","Date of Birth","Designation","Organisation","Mobile","Permanent Address","Permanent City","Permanent Zip","Permanent State","Permanent Country","Present State","Present Country","Present Address","Present City","Present Zip","Register"])
    mentors=open("/var/www/saic/SAIC/static/scripts/alumniEmailFile.csv", 'r')
    count=0
    for y in mentors:
        t=y.split("\n")[0]
        for x in data:
            if str(x.email) in t:

                try:
                    count=0
                    listItem[0]=(x.email.encode('utf-8')).replace(","," ")
                    listItem[1]=(x.firstName.encode('utf-8')).replace(","," ")
                    listItem[2]=(x.lastName.encode('utf-8')).replace(","," ")
                    listItem[3]=(x.gender.encode('utf-8')).replace(","," ")

                    listItem[4]=(x.branch.encode('utf-8')).replace(","," ")
                    listItem[5]=(x.course.encode('utf-8')).replace(","," ")
                    listItem[6]=str(x.year).replace(","," ")
                    listItem[7]=str(x.dob).replace(","," ")
                    listItem[8]=(x.designation.encode('utf-8')).replace(","," ")
                    listItem[9]=(x.organisation.encode('utf-8')).replace(","," ")
                    listItem[10]=(x.mobile.encode('utf-8')).replace(","," ")
                    listItem[11]=(x.address_permanent.encode('utf-8')).replace(","," ")
                    listItem[12]=(x.city_permanent.encode('utf-8')).replace(","," ")
                    listItem[13]=(x.zip_permanent.encode('utf-8')).replace(","," ")
                    listItem[14]=(x.state_permanent.encode('utf-8')).replace(","," ")
                    listItem[15]=(x.country_permanent.encode('utf-8')).replace(","," ")
                    listItem[16]=(x.state_present.encode('utf-8')).replace(","," ")
                    listItem[17]=(x.country_present.encode('utf-8')).replace(","," ")
                    listItem[18]=(x.address_present.encode('utf-8')).replace(","," ")
                    listItem[19]=(x.city_present.encode('utf-8')).replace(","," ")
                    listItem[20]=(x.zip_present.encode('utf-8')).replace(","," ")
                    listItem[21]=str(x.register).replace(","," ")

                    writer.writerow(listItem)
                except:
                    listItem[0]=(x.email.encode('utf-8')).replace(","," ")
                    writer.writerow(listItem)

getMentorsDetails()
