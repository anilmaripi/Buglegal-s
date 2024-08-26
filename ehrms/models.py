from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime,timedelta,date
from ckeditor.fields import RichTextField
from matplotlib.pyplot import show

# Create your models here.


class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Employs"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    reg_date = models.DateTimeField(default=datetime.now, blank=True)
    def save_login_record(self):
        login_record = EmployeeLoginLogout(employee=self.employs, login_time=datetime.now())
        login_record.save()

    def save_logout_record(self):
        latest_login_record = EmployeeLoginLogout.objects.filter(employee=self.employs).latest('login_time')
        latest_login_record.logout_time = datetime.now()
        latest_login_record.save()


from django.db import models
from django.contrib.auth.models import User

class Companys(models.Model):
    usernumber = models.OneToOneField(CustomUser, on_delete=models.CASCADE,default="1")
    organizationname = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=5, unique=True, editable=False)
    address = models.TextField()
    contact_person = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=100, default="")
    Numberofemployees = models.CharField(max_length=100, default="")
    your_title = models.CharField(max_length=100, default="")
    otp = models.CharField(max_length=4, default="")
    agreement_status = models.IntegerField(default="3")
    profilepic=models.ImageField(upload_to="media/",default="") 
    plantype=models.CharField(max_length=100,default=1)
    date=models.DateField(default=date.today) 
    freetraile=models.IntegerField(default=1)


    def save_company(self):
        self.save()

    def save(self, *args, **kwargs):
        # If registration number is not provided, generate a new one
        if not self.registration_number:
            last_company = Companys.objects.order_by('-id').first()
            if last_company:
                last_registration_number = int(last_company.registration_number)
                new_registration_number = str(last_registration_number + 1).zfill(5)
            else:
                new_registration_number = "20231"

            self.registration_number = new_registration_number

        super(Companys, self).save(*args, **kwargs)


    def __str__(self):
        return self.name





class AdminHod(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    firstname=models.CharField(max_length=100,default="")
    lastname=models.CharField(max_length=100,default="")
    username=models.CharField(max_length=100,default="")
    password=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100,default="")
    empid=models.CharField(max_length=100,default="")
    phnos = models.CharField(max_length=20, default="")  
    address=models.CharField(max_length=50,default="")
    dateofbirth = models.DateField(default=date.today())
    dateofjoining = models.DateField(default=date.today())
    Department=models.CharField(max_length=100,default="")
    manager=models.CharField(max_length=100,default="")
    gender=models.CharField(max_length=100,default="")
    location=models.CharField(max_length=100,default="")
    package=models.IntegerField(default=0)
    pincode=models.IntegerField(default=0)
    designation=models.CharField(max_length=100,default="")
    status=models.CharField(max_length=100,default="")
    bloodgroup=models.CharField(max_length=100,default="")
    adminprofilepic=models.ImageField(upload_to="media/",default="")
    options=models.CharField(max_length=100,default="")
    objects=models.Manager()
   
class typeofplans(models.Model):
    icon1=models.CharField(max_length=100)
    plans=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    annual_price = models.CharField(max_length=100)
    employe_limit = models.IntegerField(default=0)
    price_for_annual = models.CharField(max_length=100,default="")

class Meta:
    db_table="typeofplans" 


class featurestypes(models.Model):
    name=RichTextField() 
    parent_feature = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='sub_features')
    show1=models.BooleanField(default=0)
    show2=models.BooleanField(default=0)
    show3=models.BooleanField(default=0)

class SelectedPlan(models.Model):
    plan_type = models.ForeignKey('typeofplans', on_delete=models.CASCADE)
    features = models.ManyToManyField('featurestypes')

    def __str__(self):
        return f"{self.plan_type.plantype} - Features: {', '.join([feature.name for feature in self.features.all()])}"

class projectmanagement(models.Model):
    title=models.CharField(max_length=100)
    subtitle=models.CharField(max_length=100)
    image1=models.ImageField(upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")

    discription=models.CharField(max_length=1000)

class Meta:
    db_table="projectmanagement"  



class projectmanagement2(models.Model):
        title=models.CharField(max_length=100)
        discription=models.CharField(max_length=1000)
        title2=models.CharField(max_length=100,default="")
        subtitle2=models.CharField(max_length=100,default="")
        title3=models.CharField(max_length=100,default="")
        title4=models.CharField(max_length=100,default="")



class Meta:
    db_table="projectmanagement2"    



class  projectmanagement3(models.Model):
        title=models.CharField(max_length=100)
        discription=models.CharField(max_length=1000)
        image=models.ImageField(upload_to="media/")

class Meta:
    db_table="projectmanagement3" 

class Addplans(models.Model):
    plan_name = models.CharField(max_length=1000)
    featue1 = RichTextField()
    featue2 = RichTextField()
    featue3 = RichTextField()
    descrption1 = RichTextField()
    descrption2 = RichTextField()

class Meta:
    db_table="Addplans"


class FAQItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    link = models.URLField(blank=True, null=True)  
    email = models.EmailField(blank=True, null=True) 

    def __str__(self):
        return self.question
class Companyregister(models.Model):
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20)
    address = models.TextField()
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100,default="")
    Numberofemployees = models.CharField(max_length=100,default="")
    your_title = models.CharField(max_length=100,default="")
    agreement_status = models.IntegerField(default="0")
    contact_person = models.CharField(max_length=50,default="")
    otp = models.CharField(max_length=4, default="")
    usernumber = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    owner_name = models.CharField(max_length=255 ,default="")
    card_number = models.CharField(max_length=16,default="")
    expiration_date = models.CharField(max_length=5,default="")  # Assuming MM/YY format
    cvv = models.CharField(max_length=3,default="")

    def __str__(self):
        return f'{self.owner_name} - {self.card_number}'
      
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If registration number is not provided, generate a new one
        if not self.registration_number:
            last_company = Companyregister.objects.order_by('-id').first()
            if last_company:
                last_registration_number = int(last_company.registration_number)
                new_registration_number = str(last_registration_number + 1).zfill(5)
            else:
                new_registration_number = "00001"

            self.registration_number = new_registration_number

        super(Companyregister, self).save(*args, **kwargs)


    def __str__(self):
        return self.name 

class list(models.Model):
    name=models.CharField(max_length=100)
class meta:
    db_table="list"
class login1(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
class Meta:
    db_table="login" 
class working_shifts(models.Model):

    starting_time = models.TimeField(default='08:00')
    ending_time = models.TimeField(default='17:00')
    cutoff_time = models.PositiveIntegerField(default="10")
    shift_name = models.CharField(max_length=100)
    befor_time=models.PositiveIntegerField(default="2")
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
    extra_time1=models.PositiveIntegerField(default="10")

    def get_shift_duration(self):
        """
        Calculate and return the duration of the shift in hours.
        """
        if self.starting_time and self.ending_time:
            start_datetime = datetime.combine(datetime.now(), self.starting_time)
            end_datetime = datetime.combine(datetime.now(), self.ending_time)
            duration_hours = (end_datetime - start_datetime).total_seconds() 
            return round(duration_hours, 2) 
        return 0.0

class Meta:
    db_table="working_shifts" 
    def get_shift_name(self):
        if self.working:
            return self.working.shift_name
        else:
            return "N/A" 


class documents_setup1(models.Model):
    document_type = models.CharField(max_length=100, null=True, blank=True)
    compulsory=models.CharField(max_length=100)
    Enabled=models.CharField(max_length=100)
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")

class Meta:
    db_table="documents_setup1"  

class emidata(models.Model):
    eminumber=models.IntegerField(default=0)
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")

    class Meta:
        db_table="emidata"
class employ_designation3(models.Model):
    
    designation_name=models.CharField(max_length=100)
    Enabled=models.CharField(max_length=100,default='')
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="",related_name='designations')
    class Meta:
        db_table="employ_designation3"

class Employs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
      # shift_name = models.CharField(max_length=100,default="")
    working= models.ForeignKey(working_shifts, on_delete=models.CASCADE , related_name='workshifts', null=True)
    working12=models.CharField(max_length=100,default="a")
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    web_mail=models.CharField(max_length=100,default="")
    username=models.CharField(max_length=100,default="")
    password=models.CharField(max_length=100,default="")
    gender=models.CharField(max_length=255)
    profile_pic=models.FileField(upload_to='media/')
    address=models.TextField()
    empid=models.CharField(max_length=100)
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="1")
    dateofjoining=models.DateField(default=date.today())
    designation=models.CharField(max_length=100)
    dateofbirth=models.DateField(default=date.today())
    location=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    contactno=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default="")
    bloodgroup=models.CharField(max_length=100,default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    insert=models.CharField(max_length=500,default="")
    is_team_lead = models.BooleanField(default=False)
    role=models.CharField(max_length=100,default="")
    hroptions=models.IntegerField(default=0)
    projectmanagerop=models.IntegerField(default=0)
    b_name = models.CharField(max_length=100,default="")
    insert = models.CharField(max_length=500,default="")
    is_team_lead = models.BooleanField(default=False)
    desktop_user_identifier = models.UUIDField(blank=True, null=True, unique=True)
    device_identifier = models.UUIDField(blank=True, null=True, unique=True)
    is_launched = models.BooleanField(default=False)
    face_encoding = models.BinaryField(null=True, blank=True)
    fcm_token=models.TextField()
    objects = models.Manager()
    extra_time=models.PositiveIntegerField(default="0")
    receptionist_option=models.IntegerField(default=0)
    designation_employ= models.ForeignKey(employ_designation3, on_delete=models.SET_NULL , related_name='desgination', null=True)


    def missing_info(self):
        required_info=['profile_pic']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info
    # def get_shift_name(self):
    #     if self.working:
    #         return self.working.shift_name
    #     else:
    #         return "N/A"  # Provide a default value if no working shift is assigned


    def __str__(self):
        return self.last_name
    
    def calculate_overall_performance(self):
        completed_tasks = self.employeeids.filter(t_status='completed')
        total_tasks = self.employeeids.all()
        high_priority_tasks = completed_tasks.filter(t_priority='High').count()
        medium_priority_tasks = completed_tasks.filter(t_priority='Medium').count()
        low_priority_tasks = completed_tasks.filter(t_priority='Low').count()

        performance_score = (high_priority_tasks * 10 + medium_priority_tasks * 5 + low_priority_tasks * 2)

        return {
            'total_tasks_taken': total_tasks.count(),
            'total_tasks_completed': completed_tasks.count(),
            'high_priority_tasks_completed': high_priority_tasks,
            'medium_priority_tasks_completed': medium_priority_tasks,
            'low_priority_tasks_completed': low_priority_tasks,
            'performance_score': performance_score,
        }

    def __str__(self):
        return self.last_name


    
    def __str__(self):
        return self.profile_pic
    

from django.utils import timezone


class EmployeeLoginLogout(models.Model):
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.login_time}"

    def get_total_duration(self):
        if self.logout_time:
            return self.logout_time - self.login_time
        else:
            return None  # Indicate "Employee not logged out"

    def get_duration_since_last_logout(self):
        latest_logout = EmployeeLoginLogout.objects.filter(
            employee=self.employee,
            logout_time__isnull=False
        ).exclude(id=self.id).latest('logout_time')

        return self.login_time - latest_logout.logout_time if latest_logout else None
from datetime import date
class admin_project_create(models.Model):
    companyid=models.ForeignKey(Companys, on_delete=models.CASCADE)
    project_name=models.CharField(max_length=100)
    project_dec=models.CharField(max_length=100)
    admin_id=models.ForeignKey(Employs, on_delete=models.CASCADE)

    date=models.DateField(default=date.today) 
    status=models.CharField(max_length=100,default="")
    is_status=models.CharField(max_length=100,default="0")
    read = models.BooleanField(default=False)
    class Meta:
        db_table = "admin_project_create"

class Project(models.Model):
    p_name = models.CharField(max_length=100)
    p_desc = models.CharField(max_length=200)
    o_id = models.ForeignKey(Employs, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default="")
    project_deadline = models.DateTimeField(default=timezone.now)
    project_manager = models.CharField(max_length=100,default="")
    proj = models.ForeignKey(admin_project_create, on_delete=models.CASCADE, null=True,blank=True) 
    companyid = models.ForeignKey(Companys, on_delete=models.CASCADE,null=True,blank=True)
 


    def calculate_project_performance(self):
        completed_tasks = self.projectids.filter(t_status='completed')
        total_tasks_count = self.projectids.count()
        completed_tasks_count = completed_tasks.count()
        pending_tasks = self.projectids.filter(t_status='todo')
        if total_tasks_count == 0:
            return 0  # Avoid division by zero error

        completion_rate = (completed_tasks_count / total_tasks_count) * 100

        return {
            'completion_rate': completion_rate,
            'total_tasks': total_tasks_count,
            'pending_tasks': pending_tasks.count(),
            'completed_tasks':completed_tasks_count
        }

    class Meta:
        db_table = "project"

    def __str__(self):
        return self.p_name
    
    # def get_team_leader(self):
    #     try:
    #         # Get the team member who is the team leader for this project
    #         team_leader = self.teammember_set.get(is_team_lead=True)
    #         team_first_name = team_leader.employee.first_name
    #         team_last_name = team_leader.employee.last_name
    #         team_role = team_leader.employee.role
    #         team_empid = team_leader.employee.empid
    #         team_id = team_leader.employee.id
    #         return {
    #            'team_first_name': team_first_name,
    #            'team_last_name':team_last_name,
    #            'team_role':team_role,
    #            'team_empid':team_empid,
    #            'team_id':team_id
    #         }
    #     except TeamMember.DoesNotExist:
    #         return "No team leader assigned"


    def get_team_leader(self):
        try:
            # Get the team member who is the team leader for this project
            team_leader = self.teammember_set.get(is_team_lead=True)
            team_first_name = team_leader.employee.first_name
            team_last_name = team_leader.employee.last_name
            team_role = team_leader.employee.role
            team_empid = team_leader.employee.empid
            team_id = team_leader.employee.id
            return {
            'team_first_name': team_first_name,
            'team_last_name': team_last_name,
            'team_role': team_role,
            'team_empid': team_empid,
            'team_id': team_id,
            }
        except TeamMember.DoesNotExist:
            return {
                'team_first_name': None,
                'team_last_name': None,
                'team_role': None,
                'team_empid': None,
                'team_id': None,
            }

        

class TeamMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE)
    is_team_lead = models.BooleanField(default=False) 

    class Meta:
        unique_together = ('project', 'employee')
        db_table = "team_member"

    def calculate_total_score_in_project(self):
        # Calculate the total score for tasks in the current project
        tasks = Task.objects.filter(e_id=self.employee, p_id=self.project, t_status='completed')
        total_score = sum(task.calculate_task_score() for task in tasks)
        return total_score

    def calculate_total_score_across_all_projects(self):
        total_score = 0

        # Get all projects associated with the employee
        projects = Project.objects.filter(teammember__employee=self.employee)

        for project in projects:
            # Get completed tasks for the current project
            tasks = Task.objects.filter(e_id=self.employee, p_id=project, t_status='completed')

            # Calculate the score for tasks in the current project
            project_score = sum(task.calculate_task_score() for task in tasks)

            # Add the project score to the total score
            total_score += project_score

        return total_score
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} on {self.project.p_name}"

class HR(models.Model):
    b_name = models.CharField(max_length=100,default="")
    o_id = models.ForeignKey(AdminHod, on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    web_mail=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    gender=models.CharField(max_length=255)
    address=models.TextField()
    empid=models.CharField(max_length=100)
    Manager=models.CharField(max_length=100)
    dateofbirth = models.DateField(default=date.today())
    dateofjoining=models.DateField(default=date.today())
    role=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    contactno=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    bloodgroup=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    insert=models.CharField(max_length=500)
    is_team_lead = models.BooleanField(default=False)
    hroptions=models.IntegerField(default=1)
    fcm_token=models.TextField()
    objects = models.Manager()

class project_drop(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url=models.CharField(max_length=100)
    edit=models.BooleanField(default=1)
    show1=models.BooleanField(default=0)
    show2=models.BooleanField(default=0)
    show3=models.BooleanField(default=0)
    parent_category = models.ForeignKey('self', related_name='subdrop', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the task is 'ADD Employee Performance Task'
        if self.name == 'ADD Employee Performance Task':
            # Update the 'show' field for related records based on the value
            related_records = project_drop.objects.filter(
                name__in=['']
            )
            adminnames=admin_drop.objects.filter(name__in=['Employ Performance'])
            employdrop=employ_drop.objects.filter(name__in=['Employ Performance'])
            related_records.update(show1=self.show1,show2=self.show2,show3=self.show3)
            adminnames.update(show1=self.show1,show2=self.show2,show3=self.show3)
            employdrop.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name =='Create New Task':
            samenumber=employnav.objects.filter(name__in=['ASSIGN-TASK TO TEAM MEMBERS','DAILY TASK '])
            samenumber.update(show1=self.show1)

        if self.name == "Projects":
            namqq=featurestypes.objects.filter(name__in=["Add Employes Performance Task"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        
        if self.name == "Projects":
            namqq=featurestypes.objects.filter(name__in=["Create New Task"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)

        if self.name == "Projects":
            namqq=featurestypes.objects.filter(name__in=["Send The Review Link"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)

        if self.name == "project status":
            namqq=featurestypes.objects.filter(name__in=["project status"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)

        if self.name == "Daily Task Report":
            namqq=featurestypes.objects.filter(name__in=["Daily Task Report"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)

        if self.name == "Project List":
            namqq=featurestypes.objects.filter(name__in=["Project List"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)

class Task(models.Model):
    t_name = models.CharField(max_length=55)
    t_desc = models.CharField(max_length=200)
    t_status = models.CharField(max_length=55)
    t_priority = models.CharField(max_length=30)
    t_assign_date = models.DateTimeField(auto_now_add=True )
    t_deadline_date = models.DateTimeField()
    t_update_date = models.DateTimeField(default=timezone.now)
    is_expired = models.BooleanField(default=False)
    b_id = models.ForeignKey(HR, on_delete=models.CASCADE, related_name='HRids')
    p_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectids')
    o_id = models.ForeignKey(Employs, on_delete=models.CASCADE,null=True, blank=True)
    e_id = models.ForeignKey(Employs, on_delete=models.CASCADE, related_name='employeeids')
    
    def calculate_task_score(self):
        score = 0

        if self.t_status == "completed":
            time_difference = self.t_deadline_date - self.t_update_date

            if self.t_priority == "High":
                if time_difference > timedelta(days=0):
                    # Task completed before the deadline
                    score = 15 + int(time_difference.total_seconds() / 3600)  # Add score based on hours before the deadline
                else:
                    # Task completed after the deadline
                    score = 5 - int(abs(time_difference.total_seconds()) / 3600)  # Subtract score based on hours after the deadline

            elif self.t_priority == "Medium":
                if time_difference > timedelta(days=0):
                    score = 10 + int(time_difference.total_seconds() / 3600)
                else:
                    score = 3 - int(abs(time_difference.total_seconds()) / 3600)

            elif self.t_priority == "Low":
                if time_difference > timedelta(days=0):
                    score = 5 + int(time_difference.total_seconds() / 3600)
                else:
                    score = 1 - int(abs(time_difference.total_seconds()) / 3600)

        return score

    def calculate_remaining_time(self):
        if self.t_status == "completed":
            return None  # Task is already completed, no remaining time

        current_time = timezone.now()
        remaining_time = self.t_deadline_date - current_time

        # Ensure remaining time is positive (no negative remaining time)
        if remaining_time.total_seconds() < 0:
            return None

        return remaining_time
    class Meta:
        db_table = "task"

class Project_Employee_Linker(models.Model):
    p_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    e_id = models.ForeignKey(Employs, on_delete=models.CASCADE)
    o_id = models.ForeignKey(AdminHod, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('p_id', 'e_id','o_id')
        db_table = "project_emp_assign"



class types(models.Model):
    name=models.CharField(max_length=100)
   
class meta:
    db_table="types"

class Reimbursement(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    typea=models.CharField(max_length=100,default='')
    date=models.DateField(default=None)
    detail=models.CharField(max_length=5000)
    amount=models.IntegerField()
    image=models.ImageField(upload_to="media/")
    reimbursement_status=models.IntegerField(default=0)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    objects=models.Manager()

class WorkProductivityDataset(models.Model):
    w_pds = models.CharField(max_length=255)
    w_type = models.CharField(max_length=255)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        db_table = "WorkProductivityDataset"


class home6(models.Model):
   image=models.ImageField(upload_to='images/',default="")
   content=models.CharField(max_length=900,default="")
   d1=models.CharField(max_length=200,default="")
   d2=models.CharField(max_length=200,default="")
   d3=models.CharField(max_length=200,default="")
   d4=models.CharField(max_length=200,default="")
   d5=models.CharField(max_length=200,default="")
   image1=models.ImageField(upload_to='images/',default="")
   content1=models.CharField(max_length=900,default="")
   d6=models.CharField(max_length=200,default="")
   d7=models.CharField(max_length=200,default="")
   d8=models.CharField(max_length=200,default="")
   d9=models.CharField(max_length=200,default="")
   d10=models.CharField(max_length=200,default="")
   d11=models.CharField(max_length=200,default="")
   d12=models.CharField(max_length=200,default="")
   image2=models.ImageField(upload_to='images/',default="")
   content2=models.CharField(max_length=900,default="")
   d13=models.CharField(max_length=200,default="")
   d14=models.CharField(max_length=200,default="")
   d15=models.CharField(max_length=200,default="")
   d16=models.CharField(max_length=200,default="")
   d17=models.CharField(max_length=200,default="")
   d18=models.CharField(max_length=200,default="")
   image3=models.ImageField(upload_to='images/',default="")
   content3=models.CharField(max_length=900,default="")
   d19=models.CharField(max_length=200,default="")
   d20=models.CharField(max_length=200,default="")
   d21=models.CharField(max_length=200,default="")
   d22=models.CharField(max_length=200,default="")
   d23=models.CharField(max_length=200,default="")
   d24=models.CharField(max_length=200,default="")
   d25=models.CharField(max_length=200,default="")
   content1=models.CharField(max_length=200,default="")
   content2=models.CharField(max_length=200,default="")
   content3=models.CharField(max_length=200,default="")
   content4=models.CharField(max_length=200,default="")
   content5=models.CharField(max_length=200,default="")
   content6=models.CharField(max_length=200,default="")


class Meta:
    db_table="home6"




class MonitoringDetails(models.Model):
    md_title = models.CharField(max_length=200)
    md_total_time_seconds = models.CharField(max_length=200)
    md_date = models.CharField(max_length=200)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE )
    company = models.ForeignKey(Companys , on_delete=models.CASCADE,null=True,blank=True)

    

    class Meta:
        db_table = "MonitoringDetails"

class SystemStatus(models.Model):
    STATUS_CHOICES = [
        ('battery', 'Battery'),
        ('online', 'Online'),
         
    ]

    status_type = models.CharField(max_length=20, choices=STATUS_CHOICES)
    status_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE )
    company = models.ForeignKey(Companys , on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.status_type}: {self.status_message}"
    
class Screenshots(models.Model):
    image = models.ImageField(upload_to='screenshots/')
    timestamp =models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE )
    company = models.ForeignKey(Companys , on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = "Screenshots"




class Admin_Reimbursement(models.Model):
    id=models.AutoField(primary_key=True)
    admin_id=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    typea=models.CharField(max_length=100,default='')
    date=models.DateField(default=None)
    detail=models.CharField(max_length=5000)
    amount=models.IntegerField()
    image=models.ImageField(upload_to="media/")
    reimbursement_status=models.IntegerField(default=0)
    objects=models.Manager()

class adminnav(models.Model):
    name=models.CharField(max_length=100)
    icon=models.CharField(max_length=100)
    url=models.CharField(max_length=100)
    show1=models.BooleanField(default=0)
    show2=models.BooleanField(default=0)
    show3=models.BooleanField(default=0)
    is_name_exist = models.BooleanField(default=True)
    is_projectmanager= models.BooleanField(default=True)
    is_admin=models.BooleanField(default=True)
    
class employnav(models.Model):
    name=models.CharField(max_length=100)
    icon=models.CharField(max_length=100)
    url=models.CharField(max_length=100)
    show1=models.BooleanField(default=0)
    show2=models.BooleanField(default=0)
    show3=models.BooleanField(default=0)
    edit=models.BooleanField(default="0")
    is_name_exist = models.BooleanField(default=True)
    is_tl_option=models.BooleanField(default="0")
    hr_options=models.BooleanField(default="0")
    employ_options=models.BooleanField(default="1")
    projectmanager_options=models.BooleanField(default="1")
    receptionist_option=models.BooleanField(default="0")
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.name == 'MY PAY SLIP':
            related_records = adminnav.objects.filter(
                name__in=['MY PAY SLIP']
            )
            related_records.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == 'ATTENDANCE':
            attend=adminnav.objects.filter(name__in=['ATTENDANCE'])
            attend.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "REIMBURSEMENTS":
            reimbu=adminnav.objects.filter(name__in=['REIMBURSEMENTS'])
            reimbu.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == 'DOCUMENTS':
            documen=adminnav.objects.filter(name__in=['DOCUMENTS'])
            documen.update(show1=self.show1,show2=self.show2,show3=self.show3)
class employ_drop(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    url=models.CharField(max_length=100)
    show1=models.BooleanField(default=0)
    show2=models.BooleanField(default=0)
    show3=models.BooleanField(default=0)
    parent_category = models.ForeignKey('self', related_name='subdrop', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class admin_drop(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url=models.CharField(max_length=100)
    show=models.BooleanField(default=0)
    parentshow=models.BooleanField(default=0)
    show1=models.BooleanField(default=0)
    show2=models.BooleanField(default=0)
    show3=models.BooleanField(default=0)
    edit=models.BooleanField(default=1)
    parentshow=models.BooleanField(default=0)
    addon=models.BooleanField(default=0)
    parent_category = models.ForeignKey('self', related_name='subdrop', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.name == 'People':
            related_records = employ_drop.objects.filter(
                name__in=['PEOPLE']
            )
            related_records.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "Advance Salary":
            namqq=featurestypes.objects.filter(name__in=["Advance Salary"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "Company Details":
            namqq=featurestypes.objects.filter(name__in=["Company Details"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
   
        if self.name == "Create Project":
            namqq=featurestypes.objects.filter(name__in=["Create Project"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
   
   
        if self.name == "Daily Task Report":
            namqq=featurestypes.objects.filter(name__in=["Daily Task Report"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
            
        if self.name == "People":
            namqq=featurestypes.objects.filter(name__in=["People"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
   
        if self.name == "Project List":
            namqq=featurestypes.objects.filter(name__in=["Project List"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
   
        if self.name == "Add Employee Performance Task":
            namqq=featurestypes.objects.filter(name__in=["Add Employee Performance Task"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
   
        if self.name == "Create New Task":
            namqq=featurestypes.objects.filter(name__in=["Create New Task"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
   
        if self.name == "project status":
            namqq=featurestypes.objects.filter(name__in=["project status"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
   
        if self.name == "Send The Review Link":
            namqq=featurestypes.objects.filter(name__in=["Send The Review Link"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "screenshots":
            namqq=featurestypes.objects.filter(name__in=["screenshots"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        
        
        if self.name == "Detailed Monitoring":
            namqq=featurestypes.objects.filter(name__in=["Detailed Monitoring"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        
        if self.name == "Daily Task Report":
            namqq=featurestypes.objects.filter(name__in=["Daily Task Report"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        
        if self.name == "Employes Project Performance":
            namqq=featurestypes.objects.filter(name__in=["Employes Project Performance"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "Employ Performance":
            namqq=featurestypes.objects.filter(name__in=["Employ Performance"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
            project=project_drop.objects.filter(name__in=["Employ Performance"])
            project.update(show1=self.show1,show2=self.show2,show3=self.show3)
            empdrop=employ_drop.objects.filter(name__in=["Employ Performance"])
            empdrop.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "Report":
            report=employ_drop.objects.filter(name__in=['REPORTS'])
            report.update(show1=self.show1,show2=self.show2,show3=self.show3)

        if self.name == "Visitor Entry":
            namqq=featurestypes.objects.filter(name__in=["Visitor Entry"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)     


        if self.name == "Complaints":
            namqq=featurestypes.objects.filter(name__in=["Complaints"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3) 

        if self.name == "Send Messages ":
            namqq=featurestypes.objects.filter(name__in=["Send Messages"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)           
        
    




class admin_home_drop(models.Model):
    dashname = models.CharField(max_length=200, db_index=True)
    url=models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', related_name='subhomedrop', blank=True, null=True, on_delete=models.CASCADE)
    progress_value=models.IntegerField(default="0")
    check_value=models.IntegerField(default="0")
    edit_url=models.CharField(max_length=100,default="")
    class Meta:
        ordering = ('dashname',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.dashname



class loc_role_dropdown(models.Model):
    location=models.CharField(max_length=100)
    role=models.CharField(max_length=100)


class duration_year(models.Model):
    years=models.CharField(max_length=100)
    objects=models.Manager()

class duration_months(models.Model):
    months=models.CharField(max_length=100)
    objects=models.Manager()
    
class empdocs(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    empid=models.CharField(max_length=100)
    documenttype1=models.CharField(max_length=100)
    imagefile=models.ImageField(upload_to='images/')
    description=RichTextField()
    date=models.DateTimeField(default=datetime.now)
    email=models.CharField(max_length=100,default="")
    company=models.ForeignKey(Companys,on_delete=models.CASCADE,default="")
    objects=models.Manager()
    def missing_info(self):
        required_info=['documenttype1','imagefile','description']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.documenttype

class documents_setup(models.Model):
    document_type=models.CharField(max_length=100)
    compulsory=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))
    Enabled=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))

class Meta:
    db_table="documents_setup"    
   

class admin_doc(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    emp_id=models.CharField(max_length=100)
    documenttype1=models.CharField(max_length=100)
    imagefile1=models.ImageField(upload_to='media/')
    description=models.TextField()
    date=models.DateTimeField(default=datetime.now)
    objects=models.Manager()
    class Meta:
         db_table="admin_doc"




class typeofd(models.Model):    
    certificates=models.CharField(max_length=100)


class depart(models.Model):
    department=models.CharField(max_length=100)

    def __str__(self):
        return self.department
class Meta:
    db_table="depart"

class loca(models.Model):
    location=models.CharField(max_length=100)
    def __str__(self):
        return self.location
class Meta:
    db_table="loca"

class Employee_runpay(models.Model):
    employee_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department= models.ForeignKey(depart,on_delete=models.CASCADE)
    location = models.ForeignKey(loca,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    monthly_ctc = models.DecimalField(max_digits=10, decimal_places=2)
    addition = models.DecimalField(max_digits=10, decimal_places=2)
    deduction = models.DecimalField(max_digits=10, decimal_places=2)
    reimbursement = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.gross_pay = float(self.monthly_ctc) + float(self.addition) - float(self.deduction) + float(self.reimbursement)
        super(Employee_runpay, self).save(*args, **kwargs)
class Meta:
    db_table="Employee_runpay"


class year(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    fin_year=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    objects=models.Manager()


class LeaveReportEmploy(models.Model):
    id=models.AutoField(primary_key=True)
    leave_type=models.CharField(max_length=100,default="")
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    leave_date=models.DateField()
    email_leave=models.CharField(max_length=100,default="")
    to_date=models.DateField()
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def get_leave_duration(self):
        """
        Calculate and return the number of days for this leave request.
        """
        if self.leave_date and self.to_date:
            duration = (self.to_date - self.leave_date).days + 1  # Include both start and end days
            if duration == 2 and self.leave_date == self.to_date:
                return 1  # Consider a one-day leave with same start and end dates as one day
            return duration
        return 0

class LeaveReportAdmin(models.Model):
    id=models.AutoField(primary_key=True)
    leave_type=models.CharField(max_length=100)
    admin=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    to_date=models.CharField(max_length=255,default="")
    leave_message=models.TextField()    
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class employ_add_form(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Employs,on_delete=models.CASCADE,default="")
    firstname1=models.CharField(max_length=100,default="" )
    lastname1=models.CharField(max_length=100,default="")
    email2=models.CharField(max_length=100,default="")
    pan=models.CharField(max_length=100)
    ifsecode=models.CharField(max_length=100)
    acno = models.BigIntegerField(null=True, blank=True)
    beneficiaryname=models.CharField(max_length=100)
    phno=models.BigIntegerField()
    gender1=models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    address1=models.CharField(max_length=500)
    heq=models.CharField(max_length=100)
    aadharno=models.BigIntegerField()
    fathername=models.CharField(max_length=100,default="")
    fathersdob=models.DateField(blank=True,null=True)
    mothername=models.CharField(max_length=100,default="")
    mothersdob=models.DateField(blank=True,null=True)
    Childdetails1=models.CharField(max_length=100,default="")
    Childdetails2=models.CharField(max_length=100,default="")
    maritalstatus=models.CharField(max_length=100,default="")
    workexperiance=models.CharField(max_length=100,default="")
    previousemploye=models.CharField(max_length=100,default="")
    previousdesignation=models.CharField(max_length=100,default="")
    Marriageannivarsary=models.CharField(max_length=100,default="")
    emergencycontactname=models.CharField(max_length=100,default="")
    emergencycontactnumber=models.CharField(max_length=100,default="")
    emergencycontactrelation=models.CharField(max_length=100,default="")
    nationality=models.CharField(max_length=100,default="")
    qualification=models.CharField(max_length=100,default="")

    bloodgroup=models.CharField(max_length=100)
    profile_pic=models.FileField(upload_to='media/')

    objects=models.Manager()
    def missing_info(self):
        required_info=['pan','ifsecode','acno','beneficiaryname','phno','gender1','dob','address1','heq','aadharno','bloodgroup','profile_pic']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.pan
        

class task1(models.Model):
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)

    Personalphonenumber1=models.CharField(max_length=100)
    PersonalEmailAddress1=models.CharField(max_length=100)
    FathersName1=models.CharField(max_length=100)
    FathersDOB1=models.CharField(max_length=100)
    MothersName1=models.CharField(max_length=100)
    MothersDOB1=models.CharField(max_length=100)
    SpousesName1=models.CharField(max_length=100)
    SpousesDOB1=models.CharField(max_length=100)
    Childdetails1=models.CharField(max_length=100)
    Childdetails2=models.CharField(max_length=100)
    TemporaryAddress1=models.CharField(max_length=100)
    HighestEducatonalQualification1=models.CharField(max_length=100)
    Addharnumber1=models.CharField(max_length=100)
    maritalstatus1=models.CharField(max_length=100)
    workexperiance1=models.CharField(max_length=100)
    previousemploye1=models.CharField(max_length=100)
    previousdesignation1=models.CharField(max_length=100)
    Marriageannivarsary1=models.CharField(max_length=100)
    emergencycontactname1=models.CharField(max_length=100)
    emergencycontactnumber1=models.CharField(max_length=100)
    emergencycontactrelation1=models.CharField(max_length=100)
    bloodgroup1=models.CharField(max_length=100)
    nationality=models.CharField(max_length=100)


        
class admin_add_form1(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")
    firstname1=models.CharField(max_length=100,default="" )
    lastname1=models.CharField(max_length=100,default="")
    email2=models.CharField(max_length=100,default="")
    pan=models.CharField(max_length=100)
    ifsecode=models.CharField(max_length=100)
    acno=models.BigIntegerField()
    beneficiaryname=models.CharField(max_length=100)
    phno=models.BigIntegerField()
    gender1=models.CharField(max_length=100)
    dob=models.DateField()
    address1=models.CharField(max_length=500)
    heq=models.CharField(max_length=100)
    aadharno=models.BigIntegerField()
    bloodgroup=models.CharField(max_length=100)
    objects=models.Manager() 
    
    def missing_info(self):
        required_info=['pan','ifsecode','acno','beneficiaryname','phno','gender1','dob','address1','heq','aadharno','bloodgroup']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.pan   


class  employ_payslip(models.Model):
    organization=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    employId=models.CharField(max_length=100)
    dateofbirth=models.DateField(default=date.today())
    panno=models.CharField(max_length=100)
    Hiringdate=models.DateField(max_length=100)
    role=models.CharField(max_length=100)
    annual_salary=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100,default="")
    current_year=models.CharField(max_length=100,default="")

class NotificationEmploy(models.Model):
    id = models.AutoField(primary_key=True)
    employ_id = models.ForeignKey(Employs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class payslip_request(models.Model):
    student_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    startingdate=models.DateField(default=date.today())
    endingdate=models.DateField(default=None)
    reason=models.CharField(max_length=120)
    status=models.CharField(max_length=50)
    remarks=models.CharField(max_length=100)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True, blank=True)
class Meta:
    db_table="payslip_request"


class employ_tax_form(models.Model):
    email=models.CharField(max_length=100)
    Current_Monthly_Rent=models.IntegerField()
    Name_of_landlord=models.CharField(max_length=100)
    PAN_of_landlord=models.CharField(max_length=100)
    Address_of_landlord=models.CharField(max_length=400)
    Section_80C=models.IntegerField()
    Section_80CCD=models.IntegerField()
    Section_80D=models.IntegerField()
    Section_80DD=models.IntegerField()
    Section_80E=models.IntegerField()
    Section_80EEB=models.IntegerField()
    Section_80G=models.IntegerField()
    Section_80U=models.IntegerField()
    Section_80DDB=models.CharField(max_length=100,default="")
    Section_80TTA=models.CharField(max_length=100,default="")
    Section_80TTB=models.CharField(max_length=100,default="")
    Annual_interest_payable=models.IntegerField()
    Additional_benefit_under_Section=models.IntegerField()
    Name_of_lender=models.CharField(max_length=100)
    PAN_of_lender=models.CharField(max_length=100)	
    Address_of_lender=models.CharField(max_length=400)	
    Section_80EEA=models.IntegerField()
    Amount=models.IntegerField()
    Origin=models.CharField(max_length=100)
    Destination=models.CharField(max_length=100)	
    home_rent_proof=models.ImageField(upload_to="images/",default="")
    employ = models.ForeignKey(Employs, on_delete=models.CASCADE)
    TravelStartDate=models.DateField(default=None)	
    House_Property_proof=models.ImageField(upload_to="images/",default="")
    Section_80EE_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEA_proof=models.ImageField(upload_to="images/",default="")
    Section_80C_proof=models.ImageField(upload_to="images/",default="")
    Section_80D_proof=models.ImageField(upload_to="images/",default="")
    Section_80CCD1BS_proof=models.ImageField(upload_to="images/",default="")
    Section_80DD_proof=models.ImageField(upload_to="images/",default="")
    Section_80E_proof=models.ImageField(upload_to="images/",default="")
    Section_80G_proof=models.ImageField(upload_to="images/",default="")
    Section_80U_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEB_proof=models.ImageField(upload_to="images/",default="")
    Section_80DDB_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTA_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTB_proof=models.ImageField(upload_to="images/",default="")
    from_date=models.DateField(default=None)	
    to_date=models.DateField(default=None)

class admin_tax_details(models.Model):
    email=models.CharField(max_length=100)
    Current_Monthly_Rent=models.IntegerField()
    Name_of_landlord=models.CharField(max_length=100)
    PAN_of_landlord=models.CharField(max_length=100)
    Address_of_landlord=models.CharField(max_length=400)
    Section_80C=models.IntegerField()
    Section_80CCD=models.IntegerField()
    Section_80D=models.IntegerField()
    Section_80DD=models.IntegerField()
    Section_80E=models.IntegerField()
    Section_80EEB=models.IntegerField()
    Section_80G=models.IntegerField()
    Section_80U=models.IntegerField()
    Section_80DDB=models.CharField(max_length=100,default="")
    Section_80TTA=models.CharField(max_length=100,default="")
    Section_80TTB=models.CharField(max_length=100,default="")
    Annual_interest_payable=models.IntegerField()
    Additional_benefit_under_Section=models.IntegerField()
    Name_of_lender=models.CharField(max_length=100)
    PAN_of_lender=models.CharField(max_length=100)	
    Address_of_lender=models.CharField(max_length=400)	
    Section_80EEA=models.IntegerField()
    Amount=models.IntegerField()
    Origin=models.CharField(max_length=100)
    Destination=models.CharField(max_length=100)	
    admin_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    home_rent_proof=models.ImageField(upload_to="images/",default="")
    TravelStartDate=models.DateField(default=None)	
    House_Property_proof=models.ImageField(upload_to="images/",default="")
    Section_80EE_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEA_proof=models.ImageField(upload_to="images/",default="")
    Section_80C_proof=models.ImageField(upload_to="images/",default="")
    Section_80D_proof=models.ImageField(upload_to="images/",default="")
    Section_80CCD1BS_proof=models.ImageField(upload_to="images/",default="")
    Section_80DD_proof=models.ImageField(upload_to="images/",default="")
    Section_80E_proof=models.ImageField(upload_to="images/",default="")
    Section_80G_proof=models.ImageField(upload_to="images/",default="")
    Section_80U_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEB_proof=models.ImageField(upload_to="images/",default="")
    Section_80DDB_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTA_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTB_proof=models.ImageField(upload_to="images/",default="")
    from_date=models.DateField(default=None)	
    to_date=models.DateField(default=None)	



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHod.objects.create(admin=instance)
        
        if instance.user_type==2:
            Employs.objects.create(admin=instance)
       

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.employs.save()
   

class otp(models.Model):
    amount=models.IntegerField()
    paymenttype=models.CharField(max_length=100)
class Meta:
    db_table="otp"

class checkin(models.Model):
    empid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    date=models.DateField(default=None)
    time=models.TimeField(default=datetime.now)
    shift_name = models.CharField(max_length=100,default="")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    is_employee=models.CharField(max_length=100,default="0")
class Meta:
    db_table="checkin"
    
class checkout(models.Model):
    date_value=models.IntegerField()
    empid=models.CharField(max_length=100)
    date=models.DateField(default=None)
    time=models.TimeField(default=datetime.now)
    created_at=models.DateTimeField(auto_now_add=True)
    shift_name = models.CharField(max_length=100,default="")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    is_employee=models.CharField(max_length=100,default="0")

    def __str__(self):
        return f"checkout {self.id}: {self.data_value}"



class TDS(models.Model):
    id = models.AutoField(primary_key=True)
    tds_payment=models.CharField(max_length=100)
    verify_tan=models.CharField(max_length=100,default="")
    tds_filling_setup=models.CharField(max_length=10)
    filling_form=models.CharField(max_length=100)
    userid=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password1=models.CharField(max_length=100)
    tds_payment1=models.CharField(max_length=100,default='')
    tds_filling_setup1=models.CharField(max_length=10,default='')
    tds_filling_setup2=models.CharField(max_length=10,default='')
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
  
class P_tax(models.Model):
    id = models.AutoField(primary_key=True)
    professional_tax=models.CharField(max_length=100)
    pt_payment=models.CharField(max_length=100,default='')
    username3=models.CharField(max_length=100,default='')
    password4=models.CharField(max_length=100,default='')
    
    
class PF(models.Model):
    id = models.AutoField(primary_key=True)
    pf_status=models.CharField(max_length=100)
    pf_payment=models.CharField(max_length=100)
    username1=models.CharField(max_length=100)
    password2=models.CharField(max_length=100)
    pf_setup=models.CharField(max_length=100)
    pf_setup1=models.CharField(max_length=100,default='')
    pf_setup2=models.CharField(max_length=100,default='')
    pf_setup3=models.CharField(max_length=100,default='')
    pf_setup4=models.CharField(max_length=100,default='')

class ESIC(models.Model):
    id = models.AutoField(primary_key=True)
    esi_status=models.CharField(max_length=100)
    esi_payment=models.CharField(max_length=100)
    username2=models.CharField(max_length=100)
    password3=models.CharField(max_length=100)
    esi_settings=models.CharField(max_length=100)
    esi_settings1=models.CharField(max_length=100,default='')


class ad_salary(models.Model):
    student_id = models.ForeignKey(Employs, on_delete=models.CASCADE)
    amount=models.IntegerField()
    request_status=models.IntegerField(default=0)
    reason=models.CharField(max_length=100)
    eminumber=models.ForeignKey(emidata,on_delete=models.CASCADE,null=True,blank=True,default='')
    company_id=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)


class admin_ad_salary(models.Model):
    eminumber=models.ForeignKey(emidata,on_delete=models.CASCADE,null=True,blank=True,default='')
    admin_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount=models.IntegerField()
    request_status=models.IntegerField(default=0)
    reason=models.CharField(max_length=100)


class Company(models.Model):
    company_Name=models.CharField(max_length=100)
    Address=models.CharField(max_length=200)
    PAN=models.CharField(max_length=100)
    TAN=models.CharField(max_length=100)
    GSTIN=models.CharField(max_length=100)
    KYCSTATUS=models.CharField(max_length=100)
    PFSTATUS=models.CharField(max_length=100)
    ESICSTATUS=models.CharField(max_length=100)
    PTSTATUS=models.CharField(max_length=100)
    LWFSTATUS=models.CharField(max_length=100)
    INCOMETAXPORTAL= models.CharField(max_length=200)
    TRACES=models.CharField(max_length=100)
    PF=models.CharField(max_length=100)
    ESIC=models.CharField(max_length=100)
    PT=models.CharField(max_length=100)
    
    def missing_info(self):
        required_info=['company_Name ','Address','PAN','TAN','GSTIN','KYCSTATUS','PFSTATUS','ESICSTATUS','PTSTATUS','LWFSTATUS','INCOMETAXPORTAL','TRACES','PF','ESIC','PT']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.Name



STATE_CHOICES=((
    ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
    ('Andhra pradesh','Andhra pradesh'),
    ('Arrunachal prodesh','Arrunachal prodesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('chandigarh','chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra and Nagar haveli','Dadra and Nagar haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu and kashmir','Jammu and kashmir'),
    ('Uttar Pradesh','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Ladakh','Ladakh'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya pradesh','Madhya pradesh'),
    (' Maharashtra',' Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
))

   


# Create your models here.
class company_details(models.Model):
    Organisationtype=models.CharField(max_length=100)
    companypan=models.CharField(max_length=100,default="")
    companyname=models.CharField(max_length=100,default="")
    companyGSTIN=models.CharField(max_length=100)
    brandname=models.CharField(max_length=100)
    registeraddress=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    State=models.CharField(choices=STATE_CHOICES,max_length=100,default="Andhra pradesh")
    pincode=models.IntegerField(default="0")
    logo=models.ImageField(upload_to="images/",default="")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
class Meta:
    db_table="company_details" 

class details(models.Model):
    id = models.AutoField(primary_key=True)
    form1=models.CharField(max_length=100)
    form2=models.CharField(max_length=100)
    form3=models.CharField(max_length=100)

class company_logo(models.Model):
    logo=models.ImageField(upload_to="media/")
class meta:
    db_table="company_logo"



class masterctc(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    objects=models.Manager()

class Department(models.Model):
    attribute = models.CharField(max_length=100)


class Employee(models.Model):
    empname=models.CharField(max_length=100)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    final_year = models.DateField(default=None)

class pay_contractors(models.Model):
    paymentdate=models.DateField(default=None)
    invoicedate=models.DateField(default=None)
    searchcontractors=models.CharField(max_length=100,default="")
    image=models.ImageField(upload_to="images/",default="")
    repeatpayment=models.CharField(max_length=100)
    amount=models.IntegerField()
    tax=models.IntegerField()
    anyremarks=models.CharField(max_length=100)
    purpose=models.CharField(max_length=100)
    tds=models.CharField(max_length=100)
    taxcode=models.CharField(max_length=100)
    
class Meta:
    db_table="pay_contractors" 

class companylogo(models.Model):
    id=models.AutoField(primary_key=True)
    logo1=models.ImageField(upload_to="media/")
    # description=models.CharField(max_length=1000,default="")
    objects = models.Manager()
class Meta:
    db_table="companylogo" 

class company_details_first(models.Model):
    admin_id=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    Organisation_Name=models.CharField(max_length=500)
    companypan=models.CharField(max_length=700)
    companyname=models.CharField(max_length=600)
    companyGSTIN=models.CharField(max_length=800)
    brandname=models.CharField(max_length=100)
    registeraddress=models.CharField(max_length=1000)
    address=models.CharField(max_length=100)
    State=models.CharField(max_length=100)
    pincode=models.IntegerField(default="0")
    objects = models.Manager()



class set_payroll_date(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
    id=models.AutoField(primary_key=True)
    payrolldate=models.CharField(max_length=100,default="")
    auto_run_payroll=models.CharField(max_length=100)
    advance_salary_request=models.CharField(max_length=100)
    payroll=models.CharField(max_length=100,default="")


    objects = models.Manager()

class set_salary_structure(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
    id=models.AutoField(primary_key=True)
    default_salary=models.CharField(max_length=100)
    FBP_allowances=models.CharField(max_length=100)
    objects = models.Manager()


class salary_struc(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
    salarycomponent=models.CharField(max_length=100)
    select_salarycomponent=models.CharField(max_length=100,default="")

class Meta:
    db_table="salary_struc"

class salary_struct(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
    salarycomponent=models.CharField(max_length=100)
    percentageofCTC=models.CharField(max_length=100)
    percentageorfixed=models.CharField(max_length=100)
    Taxable=models.CharField(max_length=100)
    salaryid=models.IntegerField(default="1")
class Meta:
    db_table="salary_struct"

class Progress(models.Model):
    value = models.IntegerField(default=0)
    value1 = models.IntegerField(default=0)
    value2 = models.IntegerField(default=0)
    value3 = models.IntegerField(default=0)
    value4 = models.IntegerField(default=0)
    value5 = models.IntegerField(default=0)
    
    progress_form1=models.CharField(max_length=100,default=0)
    progress_form2=models.CharField(max_length=100,default=0)
    progress_form3=models.CharField(max_length=100,default=0)
    progress_form4=models.CharField(max_length=100,default=0)
    progress_form5=models.CharField(max_length=100,default=0)
    progress_form6=models.CharField(max_length=100,default=0)

class admin_chart_ac(models.Model):
    chart_ac_name=models.CharField(max_length=100)
    chart_ac_email=models.EmailField(max_length=100)
    chart_ac_no=models.IntegerField()
class Meta:
    db_table="admin_chart_ac"


class employlev(models.Model):
    type=models.CharField(max_length=1000,default="name")
    defaultleave=models.IntegerField(default="4")
    leave_id=models.IntegerField(default="1")
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")

class Meta:
    db_table="employlev"


class pvt_pub(models.Model):
    id=models.AutoField(primary_key=True)
    certificate=models.FileField(upload_to="media/")
    cmpny_pancard=models.FileField(upload_to="media/")
    cheque=models.FileField(upload_to="media/")
    owner_pancard=models.FileField(upload_to="media/")
    id_proof=models.FileField(upload_to="media/")
    gst=models.FileField(upload_to="media/")
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="pvt_pub"

class sole_proprietorship(models.Model): 
    id=models.AutoField(primary_key=True)   
    gst_certificate=models.FileField(upload_to="media/")
    cancelled_cheque=models.FileField(upload_to="media/")
    owner_pancard1=models.FileField(upload_to="media/")
    idproof=models.FileField(upload_to="media/")
    GST=models.FileField(upload_to="media/")  
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="sole_proprietorship"

class partnership(models.Model):    
    id=models.AutoField(primary_key=True)
    shop_license=models.FileField(upload_to="media/")
    cmpny_pan=models.FileField(upload_to="media/")
    cheque1=models.FileField(upload_to="media/")
    owner_pan=models.FileField(upload_to="media/")
    id_proof1=models.FileField(upload_to="media/")
    gst1=models.FileField(upload_to="media/")
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="partnership"

class trust_ngo(models.Model): 
    id=models.AutoField(primary_key=True)  
    shop_license1=models.FileField(upload_to="media/")
    cmpny_pan1=models.FileField(upload_to="media/")
    cheque2=models.FileField(upload_to="media/")
    owner_pan1=models.FileField(upload_to="media/")
    id_proof2=models.FileField(upload_to="media/")
    gst2=models.FileField(upload_to="media/")
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="trust_ngo"

class reimbursementsetup(models.Model):
    Reimbursements_Enabled=models.CharField(max_length=100)
    Make_attachments_compulsory=models.CharField(max_length=100)
    Include_reimbursements_with_payroll=models.CharField(max_length=100)
    # selected_reimbursements = models.CharField(max_length=500, null=True, blank=True)
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")

class Meta:
    db_table="reimbursementsetup"

class reimbursementsetup1(models.Model):
    reimbursement_type = models.CharField(max_length=100, null=True, blank=True)
    select_reimbursement=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')),default="")
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
class Meta:
    db_table="reimbursementsetup1"


class employ_help(models.Model):
    image1=models.ImageField(upload_to="media/")
    image2=models.ImageField(upload_to="media/")
    image3=models.ImageField(upload_to="media/")
    image4=models.ImageField(upload_to="media/")
    image5=models.ImageField(upload_to="media/")
class Meta:
    db_table="employ_help"

class integrations(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='media/')
    purpose=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    btn=models.CharField(max_length=100,default='')
    footer=models.CharField(max_length=100,default='')
    url=models.CharField(max_length=100,default='')
class Meta:
    db_table="icon"

class app(models.Model):
    response=models.CharField(max_length=100)
class Meta:
    db_table="app" 

class MonthlyTotal(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total = models.IntegerField()
    month_and_year = models.CharField(max_length=20,default="")
    def __str__(self):
        return f"{self.get_month_display()} {self.year}: {self.total}"


class adminMonthlyTotal(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total = models.IntegerField()
    month_and_year = models.CharField(max_length=20,default="")
    def __str__(self):
        return f"{self.get_month_display()} {self.year}: {self.total}"


class employhelp(models.Model):
    image1=models.ImageField(upload_to="media/")
    image2=models.ImageField(upload_to="media/")
    image3=models.ImageField(upload_to="media/")
    image4=models.ImageField(upload_to="media/")
    image5=models.ImageField(upload_to="media/")
class Meta:
    db_table="employhelp"



#settings models:


from django.db import models

# Create your models here.
class check(models.Model):
    EnabledAttendance=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    
    AllowEmployees=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    AllowHalfdayleave=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    Employeemustenter=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    Showattendence=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    automaticallyadd=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    lossofpay=models.CharField(max_length=64,choices=(('Yes','Yes'),('No','No'))) 
    usefinancal=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    track=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    type=models.CharField(max_length=100)
    defaultleave=models.CharField(max_length=100)
    monthlyincrement=models.CharField(max_length=100)
    maxleave=models.CharField(max_length=100)
    carryforward=models.CharField(max_length=100)
    Defaultshift=models.CharField(max_length=100)
    graceperiod=models.CharField(max_length=100)
    fulltime=models.CharField(max_length=100)
    halftime=models.CharField(max_length=100)
    date=models.DateField()
    description=models.CharField(max_length=100)
    attendanceenabled=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No')))
    all = models.CharField(max_length=50, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')    
    andhrapradesh = models.CharField(max_length=50, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')
    telangana = models.CharField(max_length=50, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')
    date2 = models.CharField(max_length=100,default="")
    description2 = models.CharField(max_length=100,default="")
    day = models.CharField(max_length=50, default='Monday')  
    holidays=models.CharField(max_length=100,default="")
    weekend=models.CharField(max_length=100,default="N0") 

from django.db import models

class YourModel(models.Model):
    all = models.CharField(max_length=3, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')


class default_salary_structure(models.Model):
    default_salary=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    salarycomponent=models.CharField(max_length=100)
    percentageofCTC=models.CharField(max_length=100)
    percentageorfixed=models.CharField(max_length=100)
    Taxable=models.CharField(max_length=100)
class Meta:
    db_table="default_salary_structure"   

class default_salary(models.Model):
    default_sal=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    
class Meta:
    db_table="default_salary"   


class reimbursement_setup_settings(models.Model):
    document_type=models.CharField(max_length=100,default="")
    Enabled=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))
    Reimbursements_Enabled=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    Make_attachments_compulsory=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    Include_reimbursements_with_payroll=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
class Meta:
    db_table="reimbursement_setup_settings"


class emp_reg_setup(models.Model):
    resignations=models.CharField(max_length=50)
class Meta:
    db_table="emp_reg_setup"


class tdsfillingsetup(models.Model):
    Automated_filling24=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    Automated_filling26=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
class Meta:
    db_table="tdsfillingsetup"

class employedata(models.Model):
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    employ_idlength=models.IntegerField(default=5)

    employe_id_prefix=models.CharField(max_length=100)
    employe_directory=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    additionalinfo=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))

class Meta:
    db_table="employedata"

class tax_deduction(models.Model):
     approval=models.CharField(max_length=300)
     verify=models.CharField(max_length=300)
     taxable=models.CharField(max_length=300)
class Meta:
    db_table="tax_deduction"

class empnotificationupdate(models.Model):
    id = models.AutoField(primary_key=True)
    send_email_notify=models.CharField(max_length=500)
    email_notify=models.CharField(max_length=500)

class documents_setup(models.Model):
    document_type=models.CharField(max_length=100)
    compulsory=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))
    Enabled=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))

class Meta:
    db_table="documents_setup"  


  
class editholiday12(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="1")
    sun=models.BooleanField(null=True,blank=True)
    sat1=models.BooleanField(null=True,blank=True)
    sat2=models.BooleanField(null=True,blank=True)
    sat3=models.BooleanField(null=True,blank=True)
    sat4=models.BooleanField(null=True,blank=True)
    sat5=models.BooleanField(null=True,blank=True)
    alsat=models.BooleanField(null=True,blank=True)
    mon=models.BooleanField(null=True,blank=True)
    tue=models.BooleanField(null=True,blank=True)
    web=models.BooleanField(null=True,blank=True)
    thu=models.BooleanField(null=True,blank=True)
    fri=models.BooleanField(null=True,blank=True)
    
class Meta:
    db_table="editholiday"


class customholidays(models.Model):
    date=models.DateField(null=True,blank=True)
    reason=models.CharField(max_length=100)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE)
class Meta:
    db_table="customholidays"


class halfldayvreason(models.Model):
    halfdaylev=models.BooleanField(default="0",null=True,blank=True)
    reason1=models.BooleanField(default="0",null=True,blank=True)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,default="")

class Meta:
    db_table="halfdayreason"

class publicholidays(models.Model):
    publicholiday_date=models.DateField()
    festival_name=models.CharField(max_length=100)
    finding=models.BooleanField(default='0', null=True,blank=True)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE)

class Meta:
    db_table="publicholidays"



class employlevsheet(models.Model):
    causalleave=models.IntegerField()
    medicalleave=models.IntegerField()
    earnedleave=models.IntegerField()
class Meta:
    db_table="employlevsheet"

from datetime import date
from datetime import time


class taskdata(models.Model):
    p_name = models.CharField(max_length=100)
    p_url = models.CharField(max_length=200)
    team_lead = models.IntegerField()
class Meta:
    db_table="taskdata"

from datetime import date

# class projecttask(models.Model):
#     p_name = models.ForeignKey(Project, on_delete=models.CASCADE)
#     tasks = models.CharField(max_length=100)
#     l_name = models.CharField(max_length=100)
#     task_date = models.DateField(default=None
#     def get_status(self):
#         today = date.today()

#         if self.task_date < today:
#             return "Completed"
#         elif self.task_date == today:
#             return "Ongoing"
#         else:
#             return "Upcoming"
from datetime import date
from datetime import time

class projecttask(models.Model):
    p_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    tasks = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    task_date = models.DateField(default=date.today())
    task_time = models.TimeField(default='00:00')
    deadline = models.DateField(default=date.today())
    description=models.TextField(default=None)

    def get_status(self):
        current_datetime = datetime.combine(self.task_date, self.task_time)
        current_datetime_now = datetime.now()

        end_of_day = datetime.combine(current_datetime_now.date(), time(23, 59, 59))

        if current_datetime.date() < current_datetime_now.date():
            return "Completed"
        elif current_datetime <= end_of_day:
            return "Not Started"
        else:
            return "Upcoming"

   
class teamtask(models.Model):
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    task=models.CharField(max_length=100)
    description=models.TextField(default=None)
    l_name=models.CharField(max_length=100,default='')
    tdate = models.DateField(default=date.today())
    
class Meta:
    db_table="teamtask"
    

class AveragePerformance(models.Model):
     
    project_name = models.CharField(max_length=255)
    date = models.DateField()
    avg_performance = models.FloatField()
    teamlead = models.ForeignKey(Employs, on_delete=models.CASCADE,null=True,blank=True,related_name='teamlead')


    def __str__(self):
        return f"{self.project_name} - {self.date} - {self.avg_performance} - {self.teamlead}"


class tlassigntask(models.Model):
    task=models.ForeignKey(teamtask,on_delete=models.CASCADE,null=True,blank=True)
    employid=models.ForeignKey(Employs,on_delete=models.CASCADE,null=True,blank=True)    
    description=models.TextField(default=None)
    status=models.IntegerField(default="0")
    deadline=models.CharField(max_length=100,default=timezone.now)
    project_id=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    task_date=models.DateField(default=date.today())
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    employid1=models.CharField(max_length=100,default="")
    teamid=models.CharField(max_length=100,default='')
class Meta:
     db_table="tlassigntask"



class employperformance(models.Model):
    project_name = models.CharField(max_length=100,default='')
    employ_name = models.ForeignKey(Employs, on_delete=models.CASCADE)
    project_task1 = models.CharField(max_length=100,default='')
    performance = models.FloatField()
    date = models.DateField(default=date.today)
    task_name1=models.CharField(max_length=100 ,default="")
    status=models.CharField(max_length=100,default="")
    tl_name = models.ForeignKey(Employs, on_delete=models.CASCADE,null=True,blank=True,related_name='tl')
    # @property
    # def task_name(self):
    #     if self.project_task1:
    #         return self.project_task1.tasks
    #     return None

    # @property
    # def task_date(self):
    #     if self.project_task1:
    #         return self.project_task1.task_date
    #     return None

    # @property
    # def task_time(self):
    #     if self.project_task1:
    #         return self.project_task1.task_time
    #     return None

    class Meta:
        db_table = "employperformance"

    # def __str__(self):
    #     return f"{self.employ_name} - {self.project_name}" 
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # Update related employ status
    #     self.employ_name.status = self.status
    #     self.employ_name.save()
    #     # Update related task status
    #     related_tasks = tlassigntask.objects.filter(project_id=self.project_name)
    #     for task in related_tasks:
    #         task.status = self.status
    #         task.save()    



class Meeting(models.Model):
    meeting_url = models.CharField(max_length=500)
    team_member = models.CharField(max_length=100)

    def __str__(self):
        return f"Meeting for {self.team_member.first_name} {self.team_member.last_name}"
    
from django.db import models

class employ_nav(models.Model):
    is_name_exist = models.BooleanField(default=False)
    is_tl_option = models.BooleanField(default=False)

    def __str__(self):
        return f"employ_nav: {self.id} - Name Exists: {self.is_name_exist}, TL Option: {self.is_tl_option}"
class employeeindex(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="Images/")
    descrption=RichTextField()
    descrption1=RichTextField()
    image1=models.ImageField(upload_to="Images/")
    descrption2=RichTextField()
    descrption3=RichTextField()
    image2=models.ImageField(upload_to="Images/")
    descrption4=RichTextField()
    descrption5=RichTextField()

class Meta:
     db_table="employeeindex"


class employeeindex1(models.Model):
    title=RichTextField()
    descrption=RichTextField()
    descrption1=RichTextField()

class Meta:
     db_table="employeeindex1"

class employeeindex2(models.Model):
    title=RichTextField()
    subtitle=RichTextField()
    descrption1=RichTextField()
    image=models.ImageField(upload_to="Images/")

class Meta:
     db_table="employeeindex2"


class Monitoringdata(models.Model): 
    title=RichTextField(default='')
    discription=RichTextField(default='')
    image1=models.ImageField(upload_to='images/',default='')
    image2=models.ImageField(upload_to='images/',default='')
class Meta:
    db_table="Monitoringdata"


class Monitoring(models.Model):
    m_title = models.CharField(max_length=200, null=True)
    m_log_ts = models.DateTimeField(default=timezone.now)

    m_start_time = models.TimeField(default=datetime.now)
    m_end_time = models.TimeField(default=datetime.now)
    m_total_duration = models.IntegerField(default=0,null=True,blank=True)  # Added field for total duration
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Companys, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "monitoring"
class Monitoring2(models.Model): 
    title=RichTextField()
    paragraph=RichTextField()
    icon=models.CharField(max_length=100)
    title1=RichTextField()
    discription=RichTextField()
    
class Meta:
    db_table="Monitoring2"
    
class Monitoring3(models.Model):
    icon=models.ImageField(upload_to='images/')
    title=RichTextField()
    discription1=RichTextField()
    discription2=RichTextField()
    discription3=RichTextField()
    discription4=RichTextField()
    image1=models.ImageField(upload_to='images/')
class Meta:
    db_table="Monitoring3"
    
class Monitoring4(models.Model): 
    subtitle=RichTextField()
    title=RichTextField()
    discriprion=RichTextField()
    image1=models.ImageField(upload_to='images/')
class Meta:
    db_table="Monitoring4"



class screenmonitoring1(models.Model):
    title1=models.CharField(max_length=100)
    image1=models.ImageField(upload_to='images/')
    title2=models.CharField(max_length=100)
    discription1=models.CharField(max_length=1000)
    title3=models.CharField(max_length=100)
    discription2=models.CharField(max_length=1000)
    image2=models.ImageField(upload_to='images/')

class Meta:
    db_table="screenmonitoring1"  


class screenmonitoring2(models.Model):
    icon=models.CharField(max_length=30,default='')
    title=models.CharField(max_length=100)
    discription=models.CharField(max_length=1000)

class Meta:
    db_table="screenmonitoring2"  


class screenmonitoring3(models.Model):
    title=models.CharField(max_length=100)
    discription1=models.CharField(max_length=1000)
    discription2=models.CharField(max_length=1000,default="")
    discription3=models.CharField(max_length=1000,default="")
    discription4=models.CharField(max_length=1000,default="")
    image=models.ImageField(upload_to='images/')

class Meta:
    db_table="screenmonitoring3"  


class officework1(models.Model):
    title1=models.CharField(max_length=100)
    image1=models.ImageField(upload_to='images/')
    discription1=models.CharField(max_length=1000)
    discription2=models.CharField(max_length=1000)
    discription3=models.CharField(max_length=1000)
    discription4=models.CharField(max_length=1000)
    image2=models.ImageField(upload_to='images/')

class Meta:
    db_table="officework1" 


class officework2(models.Model):
    title1=models.CharField(max_length=100)
    title2=models.CharField(max_length=100)

    image=models.ImageField(upload_to='images/')
    discription=models.CharField(max_length=1000)
    

class Meta:
    db_table="officework2"  


class officework3(models.Model):
    title1=models.CharField(max_length=100)
    title2=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/',default='')
    discription=models.CharField(max_length=1000)
    

class Meta:
    db_table="officework3"  

class officework4(models.Model):
    title1=models.CharField(max_length=100)
    title2=models.CharField(max_length=100)

    discription=models.CharField(max_length=1000)
    image=models.ImageField(upload_to='images/')

    

class Meta:
    db_table="officework4"  


class timeattendance1(models.Model):
    title1=models.CharField(max_length=100)
    image1=models.ImageField(upload_to='images/')
    discription1=models.CharField(max_length=1000)
    discription4=models.CharField(max_length=1000)
    image2=models.ImageField(upload_to='images/')
    title2=models.CharField(max_length=100)
    discription2=models.CharField(max_length=1000)
    title3=models.CharField(max_length=100)
    discription3=models.CharField(max_length=1000)
    image3=models.ImageField(upload_to='images/')

class Meta:
    db_table="timeattendance1"  



class timeattendance2(models.Model):
    title=models.CharField(max_length=100)
    discription=models.CharField(max_length=1000)
    discription1=models.CharField(max_length=100,default="")

class Meta:
    db_table="timeattendance2"  


class timeattendance3(models.Model):
    title=models.CharField(max_length=100)
    discription1=models.CharField(max_length=1000) 
    discription2=models.CharField(max_length=1000)
    discription3=models.CharField(max_length=1000)
    discription4=models.CharField(max_length=1000)
    image=models.ImageField(upload_to='images/')

class Meta:
    db_table="timeattendance3" 


class timeattendance4(models.Model):
        title1=models.CharField(max_length=100)
        image=models.ImageField(upload_to='images/')
        title2=models.CharField(max_length=100)
        discription=models.CharField(max_length=1000) 

class Meta:
    db_table="timeattendance4"



class productivity1(models.Model):
        title1=models.CharField(max_length=100)
        image1=models.ImageField(upload_to='images/')
        title2=models.CharField(max_length=100)
        subtitle1=models.CharField(max_length=100)
        title3=models.CharField(max_length=100)
        subtitle2=models.CharField(max_length=200)

class Meta:
    db_table="productivity1"


class productivity2(models.Model):
        image1=models.ImageField(upload_to='images/')
        title1=models.CharField(max_length=100)
        discription1=models.CharField(max_length=1000)
      
class Meta:
    db_table="productivity2"



class productivity3(models.Model):
        title1=models.CharField(max_length=100)
        image=models.ImageField(upload_to='images/')
        title2=models.CharField(max_length=100)
        discription=models.CharField(max_length=1000) 
class Meta:
    db_table="productivity3"


class productivity4(models.Model):
        title1=models.CharField(max_length=100)
        discription1=models.CharField(max_length=1000) 
        image=models.ImageField(upload_to='images/')
        title2=models.CharField(max_length=100)
        discription2=models.CharField(max_length=1000) 
class Meta:
    db_table="productivity4"



class timetracking1(models.Model):
    title1=models.CharField(max_length=500)
    title2=models.CharField(max_length=500)
    title3=models.CharField(max_length=500) 
    title4=models.CharField(max_length=500)
    title5=models.CharField(max_length=500)
    subtitle1=models.CharField(max_length=500)
    image1=models.ImageField(upload_to='images/')
    image2=models.ImageField(upload_to='images/')
    discription1=models.CharField(max_length=1000) 
    discription2=models.CharField(max_length=1000) 
    discription3=models.CharField(max_length=1000) 
class Meta:
    db_table="timetracking1"  


class timetracking2(models.Model):
        title=models.CharField(max_length=500)
        image=models.ImageField(upload_to='images/')
        discription=models.CharField(max_length=1000) 
class Meta:
    db_table="timetracking2" 



class timetracking3(models.Model):
        icons=models.CharField(max_length=100,default="")
        title=models.CharField(max_length=500)
        discription=models.CharField(max_length=1000) 
class Meta:
    db_table="timetracking3" 
     



class timetracking4(models.Model):
        title=models.CharField(max_length=500)
        image=models.ImageField(upload_to='images/')
        discription=models.CharField(max_length=1000) 
class Meta:
    db_table="timetracking4"


class Footer1(models.Model):
    header1 = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    header2 = models.CharField(max_length=100)
    f1 = models.CharField(max_length=100)
    f2 = models.CharField(max_length=100)
    f3 = models.CharField(max_length=100)
    f4 = models.CharField(max_length=100,default="")
    f5 = models.CharField(max_length=100,default="")
    f6 = models.CharField(max_length=100,default="")
    f7 = models.CharField(max_length=100,default="")

    
    header3 = models.CharField(max_length=100)
    # photo = models.ImageField(upload_to="images/")
    copyright = models.TextField()
    design = models.TextField()
    class Meta:
        db_table='Footer1'









class indexnave(models.Model):
    image=models.ImageField(upload_to="Images/")
    nave1=models.CharField(max_length=100)
    nave2=models.CharField(max_length=100)
    nave3=models.CharField(max_length=100)
    nave4=models.CharField(max_length=100)
    nave5=models.CharField(max_length=100)
    nave6=models.CharField(max_length=100)
    nave7=models.CharField(max_length=100)
    nave8=models.CharField(max_length=100)
    nave9=models.CharField(max_length=100)
    nave10=models.CharField(max_length=100)
    nave11=models.CharField(max_length=100)
    nave12=models.CharField(max_length=100)
    nave13=models.CharField(max_length=100)

class Meta:
     db_table="indexnave"


class footer(models.Model):
    image1=models.ImageField(upload_to='Images/')
    logo=models.ImageField(upload_to='Images/')
    title1=RichTextField()
    subtitle= models.CharField(max_length=100)
    subtitle1= models.CharField(max_length=100)
    subtitle2= models.CharField(max_length=100)
    nav= models.CharField(max_length=100)
    nav1= models.CharField(max_length=100)
    nav2= models.CharField(max_length=100)
    address=RichTextField()
    email=models.EmailField(max_length = 500)
    countrycode=models.CharField(max_length=100,default="")
    icon1=models.CharField(max_length=100,default="")
    icon2=models.CharField(max_length=100,default="")
    icon3=models.CharField(max_length=100,default="")
    contactno=models.CharField(max_length=100,default="")
    url=models.CharField(max_length=1000,default="")
    descrption1=models.CharField(max_length=500,default="")
    descrption2=models.CharField(max_length=500,default="")
    descrption3=models.CharField(max_length=500,default="")
class Meta:
    db_table="footer"



class home(models.Model):
    title1=models.CharField(max_length=255)
    discription1= models.CharField(max_length=300)
    title2=models.CharField(max_length=100)
    discription2= models.CharField(max_length=300)    
    image1=models.ImageField(upload_to='images/')
    image2=models.ImageField(upload_to='images/')
    image3=models.ImageField(upload_to='images/')
    image4=models.ImageField(upload_to='images/')
    def __str__(self):
        return self.title1

class home2(models.Model):
    image=models.ImageField(upload_to='images/')
    title=models.CharField(max_length=255)
    discription= models.CharField(max_length=300)
    image1=models.ImageField(upload_to='images/',default="")
class Meta:
    bd_table="home2"
    
class home3(models.Model):
    title=models.CharField(max_length=255,default="")
    image1=models.ImageField(upload_to='images/')
    discription1= models.CharField(max_length=300,default="")
    point1=models.CharField(max_length=100,default="")
    point2=models.CharField(max_length=100,default="")
    point3=models.CharField(max_length=100,default="")
    point4=models.CharField(max_length=100,default="")
    discription2= models.CharField(max_length=300,default="")
    image2=models.ImageField(upload_to='images/')
    image3=models.ImageField(upload_to='images/',default="")

class Meta:
    db_table="home3"
    
class home4(models.Model):
    title1=models.CharField(max_length=255,default="")
    image1=models.ImageField(upload_to='images/',default="")
    title2=models.CharField(max_length=255,default="")
    image2=models.ImageField(upload_to='images/',default="")
    

class Meta:
    db_table="home4"
    
class home5(models.Model):
    image=models.ImageField(upload_to='images/',default="")
    title=models.CharField(max_length=255,default="")
    discription= models.CharField(max_length=300,default="")
    p=models.CharField(max_length=100,default="")
    link = models.URLField(max_length=200, blank=True, null=True)
class Meta:
    db_table="home5"

class nav1(models.Model):
    photo = models.ImageField(upload_to="images/")

    name=models.CharField(max_length=100)
    url=models.CharField(max_length=100)
class meta:
    db_table:"nav1"    


class nav2(models.Model):
    name=models.CharField(max_length=100)
    url=models.CharField(max_length=100)

class meta:
    db_table:"nav2"


class NavbarItem(models.Model):
    name = models.CharField(max_length=100)
    photo1 = models.ImageField(upload_to="images/")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    url = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "NavbarItem"

    def __str__(self):
        return self.name

    def get_photo_url(self):
        return self.photo1.url if self.photo1 else ''
    
    def is_active(self, request_path):
        # Check if any child items are active
        if self.children.filter(url=request_path).exists():
            return True
        return False


    
from django.db import models

class ContactInfo2(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    phone_hours = models.CharField(max_length=50)
    email_addresses = models.TextField()



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 

class icons(models.Model):
    icon=models.ImageField(upload_to='images/')
    url=models.CharField(max_length=100)

    icon1=models.ImageField(upload_to='images/')  
    title=models.CharField(max_length=100)
    # icon1=models.CharField(max_length=100)  
    # icon=models.CharField(max_length=100)  
  
class Meta:
      db_table="icons"

class productivity5(models.Model):
        image1=models.ImageField(upload_to='images/')
        title1=models.CharField(max_length=100)
        discription1=models.CharField(max_length=1000)
class Meta:
    db_table="productivity5"
class privacy(models.Model):
    title=models.CharField(max_length=100)
    subtitle=models.CharField(max_length=100)
    content=models.TextField()
    point1=models.TextField()
    point2=models.TextField()
    point3=models.TextField()
    point4=models.TextField()
    point5=models.TextField()
    point6=models.TextField()
    point7=models.TextField()
    point8=models.TextField()
    point9=models.TextField()
    point10=models.TextField()
    images=models.ImageField(upload_to="images/")
    himage=models.ImageField(upload_to="images/",default="")
class Meta:
    db_table="privacy"


class ac(models.Model):
    heading=models.CharField(max_length=100)
    content=models.TextField()
    images=models.ImageField(upload_to="images/")
class Meta:
    db_table="ac"

class ac1(models.Model):
    
    header=models.ImageField(upload_to="images/")    


class FooterLink(models.Model):
    label = models.CharField(max_length=100)
    url = models.URLField()
    
class FooterLink0000(models.Model):
    label = models.CharField(max_length=100)
    url = models.URLField()

class FooterLink123456(models.Model):
    label = models.CharField(max_length=100)
    url = models.URLField()

class FooterService(models.Model):
    label = models.CharField(max_length=100)
    url = models.URLField()
    label1 = models.CharField(max_length=100 ,default="")
    url1 = models.URLField(default="")

class ContactInfo(models.Model):
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField() 
    address1 = models.CharField(max_length=200 ,default="")
    address2 = models.CharField(max_length=200 ,default="")
    address3 = models.CharField(max_length=200 ,default="") 

class SocialLink(models.Model):
      facebook_link = models.URLField(blank=True, null=True)
      twitter_link = models.URLField(blank=True, null=True)
      instagram_link = models.URLField(blank=True, null=True)
      youtube_link = models.URLField(blank=True, null=True)
      linkdin_link = models.URLField(blank=True, null=True)


class screenmon(models.Model):
    name=models.CharField(max_length=100)
    show1=models.BooleanField()
    show2=models.BooleanField()
    show3=models.BooleanField()
    addon=models.BooleanField(default=0)
    edit=models.BooleanField(default=1)
    parent_category = models.ForeignKey('self', related_name='subdrop', blank=True, null=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.name in ['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots']:
            related_records = admin_drop.objects.filter(
                name__in=['Monitoring logs']
            )

            if screenmon.objects.filter(name__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], show1=True).exists():
                related_records.update(show1=1)
            else:
                related_records.update(show1=0)
            if screenmon.objects.filter(name__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], show2=True).exists():
                related_records.update(show2=1)
            else:
                related_records.update(show2=0)
            if screenmon.objects.filter(name__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], show3=True).exists():
                related_records.update(show3=1)
            else:
                related_records.update(show3=0)
            if screenmon.objects.filter(name__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0)
        if self.name in ['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots']:
            related_records = employ_drop.objects.filter(
                name__in=['Monitoring logs']
            )

            if screenmon.objects.filter(name__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], show1=True).exists():
                related_records.update(show1=1)
            else:
                related_records.update(show1=0)
            if screenmon.objects.filter(name__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], show2=True).exists():
                related_records.update(show2=1)
            else:
                related_records.update(show2=0)
            if screenmon.objects.filter(name__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], show3=True).exists():
                related_records.update(show3=1)
            else:
                related_records.update(show3=0)

        if self.name == "detailed monitoring":
            namqq=featurestypes.objects.filter(name__in=["detailed monitoring"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "powerlogs":
            namqq=featurestypes.objects.filter(name__in=["powerlogs"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)
        if self.name == "screenshots":
            namqq=featurestypes.objects.filter(name__in=["screenshots"])
            namqq.update(show1=self.show1,show2=self.show2,show3=self.show3)

class Addonsuser(models.Model):
    plan=models.CharField(max_length=100)
    amount=models.IntegerField()
    order_id = models.CharField(max_length=500)
    addon=models.BooleanField(default=0)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(default=date.today())
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.plan in ['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots']:
            related_records = admin_drop.objects.filter(
                name__in=['Monitoring logs']
            )
            if Addonsuser.objects.filter(plan__in=['screen monitoring', 'detailed monitoring', 'powerlogs', 'screenshots'], addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0)

        if self.plan =="screen monitoring":
            add = screenmon.objects.filter(
                name__in=['screen monitoring']
            )
            add.update(addon=self.addon)
        if self.plan == "Advance Salary":
            advance=admin_drop.objects.filter(
                name__in=['Advance Salary']
            )
            advance.update(addon=self.addon)
        
        if self.plan in['Company Details']:
            related_records=admin_drop.objects.filter(
                name__in=['Company Details']
            ) 
            if Addonsuser.objects.filter(plan__in=['Company Details'],addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0)

        if self.plan in['Create Project']:
            related_records=admin_drop.objects.filter(
                name__in=['Create Project']
            ) 
            if Addonsuser.objects.filter(plan__in=['Create Project'],addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0) 

        if self.plan in['Employes Task Performance ']:
            related_records=admin_drop.objects.filter(
                name__in=['Employes Task Performance ']
            ) 
            if Addonsuser.objects.filter(plan__in=['Employes Task Performance '],addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0)

        if self.plan in['Employes Project Performance ']:
            related_records=admin_drop.objects.filter(
                name__in=['Employes Project Performance ']
            ) 
            if Addonsuser.objects.filter(plan__in=['Employes Project Performance '],addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0)  

        if self.plan in['Employes Avg Performance']:
            related_records=admin_drop.objects.filter(
                name__in=['Employes Avg Performance']
            ) 
            if Addonsuser.objects.filter(plan__in=['Employes Avg Performance'],addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0)    

        if self.plan in['Daily Task Report']:
            related_records=admin_drop.objects.filter(
                name__in=['Daily Task Report']
            ) 
            if Addonsuser.objects.filter(plan__in=['Daily Task Report'],addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0) 
        if self.plan in['Project List']:
            related_records=admin_drop.objects.filter(
                name__in=['Project List']
            ) 
            if Addonsuser.objects.filter(plan__in=['Project List'],addon=True).exists():
                related_records.update(addon=1)
            else:
                related_records.update(addon=0)   
  
class Addons(models.Model):
    name=models.CharField(max_length=100)
    amount=models.IntegerField()
    plantype=models.ForeignKey(typeofplans,on_delete=models.CASCADE)
class Meta:
    db_table="Addons"

class freetraildays(models.Model):
    freedays=models.IntegerField(default=15)
    monthly=models.IntegerField(default=20)
    yearly=models.IntegerField(default=30)
class Meta:
    db_table='day'




class about(models.Model):
    content=models.CharField(max_length=1000)
    images=models.ImageField(upload_to="images/")
    ###ourvision###
    content1=models.CharField(max_length=1000)
    c=models.CharField(max_length=1000,default="")
    c1=models.CharField(max_length=1000)
    c2=models.CharField(max_length=1000)
    c3=models.CharField(max_length=1000)
    images1=models.ImageField(upload_to="images/")
    ### our mission###
    content2=models.CharField(max_length=1000)
    images2=models.ImageField(upload_to="images/")
    ###our techologies###
    c4=models.CharField(max_length=1000)
    c5=models.CharField(max_length=1000)
    c6=models.CharField(max_length=1000)
    c7=models.CharField(max_length=1000)
    c8=models.CharField(max_length=1000)
    c9=models.CharField(max_length=1000)
    images3=models.ImageField(upload_to="images/")

    ###our location##
    images4=models.ImageField(upload_to="images/",default="")
    content3=models.CharField(max_length=1000,default="")



    ##work tried application###
    images5=models.ImageField(upload_to="images/",default="")
    content44=models.CharField(max_length=1000,default="")
    ###customized admin###
    images6=models.ImageField(upload_to="images/",default="")
    content55=models.CharField(max_length=1000,default="")
    ####screen monitoring###
    images7=models.ImageField(upload_to="images/",default="")
    content6=models.CharField(max_length=1000,default="")
    ###employee performance###
    images8=models.ImageField(upload_to="images/",default="")
    content7=models.CharField(max_length=1000,default="")

    
    
   
    class Meta:
           db_table="about"    
	
class adminphoto(models.Model):
    image=models.ImageField(upload_to="media/")



class plandata(models.Model):
    type1=models.CharField(max_length=1000)
    type2=models.CharField(max_length=1000)
    type3=models.CharField(max_length=1000)
    type4=models.CharField(max_length=1000,default="")




class meta:
    db_table="plandata" 


class priceingintro(models.Model):
    getapl=models.CharField(max_length=100)
    rightplan=models.CharField(max_length=100)
    forcont=models.CharField(max_length=100)
    freetrails=models.CharField(max_length=100)
class meta:
    db_table="priceingintro"

class service(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    contactno=models.CharField(max_length=100)
    otp=models.CharField(max_length=100)
    companyname=models.CharField(max_length=100)
    description=models.TextField(max_length=100)
    business=models.CharField(max_length=100)
    date=models.DateField()
    is_status=models.CharField(max_length=100,default="1")

class Meta:
    db_table="service" 	


class ourteam1(models.Model):
    image=models.ImageField(upload_to='media/')
    name=models.CharField(max_length=100)
    role=models.CharField(max_length=100)
    description=models.TextField(default="")
class meta:
    db_table="ourteam1"

class team1(models.Model):
    name1=models.CharField(max_length=100,default="")
class meta:
    db_tables="team1" 



class terms_conditions(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
class Meta:
    db_table="terms_conditions"
    

class privacy_policy(models.Model):
    subtitle=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    content=models.TextField()
    point1=models.TextField()
    point2=models.TextField()
    point3=models.TextField()
    point4=models.TextField()
    content1=models.TextField()
class Meta:
    db_table="privacy_policy"	

class cancellation_policy1(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(help_text="Enter each description point on a new line.", default='')

    def get_description_list(self):
        return self.description.split('\n')
class Meta:
    db_table="cancellation_policy1"
    
class hr_control(models.Model):
    field_name=models.CharField(max_length=1000)
    employ_name=models.IntegerField()
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE)
class meta:
    db_table="hr_control"


class hr_controls(models.Model):
    field_name = models.CharField(max_length=1000)
    employ_name = models.IntegerField()
    companyid = models.ForeignKey(Companys, on_delete=models.CASCADE)
class meta:
    db_table="hr_controls"


class salary_deductions(models.Model):
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,default="")
    deductcomponent=models.CharField(max_length=100)
    percentageofdctc=models.IntegerField()
    percentageordfixed=models.CharField(max_length=100)
    deductid=models.IntegerField()


class student_name(models.Model):
    sid=models.IntegerField()
    sname=models.CharField(max_length=100)
    sbranch=models.CharField(max_length=100)

class Meta:
    db_table="sss"



from ckeditor.fields import RichTextField
class admin_message(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    descrption = RichTextField()
    image=models.ImageField(upload_to="media/")
    role=models.CharField(max_length=100, default="")
    date=models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class payroll(models.Model):
    title1=models.CharField(max_length=100,default="")
    description1 = RichTextField(default="")
    image1=models.ImageField(upload_to="media/",default="")
class Meta:
    db_table="payroll"


class payroll1(models.Model):
    image1=models.ImageField(upload_to="media/")
    
class Meta:
    db_table="payroll1"

class payroll2(models.Model):
    title2=models.CharField(max_length=100)
    description2 = RichTextField(default="")
class Meta:
    db_table="payroll2"

class termsandconditions1(models.Model):
    terms=models.CharField(max_length=100, null=True,blank=True)
    title=models.CharField(max_length=100, default="")
    content=models.TextField(default="")
    tid=models.IntegerField()
class Meta:
    db_table="termsandconditions"


class hr_management(models.Model):
    title=models.CharField(max_length=100)
    description = RichTextField()
    image1=models.ImageField(upload_to="media/",default="")
    image2=models.ImageField(upload_to="media/",default="")

class Meta:
    db_table="hr_management"



class peopleandemploy(models.Model):
    image=models.ImageField(upload_to="media/",default="")

    title=models.CharField(max_length=100)
    description=RichTextField()
class Meta:
    db_table="peopleandemploy"

class monitorlog(models.Model):
    title=models.CharField(max_length=100,default="")
    point1=models.CharField(max_length=100,default="")
    point2=models.CharField(max_length=100,default="")
    point3=models.CharField(max_length=100,default="")
    description1=RichTextField(default="")
    description2=RichTextField(default="")
    description3=RichTextField(default="")
    image=models.ImageField(upload_to="media/",default="")

class Meta:
    db_table="monitorlog"

class hr_benefits(models.Model):
    title=models.CharField(max_length=100)
    description=RichTextField()
class Meta:
    db_table="hr_benefits"


# Create your models here.
class teamlead(models.Model):
    title1=models.CharField(max_length=1000)
    content1=models.CharField(max_length=1000)
    content2=models.CharField(max_length=1000,default="")
    image1=models.ImageField(upload_to='images/')

class Meta:
    db_table="teamlead"
class teamlead1(models.Model):
    image2=models.ImageField(upload_to='images/')
class Meta:
    db_table="teamlead1"


# Create your models here.
class empperformance(models.Model):
    title1=models.CharField(max_length=1000)
    content1=models.CharField(max_length=1000)
    image1=models.ImageField(upload_to='images/')

class Meta:
    db_table="empperformance"

class empperformance1(models.Model):
    image2=models.ImageField(upload_to='images/')
class Meta:
    db_table="empperformance1"

# Create your models here.
class leavemanagement(models.Model):
    title1=models.CharField(max_length=1000)
    content1=models.CharField(max_length=1000)
    image1=models.ImageField(upload_to='images/')

class Meta:
    db_table="leavemanagement"

class leavemanagement1(models.Model):
    image2=models.ImageField(upload_to='images/')
class Meta:
    db_table="leavemanagement1"

class face(models.Model):
    description1=models.TextField()
    content1=models.TextField()
    content11=models.TextField(default="")
    content12=models.TextField(default="")
    image1=models.ImageField(upload_to="images/")
    description2=models.TextField()
    content2=models.TextField()
    content21=models.TextField(default="")
    content22=models.TextField(default="")
    image2=models.ImageField(upload_to="images/")
    description3=models.TextField()
    content3=models.TextField()
    content31=models.TextField(default="")
    content32=models.TextField(default="")
    image3=models.ImageField(upload_to="images/")
    description4=models.TextField()
    content4=models.TextField()
    content41=models.TextField(default="")
    content42=models.TextField(default="")
    image4=models.ImageField(upload_to="images/")
    description5=models.TextField()
    content5=models.TextField()
    content51=models.TextField(default="")
    content52=models.TextField(default="")
    image5=models.ImageField(upload_to="images/")

class Meta:
    db_table="face"  

class shifcards(models.Model):
    title=models.CharField(max_length=100)
    description=RichTextField()
class Meta:
    db_table="shifcards"

class shift1(models.Model):
    title=models.CharField(max_length=100)
    description=RichTextField()
    image=models.ImageField(upload_to="media/")
    image1=models.ImageField(upload_to="media/")

class Meta:
    db_table="shift1"

class shift2(models.Model):
    title=models.CharField(max_length=100)
    description=RichTextField()
    image=models.ImageField(upload_to="media/")

class Meta:
    db_table="shift2" 
         
class admin_profile1(models.Model):
    name=models.CharField(max_length=20)
    role=models.CharField(max_length=20)
    contactnumber=models.BigIntegerField()
    designation=models.CharField(max_length=20)
    gender=models.CharField(max_length=20)
    address=models.CharField(max_length=700)
    status=models.CharField(max_length=20)
    dateofbirth=models.DateField()
    class Meta:
        db_table="admin_profile1"


class Terms_and_Conditions1(models.Model):
    
    title=models.CharField(max_length=100, null=True,blank=True)
    content=models.TextField(null=True,blank=True)
   
class Meta:
    db_table="Terms_and_Conditions1"

class Privacy_and_Policy1(models.Model):
    
    title=models.CharField(max_length=100, null=True,blank=True)
    content=models.TextField(null=True,blank=True)
   
class Meta:
    db_table="Privacy_and_Policy1"

class Cancellation_Policy2(models.Model):
    
    title=models.CharField(max_length=100, null=True,blank=True)
    content=models.TextField(null=True,blank=True)
   
class Meta:
    db_table="Cancellation_Policy2"

class faceupdaterequest(models.Model):
    empid=models.ForeignKey(Employs, on_delete=models.CASCADE)
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE)
    requestdate=models.DateField(default=datetime.now, blank=True)
    status=models.IntegerField()
    reason=models.CharField(max_length=100)
    acceptdate=models.DateField(default=datetime.now, blank=True)

class Meta:
    db_table="faceupdaterequest"

class create_link(models.Model):
    title=models.CharField(max_length=100)
    date = models.DateField(default=date.today())
    time = models.TimeField(default="00:00:00")
    time1 = models.TimeField(default="00:00:00")
class Meta:
    db_table="create_link" 


class CheckInRequest(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
    cutoff_time = models.PositiveIntegerField()
    shift = models.ForeignKey(working_shifts, on_delete=models.CASCADE)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    status=models.IntegerField(default=0)

class ExtraTimeSlot(models.Model):
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    reason = models.CharField(max_length=255, help_text="Reason for the extra time")
    created_at = models.DateTimeField(default=datetime.now)
    employees = models.ManyToManyField('Employs', related_name='extra_times')

    def __str__(self):
        return f"{self.duration} minutes for {self.reason}"

class visitor(models.Model):
    visitorname=models.CharField(max_length=100)
    phonenumber=models.BigIntegerField()
    email=models.EmailField(default=None)
    place=models.CharField(max_length=100)
    hostname=models.CharField(max_length=100)
    reason=models.TextField()
    camera=models.ImageField(upload_to="media/")
    datetime=models.DateTimeField(default=datetime.now)
class Meta:
    db_table="visitor" 




class make_complaints(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="")
    employ_id=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    email = models.EmailField()
    description=models.TextField()
    correction=models.TextField()
class Meta:
    db_table="make_complaints"


class EmpGatePass1(models.Model):
    empid = models.CharField(max_length=100)
    emp_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='emp_qr_codes/', blank=True, null=True)
    bar_code = models.ImageField(upload_to='emp_bar_codes/', blank=True, null=True)
    numeric_identifier = models.BigIntegerField(unique=False,blank=True, null=True) 
    created_at = models.DateTimeField(default=datetime.now)
    emp_id=models.ForeignKey(Employs,on_delete=models.CASCADE,null=True, blank=True)
    date1 = models.CharField(max_length=100)
    starttime = models.CharField(max_length=100)
    endtime = models.CharField(max_length=100)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True, blank=True)

class Gate_pass_request1(models.Model):
    emp_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    reason=models.CharField(max_length=120)
    status=models.CharField(max_length=50)
    date1 = models.DateField(default=date.today())
    starttime = models.TimeField(default="00:00")
    endtime = models.TimeField(default="00:00")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True, blank=True)


class Employee_Qrcodes1(models.Model):
    employee_id = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=500)
    email_id = models.EmailField()
    contact_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    applyed_at = models.CharField(max_length=900)
    issued_at = models.CharField(max_length=900)
    numeric_id = models.BigIntegerField()
    captured_at = models.DateTimeField(default=datetime.now)
    reason = models.CharField(max_length=100,default="")
    starttime = models.CharField(max_length=100,default="")
    endtime = models.CharField(max_length=100,default="")
    emp_id=models.ForeignKey(Employs,on_delete=models.CASCADE,null=True, blank=True)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.employee_name

    class Meta:
        verbose_name_plural = "Employees"
        


class visitorentrance(models.Model):
    title1=models.CharField(max_length=1000)
    content1=models.CharField(max_length=1000)
    image1=models.ImageField(upload_to='images/')

class Meta:
    db_table="visitorentrance"

class visitorentrance1(models.Model):
    image2=models.ImageField(upload_to='images/')
class Meta:
    db_table="visitorentrance1" 

class buglegal_qns(models.Model):
    qns=models.CharField(max_length=1000)
    title2=models.CharField(max_length=100,default="")
    discription=models.CharField(max_length=1000)
    link = models.URLField(blank=True, null=True)  


class Meta:
    db_table="buglegal_qns"    

class timeqns(models.Model):
    qns=models.CharField(max_length=1000)
    title2=models.CharField(max_length=100,default="")
    discription=models.CharField(max_length=1000)
    link = models.URLField(blank=True, null=True)  


class Meta:
    db_table="timeqns"    


class payrol_qns(models.Model):
    qns=models.CharField(max_length=1000)
    title2=models.CharField(max_length=100,default="")
    discription=models.CharField(max_length=1000)
    link = models.URLField(blank=True, null=True)  


class Meta:
    db_table="payroll"    

# -------------content models---------

class IntroContent(models.Model):
    title = models.CharField(max_length=100)
    intro_text = models.TextField()
    setup_text = models.TextField()
    image = models.ImageField(upload_to='intro_images/')
    image2 = models.ImageField(upload_to='intro_images/')


    def __str__(self):
        return self.title

class Step(models.Model):
    intro_content = models.ForeignKey(IntroContent, on_delete=models.CASCADE)
    step_text = models.TextField()

    def __str__(self):
        return f"Step {self.id} for {self.intro_content.title}"


class managing_data(models.Model):
    title1=models.CharField(max_length=1000)
    des=models.CharField(max_length=1000,default="")
    subhead1=models.CharField(max_length=1000,default="")
    des1=models.CharField(max_length=1000,default="")
    subhead2=models.CharField(max_length=1000)
    des2=models.CharField(max_length=1000,default="")
class Meta:
    db_table="managing_data"   



class Trail(models.Model):
    title = models.CharField(max_length=200)
    steps = models.TextField()
    image = models.ImageField(upload_to='trail_images/')
    def __str__(self):
        return self.title


class help_notificationdata(models.Model):
    main_title=models.CharField(max_length=1000)

    title=models.CharField(max_length=1000)
    subhead=models.CharField(max_length=1000)
    point1=models.CharField(max_length=1000)
    point2=models.CharField(max_length=1000)
    des1=models.CharField(max_length=1000,default="")
    subhead=models.CharField(max_length=1000)
    des2=models.CharField(max_length=1000,default="")
    point3=models.CharField(max_length=1000)
    point4=models.CharField(max_length=1000)
    point5=models.CharField(max_length=1000)
    point6=models.CharField(max_length=1000)
    point7=models.CharField(max_length=1000)
class Meta:
    db_table="help_notificationdata"   

    


class abouttime_data1(models.Model):
    main_title=models.CharField(max_length=1000)
    des1=models.CharField(max_length=1000,default="")
    subhead=models.CharField(max_length=1000,default="")
    point1=models.CharField(max_length=1000, default="")
    point2=models.CharField(max_length=1000, default="")
    subhead2=models.CharField(max_length=1000,default="")
    point3=models.CharField(max_length=1000, default="")
    point4=models.CharField(max_length=1000,default="")
    point5=models.CharField(max_length=1000,default="")
class Meta:
    db_table="abouttime_data1"   


class abouttime_data2(models.Model):
    subhead3=models.CharField(max_length=1000,default="")
    point6=models.CharField(max_length=1000,default="")
    point7=models.CharField(max_length=1000, default="")
    point11=models.CharField(max_length=1000, default="")

    subhead4=models.CharField(max_length=1000, default="")
    des2=models.CharField(max_length=1000, default="")
    point8=models.CharField(max_length=1000 ,default="")
    point9=models.CharField(max_length=1000, default="")
    point10=models.CharField(max_length=1000, default="")

class Meta:
    db_table="abouttime_data2"   

class clock(models.Model):
    title = models.CharField(max_length=200)
    des1=models.CharField(max_length=1000, default="")
    des2=models.CharField(max_length=1000, default="")
    steps = models.TextField()

    def __str__(self):
        return self.title
    

class assignqns3(models.Model):

    title = models.CharField(max_length=200)
    des1=models.CharField(max_length=1000, default="")
    des2=models.CharField(max_length=1000, default="")
    steps = models.TextField()

    def __str__(self):
        return self.title


   
class breaksqns4(models.Model):

    title = models.CharField(max_length=200)
    des1=models.CharField(max_length=1000, default="")
    des2=models.CharField(max_length=1000, default="")
    steps = models.TextField()

    def __str__(self):
        return self.title


class faq5(models.Model):
    title=models.CharField(max_length=250)
    des=models.CharField(max_length=250)

    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question



class payroll_data1(models.Model):
    maintitle = models.CharField(max_length=500)
    des= models.CharField(max_length=500)
    title = models.CharField(max_length=1000)
    steps = models.TextField()

    def __str__(self):
        return self.title
    
class payroll_qns2(models.Model):
    maintitle = models.CharField(max_length=500)
    title = models.CharField(max_length=1000)
    steps = models.TextField()

    def __str__(self):
        return self.title



class payroll_qnsdata3(models.Model):
    title = models.CharField(max_length=1000)
    steps = models.TextField()

    def __str__(self):
        return self.title

class payroll_qnsdata4(models.Model):
    maintitle = models.CharField(max_length=500)
    title = models.CharField(max_length=1000)
    steps = models.TextField()

    def __str__(self):
        return self.title


class payroll_qnsdata5(models.Model):
    maintitle = models.CharField(max_length=500)
    des1= models.CharField(max_length=500)
    des1= models.CharField(max_length=500)
    title = models.CharField(max_length=1000)
    steps = models.TextField()

    def __str__(self):
        return self.title



class helptopic(models.Model):
    icon = models.ImageField(upload_to='icons/')
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
class Meta:
    db_table="helptopic"   


class helptopic2(models.Model):
    icon = models.ImageField(upload_to='icons/')
    title = models.CharField(max_length=200)
class Meta:
    db_table="helptopic2"   


from django.urls import reverse

class SOSEvent(models.Model):
    employ = models.ForeignKey('Employs', on_delete=models.CASCADE)
    company = models.ForeignKey('Companys', on_delete=models.CASCADE)
    admin = models.ForeignKey('AdminHod', on_delete=models.CASCADE)
    triggered_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"SOS triggered by {self.employ} at {self.triggered_at}"

    def is_active(self):
        return self.active and self.triggered_at >= datetime.now() - timedelta(minutes=1)

    def get_absolute_url(self):
        return reverse('sos_detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('sos_delete', args=[str(self.id)])
class documents_qns(models.Model):
    qns=models.CharField(max_length=1000)
    title2=models.CharField(max_length=100,default="")
    discription=models.CharField(max_length=10000)
    link = models.URLField(blank=True, null=True)  
class Meta:
    db_table="documents_qns"    

class documents_qa(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    line9=models.CharField(max_length=250)
    line10=models.CharField(max_length=250)
    line11=models.CharField(max_length=250)
    line12=models.CharField(max_length=250)
    line13=models.CharField(max_length=250)
    line14=models.CharField(max_length=250)
    line15=models.CharField(max_length=250)
    line16=models.CharField(max_length=250)
    line17=models.CharField(max_length=250)
    line18=models.CharField(max_length=250)
    line19=models.CharField(max_length=250)
    line20=models.CharField(max_length=250)
    line21=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa" 

class documents_qa1(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa1" 

class documents_qa2(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa2" 

class documents_qa3(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa3" 

class documents_qa4(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa4" 

class documents_qa5(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa5" 

class documents_qa6(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa6" 

class documents_qa7(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa7" 

class documents_qa8(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa8" 
class documents_qa9(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="documents_qa9" 

# Organization & Monitoring Logs 

class organization_qns(models.Model):
    qns=models.CharField(max_length=1000)
    title2=models.CharField(max_length=100,default="")
    discription=models.CharField(max_length=10000)
    link = models.URLField(blank=True, null=True)  
class Meta:
    db_table="organization_qns"    

class organization_qa(models.Model):
    question=models.CharField(max_length=1000)
    start=models.CharField(max_length=1000)
    intro=models.CharField(max_length=1000)
    line1=models.CharField(max_length=1000)
    line2=models.CharField(max_length=1000)
    line3=models.CharField(max_length=1000)
    line4=models.CharField(max_length=1000)
    line5=models.CharField(max_length=1000)
    line6=models.CharField(max_length=1000)
    line7=models.CharField(max_length=1000)
    line8=models.CharField(max_length=1000)
    line9=models.CharField(max_length=1000)
    line10=models.CharField(max_length=1000)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa"    

class organization_qa1(models.Model):
    question=models.CharField(max_length=100)
    start=models.CharField(max_length=100)
    intro=models.CharField(max_length=100)
    line1=models.CharField(max_length=225)
    line2=models.CharField(max_length=225)
    line3=models.CharField(max_length=225)
    line4=models.CharField(max_length=225)
    line5=models.CharField(max_length=225)
    line6=models.CharField(max_length=225)
    line7=models.CharField(max_length=225)
    line8=models.CharField(max_length=225)
    line9=models.CharField(max_length=225)
    line10=models.CharField(max_length=225)
    line11=models.CharField(max_length=225)
    line12=models.CharField(max_length=225)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa1"    

class organization_qa2(models.Model):
    question=models.CharField(max_length=100)
    start=models.CharField(max_length=100)
    intro=models.CharField(max_length=100)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    line9=models.CharField(max_length=250)
    line10=models.CharField(max_length=250)
    line11=models.CharField(max_length=250)
    line12=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa2"    

class organization_qa3(models.Model):
    question=models.CharField(max_length=100)
    start=models.CharField(max_length=100)
    intro=models.CharField(max_length=100)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    line9=models.CharField(max_length=250)
    line10=models.CharField(max_length=250)
    line11=models.CharField(max_length=250)
    line12=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa3"    

class organization_qa4(models.Model):
    question=models.CharField(max_length=100)
    start=models.CharField(max_length=100)
    intro=models.CharField(max_length=100)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    line9=models.CharField(max_length=250)
    line10=models.CharField(max_length=250)
    line11=models.CharField(max_length=250)
    line12=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa4"    

class organization_qa5(models.Model):
    question=models.CharField(max_length=250)
    start1=models.CharField(max_length=250)
    start2=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa5"    

class organization_qa6(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa6"    

class organization_qa7(models.Model):
    question=models.CharField(max_length=250)
    start1=models.CharField(max_length=250)
    start2=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa7"   

class organization_qa8(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    line8=models.CharField(max_length=250)
    line9=models.CharField(max_length=250)
    line10=models.CharField(max_length=250)
    line11=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa8"    

class organization_qa9(models.Model):
    question=models.CharField(max_length=250)
    start=models.CharField(max_length=250)
    intro=models.CharField(max_length=250)
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250)
    line3=models.CharField(max_length=250)
    line4=models.CharField(max_length=250)
    line5=models.CharField(max_length=250)
    line6=models.CharField(max_length=250)
    line7=models.CharField(max_length=250)
    image=models.ImageField(upload_to="media/",default="")
    link= models.URLField(blank=True, null=True)  

class Meta:
    db_table="organization_qa9"    

class helpdata7card(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata7card"

class helpdata8card(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata8card"

class helpdata9card(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata9card"

class helpdata71(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata71"

class helpdata72(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata72"

class helpdata73(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata73"

class helpdata74(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata74"


class helpdata75(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata75"

class helpdata76(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata76"

class helpdata77(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata77"

class helpdata78(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata78"
class helpdata81(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata81"


class helpdata82(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata82"

class helpdata83(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata83"   

class helpdata84(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata84"       


class helpdata91(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata91"

class helpdata92(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata92"

class helpdata93(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata93"

class helpdata94(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata94"


class helpdata95(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata95"


class helpdata96(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata96"


class helpdata97(models.Model):
    sno=models.IntegerField(blank=False, null=True)
    cardtitle = models.CharField(max_length=100, default="timezone.now")
    qns=models.CharField(max_length=1000,default="")
    line1=models.CharField(max_length=1000,default="")
    line2=models.CharField(max_length=1000,default="")
    line3=models.CharField(max_length=1000,default="")
    line4=models.CharField(max_length=1000,default="")
    line5=models.CharField(max_length=1000,default="")
    line6=models.CharField(max_length=1000,default="")
    image1=models.ImageField(default="",upload_to="media/")
    image2=models.ImageField(default="",upload_to="media/")
    link = models.URLField(blank=True, null=True)  

class Meta:
    db_table="helpdata97"

class cafeteria_allowance(models.Model):
    noofcoupons=models.CharField(max_length=500,default="0")
    amount=models.CharField(max_length=500,default="0")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True, blank=True)
    check_field=models.CharField(max_length=100,default="")

class Coupon_emp_all(models.Model):
    emp_id = models.ForeignKey('Employs', on_delete=models.CASCADE, null=True, blank=True)
    companyid = models.ForeignKey('Companys', on_delete=models.CASCADE, null=True, blank=True)
    coupon_id = models.PositiveIntegerField(unique=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    month=models.IntegerField(default="0")
    year=models.IntegerField(default="0")
    selected_emps=models.IntegerField(default="0")



class CouponIDTracker(models.Model):
    last_coupon_id = models.PositiveIntegerField(default=0)

class adminaddnav(models.Model):
    name=models.CharField(max_length=100)
    icon=models.CharField(max_length=100)
    url=models.CharField(max_length=100)
    admin_add_option=models.IntegerField(default="0")
    employ_add_option=models.IntegerField(default="0")



class EmpGatePass1(models.Model):
    empid = models.CharField(max_length=100)
    emp_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='emp_qr_codes/', blank=True, null=True)
    bar_code = models.ImageField(upload_to='emp_bar_codes/', blank=True, null=True)
    numeric_identifier = models.BigIntegerField(unique=False,blank=True, null=True) 
    created_at = models.DateTimeField(default=datetime.now)
    emp_id=models.ForeignKey(Employs,on_delete=models.CASCADE,null=True, blank=True)
    date1 = models.CharField(max_length=100)
    starttime = models.CharField(max_length=100)
    endtime = models.CharField(max_length=100)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True, blank=True)

class Gate_pass_request1(models.Model):
    emp_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    reason=models.CharField(max_length=120)
    status=models.CharField(max_length=50)
    date1 = models.DateField(default=date.today())
    starttime = models.TimeField(default="00:00")
    endtime = models.TimeField(default="00:00")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True, blank=True)

class CapturedQRCodedata(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    employid = models.CharField(max_length=100,default="")
    employname = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=100,default="")
    contactno = models.CharField(max_length=100,default="")
    designation = models.CharField(max_length=100,default="")
    reason = models.CharField(max_length=100,default="")
    applydate = models.CharField(max_length=100,default="")
    starttime = models.CharField(max_length=100,default="")
    endtime = models.CharField(max_length=100,default="")
    approvedate = models.CharField(max_length=100,default="")
    numeric_identifier = models.CharField(max_length=100,default="")
    companyid = models.ForeignKey(Companys, on_delete=models.CASCADE, null=True, blank=True)
    emp_id = models.ForeignKey(Employs, on_delete=models.CASCADE, null=True, blank=True)

class AdditionalFormData(models.Model):
    
    companyid = models.ForeignKey(Companys, on_delete=models.CASCADE)

    image1=models.ImageField(upload_to="images/")
    count = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    job_title=models.CharField(max_length=100,default="")
    department=models.CharField(max_length=100,default="")
    location=models.CharField(max_length=100,default="")
    openings=models.CharField(max_length=100,default="")
    education=models.CharField(max_length=100,default="")
    branch=models.CharField(max_length=100,default="")
    work_experience=models.CharField(max_length=100,default="")
    skills=models.CharField(max_length=100,default="")

class Recruitment(models.Model):
    heading=models.CharField(max_length=100)
    description1=models.TextField()
    description2=models.TextField()
    image=models.ImageField(upload_to="media/")  


from django.db import models

class Applicant(models.Model):
    company_id = models.ForeignKey(Companys, on_delete=models.CASCADE, default="")
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    resume = models.FileField(upload_to="media/")
    cover_letter = models.TextField()
    education = models.TextField()
    work_experience = models.TextField()
    skills = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    job_listing = models.ForeignKey(AdditionalFormData, on_delete=models.CASCADE,default="")
    task_status = models.CharField(max_length=10, choices=[('complete', 'Complete'), ('incomplete', 'Incomplete'), ('pending', 'Pending')], default='pending')
    marks = models.IntegerField(blank=True, null=True)
    grades = models.CharField(max_length=10, default="")
    exam_status = models.CharField(max_length=100, choices=[('qualified', 'Qualified'), ('disqualified', 'Disqualified')], default='pending')
    interview = models.CharField(max_length=10, choices=[('complete', 'Complete'), ('incomplete', 'Incomplete'), ('pending', 'Pending')], default='pending')
    interview_status = models.CharField(max_length=100, choices=[('qualified', 'Qualified'), ('disqualified', 'Disqualified')], default='pending')
    letter_status=models.IntegerField(default="0")
    branch=models.CharField(max_length=100,default="")
    remarks=models.CharField(max_length=100,default="pending")


    def __str__(self):
        return self.full_name 


from django.db import models

class InterviewSettings(models.Model):
    companyid = models.ForeignKey(Companys, on_delete=models.CASCADE)
    google_meet_link = models.URLField(blank=True)
    interview_time = models.DateTimeField(blank=True, null=True)
    interview_type = models.CharField(max_length=10, choices=[('virtual', 'Virtual'), ('offline', 'Offline')], default='virtual')


    def __str__(self):
        return "Interview Settings"
    

class Onboarding(models.Model):
    
    companyid = models.ForeignKey(Companys, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    Candidatephoto=models.ImageField(upload_to="media/") 
    email = models.EmailField()
    Offerletter= models.FileField(upload_to="media/")
    contactno=models.CharField(max_length=100) 
    Adharno=models.CharField(max_length=100,default="")
    Panno=models.CharField(max_length=100,default="")
    IFSC=models.CharField(max_length=100,default="")
    Experience=models.FileField(upload_to="media/",default="")
    designation=models.CharField(max_length=100,default="")
    Language=models.CharField(max_length=100,default="")
    Payslip=models.FileField(upload_to="media/",default="")
    studycertificate=models.FileField(upload_to="media/",default="")
    markssheet=models.FileField(upload_to="media/",default="")
    Resignationletter=models.FileField(upload_to="media/",default="")
    PFno=models.CharField(max_length=100,default="")
    Accountnumber=models.CharField(max_length=100,default="")
    dateofjoining=models.DateField(default=date.today())
    linkedin=models.CharField(max_length=100,default="")
    twitter=models.CharField(max_length=100,default="")
    title=models.CharField(max_length=100,null=True, blank=True)
    yearsofexperience=models.CharField(max_length=100,null=True, blank=True,default="")
    job_description=models.CharField(max_length=100,null=True, blank=True)
    last_name=models.CharField(max_length=100,default="")
    dateofbirth=models.DateField(default=date.today())
    gender=models.CharField(max_length=100,default="")
    address=models.TextField(default="")
    bloodgroup=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=100,default="")
    city=models.CharField(max_length=100,default="")
    pincode=models.IntegerField(default="0")




class OfferLetter(models.Model):
    companyid = models.ForeignKey('Companys', on_delete=models.CASCADE,default="")
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    offer_letter_release_date = models.DateField()
    joining_date = models.DateField()
    acceptance_date = models.DateField()
    offer_letter_pdf = models.FileField(upload_to='offer_letters/', blank=True, null=True)
    email = models.EmailField(default="")


    def __str__(self):
        return f"Offer Letter for {self.name} for {self.position}"



class Candidate(models.Model):
    companyid = models.ForeignKey(Companys, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    Last_name=models.CharField(max_length=100)
    email=models.EmailField()
    Official_mail=models.EmailField()
    contactno=models.CharField(max_length=100,default="")
    job_role=models.CharField(max_length=100)
    address=models.TextField()
    image=models.ImageField(upload_to="media/")
    street=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    Pincode=models.IntegerField()
    Experience=models.FileField(upload_to="media/",default="")
    current_salary=models.IntegerField()
    source_of_hire=models.CharField(max_length=100)
    skills=models.CharField(max_length=100)
    offer_letter=models.FileField(upload_to="media/")
    Nationality=models.CharField(max_length=100,default="")
    AadharNo=models.CharField(max_length=100, default="")
    PanNo=models.CharField(max_length=100,default="")
    dob = models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=100,default="")
    Aadharimage=models.FileField(upload_to="media/",default="")
    Panimage=models.FileField(upload_to="media/",default="")
    designation=models.CharField(max_length=100,default="")
    Payslip=models.FileField(upload_to="media/",default="")
    Relivingletter=models.FileField(upload_to="media/",default="")
    PFno=models.CharField(max_length=100,default="")





class Recruitment2(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to="media/") 
    title1=models.CharField(max_length=100,default="")
    description1=models.TextField(default="")
    image1=models.ImageField(upload_to="media/",default="")
    title2=models.CharField(max_length=100,default="")
    description2=models.TextField(default="")
    image2=models.ImageField(upload_to="media/",default="")     