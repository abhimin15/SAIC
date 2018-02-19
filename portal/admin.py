from django.contrib import admin

from portal.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField

from django import forms
import csv
import time

def exportPaymentDetails(modeladmin,request,queryset):
    data=queryset

    listItem=[None] * 7
    f=open('/var/www/saic/SAIC/alumniPaymentDetails'+time.strftime("%d-%m-%Y")+'.csv', 'wb')
    writer =csv.writer(f, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Email","Mihpayid","Mode","Txn_Id","Amount","CC","Timestamp"]) 

    count=0
    for x in data:
        try:
            count=0
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            listItem[1]=str(x.mihpayid).replace(","," ")
            listItem[2]=str(x.mode).replace(","," ")
            listItem[3]=str(x.txnid).replace(","," ")
            listItem[4]=str(x.amount).replace(","," ")
            listItem[5]=str(x.cc).replace(","," ")
            listItem[6]=str(x.timestamp).replace(","," ")
            writer.writerow(listItem)
        except:
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            writer.writerow(listItem)    

exportPaymentDetails.short_description = "Export payment Details of Alumni into a csv file"

class AlumniPaymentAdmin(admin.ModelAdmin):
    actions=[exportPaymentDetails]


def exportMentorshipresponse(modeladmin,request,queryset):
    data=queryset

    listItem=[None] * 4
    f=open('/var/www/saic/SAIC/alumniMentorshipDetails'+time.strftime("%d-%m-%Y")+'.csv', 'wb')
    writer =csv.writer(f, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Email","Max No of students","Areas of Interest","Response Date"]) 

    count=0
    for x in data:
        try:
            count=0
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            listItem[1]=str(x.mentor_max).replace(","," ")
            listItem[2]=str(x.areas_mentor).replace(","," ")
            listItem[3]=str(x.last_response_date).replace(","," ")          
            writer.writerow(listItem)
        except:
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            writer.writerow(listItem)    

exportMentorshipresponse.short_description = "Export selected responses of Alumni into a csv file"

class AlumniMentorshipAdmin(admin.ModelAdmin):
    actions=[exportMentorshipresponse]


def exportAlumniCompanyDetails(modeladmin,request,queryset):
    data=queryset

    listItem=[None] * 6
    f=open('/var/www/saic/SAIC/alumniCompanyDetails'+time.strftime("%d-%m-%Y")+'.csv', 'wb')
    writer =csv.writer(f, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Email","First Name","Last Name","Company"]) 

    count=0
    for x in data:
        try:
            count=0
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            listItem[1]=str(x.firstName).replace(","," ")
            listItem[2]=str(x.lastName).replace(","," ")
            listItem[3]=str(x.organisation).replace(","," ")
            listItem[4]=str(x.year).replace(","," ")
            listItem[5]=str(x.branch).replace(","," ")
            writer.writerow(listItem)
        except:
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            writer.writerow(listItem)    

exportAlumniCompanyDetails.short_description = "Export selected Company Details of Alumni into a csv file"


def exportRegisteredAlumni(modeladmin,request,queryset):
    data=queryset.filter(register=1)

    listItem=[None] * 22
    f=open('/var/www/saic/SAIC/RegisteredAlumniDetails'+time.strftime("%d-%m-%Y")+'.csv', 'wb')
    writer =csv.writer(f, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Email","First Name","Last Name","Gender","Department","Degrees","Year Of Passing","Date of Birth","Designation","Organisation","Mobile","Permanent Address","Permanent City","Permanent Zip","Permanent State","Permanent Country","Present State","Present Country","Present Address","Present City","Present Zip","Register"]) 

    count=0
    for x in data:
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

exportRegisteredAlumni.short_description = "Export registered alumni details to a file"


def exportStudentMentorshipresponse(modeladmin,request,queryset):
    data=queryset

    listItem=[None] * 4
    f=open('/var/www/saic/SAIC/StudentMentorshipDetails'+time.strftime("%d-%m-%Y")+'.csv', 'wb')
    writer =csv.writer(f, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Email","Career Interest","Guidance Type","Response Date"]) 

    count=0
    for x in data:
        try:
            count=0
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            listItem[1]=str(x.career_interest).replace(","," ")
            listItem[2]=str(x.guidance_type).replace(","," ")
            listItem[3]=str(x.last_response).replace(","," ")          
            writer.writerow(listItem)
        except:
            listItem[0]=(x.email.encode('utf-8')).replace(","," ")
            writer.writerow(listItem)    

exportStudentMentorshipresponse.short_description = "Export selected responses of Students into a csv file"

class StudentMentorshipAdmin(admin.ModelAdmin):
    actions=[exportStudentMentorshipresponse]



class CustomUserCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            MyUser._default_manager.get(username=username)
            raise forms.ValidationError(self.error_messages['duplicate_username'])
        except MyUser.DoesNotExist:
            return username
        

    def clean_password2(self):
        #Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="password",
                                         help_text="""Raw passwords are not stored, so there is no way to see this
                                         user's password, but you can change the password using <a href=\"password/\">
                                         this form</a>.""")

    class Meta(UserChangeForm.Meta):
        model = MyUser
        fields = ('username', 'password', 'is_active', 'is_staff', 'is_superuser', 'user_permissions')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class MyUserAdmin(UserAdmin):
	form=CustomUserChangeForm
	add_form=CustomUserCreationForm

	list_display=('username','email','is_staff','is_superuser')
	list_filter=('is_superuser',)
	fieldsets=(
		(None,{'fields':('username','password','date_joined')}),('Permissions',{'fields':('is_active','is_staff','is_superuser')}),

		)

	add_fieldsets=(
		(None,{
			'classes':('wide',),
			'fields':('username','password','is_staff','is_superuser')
			}),
		)
	search_fields=('username',)
	ordering=('username',)
	filter_horizontal=('groups','user_permissions',)

class MyAlumniDetails(admin.ModelAdmin):
    search_fields=('email',)
    actions=[exportAlumniCompanyDetails,exportRegisteredAlumni]
class MyStudentDetails(admin.ModelAdmin):
    search_fields=('email',)
class MyFacultyiDetails(admin.ModelAdmin):
    search_fields=('email',)

admin.site.register(AluminiDetails,MyAlumniDetails)
admin.site.register(Verification)
admin.site.register(Notifications)
admin.site.register(MyUser,MyUserAdmin)
admin.site.register(Question)
admin.site.register(FacultyDetails,MyFacultyiDetails)
admin.site.register(StudentDetails,MyStudentDetails)
admin.site.register(RequestForContact)
admin.site.register(Broadcast)
admin.site.register(Interest)
admin.site.register(GeneralNotifications)
admin.site.register(GuestHouse)
admin.site.register(IIT_Activities)
admin.site.register(AsmpAlumniResponse,AlumniMentorshipAdmin)
admin.site.register(AsmpStudentResponse,StudentMentorshipAdmin)
admin.site.register(blackList)
admin.site.register(Chronicle)
admin.site.register(ReferenceNumber)
admin.site.register(AlumniMeetMembers)
admin.site.register(PaymentDetails,AlumniPaymentAdmin)
admin.site.register(travelDetail)
