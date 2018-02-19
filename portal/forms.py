from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from portal.models import *
from django.forms import extras
from django.contrib.admin.widgets import AdminDateWidget 
from functools import partial
from django.utils.safestring import mark_safe
from django.forms.extras.widgets import SelectDateWidget


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class AluminiForm(forms.Form):
	DateInput = partial(forms.DateInput, {'class': 'datepicker'})
	ranges = [(n, min(n+1,1930)) for n in xrange(1930,2020,1)]
	yearOfPassing=[(n, min(n, 2017)) for n in xrange(1920,2017,1)]
	birthYear=[(n, min(n,1920)) for n in xrange(1930,2002,1)]
	courseChoices=(('UGD', 'UGD(BTech. 4 years)',), ('IDD', 'IDD(5 years)',),('IMD', 'IMD(5 years)',),('M.Tech./M.Pharm.', 'M.Tech./M.Pharm.(2 years)',),('Ph.D', 'Ph.D',),)
	branchChoices=(('BC: School of Biochemical Engineering', 'BC: School of Biochemical Engineering',),('BM: School of Biomedical Engineering', 'BM: School of Biomedical Engineering',),('CE: Department of Civil Engineering', 'CE: Department of Civil Engineering',),('CH: Department of Chemical Engineering & Technology', 'CH: Department of Chemical Engineering & Technology',),('CR: Department of Ceramic Engineering', 'CR: Department of Ceramic Engineering',),('CS: Department of Computer Science & Engineering', 'CS: Department of Computer Science & Engineering',),('CY: Department of Chemistry (Applied Chemistry)', 'CY: Department of Chemistry (Applied Chemistry)',),('EC: Department of Electronics Engineering', 'EC: Department of Electronics Engineering',),('EE: Department of Electrical Engineering', 'EE: Department of Electrical Engineering',),('MA: Department of Mathematical Sciences (Applied Maths)', 'MA: Department of Mathematical Sciences (Applied Maths)',),('ME: Department of Mechanical Engineering', 'ME: Department of Mechanical Engineering',),('MN: Department of Mining Engineering', 'MN: Department of Mining Engineering',),('MS: School of Material Science & Technology', 'MS: School of Material Science & Technology',),('MT: Department of Metallurgical Engineering', 'MT: Department of Metallurgical Engineering',),('PH: Department of Pharmaceutics', 'PH: Department of Pharmaceutics',),('PY: Department of Physics (Applied Pysics)', 'PY: Department of Physics (Applied Physics)',),('Other','Other'),)
	firstName = forms.CharField(label='First Name:',widget=forms.TextInput(attrs={'class' : 'form-control roundcorner','data-minlength':'1','id':'firstName','placeholder':"Please enter your first name here","data-error":"Field required","maxlength":"32","data-minlength":"1"}), max_length=32,required=True)
	lastName = forms.CharField(label='Last Name:',widget=forms.TextInput(attrs={'class' : 'form-control roundcorner','id':'lastName','placeholder':"Please enter your last name here"}), max_length=32)
	gender = forms.ChoiceField(label='Gender:',widget=forms.Select(attrs={'class' : 'form-control roundcorner','id':'gender'}),choices=(('Male','Male'),('Female','Female')))
	dob=forms.DateField(label='Date Of Birth:',widget=SelectDateWidget(attrs={'class' : 'form-control roundcorner','style':'width:32.3%;display:inline-block;','id':'dob'},years=range(1930,2002)))
	
	course = forms.MultipleChoiceField(label="Degree (Select atleast one option):",required=True,widget=forms.CheckboxSelectMultiple(attrs={'class' : 'checkbox-inline','id':'course'}),choices=courseChoices,)
	#motherName = forms.CharField(label="Mother's Name:",widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=40)
	
	branch = forms.ChoiceField(label='Department:',widget=forms.Select(attrs={'class' : 'form-control ','id':'branch'}),choices=branchChoices)
	year = forms.ChoiceField(label='Graduation Year:',widget=forms.Select(attrs={'class' : 'form-control roundcorner','id':'year'}),choices=yearOfPassing,required=True)
	organisation = forms.CharField(label='Current/Last Organisation:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'organisation'}), max_length=40,required=True)	
	designation = forms.CharField(label='Designation:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'designation'}), max_length=40,required=True)
	#course = forms.ChoiceField(label='Course:',widget=forms.Select(attrs={'class' : 'form-control'}),choices=(('Btech.','Btech.'),("IDD",'IDD'),))
	mobile = forms.CharField(label='Mobile No.:',widget=forms.TextInput(attrs={'class' : 'form-control','style':'display:inline','id':'mobile','placeholder':"Enter your mobile number with country code.For eg +91XXXXXXXXXX"}), max_length=15)
	#home = forms.CharField(label='Mobile No.:',widget=forms.TextInput(attrs={'class' : 'form-control','style':'display:inline'}), max_length=15)

class StudentForm(forms.Form):
	DateInput = partial(forms.DateInput, {'class': 'datepicker'})
	ranges = [(n, min(n+1, 2021)) for n in xrange(1930,2021,1)]
	yearOfPassing=[(n, min(n, 2021)) for n in xrange(1920,2021,1)]
	birthYear=[(n, min(n,1920)) for n in xrange(1930,2005,1)]
	courseChoices=(('UGD', 'UGD',), ('IDD', 'IDD',),('IMD', 'IMD',),('M.Tech./M.Pharm.', 'M.Tech./M.Pharm.',),('Ph.D', 'Ph.D',),)
	branchChoices=(('BC: School of Biochemical Engineering', 'BC: School of Biochemical Engineering',),('BM: School of Biomedical Engineering', 'BM: School of Biomedical Engineering',),('CE: Department of Civil Engineering', 'CE: Department of Civil Engineering',),('CH: Department of Chemical Engineering & Technology', 'CH: Department of Chemical Engineering & Technology',),('CR: Department of Ceramic Engineering', 'CR: Department of Ceramic Engineering',),('CS: Department of Computer Science & Engineering', 'CS: Department of Computer Science & Engineering',),('CY: Department of Chemistry (Applied Chemistry)', 'CY: Department of Chemistry (Applied Chemistry)',),('EC: Department of Electronics Engineering', 'EC: Department of Electronics Engineering',),('EE: Department of Electrical Engineering', 'EE: Department of Electrical Engineering',),('MA: Department of Mathematical Sciences (Applied Maths)', 'MA: Department of Mathematical Sciences (Applied Maths)',),('ME: Department of Mechanical Engineering', 'ME: Department of Mechanical Engineering',),('MN: Department of Mining Engineering', 'MN: Department of Mining Engineering',),('MS: School of Material Science & Technology', 'MS: School of Material Science & Technology',),('MT: Department of Metallurgical Engineering', 'MT: Department of Metallurgical Engineering',),('PH: Department of Pharmaceutics', 'PH: Department of Pharmaceutics',),('PY: Department of Physics (Applied Pysics)', 'PY: Department of Physics (Applied Physics)',),)
	firstName = forms.CharField(label='First Name:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'firstName','placeholder':"Please enter your first name here"}), max_length=20)
	lastName = forms.CharField(label='Last Name:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'lastName','placeholder':"Please enter your last name here"}), max_length=20)
	gender = forms.ChoiceField(label='Gender:',widget=forms.Select(attrs={'class' : 'form-control','id':'gender'}),choices=(('Male','Male'),('Female','Female'),))
	dob=forms.DateField(label='Date Of Birth:',widget=SelectDateWidget(attrs={'class' : 'form-control','style':'width:32.3%;display:inline-block;','id':'dob'},years=range(1930,2005)))
	course = forms.MultipleChoiceField(label="Degree (Select atleast one option):",required=True,widget=forms.CheckboxSelectMultiple(attrs={'class' : 'checkbox-inline','id':'course'}),choices=courseChoices,)
	#motherName = forms.CharField(label="Mother's Name:",widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=40)
	roll=forms.CharField(label='Roll No:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'rollNo','placeholder':"Please enter your Enrollment No."}), max_length=12)
	branch = forms.ChoiceField(label='Department:',widget=forms.Select(attrs={'class' : 'form-control','id':'branch'}),choices=branchChoices)
	year = forms.ChoiceField(label='Graduation Year:',widget=forms.Select(attrs={'class' : 'form-control','id':'year'}),choices=yearOfPassing)
	#course = forms.ChoiceField(label='Course:',widget=forms.Select(attrs={'class' : 'form-control'}),choices=(('Btech.','Btech.'),("IDD",'IDD'),))
	mobile = forms.CharField(label='Mobile No.:',widget=forms.TextInput(attrs={'class' : 'form-control','style':'display:inline','id':'mobile','placeholder':"Enter your mobile number with country code.For eg +91XXXXXXXXXX"}), max_length=15)
	#home = forms.CharField(label='Mobile No.:',widget=forms.TextInput(attrs={'class' : 'form-control','style':'display:inline'}), max_length=15)

class FacultyForm(forms.Form):
	DateInput = partial(forms.DateInput, {'class': 'datepicker'})
	ranges = [(n, min(n+1, 2020)) for n in xrange(1930,2020,1)]
	yearOfPassing=[(n, min(n, 2016)) for n in xrange(1920,2016,1)]
	birthYear=[(n, min(n,1920)) for n in xrange(1930,2002,1)]
	branchChoices=(('BC: School of Biochemical Engineering', 'BC: School of Biochemical Engineering',),('BM: School of Biomedical Engineering', 'BM: School of Biomedical Engineering',),('CE: Department of Civil Engineering', 'CE: Department of Civil Engineering',),('CH: Department of Chemical Engineering & Technology', 'CH: Department of Chemical Engineering & Technology',),('CR: Department of Ceramic Engineering', 'CR: Department of Ceramic Engineering',),('CS: Department of Computer Science & Engineering', 'CS: Department of Computer Science & Engineering',),('CY: Department of Chemistry (Applied Chemistry)', 'CY: Department of Chemistry (Applied Chemistry)',),('EC: Department of Electronics Engineering', 'EC: Department of Electronics Engineering',),('EE: Department of Electrical Engineering', 'EE: Department of Electrical Engineering',),('MA: Department of Mathematical Sciences (Applied Maths)', 'MA: Department of Mathematical Sciences (Applied Maths)',),('ME: Department of Mechanical Engineering', 'ME: Department of Mechanical Engineering',),('MN: Department of Mining Engineering', 'MN: Department of Mining Engineering',),('MS: School of Material Science & Technology', 'MS: School of Material Science & Technology',),('MT: Department of Metallurgical Engineering', 'MT: Department of Metallurgical Engineering',),('PH: Department of Pharmaceutics', 'PH: Department of Pharmaceutics',),('PY: Department of Physics (Applied Pysics)', 'PY: Department of Physics (Applied Physics)',),)
	firstName = forms.CharField(label='First Name:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'firstName','placeholder':"Please enter your first name here"}), max_length=20)
	lastName = forms.CharField(label='Last Name:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'lastName','placeholder':"Please enter your last name here"}), max_length=20)
	gender = forms.ChoiceField(label='Gender:',widget=forms.Select(attrs={'class' : 'form-control','id':'gender'}),choices=(('Male','Male'),('Female','Female'),))
	dob=forms.DateField(label='Date Of Birth:',widget=SelectDateWidget(attrs={'class' : 'form-control','style':'width:32.3%;display:inline-block;','id':'dob'},years=range(1930,2002)))
      	#motherName = forms.CharField(label="Mother's Name:",widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=40)
	
	branch = forms.ChoiceField(label='Department:',widget=forms.Select(attrs={'class' : 'form-control','id':'branch'}),choices=branchChoices)
	year = forms.ChoiceField(label='Joining Year:',widget=forms.Select(attrs={'class' : 'form-control','id':'Joinyear'}),choices=yearOfPassing)
	DesignationChoice=(('Professor','Professor'),('Associate Professor','Associate Professor'),('Assistant Professor','Assistant Professor'),('Research Professor','Research Professor'),('Visiting Professor','Visiting Professor'),('Retired Professor','Retired Professor'),)
	designation =forms.ChoiceField(label='Designation:',widget=forms.Select(attrs={'class' : 'form-control','id':'FacultyDesignation'}),choices=DesignationChoice)
	#course = forms.ChoiceField(label='Course:',widget=forms.Select(attrs={'class' : 'form-control'}),choices=(('Btech.','Btech.'),("IDD",'IDD'),))
	mobile = forms.CharField(label='Mobile No.:',widget=forms.TextInput(attrs={'class' : 'form-control','style':'display:inline','id':'mobile','placeholder':"Enter your mobile number with country code.For eg +91XXXXXXXXXX"}), max_length=15)
	#home = forms.CharField(label='Mobile No.:',widget=forms.TextInput(attrs={'class' : 'form-control','style':'display:inline'}), max_length=15)

	
class PassRecoveryForm(forms.Form):
	password = forms.CharField(label='New Password:',widget=forms.PasswordInput(attrs={'class' : 'form-control','id':'pass'}),)
	passwordC = forms.CharField(label='Confirm Password:',widget=forms.PasswordInput(attrs={'class' : 'form-control','id':'passConfirm'}),)
	
class AddressForm(forms.Form):
	address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'address','placeholder':'Block,Street,City'}), max_length=400)
	city = forms.CharField(label='City:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'city'}), max_length=40)
	state = forms.CharField(label='State:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'state'}), max_length=40)
	country = forms.CharField(label='Country:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'country'}), max_length=40)
		
	zipCode=forms.CharField(label='ZipCode:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'zipCode'}), max_length=40)
class AddressFormPresent(forms.Form):
	addressPresent = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'presentaddress','placeholder':'Block,Street,City'}), max_length=400)
	cityPresent = forms.CharField(label='City:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'presentcity'}), max_length=20)
	statePresent = forms.CharField(label='State:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'presentstate'}), max_length=40)
	countryPresent = forms.CharField(label='Country:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'presentcountry'}), max_length=40)
		
	zipCodePresent=forms.CharField(label='ZipCode:',widget=forms.TextInput(attrs={'class' : 'form-control','id':'presentzipCode'}), max_length=20)

class DocumentForm(forms.Form):
	photo=forms.FileField(label='Select a photo',help_text="max. 5 Mb")



class printstory(forms.ModelForm):
    heading_story = models.CharField(max_length=200)
    content_story = models.CharField(max_length=200)
    date_story = models.DateTimeField()
    who_posted=models.CharField(default=" ")
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Question
        fields = "__all__"

class searchForm(forms.Form):
	branchChoices=(('','',),('BC: School of Biochemical Engineering', 'BC: School of Biochemical Engineering',),('BM: School of Biomedical Engineering', 'BM: School of Biomedical Engineering',),('CE: Department of Civil Engineering', 'CE: Department of Civil Engineering',),('CH: Department of Chemical Engineering & Technology', 'CH: Department of Chemical Engineering & Technology',),('CR: Department of Ceramic Engineering', 'CR: Department of Ceramic Engineering',),('CS: Department of Computer Science & Engineering', 'CS: Department of Computer Science & Engineering',),('CY: Department of Chemistry (Applied Chemistry)', 'CY: Department of Chemistry (Applied Chemistry)',),('EC: Department of Electronics Engineering', 'EC: Department of Electronics Engineering',),('EE: Department of Electrical Engineering', 'EE: Department of Electrical Engineering',),('MA: Department of Mathematical Sciences (Applied Maths)', 'MA: Department of Mathematical Sciences (Applied Maths)',),('ME: Department of Mechanical Engineering', 'ME: Department of Mechanical Engineering',),('MN: Department of Mining Engineering', 'MN: Department of Mining Engineering',),('MS: School of Material Science & Technology', 'MS: School of Material Science & Technology',),('MT: Department of Metallurgical Engineering', 'MT: Department of Metallurgical Engineering',),('PH: Department of Pharmaceutics', 'PH: Department of Pharmaceutics',),('PY: Department of Physics (Applied Pysics)', 'PY: Department of Physics (Applied Physics)',),)
	search_byName = forms.CharField(label='Name:',widget=forms.TextInput(attrs={'class' : 'form-control roundcorner searchname','id':'searchinput'}),required=False)
	search_byYear = forms.IntegerField(label='Year:',widget=forms.NumberInput(attrs={'class' : 'form-control roundcorner searchyear','id':'searchinput','min':'1920','max':'2021'}),required=False)
	search_byDepartment = forms.ChoiceField(label='Department:',widget=forms.Select(attrs={'class' : 'form-control roundcorner searchdept','id':'searchinput'}),choices=branchChoices,required=False)
	
class guestHouse(forms.Form):
	no_of_attendees = forms.IntegerField(label='No. of guest(s):',widget=forms.NumberInput(attrs={'class' : 'form-control roundcorner','id':'attendees','min':'1','max':'200'}),)
	no_of_rooms= forms.IntegerField(label='No. of rooms required:',widget=forms.NumberInput(attrs={'class' : 'form-control roundcorner','id':'rooms','min':'1','max':'200'}),)
        date_end   =forms.CharField(label='Check-out Date:',widget=forms.TextInput(attrs={'class' : 'form-control roundcorner','id':'datepicker_end'}),)
	date_start = forms.CharField(label='Check-in Date:',widget=forms.TextInput(attrs={'class' : 'form-control roundcorner','id':'datepicker_start'}),)
	comments = forms.CharField(label='Comments(if any):',widget=forms.TextInput(attrs={'class' : 'form-control roundcorner','id':'comments'}),required=False)
	mobile = forms.CharField(label='Mobile No.:',widget=forms.TextInput(attrs={'class' : 'form-control','style':'display:inline','id':'mobile','placeholder':"Enter your mobile number with country code.For eg +91XXXXXXXXXX"}), max_length=15)

class OrderForm(forms.Form):
    # cart order related fields
    txnid = forms.CharField(widget=forms.HiddenInput())
    productinfo = forms.CharField(widget=forms.HiddenInput())
    amount = forms.DecimalField(decimal_places=2,widget=forms.HiddenInput(attrs={'id':'amount_field'}))

    # buyer details
    firstname = forms.CharField(widget=forms.HiddenInput())
    lastname = forms.CharField(required=False,widget=forms.HiddenInput())
    email = forms.EmailField(widget=forms.HiddenInput())
    phone = forms.RegexField(regex=r'\d{10}', min_length=10,max_length=15,widget=forms.HiddenInput())
    address1 = forms.CharField(required=False,widget=forms.HiddenInput())
    address2 = forms.CharField(required=False,widget=forms.HiddenInput())
    city = forms.CharField(required=False,widget=forms.HiddenInput())
    state = forms.CharField(required=False,widget=forms.HiddenInput())
    country = forms.CharField(required=False,widget=forms.HiddenInput())
    zipcode = forms.RegexField(regex=r'\d{6}', min_length=6, max_length=6, required=False,widget=forms.HiddenInput())	


class paymentForm(forms.Form):
	delegateOption=(('Indian Delegate', 'Indian Delegate',),('Foreign Delegate', 'Foreign Delegate',),)
	delegate = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control','id':'delegate'}),choices=delegateOption)
	persons_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control','id':'persons_count'}),min_value=1,max_value=6,required=True)
	person1=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'person1','readonly':'readonly'}), max_length=50)
	
	person2=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'person2'}), max_length=50,required=False)
	person3=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'person3'}), max_length=50,required=False)
	person4=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'person4'}), max_length=50,required=False)
	person5=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'person5'}), max_length=50,required=False)
	person6=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','id':'person6'}), max_length=50,required=False)
	terms=forms.MultipleChoiceField(widget=forms.CheckboxInput(attrs={'id':'termsPay','value':"I abide by the <a>terms and conditions</a>"}),required=True)
	
    
