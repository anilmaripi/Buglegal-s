# from tkinter.tix import Form
from django import forms
from django.forms import ChoiceField

from ehrms.models import  Employs,Employee,ContactInfo2

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class DateInput(forms.DateInput):
    input_type = "date"

class AddEmployForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    Manager=forms.CharField(label="Manager",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    empid=forms.CharField(label="empid",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    role=forms.CharField(label="role",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    location=forms.CharField(label="location",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    package=forms.IntegerField(label="package",widget=forms.NumberInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    pincode=forms.IntegerField(label="pincode",widget=forms.NumberInput(attrs={"class":"form-control"}))

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))
    contactno=forms.IntegerField(label="contactno",widget=forms.NumberInput(attrs={"class":"form-control"}))
    dateofjoining=forms.DateField(label="dateofjoining",widget=forms.DateInput(attrs={"class":"form-control"}))

class EditEmployForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    Manager=forms.CharField(label="Manager",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    empid=forms.CharField(label="empid",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    role=forms.CharField(label="role",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    location=forms.CharField(label="location",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    package=forms.IntegerField(label="package",widget=forms.NumberInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    pincode=forms.IntegerField(label="pincode",widget=forms.NumberInput(attrs={"class":"form-control"}))

   

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
    contactno=forms.IntegerField(label="contactno",widget=forms.NumberInput(attrs={"class":"form-control"}))
    dateofjoining=forms.DateField(label="dateofjoining",widget=forms.DateInput(attrs={"class":"form-control"}))

class dataForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'



from .models import YourModel

class YourForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = ('all',)





from .models import Screenshots

class ScreenshotsForm(forms.ModelForm):
    class Meta:
        model = Screenshots
        fields = ['image']



class ContactInfo2Form(forms.ModelForm):
    class Meta:
        model = ContactInfo2
        fields = [
            'address',
            'city',
            'state',
            'zip_code',
            'country',
            'phone_number',
            'phone_hours',
            'email_addresses',
        ]
        widgets = {
            'email_addresses': forms.Textarea(attrs={'rows': 3}),  # Adjust textarea for email entry
        }

    def clean_email_addresses(self):
        email_addresses = self.cleaned_data['email_addresses']
        # Validate email addresses here (e.g., using a regular expression)
        return email_addresses


from .models import IntroContent, Step,Trail,clock,assignqns3,breaksqns4

class IntroContentForm(forms.ModelForm):
    class Meta:
        model = IntroContent
        fields = ['title', 'intro_text', 'setup_text', 'image','image2']

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['intro_content', 'step_text']




class TrailForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = ['title', 'steps', 'image']


class InstructionForm(forms.ModelForm):
    class Meta:
        model = clock  # Specify the model to use
        fields = ['title', 'des1', 'des2', 'steps']  # Specify which fields to include in the form

class InstructionForm1(forms.ModelForm):
    class Meta:
        model = assignqns3  
        fields = ['title', 'des1', 'des2', 'steps']  



class InstructionForm2(forms.ModelForm):
    class Meta:
        model = breaksqns4  
        fields = ['title', 'des1', 'des2', 'steps']  


