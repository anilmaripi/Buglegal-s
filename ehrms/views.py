import datetime
import json
import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from login_required import login_not_required
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render ,redirect
from django.urls import reverse

from ehrms.models import CustomUser,HR,adminnav,Employs,project_drop,admin_home_drop,admin_drop,home6,freetraildays
from worktride import settings

from django.shortcuts import render, redirect
from django.contrib import messages
import requests,random
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Companys
from django.utils import timezone
from datetime import datetime,timedelta
import pytz

#  Installing Required packages
import sys
import subprocess
from subprocess import STDOUT, check_call

def install_dependencies():
    devnull = open(os.devnull, "w")
    
    def run_command(command):
        return check_call(command, stdout=devnull, stderr=STDOUT)

    # Check if libgl1-mesa-glx is installed
    retval = subprocess.call(["dpkg", "-s", "libgl1-mesa-glx"], stdout=devnull, stderr=subprocess.STDOUT)
    
    if retval != 0:
        # Update and install system dependencies
        system_commands = [
            ['apt-get', 'update'],
            ['apt-get', 'install', '-y', 'libgl1-mesa-glx'],
            ['apt-get', 'install', '-y', 'libglib2.0-0'],
            ['apt-get', 'install', '-y', 'tk'],
        ]
        
        for command in system_commands:
            run_command(command)
 
    else:
        print("Dependencies are already installed")
    
    devnull.close()

# Call the function when necessary in your application
install_dependencies()

# End of package installation

def showDemoPage(request):
    return render(request,"demo.html")
    
# def ShowLoginPage(request):
#     return render(request,"login_page.html")

def ShowLoginPage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1 :
            return HttpResponseRedirect("/adminAdashboard/")
        elif request.user.user_type =="1":
            compcheck=Companys.objects.filter(usernumber=request.user.id).first()
            if compcheck:
               return HttpResponseRedirect('/admin_home')
            else:
                messages.error(request,"Invalid Credentails")
                logout(request)
                return HttpResponseRedirect('/show_login/')
        else:
            compchecks=Employs.objects.filter(admin=request.user.id).first()
            if compchecks:
               return HttpResponseRedirect("/Employ_home")
            else:
                messages.error(request,"Invalid Credentails")
                logout(request)
                return HttpResponseRedirect('/show_login/')
    else:
       return render(request,"login_page.html")
       

# def doLogin(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
        # captcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        # cap_data={"secret":cap_secret,"response":captcha_token}
        # cap_server_response=requests.post(url=cap_url,data=cap_data)
        # cap_json=json.loads(cap_server_response.text)

        # if cap_json['success']==False:
        #     messages.error(request,"Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/")

        # user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        # if user is not None and user != "multipleuser":
        #     request.session['email_2']=user.email;
        #     login(request,user)
        #     if user.is_superuser == 1 :
        #             return HttpResponseRedirect("/adminAdashboard/")
        #     else:
        #         companys=Companys.objects.filter(usernumber=request.user.id).first()
        #         loginemploy=Employs.objects.filter(admin=request.user.id).first()
        #         if loginemploy:
        #           compid=Companys.objects.filter(id=loginemploy.companyid.id).first()
        #         if companys:
        #             fretraile=companys.freetraile
        #             plandate=companys.date
        #         elif loginemploy:
        #             fretraile=compid.freetraile
        #             plandate=compid.date
        #         else:
        #             fretraile=None
        #             plandate=None
        #         current_date1 = datetime.now(pytz.utc) 
        #         if plandate:
        #            logindate_datetime = datetime.combine(plandate, datetime.min.time(), tzinfo=pytz.utc)
        #         else:
        #             logindate_datetime=None
        #         free=freetraildays.objects.first()
        #         freeday=free.freedays
        #         month=free.monthly
        #         year=free.yearly
        #         if plandate and (current_date1 - logindate_datetime).days > freeday and fretraile == 1:
        #             messages.error(request,"Your Free Trail Expired")
        #             return HttpResponseRedirect("/show_login")
        #         elif plandate and (current_date1 - logindate_datetime).days >month and fretraile == 0:
        #             messages.error(request,"Your Plan Expired")
        #             return HttpResponseRedirect("/show_login")
        #         elif plandate and (current_date1 - logindate_datetime).days >year and fretraile == 2:
        #             messages.error(request,"Your Plan Expired")
        #             return HttpResponseRedirect("/show_login")
        #         else:
        #             if user.user_type == "2" :               
        #                 user.save_login_record()
        #             if user.user_type=="1":
        #                 if companys :
        #                     return HttpResponseRedirect('/admin_home')  
        #                 else:
        #                      return HttpResponseRedirect("/show_login")    

        #             if  user.user_type == "0" :
        #                 messages.error(request,"You have been disabled")
        #                 return HttpResponseRedirect("/show_login")    
        #             else:
        #                 if compid:
        #                     return HttpResponseRedirect(reverse("Employ_home"))
        #                 else:
        #                     return HttpResponseRedirect("/show_login")    

        # elif user == "multipleuser" :
        #     messages.error(request,"Invalid")
        #     return HttpResponseRedirect("/show_login")
        # else:
        #     messages.error(request,"Invalid Username or Password")
        #     return HttpResponseRedirect("/show_login")

from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
import pytz
from ehrms.models import CustomUser

def doLogin(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)  
        if user is not None:
            login(request, user)
            return redirect_authenticated_user(request, user)
        else:
            messages.error(request, "Invalid Username or Password")
            return HttpResponseRedirect("/show_login")
    
    else:
        return HttpResponseRedirect("/show_login")

def social_login_complete(request):
    user_id = request.session.get('socialaccount_user')
    backend = request.session.get('socialaccount_backend')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            login(request, user,backend=backend)
            return redirect_authenticated_user(request, user)
        except User.DoesNotExist:
            messages.error(request, "User not found")
    else:
        messages.error(request, "Social login error")
    return redirect('/show_login')



def redirect_authenticated_user(request, user):
    if user.is_superuser:
        return HttpResponseRedirect("/adminAdashboard/")
    else:
        companys=Companys.objects.filter(usernumber=request.user.id).first()
        loginemploy=Employs.objects.filter(admin=request.user.id).first()
        compid = None
        fretraile = None
        plandate = None
        
        if loginemploy:
            compid = loginemploy.companyid
        if companys:
            fretraile = companys.freetraile
            plandate = companys.date
        elif loginemploy:
            compid = loginemploy.companyid
            fretraile = compid.freetraile
            plandate = compid.date
        
        current_date = datetime.now(pytz.utc)
        if plandate:
            logindate_datetime = datetime.combine(plandate, datetime.min.time(), tzinfo=pytz.utc)
        else:
            logindate_datetime = None
        
        free = freetraildays.objects.first()
        freeday = free.freedays
        month = free.monthly
        year = free.yearly

        if plandate and (current_date - logindate_datetime).days > freeday and fretraile == 1:
            messages.error(request, "Your Free Trail Expired")
            return HttpResponseRedirect("/show_login")
        elif plandate and (current_date - logindate_datetime).days > month and fretraile == 0:
            messages.error(request, "Your Plan Expired")
            return HttpResponseRedirect("/show_login")
        elif plandate and (current_date - logindate_datetime).days > year and fretraile == 2:
            messages.error(request, "Your Plan Expired")
            return HttpResponseRedirect("/show_login")
        else:
            if user.user_type == "2":
                user.save_login_record()
            if user.user_type == "1":
                if companys:
                    return HttpResponseRedirect('/admin_home')
                else:
                    return HttpResponseRedirect("/show_login")

            if user.user_type == "0":
                messages.error(request, "You have been disabled")
                return HttpResponseRedirect("/show_login")
            else:
                if compid:
                    return HttpResponseRedirect(reverse("Employ_home"))
                else:
                    return HttpResponseRedirect("/show_login")



def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):

    if request.user.user_type == "2" :
        request.user.save_logout_record() 
    logout(request)
    return HttpResponseRedirect("/show_login/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("Ok")

def signup_admin(request):
    return render(request,"signup_admin_page.html")
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Companyregister

def company_list(request):
    search_query = request.GET.get('se')
    companies = Companys.objects.all()

    if search_query:
        companies = companies.filter(contact_person__icontains=search_query)
        companies = companies.filter(organizationname__icontains=search_query)

    items_per_page = 10 
    paginator = Paginator(companies, items_per_page)
    page = request.GET.get('page')

    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        agreement_status = request.POST.get('agreement_status')

        if company_id is not None and agreement_status is not None:
            try:
                company = Companys.objects.get(id=company_id)
                company.agreement_status = int(agreement_status)
                company.save()

                if agreement_status == '1':
                    subject = 'Agreement Accepted'
                    message = f'Thank you, we have accepted your agreement, {company.username}!'
                elif agreement_status == '2':
                    subject = 'Agreement Declined'
                    message = f'Sorry, we have not accepted your agreement, {company.username}!'
                else:
                    subject = 'Agreement Status Update'
                    message = f'Agreement status updated for {company.username}.'

                from_email = 'developtrees1@gmail.com'
                to_email = [company.email]

                send_mail(subject, message, from_email, to_email, fail_silently=False)

                return redirect('company_list')  # Redirect to avoid resubmission on refresh
            except Companys.DoesNotExist:
                return HttpResponse("Company not found", status=404)
            except Exception as e:
                return HttpResponse(f"Error: {str(e)}", status=500)
 
    return render(request,'admin-template/company_list.html', {'companies': companies, 'search_query': search_query})
def contact_retrieve(request):
    sh=Contact.objects.all()
    items_per_page = 5


    paginator = Paginator(sh, items_per_page)
    page = request.GET.get('page')

    try:
        sh = paginator.page(page)
    except PageNotAnInteger:
        sh = paginator.page(1)
    except EmptyPage:
        sh = paginator.page(paginator.num_pages)
    return render(request,"contact_retrieve.html",{'sh':sh})


def formdeatiles(request,id):
    post=Addonsuser.objects.filter(companyid=id)
    post1=Companys.objects.filter(id=id).first()
    cdate=post1.date
    free1=post1.freetraile
    free=freetraildays.objects.first()
    freeday=free.freedays
    current_date1 = datetime.now(pytz.utc) 
    if free1 == 0:
      logindate_datetime = datetime.combine(cdate, datetime.min.time(), tzinfo=pytz.utc)+timedelta(days=30)
    elif free1 == 2:
        logindate_datetime = datetime.combine(cdate, datetime.min.time(), tzinfo=pytz.utc)+timedelta(days=300)
    elif free1 == 1:
        logindate_datetime = datetime.combine(cdate, datetime.min.time(), tzinfo=pytz.utc)+timedelta(days=freeday)
    plancheck=current_date1 > logindate_datetime
    remainingdays1=(current_date1-logindate_datetime).days

    # logindate_datetime = datetime.combine(cdate, datetime.min.time(), tzinfo=timezone.utc)+timedelta(days=30)
    # remainingdays=(current_date1-logindate_datetime).days
        
   

    return render(request,'admin-template/update.html',{'post1':post1,'remainingdays1':remainingdays1, 'post':post,'plancheck':plancheck})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Companyregister.objects.get(username=username, password=password)

            if user.agreement_status == 1:
                request.session['user_id'] = user.id 
                return redirect("/reg")
            elif user.agreement_status == 0:
                error_message = "Your registration process is in progress. Please wait for approval."
                return render(request, "admin-template/login.html", {'error_message': error_message})
            elif user.agreement_status == 2:
                error_message = "Your registration has been rejected. Please contact the admin for more information."
                return render(request, "admin-template/login.html", {'error_message': error_message})
           

        except Companyregister.DoesNotExist:
            error_message = "Invalid login credentials. Please try again."
            return render(request, "admin-template/login.html", {'error_message': error_message})

    return render(request, "admin-template/login.html")


def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    # try:
    user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
    user.email=email
    user.save()
    messages.success(request,"Successfully Created Admin")
    return HttpResponseRedirect(reverse("show_login"))
    # except:
    #     messages.error(request,"Failed to Create Admin")
    #     return HttpResponseRedirect(reverse("show_login"))
def signup_employ(request):
    return render(request,"registration/signup_employ_page.html")


def do_employ_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.save()
        messages.success(request,"Successfully Created Employ")
        return HttpResponseRedirect(reverse("signup_employ"))
    except:
        messages.error(request,"Failed to Create employ")
        return HttpResponseRedirect(reverse("signup_employ"))



from .models import AdminHod


def admin_Password(request):
   
    usernumber = Companys.objects.filter(usernumber=request.user.id).first()

   
    if usernumber:
        user = CustomUser.objects.filter(id=request.user.id).first()
        userid1 = user.id
        try:
            admin = Companys.objects.get(id=1) 
        except Companys.DoesNotExist:
            admin = None

        s = adminnav.objects.all()
        h = HR.objects.all()
        employs_all = Employs.objects.all()
        # admin_drops = admin_drop.objects.filter(parent_category=None).order_by('id')
        # admin_home_drops = admin_home_drop.objects.filter(parent_category=None).order_by('id')
        data = Companys.objects.filter(id=request.user.id)
        # projects_drops = project_drop.objects.filter(parent_category=None).order_by('id')

        return render(request, "admin-template/admin_password.html", {
            'usernumber': usernumber,
            'user': user,
            'admin': admin,
            # 'admin_home_drops': admin_home_drops,
            's': s,
            'h': h,
            # 'projects_drops': projects_drops,
            'data': data,
            'employs_all': employs_all,
            # 'admin_drops': admin_drops
        })






from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash

def admin_Password_save(request):
   
    if request.user.is_authenticated:
        if request.method == "POST":
            password = request.POST.get("password")
            
            customuser = request.user
            
            if password is not None and password != "":
                customuser.set_password(password)
                customuser.save()
                
               
                update_session_auth_hash(request, customuser)
                
                messages.success(request, 'Password changed successfully.')
                return redirect('/show_login')
    
    return render(request, "admin-template/admin_Password.html")


from django.shortcuts import render, redirect
from .models import Companys
from django.contrib import messages
import requests,random
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Companys,editholiday12,halfldayvreason,employedata,task1


def send_msg(number, message, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    api = "NRvfwbSioQCdmu4B18zHDX9rTaF7xpjVkJ2YgUc3tsALKEZnqMgOSwY0HuKL1GVcAzXNIDW6Qq3Jfedt"
    querystring = {"authorization": api, "sender_id": "TEERDHA", "message": message, "language": "english", "route": "otp", "numbers": number, "variables_values": otp, "flash": "0"}
    headers = {'cache-control': "no-cache"}
    return requests.get(url, headers=headers, params=querystring)

def store_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        request.session['phone_number'] = phone_number
        response_data = {'success': True}
        return JsonResponse(response_data)

def send_otp(request):
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')

        if phone_number:
            otp = random.randint(1000, 9999)
            request.session['generated_otp'] = otp

            response = send_msg(phone_number, "Your OTP is: {}".format(otp), otp)

            if response.status_code == 200:
                response_data = {'success': True}
            else:
                response_data = {'success': False, 'error': 'Failed to send OTP via SMS.'}
        else:
            response_data = {'success': False, 'error': 'Phone number not found in session.'}

        return JsonResponse(response_data)

    # Return a 405 Method Not Allowed response for GET requests
    return HttpResponseNotAllowed(['POST'])

def resend_otp(request):
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')

        if phone_number:
            otp = random.randint(1000, 9999)
            request.session['generated_otp'] = otp

            response = send_msg(phone_number, "Your OTP is: {}".format(otp), otp)

            if response.status_code == 200:
                response_data = {'success': True}
            else:
                response_data = {'success': False, 'error': 'Failed to send OTP via SMS.'}
        else:
            response_data = {'success': False, 'error': 'Phone number not found in session.'}

        return JsonResponse(response_data)

    # Return a 405 Method Not Allowed response for GET requests
    return HttpResponseNotAllowed(['POST'])

def verify_otp(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('generated_otp', '')

        if user_entered_otp == str(generated_otp):
            response_data = {'message': 'OTP is valid.'}
        else:
            response_data = {'message': 'Invalid OTP. Please try again.'}

        return JsonResponse(response_data)



from django.contrib.auth import get_user_model

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Companys,set_payroll_date,working_shifts
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from ehrms.models import CustomUser

def adminA(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            error_message = "Invalid login credentials. Please try again."
            return render(request, "admin-template/adminA.html", {'error_message': error_message})
        
        if check_password(password, user.password):
            return redirect('/adminAdashboard')
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, "admin-template/adminA.html", {'error_message': error_message})

    return render(request, "admin-template/adminA.html")


def logout_view(request):
    logout(request)
    return redirect("/adminA")

# from django.contrib.auth.decorators import user_passes_test
# @login_required(login_url="/show_login")
# @user_passes_test(lambda u: u.is_superuser)
# def adminAdashboard(request):
#     return render(request, "admin-template/adminAdashboard.html")

def adminAdashboard(request):
    superadminpic = adminphoto.objects.all()
    notifications = Companys.objects.all()  # For superusers, get all notifications
    notifications=ContactMessage.objects.all()
    
    notification_count = notifications.count()
  
    return render(request, "admin-template/adminAdashboard.html", {
        'superadminpic': superadminpic,
        'notifications': notifications,
        'notification_count': notification_count
       
    })
   

def supernotification(request):
    return render(request,"admin-template/superadmin.html")
from notifications.models import Notification
def super_mark_as_read(request, notifi_id):
    if request.method == "POST":
        notification = Notification.objects.get(id=notifi_id)
        notification.mark_as_read()

        if notification.verb == 'Company Registered':
            description_parts = notification.description.split()
            plan_name = description_parts[-2].lower()  
            if plan_name == 'basic':
                return redirect("/company_list1/")
            elif plan_name == 'gold':
                return redirect("/company_list2/")
            elif plan_name == 'platinum':
                return redirect("/company_list3/")
            elif plan_name == 'diamond':
                return redirect("/company_list4/")
            else:
                return redirect("/company_list/")  
            
        elif notification.verb == 'Contact':
            return redirect("/contact-messages/")  
        
        elif notification.verb == 'Demo':
            return redirect("/solution5/")  
        else:
            return redirect("/") 

    return redirect("/")  
from django.shortcuts import redirect
import time
from threading import Thread
from django.template.loader import render_to_string

# def send_followup_email_after_delay(email, delay,message):
#     time.sleep(delay)
    
#     subject = 'Follow-up Email'
#     from_email = 'developtrees1@gmail.com'  

#     send_mail(subject,message,  from_email, [email])



def send_followup_email_after_delay1(email, delay,message):
    time.sleep(delay)

    registration_link =  "https://rzp.io/i/kvy1M77V2"

    
    subject = 'Follow-up Email'
    from_email = 'developtrees1@gmail.com'
    context = {'registration_link': registration_link}

    message = render_to_string('sms2_template.html', context)
    

    send_mail(subject,message,  from_email, [email],html_message=message)




def send_followup_email_after_delay2(email, delay,message):
    time.sleep(delay)

    registration_link =  "https://rzp.io/i/kvy1M77V2"

    
    subject = 'Follow-up Email'
    from_email = 'developtrees1@gmail.com'
    context = {'registration_link': registration_link}

    message = render_to_string('sms3_template.html', context)


    send_mail(subject,message,  from_email, [email],html_message=message)


def send_followup_email_after_delay3(email, delay,message):
    time.sleep(delay)

    registration_link =  "https://rzp.io/i/kvy1M77V2"

    
    subject = 'Follow-up Email'
    from_email = 'developtrees1@gmail.com'
    context = {'registration_link': registration_link}

    message = render_to_string('sms4_template.html', context)
    

    send_mail(subject,message,  from_email, [email],html_message=message)



def send_followup_email_after_delay4(email, delay,message):
    time.sleep(delay)

    registration_link =  "https://rzp.io/i/kvy1M77V2"

    
    subject = 'Follow-up Email'
    from_email = 'developtrees1@gmail.com'
    context = {'registration_link': registration_link}

    message = render_to_string('sms5_template.html', context)


    send_mail(subject,message,  from_email, [email],html_message=message)



def send_followup_email_after_delay5(email, delay,message):
    time.sleep(delay)

    registration_link =  "https://rzp.io/i/kvy1M77V2"

    
    subject = 'Follow-up Email'
    from_email = 'developtrees1@gmail.com'
    context = {'registration_link': registration_link}

    message = render_to_string('sms6_template.html', context)


    send_mail(subject,message,  from_email, [email],html_message=message)



def send_sms(phone_number, message):
    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        api = "NRvfwbSioQCdmu4B18zHDX9rTaF7xpjVkJ2YgUc3tsALKEZnqMgOSwY0HuKL1GVcAzXNIDW6Qq3Jfedt"
        querystring = {
            "authorization": api,
            "sender_id": "FSTSMS",
            "message": message,
            "language": "english",
            "route": "q",
            "numbers": phone_number,
            "flash": "0",
        }
        headers = {
            'cache-control': "no-cache"
        }
        response = requests.get(url, headers=headers, params=querystring)

        # Check the response status code
        if response.status_code == 200:
            return True  # SMS sent successfully
        else:
            print(f"Failed to send SMS. Status code: {response.status_code}")
            return False

    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False

from apscheduler.schedulers.background import BackgroundScheduler
import datetime

def send_sms_after_15_days(phone_number, message):
    # Your send_sms function here
    # ...
    # ...
    message = f"your free trial is expired today"

    # ...
    if send_sms(phone_number, message):                      
        print("SMS sent successfully")
    else:
        print("Failed to send SMS")


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_username_existadmin(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_email_existadmin(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


CustomUser = get_user_model()

def register_company(request,id):
    request.session['planid']=id
    if request.method == 'POST':
        organizationname = request.POST.get('organizationname')
        registration_number = request.POST.get('registration_number')
        address = request.POST.get('address')
        contact_person = request.POST.get('contact_person')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        # Numberofemployees = request.POST.get('Numberofemployees')
        your_title = request.POST.get('your_title')
        user_entered_otp = request.POST.get("otp")
        generated_otp = request.session.get('generated_otp', '')

        # Verify OTP
        if user_entered_otp == str(generated_otp):
            try:
                user = CustomUser.objects.get(email=email)
                messages.error(request,'User With This Email Already Exists.')
                return render(request, 'admin-template/company_register.html')
            except CustomUser.DoesNotExist:
                # User does not exist, create a new one
                user = CustomUser(username=contact_person, email=email)
                user.set_password(password)
                user.save()
            except IntegrityError as e:
                messages.error(request, f'Error creating or retrieving user: {e}')
                return render(request, 'admin-template/company_register.html')
            
            company_plan = typeofplans.objects.get(id=id)
            company=Companys.objects.create(
                usernumber=user,
                organizationname=organizationname,
                registration_number=registration_number,
                address=address,
                contact_person=contact_person,
                email=email,
                phone_number=phone_number,
                password=password,
                # Numberofemployees=Numberofemployees,
                # your_title=your_title,
                otp=user_entered_otp,
                plantype=id,
            
                

            )
             
            
            editholidays=editholiday12.objects.create(
                companyid=company,
                sun=1
            )
            halfreason=halfldayvreason.objects.create(
                companyid=company,
                halfdaylev=1,
                reason1=1

            )
            emplenght=employedata.objects.create(
                companyid=company
            )
            taskdat=task1.objects.create(
                companyid=company
            )
            payroll1=set_payroll_date.objects.create(
                companyid=company
            )
            workshift=working_shifts.objects.create(
                 companyid=company,
                 cutoff_time=2,
                 befor_time=10,
                 shift_name="general"
            )
            companydetail=company_details.objects.create(
                companyid=company
            )

            salarycomponent=['Basic Salary','HRA','LTA']
            percentageofCTC=['50','30','20']
            percentageorfixed=['Percentage','Percentage','Percentage']
           
            salaryid=['1','2','3']
            percentageofCTC1 = [value for value in percentageofCTC if value.strip()]
            percentageofCTC_int = [int(x) for x in percentageofCTC1]
            sum_of_percentageofCTC = sum(percentageofCTC_int)
            if len(salarycomponent) == len(percentageofCTC) == len(salaryid):
              if sum_of_percentageofCTC == 100:
                 for sal,pectc,pefix,salid in zip(salarycomponent,percentageofCTC,percentageorfixed,salaryid):
                   if sal:
                        preup,persave=salary_struct.objects.get_or_create(salaryid=salid,defaults={'salarycomponent':sal,'percentageofCTC':pectc,'percentageorfixed':pefix},companyid=company)

            registration_link =  "https://rzp.io/i/kvy1M77V2"

            subject = 'Registration Successful'
            context = {'registration_link': registration_link}
            message = render_to_string('sms1_template.html', context)

            from_email = 'developtrees1@gmail.com'  
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list,html_message=message)
            date13 = datetime.now() + timedelta(days=13)
            Thread(target=send_followup_email_after_delay1, args=(email, date13, 'your free trial is expired with in 2 days')).start()  

            date14 = datetime.now() + timedelta(days=14)
            Thread(target=send_followup_email_after_delay2, args=(email, date14, 'your free trial is expired with in 1 days')).start() 

            date15 = datetime.now() + timedelta(days=15)
            Thread(target=send_followup_email_after_delay3, args=(email, date15, 'your free trial is expired today')).start() 

            date16 = datetime.now() + timedelta(days=16)
            Thread(target=send_followup_email_after_delay4, args=(email, date16, 'Your free trial is expired recharge now')).start() 

            date17 = datetime.now() + timedelta(days=17)
            Thread(target=send_followup_email_after_delay5, args=(email, date17,  'your free trial is expired')).start() 

            # Thread(target=send_followup_email_after_delay1, args=(email,180,'your free trial expire soon')).start()  
            # Thread(target=send_followup_email_after_delay2, args=(email, 300,'your free trial expire tommorow')).start() 
            # Thread(target=send_followup_email_after_delay3, args=(email, 360,'your free trial expire today')).start() 
            # Thread(target=send_followup_email_after_delay4, args=(email, 420,'your free trial expired 1day ago')).start() 
            # Thread(target=send_followup_email_after_delay5, args=(email, 480,'your free trial expired 2days ago')).start() 
            scheduler = BackgroundScheduler()
            scheduler.add_job(send_sms_after_15_days, 'date', run_date=datetime.now() + timedelta(days=1), args=[phone_number, message])
            scheduler.start()


            receiver_user = CustomUser.objects.filter(is_superuser=1).first()
            notify.send(
                sender=company.usernumber,
                recipient=receiver_user,
                verb='Company Registered',
                description=f"{organizationname} has registered for the {company_plan.annual_price}."

           )


            message = f"Registration Successfully"
            if send_sms(phone_number, message):                      
                print("SMS sent successfully")
            else:
                print("Failed to send SMS")


           

            messages.success(request, "Sucessfully registered ")
            del request.session['generated_otp']
            return redirect('/show_login/')
            
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'admin-template/company_register.html')

    return render(request, 'admin-template/company_register.html')


def planexpireauthentication(request):
    if request.method == "POST":
        user=authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user is not None:
            request.session['email_2']=user.email;
            request.session['password']=user.password
            if user:
                return HttpResponseRedirect('/planexpire_payment/')
            else:
                return HttpResponse("you Don't have any active Plan")
        else:
            messages.error(request,"Invalid Username or Password")
    return render(request,"addonauthentication.html")


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import admin_drop





from ehrms.models import nav1,nav2
def nav1_insertform(request):
    if request.method=='POST':
        photo= request.FILES.get('photo')
        name=request.POST['name']
        url=request.POST['url']
    
        k=nav1(name=name,url=url,photo=photo)
        k.save()
    return render(request, "nav_insertform.html")


def  nav_retrieve(request):
    k5=nav1.objects.all()
    return render(request,"nav_retrieve.html",{"k5":k5})

def nav2_insertform(request):
    if request.method=='POST':       
        name=request.POST['name']
        url=request.POST['url']
    
        k=nav2(name=name,url=url)
        k.save()
    return render(request, "nav2_insertform.html")

def  nav2_retrieve(request):
    k=nav2.objects.all()
    return render(request,"nav2_retrieve.html",{"k":k})


def nav(request):
    return render(request,"nav.html")

from .models import NavbarItem







def navbar_retrieve(request):
    navbar_items = NavbarItem.objects.filter(parent=None)
    return render(request, 'index.html', {'navbar_items': navbar_items})


def add_navbar_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        photo1= request.FILES.get('photo1')
        parent_id = request.POST.get('parent')
        url = request.POST.get('url')
        links = FooterLink.objects.all()
        services = FooterService.objects.all()
        contact_info = ContactInfo.objects.first()
        social = SocialLink.objects.all()


        parent = NavbarItem.objects.get(id=parent_id) if parent_id else None

        NavbarItem.objects.create(name=name, parent=parent, url=url,photo1=photo1)

    navbar_items = NavbarItem.objects.all()
    return render(request, 'add_navbar_item.html', {'navbar_items': navbar_items, 'links': links,
        'services': services,
        'contact_info': contact_info,'social':social})



from .models import admin_drop, adminnav, employnav, employ_drop, project_drop,screenmon,Addons




def subscription(request):
    k=typeofplans.objects.filter(plans__contains='4')
    k1=typeofplans.objects.filter(plans__contains='5')
    k2=typeofplans.objects.filter(plans__contains='6')
    k3=typeofplans.objects.filter(plans__contains='Based on demand')
    a=typeofplans.objects.filter(plans__contains='4')
    a1=typeofplans.objects.filter(plans__contains='5')
    a2=typeofplans.objects.filter(plans__contains='6')
    a3=typeofplans.objects.filter(plans__contains='Based on demand')
    b=typeofplans.objects.filter(plans__contains='4')
    b1=typeofplans.objects.filter(plans__contains='5')
    b2=typeofplans.objects.filter(plans__contains='6')
    b3=typeofplans.objects.filter(plans__contains='Based on demand')
    c=typeofplans.objects.filter(plans__contains='4')
    c1=typeofplans.objects.filter(plans__contains='5')
    c2=typeofplans.objects.filter(plans__contains='6')
    c3=typeofplans.objects.filter(plans__contains='Based on demand')

    d=typeofplans.objects.filter(plans__contains='4')
    d1=typeofplans.objects.filter(plans__contains='5')
    d2=typeofplans.objects.filter(plans__contains='6')
    d3=typeofplans.objects.filter(plans__contains='Based on demand')
    
    plans_list=typeofplans.objects.all()
    features_list=featurestypes.objects.filter(show1=1)
    features_list1=featurestypes.objects.all()
    features_list2=featurestypes.objects.filter(show3=1)  
    features_list3=featurestypes.objects.all()
    s=plandata.objects.all()
    selected_plans = SelectedPlan.objects.all()
    newplan=Addons.objects.filter(plantype=1)
    newplan1=Addons.objects.filter(plantype=2)
    newplan2=Addons.objects.filter(plantype=3)
    newplan3=Addons.objects.filter(plantype=4)
    faq_items = FAQItem.objects.all()   
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    context = {'services':services,'s':s,'faq_items':faq_items,'social':social,'contact_info':contact_info,'links':links,'d':d,'d1':d1,'d2':d2,'d3':d3,'k':k,'k1':k1,'k2':k2,'k3':k3,'a':a,'a1':a1,'a2':a2,'a3':a3,'b':b,'b1':b1,'b2':b2,'b3':b3,'c':c,'c1':c1,'c2':c2,'c3':c3,'faq_items':faq_items,'selected_plans':selected_plans,'newplan':newplan,'newplan1':newplan1,'newplan2':newplan2,'newplan3':newplan3,'plans_list': plans_list, 'features_list': features_list, 'features_list1':features_list1,'features_list2':features_list2,'features_list3':features_list3, "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID}
    
    return render(request, "plans2.html", context=context)

def admincontrol2(request):
    if request.method == 'POST':
        try:
            shou = admin_drop.objects.filter(edit=1)
            for instance in shou:
                show_key = f'admindrop_show_{instance.id}'
                instance.show2 = int(request.POST.get(show_key, 0))
                instance.save()
            prdrop = project_drop.objects.filter(edit=1)
            for i in prdrop:
                show_key = f'prdrop_show_{i.id}'
                i.show2 = int(request.POST.get(show_key, 0))
                i.save()
            screen=screenmon.objects.all()
            for i in screen:
                show_key = f'screen_show_{i.id}'
                i.show2 = int(request.POST.get(show_key, 0))
                i.save()
            adnav=employnav.objects.filter(edit=1)
            for i in adnav:
                show_key = f'admin_show_{i.id}'
                i.show2 = int(request.POST.get(show_key, 0))
                i.save()
            return redirect('admincontrol2')
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    
    shou = admin_drop.objects.filter(edit=1)
    prdrop = project_drop.objects.filter(edit=1)
    screen=screenmon.objects.all()
    adnav=employnav.objects.filter(edit=1)
    context = {'shou': shou, 'prdrop': prdrop,'screen':screen,'adnav':adnav}
    return render(request, 'admincontrol2.html', context)

def admincontrol3(request):
    if request.method == 'POST':


        try:
            shou = admin_drop.objects.filter(edit=1)
            for instance in shou:
                show_key = f'admindrop_show_{instance.id}'
                instance.show3 = int(request.POST.get(show_key, 0))
                instance.save()
            prdrop = project_drop.objects.filter(edit=1)
            for i in prdrop:
                show_key = f'prdrop_show_{i.id}'
                i.show3 = int(request.POST.get(show_key, 0))
                i.save()
            screen=screenmon.objects.filter(edit=1)
            for i in screen:
                show_key = f'screen_show_{i.id}'
                i.show3 = int(request.POST.get(show_key, 0))
                i.save()
            adnav=employnav.objects.filter(edit=1)
            for i in adnav:
                show_key = f'admin_show_{i.id}'
                i.show3 = int(request.POST.get(show_key, 0))
                i.save()
            return redirect('admincontrol3')
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    shou = admin_drop.objects.filter(edit=1)
    prdrop = project_drop.objects.filter(edit=1)
    screen=screenmon.objects.filter(edit=1)
    adnav=employnav.objects.filter(edit=1)
    context = {'shou': shou, 'prdrop': prdrop,'screen':screen,'adnav':adnav}
    return render(request, 'admincontrol3.html', context)


def plans_types(request):
    if request.method == "POST":
        icon1=request.POST["icon1"]
        plantype=request.POST["plantype"]
        price = request.POST["price"]
        annual_price = request.POST["price"]
        price_for_annual = request.POST["price_for_annual"]
        k=typeofplans(price_for_annual=price_for_annual ,icon1=icon1,plantype=plantype,price=price,annual_price=annual_price)
        k.save()
    return render(request,"plans_types.html")
from django.shortcuts import render, redirect

from django.shortcuts import render, get_object_or_404, redirect
from .models import typeofplans

def update_plan(request, pk):
    plan = get_object_or_404(typeofplans, pk=pk)

    if request.method == "POST":
      
        plan.price = request.POST["price"]
        plan.annual_price = request.POST["annual_price"]
        plan.employe_limit = request.POST["employe_limit"]
        plan.price_for_annual = request.POST["price_for_annual"]
        plan.save()
        return redirect("display_plans")

    return render(request, "update_plan.html", {"plan": plan})



from django.shortcuts import get_object_or_404, redirect
from .models import typeofplans

def delete_plan(request, pk):
    plan = get_object_or_404(typeofplans, pk=pk)
    
    if request.method == "POST":
        plan.delete()
        return redirect("plans_types")

    return render(request, "delete_plan.html", {"plan": plan})


from django.shortcuts import render
from .models import typeofplans

def display_plans(request):
    plans = typeofplans.objects.all()
    return render(request, "display_plans.html", {"plans": plans})





def plans_types(request):
    if request.method == "POST":
        icon1=request.POST["icon1"]
        plantype=request.POST["plantype"]
        price = request.POST["price"]
        annual_price = request.POST["price"]
        k=typeofplans(icon1=icon1,plantype=plantype,price=price,annual_price=annual_price)
        k.save()
    return render(request,"plans_types.html")

from django.http import HttpResponse
def admincontrol(request):
    if request.method == 'POST':
        try:
            shou = admin_drop.objects.filter(edit=1)
            for instance in shou:
                show_key = f'admindrop_show_{instance.id}'
                instance.show1 = int(request.POST.get(show_key, 0))
                instance.save()
            prdrop = project_drop.objects.filter(edit=1)
            for i in prdrop:
                show_key = f'prdrop_show_{i.id}'
                i.show1 = int(request.POST.get(show_key, 0))
                i.save()
            screen=screenmon.objects.filter(edit=1)
            for i in screen:
                show_key = f'screen_show_{i.id}'
                i.show1 = int(request.POST.get(show_key, 0))
                i.save()
            adnav=employnav.objects.filter(edit=1)
            for i in adnav:
                show_key = f'admin_show_{i.id}'
                i.show1 = int(request.POST.get(show_key, 0))
                i.save()
            return redirect('admincontrol')

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    
    shou = admin_drop.objects.filter(edit=1)
    prdrop = project_drop.objects.filter(edit=1)
    screen=screenmon.objects.filter(edit=1)
    adnav=employnav.objects.filter(edit=1)
    context = {'shou': shou,'screen':screen,'prdrop':prdrop}
    return render(request, 'admincontrol.html', context)

def addonauthentication(request):
    if request.method == "POST":
        user=authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user is not None and user is not "multipleuser":
            request.session['email_2']=user.email;
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/addonfectures')
            else:
                messages.error(request,"you Don't have any company register")
        else:
            messages.error(request,"Invalid Username or Password")

    return render(request,"addonauthentication.html")


import json

from django.contrib import messages
from .models import Companys, Addons, Addonsuser
import razorpay
import uuid

        
        
        
        
# def addonfectures(request):
#     url = "https://api.cashfree.com/pg/orders"

#     headers = {
#             "X-Client-Id": "65027036b36cd7d08b4c5d7b33072056",
#             "X-Client-Secret": "cfsk_ma_prod_e9af870c9a9b8b0880ec4ed0617d7b98_2651c73f",
#             "x-api-version": "2023-08-01",
#         }
#     order_id = uuid.uuid4().hex
#     customer_id = uuid.uuid4().hex
#     if request.user.is_authenticated:
#         data = Companys.objects.filter(usernumber=request.user.id).first()
#         email=data.email
#         Mobile=data.phone_number
#         username=data.organizationname

#         if data:
#                 data1 = data.plantype
#                 newplan = Addons.objects.filter(plantype=data1)
#                 if newplan:
#                     messages.error(request, "")
#                 else:
#                     messages.error(request, "")
#                     return HttpResponseRedirect("/")
#         else:
#             data1=None
#             newplan=None
#     else:
#          data=None
#          data1=None
#          newplan=None
#          messages.error(request, "")
                
           


#     selected_plans = []
#     selected_amounts = []

#     if request.method == "POST":
#         selected_plans = request.POST.getlist('plan')
#         request.session['selected_plans']=selected_plans
#         selected_amounts = [request.POST.get(f'amount_{plan}', '') for plan in selected_plans]

#         selected_amounts = [amount for amount in selected_amounts if amount]
#         request.session['selected_amounts']=selected_amounts
#         if selected_amounts:
#             total_amount = sum(map(int, selected_amounts))

#             payload = {
#             "order_id": order_id,
#             "order_amount": total_amount,
#             "order_currency": "INR",
#             "customer_details": {
#                 "customer_id": customer_id,
#                 "customer_name": username,
#                 "customer_email": email,
#                 "customer_phone": Mobile,
                
#             },
#             "order_meta":{
#                 "return_url":"https://buglegal.com/handle_payment/?order_id=order_id"
#             }

#         }
            
#             for plan, amount in zip(selected_plans, selected_amounts):
#                 if plan:
#                     request.session['form_data']= {'plan': plan, 'amount': int(amount),'addon':1,'order_id':order_id}
                    
#             response = requests.post(url=url, headers=headers, json=payload)
#             payment_ses=response.json()
#             if response.status_code == 200 and payment_ses.get('status') == "OK":
#                 return redirect("/handle_payment/")
#             return render(request,"loader1.html",{'response':response,'payment_ses':payment_ses})
#             return redirect("/handle_payment/")
#     return render(request, "addonfectures.html", {'data': data, 'newplan': newplan, 'selected_plans': selected_plans, 'selected_zip': zip(selected_plans, selected_amounts)})

def addonfectures(request):
    url = "https://api.cashfree.com/pg/orders"

    headers = {
            "X-Client-Id": "65027036b36cd7d08b4c5d7b33072056",
            "X-Client-Secret": "cfsk_ma_prod_e9af870c9a9b8b0880ec4ed0617d7b98_2651c73f",
            "x-api-version": "2023-08-01",
        }
    order_id = uuid.uuid4().hex
    customer_id = uuid.uuid4().hex
    request.session['order_idpex2']=order_id

    if request.user.is_authenticated:
        data = Companys.objects.filter(usernumber=request.user.id).first()
        email=data.email
        Mobile=data.phone_number
        username=data.organizationname

        if data:
                data1 = data.plantype
                newplan = Addons.objects.filter(plantype=data1)
                if newplan:
                    messages.error(request, "")
                else:
                    messages.error(request, "No Addons For Your Plan")
                    # return HttpResponseRedirect("/")
        else:
            data1=None
            newplan=None
    else:
         data=None
         data1=None
         newplan=None
         messages.error(request, "You Don't Have Any Active Plan")
                
           


    selected_plans = []
    selected_amounts = []

    if request.method == "POST":
        selected_plans = request.POST.getlist('plan')
        request.session['selected_plans']=selected_plans
        selected_amounts = [request.POST.get(f'amount_{plan}', '') for plan in selected_plans]

        selected_amounts = [amount for amount in selected_amounts if amount]
        request.session['selected_amounts']=selected_amounts
        if selected_amounts:
            total_amount = sum(map(int, selected_amounts))

            payload = {
            "order_id": order_id,
            "order_amount": total_amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": customer_id,
                "customer_name": username,
                "customer_email": email,
                "customer_phone": Mobile,
                
            },
            "order_meta":{
                "return_url":"https://buglegal.com/handle_payment/?order_id=order_id"
            }

        }
            
            for plan, amount in zip(selected_plans, selected_amounts):
                if plan:
                    request.session['form_data']= {'plan': plan, 'amount': int(amount),'addon':1,'order_id':order_id}
                    
            response = requests.post(url=url, headers=headers, json=payload)
            payment_ses=response.json()
            if response.status_code == 200 and payment_ses.get('status') == "OK":
                return redirect("/handle_payment/")
            return render(request,"loader1.html",{'response':response,'payment_ses':payment_ses})
            return redirect("/handle_payment/")
    return render(request, "addonfectures.html", {'data': data, 'newplan': newplan, 'selected_plans': selected_plans, 'selected_zip': zip(selected_plans, selected_amounts)})

def handle_payment_success(request):
    form_data = request.session.get('form_data')
    selected_plans=request.session.get('selected_plans')
    selected_amounts=request.session.get('selected_amounts')
    
    if form_data:
        addon=form_data['addon']
        order_id=form_data['order_id']
        data = Companys.objects.filter(usernumber=request.user.id).first()
        url = f"https://api.cashfree.com/pg/orders/{order_id}"

        headers = {
            "X-Client-Id": "65027036b36cd7d08b4c5d7b33072056",
            "X-Client-Secret": "cfsk_ma_prod_e9af870c9a9b8b0880ec4ed0617d7b98_2651c73f",
            "x-api-version": "2023-08-01",
            "x-request-id":"4dfb9780-46fe-11ee-be56-0242ac120002",
            "x-idempotency-key":"47bf8872-46fe-11ee-be56-0242ac120002"
        }
        response = requests.post(url=url, headers=headers)
        payment_ses=response.json()
        order_status = payment_ses.get('order_status')
        if order_status == "PAID":
            for plan, amount in zip(selected_plans, selected_amounts):
                    if plan:       
                        date = Addonsuser(plan=plan, amount=amount,addon=addon,order_id=order_id,companyid=data)
                        date.save()
            del request.session['form_data']
            return render(request, "payment_success.html")
        else:
            return render(request, "payment_fail.html")

    else:
        messages.error(request, "Form data not found.")
        return redirect('/addonfectures/')  



def SubscriptionDetail(request):
    plan_type = request.GET.get('plan_type')
    amount = request.GET.get('amount')
    plan_name = request.GET.get('plan_name')
    print(f"Received plan_type: {plan_type}, amount: {amount}")

    # Rest of your view logic

    return render(request, 'SubscriptionDetails.html', {'plan_name':plan_name,'plan_type': plan_type, 'amount': amount, "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID})



from .models import FAQItem
from django.shortcuts import render, redirect

def faq_view(request):
    faq_items = FAQItem.objects.all()
    return render(request, 'faq.html', {'faq_items': faq_items})

def add_faq_view(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        link = request.POST.get('link', '')
        email = request.POST.get('email', '')

        faq_item = FAQItem.objects.create(question=question, answer=answer, link=link, email=email)        
        messages.success(request, 'FAQ item created successfully.')
        return redirect('faq_view') 

    return render(request, 'add_faq.html')

# views.py
from django.shortcuts import render, get_object_or_404, redirect


def update_faq_view(request, faq_id):
    faq_item = get_object_or_404(FAQItem, pk=faq_id)

    if request.method == 'POST':
        faq_item.question = request.POST.get('question', '')
        faq_item.answer = request.POST.get('answer', '')
        faq_item.link = request.POST.get('link', '')
        faq_item.email = request.POST.get('email', '')
        faq_item.save()
        messages.success(request, 'FAQ item updated successfully.')
        return redirect('faq_view') 

    return render(request, 'update_faq.html', {'faq_item': faq_item})



def delete_faq_view(request, faq_id):
    faq_item = get_object_or_404(FAQItem, pk=faq_id)

    if request.method == 'POST':
        faq_item.delete()
        messages.success(request, 'FAQ item deleted successfully.')
        return redirect('faq_view')  

    return render(request, 'delete_faq.html', {'faq_item': faq_item})




def features_types(request):
    if request.method == "POST":
        name=request.POST["name"]
        k=featurestypes(name=name)
        k.save()
    return render(request,"features_types.html")


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages 
from .models import typeofplans, featurestypes, SelectedPlan

def select_features_types(request):
    selected_plan = None

    if request.method == 'POST':
        selected_plan_id = request.POST.get('plan_type')
        selected_features = request.POST.getlist('features')

        existing_plan = SelectedPlan.objects.filter(plan_type_id=selected_plan_id).first()

        if existing_plan:
            existing_plan.features.clear()
            features = featurestypes.objects.filter(pk__in=selected_features)
            existing_plan.features.set(features)
        else:
            plan_type = typeofplans.objects.get(pk=selected_plan_id)
            features = featurestypes.objects.filter(pk__in=selected_features)
            selected_plan = SelectedPlan.objects.create(plan_type=plan_type)
            selected_plan.features.set(features)

        # Add a success message
        messages.success(request, 'Plan and features Update successfully!')

        # Redirect to the plans page or wherever you want to display the selected plans
        # return redirect('plans')

    plans = typeofplans.objects.all()
    features = featurestypes.objects.all()

    # Get the selected plan if it exists
    selected_plan_id = request.GET.get('plan_type')
    if selected_plan_id:
        selected_plan = SelectedPlan.objects.filter(plan_type_id=selected_plan_id).first()

    return render(request, "selectfeaturetye.html", {'plans': plans, 'features': features, 'selected_plan': selected_plan})



def get_features(request, plan_id):
    selected_plan = SelectedPlan.objects.filter(plan_type_id=plan_id).first()
    features = list(selected_plan.features.values_list('id', flat=True)) if selected_plan else []
    return JsonResponse({'features': features})




from django.http import JsonResponse
from .models import featurestypes

def toggle_feature(request, feature_id):
    try:
        feature = featurestypes.objects.get(id=feature_id)
        feature.is_enabled = not feature.is_enabled  
        feature.save()
        return JsonResponse({'success': True, 'is_enabled': feature.is_enabled})
    except featurestypes.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Feature not found'})

from .models import Addplans

def render_plan_form(request):
    selected_features = featurestypes.objects.filter(is_available=True)
    plans = Addplans.objects.all()

    return render(request, 'your_template.html', {'selected_features': selected_features, 'plans': plans})


def new_plan(request):
    if request.method == "POST":
        plan_name=request.POST["plan_name"]
        featue1=request.POST["featue1"]
        featue2=request.POST["featue2"]
        featue3=request.POST["featue3"]
        descrption1=request.POST["descrption1"]
        descrption2=request.POST["descrption2"]
        k=Addplans(plan_name=plan_name,featue1=featue1,featue2=featue2,featue3=featue3,descrption1=descrption1,descrption2=descrption2)
        k.save()
    return render(request,"new_plan.html")

def faq_retrive(request):
    faq_items = FAQItem.objects.all()

    return render(request, 'faqretrive.html', {'faq_items': faq_items})




















from django.template import *



def homepage(request):
    k=home.objects.all()
    k1=home2.objects.all()
    k2=home3.objects.all()
    k3=home4.objects.all()
    k4=home5.objects.all()
    k5=nav1.objects.all()
    k6=home6.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    navbar_items = NavbarItem.objects.filter(parent=None)
    return render(request,"index.html",{'k6':k6,'k':k,'k1':k1,'k2':k2,'k3':k3,'k4':k4,"k5":k5,'navbar_items':navbar_items,'links': links,'services': services,'contact_info': contact_info,'social':social})
def productivity5_create(request):
    if request.method == 'POST':
        image1 = request.FILES.get('image1')

        title1 = request.POST.get('title1')
        discription1 = request.POST.get('discription1')
       
        productivity5.objects.create(
            image1=image1,
            title1=title1,
            discription1=discription1,
           
        )


    return render(request, 'productivity5_form.html')

def productivity5_list(request):
    projects5 = productivity5.objects.all()
    return render(request, 'productivity5_list.html', {'projects5': projects5})




from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity5

def productivity5_update(request, pk):
    project5 = get_object_or_404(productivity5, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project5.image1 = request.FILES.get('image1')

        project5.title1 = request.POST.get('title1')
        project5.discription1 = request.POST.get('discription1')
       
        project5.save()

        return redirect('/productivity5_list')

    return render(request, 'productivity5_update.html', {'project5': project5})



from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity5

def productivity5_delete(request, pk):
    project5 = get_object_or_404(productivity5, pk=pk)
    
    if request.method == 'POST':
        project5.delete()
        return redirect('productivity5_list')

    return render(request, 'productivity5_confirm_delete.html', {'project5': project5})



from .models import icons





def icons_insert(request):
    if request.method == "POST":
        title=request.POST['title']
        # icon1=request.POST['icon1']
        # icon=request.POST['icon']
        icon1=request.FILES.get('icon1')
        icon=request.FILES.get('icon')
        url=request.POST['url']
        k1=icons(title=title,icon1=icon1,icon=icon,url=url)
        k1.save()
    return render(request,'icons_insert.html',)

def display_icons_data(request):
    icons_data = icons.objects.all()
    return render(request, 'display_icons_data.html', {'icons_data': icons_data})

def edit_icons_data(request, pk):
    data = get_object_or_404(icons, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.icon1 = request.POST['icon1']
        data.icon = request.POST['icon']
        data.url = request.POST['url']
        data.save()
        return redirect('display_icons_data')
    return render(request, 'edit_icons_data.html', {'data': data})

def delete_icons_data(request, pk):
    data = get_object_or_404(icons, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('display_icons_data')
    return render(request, 'delete_icons_data.html', {'data': data})





from django.shortcuts import render,redirect
from .models import privacy
from django.http import HttpResponse

# Create your views here.
def regprivacy(request):
    if request.method=="GET":
        priv=privacy.objects.all()
        return render(request,"dataprivacy.html",{'priv':priv})
def displayprivacy(request):
     if request.method=="GET":
        pri=privacy.objects.all()
        links = FooterLink.objects.all()
        services = FooterService.objects.all()
        contact_info = ContactInfo.objects.first()
        social = SocialLink.objects.all()    
     return render(request,"display.html",{'social':social, 'contact_info':contact_info, 'pri':pri,'links':links,'services':services})

def inserted(request):
     if request.method=="POST":
          title=request.POST['title']
          subtitle=request.POST['subtitle']
          content=request.POST['content']
          point1=request.POST['point1']
          point2=request.POST['point2']
          point3=request.POST['point3']
          point4=request.POST['point4']
          point5=request.POST['point5'] 
          point6=request.POST['point6']
          point7=request.POST['point7']
          point8=request.POST['point8']
          point9=request.POST['point9']
          point10=request.POST['point10']
          images=request.FILES.get('images')

         
          p=privacy(title=title,subtitle=subtitle,content=content,point1=point1,point2=point2,point3=point3,point4=point4,point5=point5,point6=point6,point7=point7,point8=point8,point9=point9,point10=point10,images=images)
          p.save()
          
          return redirect ("/regprivacy/")
     return render(request,"datainserted.html")



def privacyedit(request,id):
   pri1=privacy.objects.filter(id=id).first()
   return render(request,'updateprivacy.html',{'pri1':pri1})



def update(request, id):
    pri1=privacy.objects.filter(id=id).first()


    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        imag=request.FILES.get('image')
        pri1.title = request.POST.get('title')
        pri1.subtitle = request.POST.get('subtitle')
        pri1.content = request.FILES.get('content')
        pri1.point1 = request.POST.get('point1')
        pri1.point2 = request.POST.get('point2')
        pri1.point3 = request.POST.get('point3')
        pri1.point4 = request.POST.get('point4')
        pri1.point5 = request.POST.get('point5')
        pri1.point6 = request.POST.get('point6')
        pri1.point7 = request.POST.get('point7')
        pri1.point8 = request.POST.get('point8')
        pri1.point9=request.POST.get('point9')
        pri1.point10=request.POST.get('point10')
        if imag:
          pri1.images=request.FILES.get('image')
        pri1.save()

        return redirect("/regprivacy/")


    return render(request, 'updateprivacy.html', {'pri1': pri1})

def delete(request,id):
    d=privacy.objects.get(id=id)
    d.delete()
    return redirect("/regprivacy/")





from django.shortcuts import render,redirect
from .models import ac
def home_ac(request):
    if request.method=="GET":
        h=ac.objects.all()
    return render(request,"home-ac.html",{'h':h})


def Admin_Control(request):
   
    d=ac.objects.all()
    l=ac1.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return render(request,"display-ac.html",{'d':d,'links':links,'services':services,'contact_info':contact_info,'social':social,'l':l})


def insert_ac(request):
    if request.method=="POST":
        heading=request.POST['heading']
        content=request.POST['content']
        images=request.FILES.get('images')
        i=ac(heading=heading,content=content,images=images)
        i.save()
        return redirect("/home_ac/")
    return render(request,"insert-ac.html")



def edit_ac(request,id):
    if request.method=="GET":
        e=ac.objects.get(id=id)
    return render(request,"update-ac.html",{"e":e})

def update_ac(request,id):
    e=ac.objects.filter(id=id).first()
    imga=request.FILES.get('images')
    if request.method=="POST":
        e.heading = request.POST.get('heading')
        e.content = request.POST.get('content')
        if imga:
           e.images = request.FILES.get('images')
        
        e.save()
        return redirect("/home_ac/")
    return render(request,"update-ac.html",{'e':e})




def delete_ac(request,id):
    d=ac.objects.get(id=id)
    d.delete()
    return redirect("/home_ac/")


from django.shortcuts import render, redirect, get_object_or_404
from .models import NavbarItem

def navbaritems(request):
    if request.method=="GET":
        n=NavbarItem.objects.all()
        return render(request,"navbaritems_table.html",{'n':n})

def navbaritems_insert(request):
    if request.method=="POST":
        name=request.POST['name']
        photo1=request.FILES.get('photo1')
        nav=NavbarItem(name=name,photo1=photo1)
        nav.save()

        return redirect("/navbaritems")
    return render(request,"navbaritems_insert.html")  
    

def navbaritems_edit(request,id):
    if request.method=="GET":
        u=NavbarItem.objects.get(id=id)
    return render(request,"navbaritems_update.html",{'u':u})


def navbaritems_update(request,id):
    if request.method=="POST":
        name=request.POST['name']
        photo1=request.FILES.get('photo1')
        u=NavbarItem.objects.get(id=id)
        u.name=name
        u.photo1=photo1
       
        u.save()
        return redirect('/navbaritems/')

    return render(request,"navbaritems_update.html")


def navbaritems_delete(request,id):
    d=NavbarItem.objects.get(id=id)
    d.delete()
    return redirect("/navbaritems")





def navbar(request):
    navbar_items=NavbarItem.objects.all()
    footer_item=Footer1.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()

    return render(request,"navbar.html",{'navbar_items':navbar_items,'footer_item':footer_item, 'links': links,
        'services': services,
        'contact_info': contact_info,'social':social})
    


def timeattendance(request):
    return render(request,"attendance.html")

def activitymonitoring(request):
    k=Monitoringdata.objects.all()
    k1=Monitoring2.objects.all()
    k2=Monitoring3.objects.all()
    k3=Monitoring3.objects.all()
    k4=Monitoring4.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return render(request,"activity.html",{"links":links,'services':services,'contact_info':contact_info,'social':social,  'k':k,'k1':k1,'k2':k2,'k3':k3,'k4':k4})




def Productivity_Monitoring(request):
    projects = productivity1.objects.all()
    projects1 = productivity2.objects.all()
    projects2 = productivity3.objects.all()
    projects3 = productivity4.objects.all()
    projects4 = productivity5.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()

    return render(request,"product.html",{'social':social,'contact_info':contact_info, 'links':links,'services':services, 'projects':projects,'projects1':projects1,'projects2':projects2,'projects3':projects3,'projects4':projects4})


def timetracking(request):  
        projects = timetracking1.objects.all()
        projects1 = timetracking2.objects.all()
        projects2 = timetracking3.objects.all()
        projects3 = timetracking4.objects.all()
        links = FooterLink.objects.all()
        services = FooterService.objects.all()
        contact_info = ContactInfo.objects.first()
        social = SocialLink.objects.all()
        return render(request,'time.html',{ 'social':social,'links':links,'services':services,'contact_info':contact_info, 'projects':projects,'projects1':projects1,'projects2':projects2,'projects3':projects3})


def officework(request):
    officework1_items = officework1.objects.all()
    officework2_items = officework2.objects.all()
    officework3_items = officework3.objects.all()
    officework4_items = officework4.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return render(request,"office1.html",{"links":links,'services':services,'contact_info': contact_info,'social':social,  'officework1_items':officework1_items,'officework2_items':officework2_items,'officework3_items':officework3_items,'officework4_items':officework4_items})






def projectmanagment(request):
    projects = projectmanagement.objects.all()
    projects1 = projectmanagement2.objects.all()
    projects2 = projectmanagement3.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return render(request,"project.html" ,{'social':social, "links":links,'services':services,'contact_info':contact_info, "projects":projects, "projects1":projects1, "projects2":projects2})


def projectmanagement_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')

        discription = request.POST.get('discription')

        projectmanagement.objects.create(
            title=title,
            subtitle=subtitle,
            image1=image1,
            image2=image2,
            discription=discription
        )


    return render(request, 'projectmanagement_form.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import projectmanagement

def projectmanagement_update(request, pk):
    project = get_object_or_404(projectmanagement, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project.title = request.POST.get('title')
        project.subtitle = request.POST.get('subtitle')
        project.image1 = request.FILES.get('image1')
        project.image2 = request.FILES.get('image2')

        project.discription = request.POST.get('discription')
        project.save()

        return redirect('all_projects')

    return render(request, 'projectmanagement_update.html', {'project': project})


from django.shortcuts import render, get_object_or_404, redirect
from .models import projectmanagement

def projectmanagement_delete(request, pk):
    project = get_object_or_404(projectmanagement, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('all_projects')

    return render(request, 'projectmanagement_confirm_delete.html', {'project': project})


from django.shortcuts import render
from .models import projectmanagement

def projectmanagement_list(request):
    projects = projectmanagement.objects.all()
    return render(request, 'projectmanagement_list.html', {'projects': projects})








from django.shortcuts import render, redirect
from .models import projectmanagement2

def projectmanagement2_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        discription = request.POST.get('discription')
        title2 = request.POST.get('title2')
        subtitle2 = request.POST.get('subtitle2')
        title3 = request.POST.get('title3')
        title4 = request.POST.get('title4')


        projectmanagement2.objects.create(
            title=title,
            discription=discription,
            title2=title2,
            subtitle2=subtitle2,
            title3=title3,
            title4=title4,


        )


    return render(request, 'projectmanagement2_form.html')



from django.shortcuts import render
from .models import projectmanagement2

def projectmanagement2_list(request):
    projects1 = projectmanagement2.objects.all()
    return render(request, 'projectmanagement2_list.html', {'projects1': projects1})



from django.shortcuts import render, get_object_or_404, redirect
from .models import projectmanagement2

def projectmanagement2_update(request, pk):
    project = get_object_or_404(projectmanagement2, pk=pk)

    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.discription = request.POST.get('discription')
        project.title2 = request.POST.get('title2')
        project.title3 = request.POST.get('title3')
        project.title4 = request.POST.get('title4')

        project.subtitle2 = request.POST.get('subtitle2')
        project.save()

        return redirect('all_projects')

    return render(request, 'projectmanagement2_update.html', {'project': project})


from django.shortcuts import render, get_object_or_404, redirect
from .models import projectmanagement2

def projectmanagement2_delete(request, pk):
    project = get_object_or_404(projectmanagement2, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('all_projects')

    return render(request, 'projectmanagement2_confirm_delete.html', {'project': project})



def projectmanagement3_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        discription = request.POST.get('discription')

        projectmanagement3.objects.create(
            title=title,
            image=image,
            discription=discription
        )


    return render(request, 'projectmanagement3_form.html')



from django.shortcuts import render
from .models import projectmanagement2

def projectmanagement3_list(request):
    projects2 = projectmanagement3.objects.all()
    return render(request, 'projectmanagement3_list.html', {'projects2': projects2})



from django.shortcuts import render, get_object_or_404, redirect
from .models import projectmanagement3

def projectmanagement3_update(request, pk):
    project = get_object_or_404(projectmanagement3, pk=pk)

    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.discription = request.POST.get('discription')
        project.image = request.POST.get('image')
        project.save()

        return redirect('all_projects')

    return render(request, 'projectmanagement3_update.html', {'project': project})


from django.shortcuts import render, get_object_or_404, redirect
from .models import projectmanagement3

def projectmanagement3_delete(request, pk):
    project = get_object_or_404(projectmanagement3, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('all_projects')

    return render(request, 'projectmanagement3_confirm_delete.html', {'project': project})


from django.shortcuts import render
from .models import projectmanagement, projectmanagement2, projectmanagement3

def all_projects(request):
    projects = projectmanagement.objects.all()
    projects1 = projectmanagement2.objects.all()
    projects2 = projectmanagement3.objects.all()

    return render(request, 'all_projects.html', {'projects': projects, 'projects1': projects1, 'projects2': projects2})


def features(request):
    return render(request,"features.html")


from .models import AdminHod


# def admin_Password(request):
#     admin = AdminHod.objects.get(admin=request.user.id) 

#     user = CustomUser.objects.filter(id=request.user.id).first()
#     userid1 = user.id
#     da1 = AdminHod.objects.filter(admin=request.user.id).first()
#     da2 = da1.id
#     admin = AdminHod.objects.get(id=1)
#     s = adminnav.objects.all()
#     # projectm = admin_project_create.objects.filter(admin_id=userid1)
#     h = HR.objects.all()
#     employs_all = Employs.objects.all()
#     admin_drops=admin_drop.objects.filter(parent_category=None).order_by('id')
#     admin_home_drops=admin_home_drop.objects.filter(parent_category=None).order_by('id')
#     data = AdminHod.objects.filter(id=request.user.id)
#     projects_drops=project_drop.objects.filter(parent_category=None).order_by('id')

 

#     return render(request,"admin-template/admin_Password.html", {'admin': admin,'user':user,'da1':da1,'da2':da2,'admin':admin,'admin_home_drops':admin_home_drops,'s':s,'h':h,'projects_drops':projects_drops,'data':data,'employs_all':employs_all,'admin_drops':admin_drops})







# def admin_Password_save(request):
#     # admin = AdminHod.objects.get(admin=request.user.id), {'admin': admin} 

#     if request.method =="POST":
#         password=request.POST.get("password")

        
#         customuser=CustomUser.objects.get(id=request.user.id)
#         if password!=None and password!="":
#             customuser.set_password(password)
#             customuser.save()

#             employ=AdminHod.objects.get(admin=customuser)
#             employ.save()
#             return redirect('/admin_home')

#     return render(request, "admin-template/admin_Password.html")
from .models import indexnave

def employeemonitoring(request):
  
    k=employeeindex.objects.all()
    k1=employeeindex1.objects.all()
    k2=employeeindex2.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()

    return render(request,"employee.html",{'k':k,'k1':k1,'k2':k2,'links':links,'services':services,'contact_info':contact_info,'social':social})
def employeemonitoring1(request):
    if request.method == "POST":
        title = request.POST["title"]
        image=request.FILES.get('image')
        descrption = request.POST["descrption"]
        descrption1 = request.POST["descrption1"]
        image1=request.FILES.get('image1')
        descrption2 = request.POST["descrption2"]
        descrption3 = request.POST["descrption3"]
        descrption4 = request.POST["descrption4"]
        descrption5 = request.POST["descrption5"]
        image2=request.FILES.get('image2')
        k=employeeindex(title=title,image=image,descrption=descrption,descrption1=descrption1,image1=image1,image2=image2,descrption2=descrption2,descrption3=descrption3,descrption4=descrption4,descrption5=descrption5)
        k.save()
        # return HttpResponse("File uploaded successfully!")

    return render(request,"employeemonitoring1.html")




def edit_employee_index(request, pk):
    data = get_object_or_404(employeeindex, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.descrption = request.POST['descrption']
        data.descrption1 = request.POST['descrption1']
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        data.descrption2 = request.POST['descrption2']
        data.descrption3 = request.POST['descrption3']
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        data.descrption4 = request.POST['descrption4']
        data.descrption5 = request.POST['descrption5']
        if 'image2' in request.FILES:
            data.image2 = request.FILES['image2']
        data.save()
        return redirect('all_employmonitring')
    return render(request, 'edit_employeeindex_data.html', {'data': data})


def delete_employee_index(request, pk):
    data = get_object_or_404(employeeindex, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_employmonitring')
    return render(request, 'delete_employeeindex_data.html', {'data': data})

def display_employeeindex_data(request):
    employees1 = employeeindex.objects.all()
    return render(request, 'display_employeeindex_data.html', {'employees1': employees1})












def employeemonitoring2(request):
    if request.method == "POST":
        title = request.POST["title"]
        descrption = request.POST["descrption"]
        descrption1 = request.POST["descrption1"]
        k=employeeindex1(title=title,descrption=descrption,descrption1=descrption1)
        k.save()

    return render(request,"employeemonitoring2.html")


def edit_employeeindex1(request, pk):
    data = get_object_or_404(employeeindex1, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.descrption = request.POST['descrption']
        data.descrption1 = request.POST['descrption1']
        data.save()
        return redirect('all_employmonitring')
    return render(request, 'edit_employeeindex1_data.html', {'data': data})


def delete_employeeindex1(request, pk):
    data = get_object_or_404(employeeindex1, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_employmonitring')
    return render(request, 'delete_employeeindex1_data.html', {'data': data})


def display_employeeindex1_data(request):
    employees2 = employeeindex1.objects.all()
    return render(request, 'display_employeeindex1_data.html', {'employees2': employees2})




def employeemonitoring3(request):
    if request.method == "POST":
        title = request.POST["title"]
        subtitle=request.POST["subtitle"]
        descrption1 = request.POST["descrption1"]
        image=request.FILES.get('image')
        image1=request.FILES.get('image1')
        k=employeeindex2(title=title,subtitle=subtitle,descrption1=descrption1,image=image,image1=image1)
        k.save()

    return render(request,"employeemonitoring3.html")


def edit_employeeindex2(request, pk):
    data = get_object_or_404(employeeindex2, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.subtitle = request.POST['subtitle']
        data.descrption1 = request.POST['descrption1']
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        data.save()
        return redirect('all_employmonitring')
    return render(request, 'edit_employeeindex2_data.html', {'data': data})


def delete_employeeindex2(request, pk):
    data = get_object_or_404(employeeindex2, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_employmonitring')
    return render(request, 'delete_employeeindex2_data.html', {'data': data})


def display_employeeindex2_data(request):
    employees3 = employeeindex2.objects.all()
    return render(request, 'display_employeeindex2_data.html', {'employees3': employees3})



from django.shortcuts import render
from .models import employeeindex, employeeindex1, employeeindex2

def all_employmonitring(request):
    employees1 = employeeindex.objects.all()
    employees2 = employeeindex1.objects.all()
    employees3 = employeeindex2.objects.all()
    return render(request, 'all_employmonitring.html', {'employees1': employees1, 'employees2': employees2, 'employees3': employees3})






from .models import Monitoringdata,Monitoring2,Monitoring3,Monitoring4
def Monitoring_view(request):
    if request.method=='POST':
        title=request.POST['title']
        discription=request.POST['discription']
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        k=Monitoringdata(title=title,discription=discription,image1=image1,image2=image2)
        k.save()
    return render(request, "Monitoring_view.html")



from django.shortcuts import render, get_object_or_404, redirect
from .models import Monitoringdata

def display_monitoring_data(request):
    monitoring_data = Monitoringdata.objects.all()
    return render(request, 'display_monitoring_data.html', {'monitoring_data': monitoring_data})

def edit_monitoring_data(request, pk):
    data = get_object_or_404(Monitoringdata, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.discription = request.POST['discription']
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            data.image2 = request.FILES['image2']
        data.save()
        return redirect('all_activemonitring')
    return render(request, 'edit_monitoring_data.html', {'data': data})

def delete_monitoring_data(request, pk):
    data = get_object_or_404(Monitoringdata, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_activemonitring')
    return render(request, 'delete_monitoring_data.html', {'data': data})



def Monitoring_view2(request):
    if request.method=='POST':
        title=request.POST['title']
        paragraph=request.POST['paragraph']
        discription=request.POST['discription']
        icon=request.FILES.get('icon')
        title1=request.POST['title1']
        k=Monitoring2(title=title,paragraph=paragraph,discription=discription,icon=icon,title1=title1)
        k.save()
        Mr_data = Monitoring2.objects.all()

    return render(request, "Monitoring_view2.html")

from django.shortcuts import render, get_object_or_404, redirect
from .models import Monitoring2

def display_monitoring2_data(request):
    monitoring2_data = Monitoring2.objects.all()
    return render(request, 'display_monitoring2_data.html', {'monitoring2_data': monitoring2_data})

def edit_monitoring2_data(request, pk):
    data = get_object_or_404(Monitoring2, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.paragraph = request.POST['paragraph']
        data.discription = request.POST['discription']
        if 'icon' in request.POST:
            data.icon = request.POST['icon']
        data.title1 = request.POST['title1']
        data.save()
        return redirect('all_activemonitring')
    return render(request, 'edit_monitoring2_data.html', {'data': data})

def delete_monitoring2_data(request, pk):
    data = get_object_or_404(Monitoring2, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_activemonitring')
    return render(request, 'delete_monitoring2_data.html', {'data': data})


def Montoring_view3(request):
    if request.method=='POST':
        icon = request.FILES.get('icon')
        title=request.POST['title']
        discription1=request.POST['discription1']
        discription2=request.POST['discription2']
        discription3=request.POST['discription3']
        discription4=request.POST['discription4']
        image1=request.FILES.get('image1')
        k=Monitoring3(title=title,discription1=discription1,discription2=discription2,discription3=discription3,discription4=discription4,image1=image1,icon=icon)
        k.save()
    return render(request, "Monitoring_view3.html")




def display_monitoring3_data(request):
    monitoring3_data = Monitoring3.objects.all()
    return render(request, 'display_monitoring3_data.html', {'monitoring3_data': monitoring3_data})



def edit_monitoring3_data(request, pk):
    data = get_object_or_404(Monitoring3, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.discription1 = request.POST['discription1']
        data.discription2 = request.POST['discription2']
        data.discription3 = request.POST['discription3']
        data.discription4 = request.POST['discription4']
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        if 'icon' in request.POST:
            data.icon = request.POST['icon']
        data.save()
        return redirect('all_activemonitring')
    return render(request, 'edit_monitoring3_data.html', {'data': data})


def delete_monitoring3_data(request, pk):
    data = get_object_or_404(Monitoring3, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_activemonitring')
    return render(request, 'delete_monitoring3_data.html', {'data': data})


def Montoring_view4(request):
    if request.method=='POST':
        title=request.POST['title']
        subtitle=request.POST['subtitle']
        discriprion=request.POST['discriprion']
        image1=request.FILES.get('image1')
        k=Monitoring4(title=title, discriprion= discriprion,image1=image1,subtitle=subtitle)
        k.save()
    return render(request, "Monitoring_view4.html")

def display_monitoring4_data(request):
    monitoring4_data = Monitoring4.objects.all()
    return render(request, 'display_monitoring4_data.html', {'monitoring4_data': monitoring4_data})

def edit_monitoring4_data(request, pk):
    data = get_object_or_404(Monitoring4, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.subtitle = request.POST['subtitle']
        data.discriprion = request.POST['discriprion']
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        data.save()
        return redirect('all_activemonitring')
    return render(request, 'edit_monitoring4_data.html', {'data': data})

def delete_monitoring4_data(request, pk):
    data = get_object_or_404(Monitoring4, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_activemonitring')
    return render(request, 'delete_monitoring4_data.html', {'data': data})


from django.shortcuts import render
from .models import Monitoringdata,Monitoring2,Monitoring3,Monitoring4

def all_activemonitring(request):
    monitoring_data = Monitoringdata.objects.all()
    
    monitoring2_data = Monitoring2.objects.all()
    monitoring3_data = Monitoring3.objects.all()
    monitoring4_data = Monitoring4.objects.all()
 
    return render(request, 'all_activemonitring.html', {'monitoring_data': monitoring_data, 'monitoring2_data': monitoring2_data, 'monitoring3_data': monitoring3_data,'monitoring4_data':monitoring4_data})






from .models import screenmonitoring1,screenmonitoring2,screenmonitoring3
def screenmonitoring(request):
    projects = screenmonitoring1.objects.all()
    projects1 = screenmonitoring2.objects.all()
    projects2 = screenmonitoring3.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()

    return render(request,"screen.html",{'links':links,'services':services,'contact_info':contact_info,'social':social, 'projects':projects,'projects1':projects1,'projects2':projects2})


def screenmonitoring1_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        image1 = request.FILES.get('image1')
        title2 = request.POST.get('title2')
        discription1 = request.POST.get('discription1')
        title3 = request.POST.get('title3')
        discription2 = request.POST.get('discription2')
        image2 = request.FILES.get('image2')


        screenmonitoring1.objects.create(
            title1=title1,
            image1=image1,
            title2=title2,
            discription1=discription1,
            title3=title3,
            discription2=discription2,
            image2=image2,

        )


    return render(request, 'screenmonitoring1_form.html')


def screenmonitoring1_list(request):
    projects = screenmonitoring1.objects.all()
    return render(request, 'screenmonitoring1_list.html', {'projects': projects})





from django.shortcuts import render, get_object_or_404, redirect
from .models import screenmonitoring1

def screenmonitoring1_update(request, pk):
    project = get_object_or_404(screenmonitoring1, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project.title1 = request.POST.get('title1')
        project.image1 = request.FILES.get('image1')
        project.title2 = request.POST.get('title2')
        project.discription1 = request.POST.get('discription1')
        project.title3 = request.POST.get('title3')
        project.discription2 = request.POST.get('discription2')
        project.image2 = request.FILES.get('image2')
        project.save()

        return redirect('/screenmonitoring_all_projects')

    return render(request, 'screenmonitoring1_update.html', {'project': project})


from django.shortcuts import render, get_object_or_404, redirect
from .models import screenmonitoring1

def screenmonitoring1_delete(request, pk):
    project = get_object_or_404(screenmonitoring1, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('screenmonitoring_all_projects')

    return render(request, 'screenmonitoring1_confirm_delete.html', {'project': project})





def screenmonitoring2_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        discription = request.POST.get('discription')


        screenmonitoring2.objects.create(
            title=title,
            discription=discription,

        )


    return render(request, 'screenmonitoring2_form.html')


def screenmonitoring2_list(request):
    projects1 = screenmonitoring2.objects.all()
    return render(request, 'screenmonitoring2_list.html', {'projects1': projects1})


from django.shortcuts import render, get_object_or_404, redirect
from .models import screenmonitoring2

def screenmonitoring2_update(request, pk):
    project1 = get_object_or_404(screenmonitoring2, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project1.title = request.POST.get('title')
        project1.discription = request.POST.get('discription')
        project1.save()

        return redirect('/screenmonitoring_all_projects')

    return render(request, 'screenmonitoring2_update.html', {'project1': project1})


from django.shortcuts import render, get_object_or_404, redirect
from .models import screenmonitoring2

def screenmonitoring2_delete(request, pk):
    project1 = get_object_or_404(screenmonitoring2, pk=pk)
    
    if request.method == 'POST':
        project1.delete()
        return redirect('screenmonitoring_all_projects')

    return render(request, 'screenmonitoring2_confirm_delete.html', {'project1': project1})



def screenmonitoring3_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        discription1 = request.POST.get('discription1')
        image = request.FILES.get('image')
        discription2 = request.POST.get('discription2')
        discription3 = request.POST.get('discription3')
        discription4 = request.POST.get('discription4')

        screenmonitoring3.objects.create(
            title=title,
            discription1=discription1,
            image=image,
            discription2=discription2,
            discription3=discription3,
            discription4=discription4

        )


    return render(request, 'screenmonitoring3_form.html')

def screenmonitoring3_list(request):
    projects2 = screenmonitoring3.objects.all()
    return render(request, 'screenmonitoring3_list.html', {'projects2': projects2})


from django.shortcuts import render, get_object_or_404, redirect
from .models import screenmonitoring3

def screenmonitoring3_update(request, pk):
    project2 = get_object_or_404(screenmonitoring3, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project2.title = request.POST.get('title')
        project2.discription1 = request.POST.get('discription1')
        project2.image = request.FILES.get('image')
        project2.discription2 = request.POST.get('discription2')
        project2.discription3 = request.POST.get('discription3')
        project2.discription4 = request.POST.get('discription4')
        project2.save()

        return redirect('/screenmonitoring_all_projects')

    return render(request, 'screenmonitoring3_update.html', {'project2': project2})


from django.shortcuts import render, get_object_or_404, redirect
from .models import screenmonitoring3

def screenmonitoring3_delete(request, pk):
    project2 = get_object_or_404(screenmonitoring3, pk=pk)
    
    if request.method == 'POST':
        project2.delete()
        return redirect('screenmonitoring_all_projects')

    return render(request, 'screenmonitoring3_confirm_delete.html', {'project2': project2})


def screenmonitoring_all_projects(request):
    projects = screenmonitoring1.objects.all()
    projects1 = screenmonitoring2.objects.all()
    projects2 = screenmonitoring3.objects.all()

    return render(request, 'screenmonitoring_all_projects.html', {'projects': projects, 'projects1': projects1, 'projects2': projects2})




from .models import officework1

def officework1_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        image1 = request.FILES.get('image1')
        discription1 = request.POST.get('discription1')
        discription2 = request.POST.get('discription2')
        discription3 = request.POST.get('discription3')
        discription4 = request.POST.get('discription4')
        image2 = request.FILES.get('image2')

        officework1_obj = officework1(
            title1=title1,
            image1=image1,
            discription1=discription1,
            discription2=discription2,
            discription3=discription3,
            discription4=discription4,
            image2=image2
        )
        officework1_obj.save()

    return render(request, 'officework1_create.html')


def officework1_list(request):
    officework1_items = officework1.objects.all()
    return render(request, 'officework1_list.html', {'officework1_items': officework1_items})


def officework1_update(request, pk):
    officework1_item = get_object_or_404(officework1, pk=pk)

    if request.method == 'POST':
        officework1_item.title1 = request.POST.get('title1')
        officework1_item.image1 = request.FILES.get('image1')
        officework1_item.discription1 = request.POST.get('discription1')
        officework1_item.discription2 = request.POST.get('discription2')
        officework1_item.discription3 = request.POST.get('discription3')
        officework1_item.discription4 = request.POST.get('discription4')
        officework1_item.image2 = request.FILES.get('image2')
        officework1_item.save()
        return redirect('officework_all_projects')

    return render(request, 'officework1_update.html', {'officework1_item': officework1_item})


def officework1_delete(request, pk):
    officework1_item = get_object_or_404(officework1, pk=pk)

    if request.method == 'POST':
        officework1_item.delete()
        return redirect('officework_all_projects')

    return render(request, 'officework1_delete.html', {'officework1_item': officework1_item})



from .models import officework2

def officework2_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        title2 = request.POST.get('title2')

        image = request.FILES.get('image')
        discription = request.POST.get('discription')
        

        officework2_obj = officework2(
            title1=title1,
            title2=title2,
            image=image,
            discription=discription
            
        )
        officework2_obj.save()

    return render(request, 'officework2_create.html')


def officework2_list(request):
    officework2_items = officework2.objects.all()
    return render(request, 'officework2_list.html', {'officework2_items': officework2_items})



def officework2_update(request, pk):
    officework2_item = get_object_or_404(officework2, pk=pk)

    if request.method == 'POST':
        officework2_item.title1 = request.POST.get('title1')
        officework2_item.title2 = request.POST.get('title2')

        officework2_item.image = request.FILES.get('image')
        officework2_item.discription = request.POST.get('discription')
       
        officework2_item.save()
        return redirect('officework_all_projects')

    return render(request, 'officework2_update.html', {'officework2_item': officework2_item})



def officework2_delete(request, pk):
    officework2_item = get_object_or_404(officework2, pk=pk)

    if request.method == 'POST':
        officework2_item.delete()
        return redirect('officework_all_projects')

    return render(request, 'officework2_delete.html', {'officework2_item': officework2_item})



from django.shortcuts import render, redirect
from .models import officework3

def officework3_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        title2 = request.POST.get('title2')

        discription = request.POST.get('discription')
        

        officework3_obj = officework3(
            title1=title1,
            title2=title2,
            discription=discription
            
        )
        officework3_obj.save()

    return render(request, 'officework3_create.html')


def officework3_list(request):
    officework3_items = officework3.objects.all()
    return render(request, 'officework3_list.html', {'officework3_items': officework3_items})



def officework3_update(request, pk):
    officework3_item = get_object_or_404(officework3, pk=pk)

    if request.method == 'POST':
        officework3_item.title1 = request.POST.get('title1')
        officework3_item.title2 = request.POST.get('title2')

        officework3_item.discription = request.POST.get('discription')
       
        officework3_item.save()
        return redirect('officework_all_projects')

    return render(request, 'officework3_update.html', {'officework3_item': officework3_item})



def officework3_delete(request, pk):
    officework3_item = get_object_or_404(officework3, pk=pk)

    if request.method == 'POST':
        officework3_item.delete()
        return redirect('officework_all_projects')

    return render(request, 'officework3_delete.html', {'officework3_item': officework3_item})




from django.shortcuts import render, redirect
from .models import officework4

def officework4_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        title2 = request.POST.get('title2')

        discription = request.POST.get('discription')
        image = request.FILES.get('image')

        

        officework4_obj = officework4(
            title1=title1,
            title2=title2,
            discription=discription,
            image=image

            
        )
        officework4_obj.save()

    return render(request, 'officework4_create.html')


def officework4_list(request):
    officework4_items = officework4.objects.all()
    return render(request, 'officework4_list.html', {'officework4_items': officework4_items})



def officework4_update(request, pk):
    officework4_item = get_object_or_404(officework4, pk=pk)

    if request.method == 'POST':
        officework4_item.title1 = request.POST.get('title1')
        officework4_item.title2 = request.POST.get('title2')

        officework4_item.discription = request.POST.get('discription')
        officework4_item.image = request.FILES.get('image')
       
        officework4_item.save()
        return redirect('officework_all_projects')

    return render(request, 'officework4_update.html', {'officework4_item': officework4_item})



def officework4_delete(request, pk):
    officework4_item = get_object_or_404(officework4, pk=pk)

    if request.method == 'POST':
        officework4_item.delete()
        return redirect('officework_all_projects')

    return render(request, 'officework4_delete.html', {'officework4_item': officework4_item})



def officework_all_projects(request):
    officework1_items = officework1.objects.all()
    officework2_items = officework2.objects.all()
    officework3_items = officework3.objects.all()
    officework4_items = officework4.objects.all()
    return render(request, 'officework_all_projects.html', {'officework1_items': officework1_items, 'officework2_items': officework2_items, 'officework3_items': officework3_items,'officework4_items':officework4_items})

    


def timeattendance1_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        image1 = request.FILES.get('image1')
        discription1 = request.POST.get('discription1')
        image2 = request.FILES.get('image2')
        title2 = request.POST.get('title2')
        discription2 = request.POST.get('discription2')
        title3 = request.POST.get('title3')
        discription3 = request.POST.get('discription3')
        discription4 = request.POST.get('discription4')
        image3 = request.FILES.get('image3')


        timeattendance1.objects.create(
            title1=title1,
            image1=image1,
            discription1=discription1,
            image2=image2,
            title2=title2,
            discription2=discription2,
            title3=title3,
            discription3=discription3,
            discription4=discription4,
            image3=image3,

        )


    return render(request, 'timeattendance1_form.html')

def timeattendance1_list(request):
    projects = timeattendance1.objects.all()
    return render(request, 'timeattendance1_list.html', {'projects': projects})





from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance1

def timeattendance1_update(request, pk):
    project = get_object_or_404(timeattendance1, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project.title1 = request.POST.get('title1')
        project.image1 = request.FILES.get('image1')
        project.discription1 = request.POST.get('discription1')
        project.image2 = request.FILES.get('image2')
        project.title2 = request.POST.get('title2')
        project.discription2 = request.POST.get('discription2')
        project.title3 = request.POST.get('title3')
        project.discription3 = request.POST.get('discription3')
        project.discription4 = request.POST.get('discription4')
        project.image3 = request.FILES.get('image3')
        project.save()

        return redirect('/timeattendance_all_projects')

    return render(request, 'timeattendance1_update.html', {'project': project})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance1

def timeattendance1_delete(request, pk):
    project = get_object_or_404(timeattendance1, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('timeattendance_all_projects')

    return render(request, 'timeattendance1_confirm_delete.html', {'project': project})




def timeattendance2_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        discription = request.POST.get('discription')
       

        timeattendance2.objects.create(
            title=title,
            discription=discription,
            
        )


    return render(request, 'timeattendance2_form.html')

def timeattendance2_list(request):
    projects1 = timeattendance2.objects.all()
    return render(request, 'timeattendance2_list.html', {'projects1': projects1})




from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance2

def timeattendance2_update(request, pk):
    project1 = get_object_or_404(timeattendance2, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project1.title = request.POST.get('title')
        project1.discription = request.POST.get('discription')
        
        project1.save()

        return redirect('/timeattendance_all_projects')

    return render(request, 'timeattendance2_update.html', {'project1': project1})



from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance2

def timeattendance2_delete(request, pk):
    project1 = get_object_or_404(timeattendance2, pk=pk)
    
    if request.method == 'POST':
        project1.delete()
        return redirect('timeattendance_all_projects')

    return render(request, 'timeattendance2_confirm_delete.html', {'project1': project1})





def timeattendance3_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        discription1 = request.POST.get('discription1')
        discription2 = request.POST.get('discription2')
        discription3 = request.POST.get('discription3')
        discription4 = request.POST.get('discription4')
        image = request.FILES.get('image')
       

        timeattendance3.objects.create(
            title=title,
            discription1=discription1,
            discription2=discription2,
            discription3=discription3,
            discription4=discription4,
            image=image,
            
        )


    return render(request, 'timeattendance3_form.html')



def timeattendance3_list(request):
    projects2 = timeattendance3.objects.all()
    return render(request, 'timeattendance3_list.html', {'projects2': projects2})




from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance3

def timeattendance3_update(request, pk):
    project2 = get_object_or_404(timeattendance3, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project2.title = request.POST.get('title')
        project2.discription1 = request.POST.get('discription1')
        project2.discription2 = request.POST.get('discription2')
        project2.discription3 = request.POST.get('discription3')
        project2.discription4 = request.POST.get('discription4')
        project2.image = request.FILES.get('image')
        
        project2.save()

        return redirect('/timeattendance_all_projects')

    return render(request, 'timeattendance3_update.html', {'project2': project2})



from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance3

def timeattendance3_delete(request, pk):
    project2 = get_object_or_404(timeattendance3, pk=pk)
    
    if request.method == 'POST':
        project2.delete()
        return redirect('timeattendance_all_projects')

    return render(request, 'timeattendance3_confirm_delete.html', {'project2': project2})



def timeattendance4_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        image = request.FILES.get('image')
        title2 = request.POST.get('title2')
        discription = request.POST.get('discription')


        timeattendance4.objects.create(
            title1=title1,
            image=image,
            title2=title2,
            discription=discription,

        )


    return render(request, 'timeattendance4_form.html')


def timeattendance4_list(request):
    projects3 = timeattendance4.objects.all()
    return render(request, 'timeattendance4_list.html', {'projects3': projects3})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance4

def timeattendance4_update(request, pk):
    project3 = get_object_or_404(timeattendance4, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project3.title1 = request.POST.get('title1')
        project3.image = request.FILES.get('image')
        project3.title2 = request.POST.get('title2')
        project3.discription = request.POST.get('discription')
        
        project3.save()

        return redirect('/timeattendance_all_projects')

    return render(request, 'timeattendance4_update.html', {'project3': project3})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timeattendance4

def timeattendance4_delete(request, pk):
    project3 = get_object_or_404(timeattendance4, pk=pk)
    
    if request.method == 'POST':
        project3.delete()
        return redirect('timeattendance_all_projects')

    return render(request, 'timeattendance4_confirm_delete.html', {'project3': project3})

def timeattendance(request):
    projects = timeattendance1.objects.all()
    projects1 = timeattendance2.objects.all()
    projects2 = timeattendance3.objects.all()
    projects3 = timeattendance4.objects.all()

    return render(request,"attendance.html",{'projects':projects,'projects1':projects1,'projects2':projects2,'projects3':projects3})

def timeattendance_all_projects(request):
    projects = timeattendance1.objects.all()
    projects1 = timeattendance2.objects.all()
    projects2 = timeattendance3.objects.all()
    projects3 = timeattendance4.objects.all()

    return render(request, 'timeattendance_all_projects.html', {'projects': projects, 'projects1': projects1, 'projects2': projects2,'projects3':projects3})




def productivity1_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        image1 = request.FILES.get('image1')
        title2 = request.POST.get('title2')
        subtitle1 = request.POST.get('subtitle1')
        title3 = request.POST.get('title3')
        subtitle2 = request.POST.get('subtitle2')
       


        productivity1.objects.create(
            title1=title1,
            image1=image1,
            title2=title2,
            subtitle1=subtitle1,
            title3=title3,
            subtitle2=subtitle2,
           

        )


    return render(request, 'productivity1_form.html')

def productivity1_list(request):
    projects = productivity1.objects.all()
    return render(request, 'productivity1_list.html', {'projects': projects})





from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity1

def productivity1_update(request, pk):
    project = get_object_or_404(productivity1, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project.title1 = request.POST.get('title1')
        project.image1 = request.FILES.get('image1')
        project.title2 = request.POST.get('title2')
        project.subtitle1 = request.POST.get('subtitle1')
        project.title3 = request.POST.get('title3')
        project.subtitle2 = request.POST.get('subtitle2')
        
        project.save()

        return redirect('/productivity_all_projects')

    return render(request, 'productivity1_update.html', {'project': project})


from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity1

def productivity1_delete(request, pk):
    project = get_object_or_404(productivity1, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('productivity_all_projects')

    return render(request, 'productivity1_confirm_delete.html', {'project': project})




def productivity2_create(request):
    if request.method == 'POST':
        image1 = request.FILES.get('image1')

        title1 = request.POST.get('title1')
        discription1 = request.POST.get('discription1')
       
        productivity2.objects.create(
            image1=image1,
            title1=title1,
            discription1=discription1,
           
            
        )


    return render(request, 'productivity2_form.html')

def productivity2_list(request):
    projects1 = productivity2.objects.all()
    return render(request, 'productivity2_list.html', {'projects1': projects1})




from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity2

def productivity2_update(request, pk):
    project1 = get_object_or_404(productivity2, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project1.image1 = request.FILES.get('image1')

        project1.title1 = request.POST.get('title1')
        project1.discription1 = request.POST.get('discription1')
       
        
        project1.save()

        return redirect('/productivity_all_projects')

    return render(request, 'productivity2_update.html', {'project1': project1})


from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity2

def productivity2_delete(request, pk):
    project1 = get_object_or_404(productivity2, pk=pk)
    
    if request.method == 'POST':
        project1.delete()
        return redirect('productivity_all_projects')

    return render(request, 'productivity2_confirm_delete.html', {'project1': project1})




def productivity3_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        image = request.FILES.get('image')
        title2 = request.POST.get('title2')
        discription = request.POST.get('discription')
        
        
        
        productivity3.objects.create(
            title1=title1,
            image=image,
            title2=title2,
            discription=discription
           

        )


    return render(request, 'productivity3_form.html')

def productivity3_list(request):
    projects2 = productivity3.objects.all()
    return render(request, 'productivity3_list.html', {'projects2': projects2})


from .models import Footer1


def footerinst(request):
    if request.method == 'POST':
        header1 = request.POST['header1']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        header2 = request.POST['header2']
        f1 = request.POST['f1']
        f2 = request.POST['f2']
        f3 = request.POST['f3']
        header3 = request.POST['header3']
        # photo= request.FILES.get('photo')
        copyright = request.POST['copyright']
        design = request.POST['design']
        k = Footer1(header1=header1,address=address, phone=phone, email=email,header2=header2,f1=f1,f2=f2,f3=f3,header3=header3,copyright=copyright,design=design)
        k.save()
        return HttpResponse("row  is inserted")
    return render(request, 'footerinst.html')

def footerretrive(request):

    return render(request,"footer.html")


from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity3

def productivity3_update(request, pk):
    project2 = get_object_or_404(productivity3, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
     
        project2.title1 = request.POST.get('title1')
        project2.image = request.FILES.get('image')
        project2.title2 = request.POST.get('title2')
        project2.discription = request.POST.get('discription')
        project2.save()

        return redirect('/productivity_all_projects')

    return render(request, 'productivity3_update.html', {'project2': project2})

from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity3

def productivity3_delete(request, pk):
    project2 = get_object_or_404(productivity3, pk=pk)
    
    if request.method == 'POST':
        project2.delete()
        return redirect('productivity_all_projects')

    return render(request, 'productivity3_confirm_delete.html', {'project2': project2})


def productivity4_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        discription1 = request.POST.get('discription1')
        image = request.FILES.get('image')
        title2 = request.POST.get('title2')
        discription2 = request.POST.get('discription2')
        
        
        
        productivity4.objects.create(
            title1=title1,
            discription1=discription1,

            image=image,
            title2=title2,
            discription2=discription2
           

        )


    return render(request, 'productivity4_form.html')

def productivity4_list(request):
    projects3 = productivity4.objects.all()
    return render(request, 'productivity4_list.html', {'projects3': projects3})





from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity4

def productivity4_update(request, pk):
    project3 = get_object_or_404(productivity4, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project3.title1 = request.POST.get('title1')
        project3.discription1 = request.POST.get('discription1')
        project3.image = request.FILES.get('image')
        project3.title2 = request.POST.get('title2')
        project3.discription2 = request.POST.get('discription2')
        
        project3.save()

        return redirect('/productivity_all_projects')

    return render(request, 'productivity4_update.html', {'project3': project3})




from django.shortcuts import render, get_object_or_404, redirect
from .models import productivity4

def productivity4_delete(request, pk):
    project3 = get_object_or_404(productivity4, pk=pk)
    
    if request.method == 'POST':
        project3.delete()
        return redirect('productivity_all_projects')

    return render(request, 'productivity4_confirm_delete.html', {'project3': project3})



def productivity_all_projects(request):
    projects = productivity1.objects.all()
    projects1 = productivity2.objects.all()
    projects2 = productivity3.objects.all()
    projects3 = productivity4.objects.all()
    projects4 = productivity5.objects.all()


    return render(request, 'productivity_all_projects.html', {'projects': projects, 'projects1': projects1, 'projects2': projects2,'projects3':projects3,'projects4':projects4})





def timetracking1_create(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        title2 = request.POST.get('title2')
        title3 = request.POST.get('title3')
        title4 = request.POST.get('title4')
        title5 = request.POST.get('title5')
        subtitle1 = request.POST.get('subtitle1')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        discription1 = request.POST.get('discription1')
        discription2 = request.POST.get('discription2')
        discription3 = request.POST.get('discription3')

        timetracking1.objects.create(
            title1=title1,
            title2=title2,
            title3=title3,
            title4=title4,
            title5=title5,
            subtitle1=subtitle1,
            image1=image1,
            image2=image2,
            discription1=discription1,
            discription2=discription2,
            discription3=discription3,

        )


    return render(request, 'timetracking1_form.html')

def timetracking1_list(request):
    projects = timetracking1.objects.all()
    return render(request, 'timetracking1_list.html', {'projects': projects})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking1

def timetracking1_update(request, pk):
    project = get_object_or_404(timetracking1, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project.title1 = request.POST.get('title1')
        project.title2 = request.POST.get('title2')
        project.title3 = request.POST.get('title3')
        project.title4 = request.POST.get('title4')
        project.title5 = request.POST.get('title5')
        project.subtitle1 = request.POST.get('subtitle1')
        project.image1 = request.FILES.get('image1')
        project.image2 = request.FILES.get('image2')
        project.discription1 = request.POST.get('discription1')
        project.discription2 = request.POST.get('discription2')
        project.discription3 = request.POST.get('discription3')
        project.save()

        return redirect('/timetracking_all_projects')

    return render(request, 'timetracking1_update.html', {'project': project})



from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking1

def timetracking1_delete(request, pk):
    project = get_object_or_404(timetracking1, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('timetracking_all_projects')

    return render(request, 'timetracking1_confirm_delete.html', {'project': project})




def timetracking2_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        discription = request.POST.get('discription')


        timetracking2.objects.create(
            title=title,
            image=image,
            discription=discription,

        )


    return render(request, 'timetracking2_form.html')


def timetracking2_list(request):
    projects1 = timetracking2.objects.all()
    return render(request, 'timetracking2_list.html', {'projects1': projects1})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking2

def timetracking2_update(request, pk):
    project1 = get_object_or_404(timetracking2, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project1.title = request.POST.get('title')
        project1.image = request.FILES.get('image')
        project1.discription = request.POST.get('discription')
        project1.save()

        return redirect('/timetracking_all_projects')

    return render(request, 'timetracking2_update.html', {'project1': project1})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking2

def timetracking2_delete(request, pk):
    project1 = get_object_or_404(timetracking2, pk=pk)
    
    if request.method == 'POST':
        project1.delete()
        return redirect('timetracking_all_projects')

    return render(request, 'timetracking2_confirm_delete.html', {'project1': project1})





def timetracking3_create(request):
    if request.method == 'POST':
        icons = request.POST.get('icons')
        title = request.POST.get('title')
        discription = request.POST.get('discription')


        timetracking3.objects.create(
            icons=icons,
            title=title,
            discription=discription,

        )


    return render(request, 'timetracking3_form.html')



def timetracking3_list(request):
    projects2 = timetracking3.objects.all()
    return render(request, 'timetracking3_list.html', {'projects2': projects2})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking3

def timetracking3_update(request, pk):
    project2 = get_object_or_404(timetracking3, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project2.title = request.POST.get('title')
        project2.discription = request.POST.get('discription')
        project2.save()

        return redirect('/timetracking_all_projects')

    return render(request, 'timetracking3_update.html', {'project2': project2})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking3

def timetracking3_delete(request, pk):
    project2 = get_object_or_404(timetracking3, pk=pk)
    
    if request.method == 'POST':
        project2.delete()
        return redirect('timetracking_all_projects')

    return render(request, 'timetracking3_confirm_delete.html', {'project2': project2})




def timetracking4_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        discription = request.POST.get('discription')


        timetracking4.objects.create(
            title=title,
            image=image,
            discription=discription,

        )


    return render(request, 'timetracking4_form.html')


def timetracking4_list(request):
    projects3 = timetracking4.objects.all()
    return render(request, 'timetracking4_list.html', {'projects3': projects3})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking4

def timetracking4_update(request, pk):
    project3 = get_object_or_404(timetracking4, pk=pk)

    if request.method == 'POST':
        # Update the fields as needed based on your requirements
        project3.title = request.POST.get('title')
        project3.image = request.FILES.get('image')
        project3.discription = request.POST.get('discription')
        project3.save()

        return redirect('/timetracking_all_projects')

    return render(request, 'timetracking4_update.html', {'project3': project3})


from django.shortcuts import render, get_object_or_404, redirect
from .models import timetracking4

def timetracking4_delete(request, pk):
    project3 = get_object_or_404(timetracking4, pk=pk)
    
    if request.method == 'POST':
        project3.delete()
        return redirect('timetracking_all_projects')

    return render(request, 'timetracking4_confirm_delete.html', {'project3': project3})



def timetracking_all_projects(request):
    projects = timetracking1.objects.all()
    projects1 = timetracking2.objects.all()
    projects2 = timetracking3.objects.all()
    projects3 = timetracking4.objects.all()
    return render(request, 'timetracking_all_projects.html', {'projects':projects,'projects1':projects1,'projects2':projects2,'projects3':projects3})














    

    




def navebar(request):                                            
    if request.method == "POST":
        image=request.FILES.get('image')
        nave1 = request.POST["nave1"]
        nave2 = request.POST["nave2"]
        nave3 = request.POST["nave3"]
        nave4 = request.POST["nave4"]
        nave5 = request.POST["nave5"]
        nave6 = request.POST["nave6"]
        nave7 = request.POST["nave7"]
        nave8 = request.POST["nave8"]
        nave9 = request.POST["nave9"]
        nave10 = request.POST["nave10"]
        nave11 = request.POST["nave11"]
        nave12 = request.POST["nave12"]
        nave13 = request.POST["nave13"]

        k=indexnave(image=image,nave1=nave1,nave2=nave2,nave3=nave3,nave4=nave4,nave5=nave5,nave6=nave6,nave7=nave7,nave8=nave8,nave9=nave9,nave10=nave10,nave11=nave11,nave12=nave12,nave13=nave13)
        k.save()
    return render(request,"navebar.html")


def nvbar(request):
    t=indexnave.objects.all()
    return render(request,"nave.html")

 
def footer_view(request):
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()


    return render(request, 'footer.html', {
        'links': links,
        'services': services,
        'contact_info': contact_info,
        'social' : social
    })

def footer_table(request):
    home1=FooterLink.objects.all()
    
    home2=FooterService.objects.all()
    data1=SocialLink.objects.all()
    data2=ContactInfo.objects.all()
    return render(request,"footertable.html",{'home1':home1,'home2':home2,'data1':data1,'data2':data2})

def footer_link(request):
    if request.method == 'POST':
        label = request.POST['label']
        url = request.POST['url']
        k = FooterLink(label=label,url=url)
        k.save()
        return redirect("/footer_table")
    return render(request,"footer_link_form.html")
def footer_link_edit(request,id):
    if request.method=="GET":
        post=FooterLink.objects.get(id=id)
        return render(request,"footer_link_update.html",{'post':post})
def footer_link_update(request,id):
    if request.method=="POST":
        label=request.POST['label']
        url= request.POST['url']
        k=FooterLink.objects.get(id=id)
        k.label=label
        k.url=url
       
        k.save()
        return redirect('/footer_table/')
    return render(request,"footer_link_update.html")
def footer_link_delete(request,id):
    post = get_object_or_404(FooterLink, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/footer_table/")
    return render(request, "footer_link_delete.html", {"post": post})

def footer_service(request):
    if request.method == 'POST':
        label = request.POST['label']
        url = request.POST['url']
        k = FooterService(label=label,url=url)
        k.save()
        return redirect("/footer_table")
    return render(request,"footer_service_form.html")
def footer_service_edit(request,id):
    if request.method=="GET":
        post=FooterService.objects.get(id=id)
        return render(request,"footer_service_update.html",{'post':post})
def footer_service_update(request,id):
    if request.method=="POST":
        label=request.POST['label']
        url= request.POST['url']
        k=FooterService.objects.get(id=id)
        k.label=label
        k.url=url
       
        k.save()
        return redirect('/footer_table/')
    return render(request,"footer_service_update.html")
def footer_service_delete(request,id):
    post = get_object_or_404(FooterService, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/footer_table/")
    return render(request, "footer_service_delete.html", {"post": post})
  

def footer_social(request):
    if request.method == 'POST':
        facebook_link = request.POST['facebook_link']
        twitter_link = request.POST['twitter_link']
        instagram_link = request.POST['instagram_link']
        youtube_link = request.POST['youtube_link']
        linkdin_link = request.POST['linkdin_link']


        k = SocialLink(linkdin_link=linkdin_link,youtube_link=youtube_link,twitter_link=twitter_link,instagram_link=instagram_link,facebook_link=facebook_link)
        k.save()
        return redirect("/footer_table")
    return render(request,"footer_social_form.html")
def footer_social_edit(request,id):
    if request.method=="GET":
        post=SocialLink.objects.get(id=id)
        return render(request,"footer_social_update.html",{'post':post})
def footer_social_update(request,id):
    if request.method=="POST":
        facebook_link=request.POST['facebook_link']
        twitter_link= request.POST['twitter_link']
        instagram_link=request.POST['instagram_link']
        youtube_link=request.POST['youtube_link']
        linkdin_link=request.POST['linkdin_link']
        k=SocialLink.objects.get(id=id)
        k.youtube_link=youtube_link
        k.linkdin_link=linkdin_link
        k.facebook_link=facebook_link
        k.twitter_link=twitter_link
        k.instagram_link=instagram_link
       
        k.save()
        return redirect('/footer_table/')
    return render(request,"footer_social_update.html")
def footer_social_delete(request,id):
    post = get_object_or_404(SocialLink, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/footer_table/")
    return render(request, "footer_social_delete.html", {"post": post})

  

def footer_contact(request):
    if request.method == 'POST':
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        

        k = ContactInfo(address=address,phone=phone,email=email)
        k.save()
        return redirect("/footer_table")
    return render(request,"footer_contact_form.html")
def footer_contact_edit(request,id):
    if request.method=="GET":
        post=ContactInfo.objects.get(id=id)
        return render(request,"footer_contact_edit.html",{'post':post})
def footer_contact_update(request,id):
    if request.method=="POST":
        address=request.POST['address']
        phone= request.POST['phone']
        email=request.POST['email']
        k=ContactInfo.objects.get(id=id)
        k.address=address
        k.phone=phone
        k.email=email
       
        k.save()
        return redirect('/footer_table/')
    return render(request,"footer_contact_edit.html")
def footer_contact_delete(request,id):
    post = get_object_or_404(ContactInfo, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/footer_table/")
    return render(request, "footer_contact_delete.html", {"post": post})


from .models import  home,home2,home3,home4,home5,nav1,nav2
from .models import FooterLink,FooterService,ContactInfo,SocialLink
def homepage1(request):
    if request.method=="POST":
        title1=request.POST['title1']
        discription1= request.POST['discription1']
        image1 = request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        title2=request.POST['title2']
        image4=request.FILES.get('image4')
        discription2= request.POST['discription2']    
       
        k=home(title1=title1,discription1=discription1,image1=image1,image2=image2,image3=image3,title2=title2,image4=image4,discription2=discription2)
        k.save()
        return redirect("/homedata1")
    return render(request,"home1.html")

def homepage2(request):
    if request.method=="POST":
        image = request.FILES.get('image')
        title=request.POST['title']
        discription= request.POST['discription']
        image1 = request.FILES.get('image1')
       
        k1=home2(image=image,title=title,discription=discription,image1=image1)
        k1.save()
        return redirect("/homedata1")

    return render(request,"home2.html")
def homepage3(request):
    if request.method=="POST":
        title=request.POST['title']
        image1 = request.FILES.get('image1')
        discription1= request.POST['discription1']
        point1= request.POST['point1']
        point2= request.POST['point2']
        point3= request.POST['point3']
        point4= request.POST['point4']
        discription2= request.POST['discription2']
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')


        
        k2=home3(title=title,image1=image1,discription1=discription1,point1=point1,point2=point2,point3=point3,point4=point4,discription2=discription2,image2=image2,image3=image3)
        k2.save()
        return redirect("/homedata1")

    return render(request,"home3.html")

def homepage4(request):
    if request.method=="POST":
        title1=request.POST['title1']
        image1 = request.FILES.get('image1')
        title2=request.POST['title2']
        image2 = request.FILES.get('image2')
        k3=home4(title1=title1,image1=image1,title2=title2,image2=image2)
        k3.save()
        return redirect("/homedata1")
    return render(request,"home4.html")
def homepage5(request):
    if request.method=="POST":
        image = request.FILES.get('image')
        title=request.POST['title']
        discription= request.POST['discription']
        p=request.POST['p']
        link = request.FILES.get('link')

        k4=home5(image=image,title=title,discription=discription,p=p,link=link)
        k4.save()
        return redirect("/homedata1")

    return render(request,"home5.html")

def homedata1(request):
    post=home.objects.all()
    home1=home2.objects.all()
    data=home3.objects.all()
    data1=home4.objects.all()
    data2=home5.objects.all()
    return render(request,"data.html",{'post':post,'home1':home1,'data':data,'data1':data1,'data2':data2})
 
def edit1(request,id):
    if request.method=="GET":
        post=home.objects.get(id=id)
        return render(request,"update1.html",{'post':post})
def update1(request,id):
    if request.method=="POST":
        title1=request.POST['title1']
        discription1= request.POST['discription1']
        image1 = request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        title2=request.POST['title2']
        image4=request.FILES.get('image4')
        discription2= request.POST['discription2']    
        k=home.objects.get(id=id)
        k.title1=title1
        k.discription1=discription1
        k.image1=image1
        k.image2=image2
        k.image3=image3
        k.title2=title2
        k.image4=image4
        k.discription2=discription2
        k.save()
        return redirect("/homedata1")
    return render(request,"update1.html")
def delete1(request,id):
    post = get_object_or_404(home, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/homedata1/")
    return render(request, "delete1.html", {"post": post})


def data2(request):
    if request.method=="GET":
        post=home2.objects.all()
        return render(request,"data2.html",{'post':post}) 
def edit2(request,id):
    if request.method=="GET":
        post=home2.objects.get(id=id)
        return render(request,"update2.html",{'post':post})
def update2(request,id):
    if request.method=="POST":
       
        image=request.FILES.get('image')
        title=request.POST['title']
        discription= request.POST['discription']
        image1=request.FILES.get('image1')
    
        k1=home2.objects.get(id=id)
       
        k1.image=image
        k1.title=title
        k1.discription=discription
        k1.image1=image1
        k1.save()
        return redirect("/homedata1")
    return render(request,"update2.html")
def delete2(request,id):
    post = get_object_or_404(home2, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/homedata1/")
    return render(request, "delete2.html", {"post": post})
  

def data3(request):
    if request.method=="GET":
        post=home3.objects.all()
        return render(request,"data3.html",{'post':post}) 
def edit3(request,id):
    if request.method=="GET":
        post=home3.objects.get(id=id)
        return render(request,"update3.html",{'post':post})
def update3(request,id):
    if request.method=="POST":
        title=request.POST['title']
        image1 = request.FILES.get('image1')

        discription1= request.POST['discription1']
        point1=request.POST['point1']
        point2=request.POST['point2']
        point3=request.POST['point3']
        point4=request.POST['point4']
        discription2= request.POST['discription2']    

        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
       
        k2=home3.objects.get(id=id)
        k2.title=title

        k2.image1=image1
        k2.discription1=discription1

        k2.point1=point1
        k2.point2=point2
        k2.point3=point3
        k2.point4=point4
       
        k2.discription2=discription2
        k2.image2=image2
        k2.image3=image3

        k2.save()
        return redirect("/homedata1")
    return render(request,"update3.html")
def delete3(request,id):
    post = get_object_or_404(home3, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/homedata1/")
    return render(request, "delete3.html", {"post": post})

def data4(request):
    if request.method=="GET":
        post=home4.objects.all()
        return render(request,"data4.html",{'post':post}) 
def edit4(request,id):
    if request.method=="GET":
        post=home4.objects.get(id=id)
        return render(request,"update4.html",{'post':post})
def update4(request,id):
    if request.method=="POST":
        title1=request.POST['title1']
 
        image1=request.FILES.get('image1')
        title2=request.POST['title2']
        image2=request.FILES.get('image2')
   
        k3=home4.objects.get(id=id)
        k3.title1=title1

        k3.image1=image1
        k3.title2=title2
        k3.image2=image2

        k3.save()
        return redirect("/homedata1")
    return render(request,"update4.html")
def delete4(request,id):
    post = get_object_or_404(home4, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/homedata1/")
    return render(request, "delete4.html", {"post": post})

def data5(request):
    if request.method=="GET":
        post=home5.objects.all()
        return render(request,"data5.html",{'post':post}) 
def edit5(request,id):
    if request.method=="GET":
        post=home5.objects.get(id=id)
        return render(request,"update5.html",{'post':post})
def update5(request,id):
    hom=home5.objects.filter(id=id).first()
    if request.method=="POST":
       
        image=request.FILES.get('image')
        title=request.POST['title']
        discription= request.POST['discription']    
        p=request.POST['p']
        link=request.POST['link']
    
        k4=home5.objects.get(id=id)
       
        k4.image=image
        k4.title=title
        k4.discription=discription
        k4.p=p
        k4.link=link
        k4.save()
        return redirect("/homedata1")
    return render(request,"update5.html",{'hom':hom})

def delete5(request,id):
    post = get_object_or_404(home5, id=id)    
    if request.method == "POST":
        post.delete()
        return redirect("/homedata1/")
    return render(request, "delete5.html", {"post": post})



from .models import home6
def homepage6(request):
    if request.method=='POST':
        image=request.FILES.get('image')
        content=request.POST.get('content')
        d1=request.POST.get('d1')
        d2=request.POST.get('d2')
        d3=request.POST.get('d3')
        d4=request.POST.get('d4')
        d5=request.POST.get('d5')
        image1=request.FILES.get('image1')
        content1=request.POST.get('content1')
        d6=request.POST.get('d6')
        d7=request.POST.get('d7')
        d8=request.POST.get('d8')
        d9=request.POST.get('d9')
        d10=request.POST.get('d10')
        d11=request.POST.get('d11')
        d12=request.POST.get('d12')
        image2=request.FILES.get('image2')
        content2=request.POST.get('content2')
        d13=request.POST.get('d13')
        d14=request.POST.get('d14')
        d15=request.POST.get('d15')
        d16=request.POST.get('d16')
        d17=request.POST.get('d17')
        d18=request.POST.get('d18')
        image3=request.FILES.get('image3')
        content3=request.POST.get('content3')
        d19=request.POST.get('d19')
        d20=request.POST.get('d20')
        d21=request.POST.get('d21')
        d22=request.POST.get('d22')
        d23=request.POST.get('d23')
        d24=request.POST.get('d24')
        d25=request.POST.get('d25')


        k6=home6(image=image,content=content,d1=d1,d2=d2,d3=d3,d4=d4,d5=d5,image1=image1,content1=content1,d6=d6,d7=d7,d8=d8,d9=d9,d10=d10,d11=d11,d12=d12,image2=image2,content2=content2,d13=d13,d14=d14,d15=d15,d16=d16,d17=d17,d18=d18,image3=image3,content3=content3,d19=d19,d20=d20,d21=d21,d22=d22,d23=d23,d24=d24,d25=d25)
        k6.save()
    return render(request,"home6.html")



def company_list1(request):
    companies = Companys.objects.filter(plantype="1").order_by('-id')  
    companies1 = Companys.objects.filter(plantype="1").last()
   

    items_per_page = 5  


    paginator = Paginator(companies, items_per_page)

    page = request.GET.get('page')

    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        agreement_status = request.POST.get('agreement_status')

        if company_id is not None and agreement_status is not None:
            company = Companys.objects.get(id=company_id)
            company.agreement_status = int(agreement_status)
            company.save()

            if agreement_status == '1':
                subject = 'Agreement Accepted'
                message = f'Thank you, we have accepted your agreement, {company.username}!'
            elif agreement_status == '2':
                subject = 'Agreement Declined'
                message = f'Sorry, we have not accepted your agreement, {company.username}!'
            else:
                subject = 'Agreement Status Update'
                message = f'Agreement status updated for {company.username}.'

            from_email = 'developtrees1@gmail.com'  
            to_email = [company.email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
            except Exception as e:
                print(f"Error sending email: {e}")

    return render(request, 'admin-template/company_list.html', {'companies': companies,'companies1':companies1})
def delete_company_list1(request,id):
    compani=get_object_or_404(Companys,id=id)
    compani.delete()
    messages.success(request,"Your Data was deleted successfully")
    return redirect('/company_list/')
def company_list2(request):
    companies = Companys.objects.filter(plantype="2").order_by('-id')  
    companies1 = Companys.objects.filter(plantype="2").last()
    items_per_page = 5  


    paginator = Paginator(companies, items_per_page)

    page = request.GET.get('page')

    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        agreement_status = request.POST.get('agreement_status')

        if company_id is not None and agreement_status is not None:
            company = Companys.objects.get(id=company_id)
            company.agreement_status = int(agreement_status)
            company.save()

            if agreement_status == '1':
                subject = 'Agreement Accepted'
                message = f'Thank you, we have accepted your agreement, {company.username}!'
            elif agreement_status == '2':
                subject = 'Agreement Declined'
                message = f'Sorry, we have not accepted your agreement, {company.username}!'
            else:
                subject = 'Agreement Status Update'
                message = f'Agreement status updated for {company.username}.'

            from_email = 'developtrees1@gmail.com'  
            to_email = [company.email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
            except Exception as e:
                print(f"Error sending email: {e}")

    return render(request, 'admin-template/company_list.html', {'companies': companies,'companies1':companies1})

def company_list3(request):
    companies = Companys.objects.filter(plantype="3").order_by('-id')  
    companies1 = Companys.objects.filter(plantype="3").last()
    items_per_page = 5  


    paginator = Paginator(companies, items_per_page)

    page = request.GET.get('page')

    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        agreement_status = request.POST.get('agreement_status')

        if company_id is not None and agreement_status is not None:
            company = Companys.objects.get(id=company_id)
            company.agreement_status = int(agreement_status)
            company.save()

            if agreement_status == '1':
                subject = 'Agreement Accepted'
                message = f'Thank you, we have accepted your agreement, {company.username}!'
            elif agreement_status == '2':
                subject = 'Agreement Declined'
                message = f'Sorry, we have not accepted your agreement, {company.username}!'
            else:
                subject = 'Agreement Status Update'
                message = f'Agreement status updated for {company.username}.'

            from_email = 'developtrees1@gmail.com'  
            to_email = [company.email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
            except Exception as e:
                print(f"Error sending email: {e}")

    return render(request, 'admin-template/company_list.html', {'companies': companies,'companies1':companies1})

def company_list4(request):
    companies = Companys.objects.filter(plantype="4").order_by('-id')  
    companies1 = Companys.objects.filter(plantype="4").last()
    items_per_page = 5  


    paginator = Paginator(companies, items_per_page)

    page = request.GET.get('page')

    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        agreement_status = request.POST.get('agreement_status')

        if company_id is not None and agreement_status is not None:
            company = Companys.objects.get(id=company_id)
            company.agreement_status = int(agreement_status)
            company.save()

            if agreement_status == '1':
                subject = 'Agreement Accepted'
                message = f'Thank you, we have accepted your agreement, {company.username}!'
            elif agreement_status == '2':
                subject = 'Agreement Declined'
                message = f'Sorry, we have not accepted your agreement, {company.username}!'
            else:
                subject = 'Agreement Status Update'
                message = f'Agreement status updated for {company.username}.'

            from_email = 'developtrees1@gmail.com'  
            to_email = [company.email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
            except Exception as e:
                print(f"Error sending email: {e}")

    return render(request, 'admin-template/company_list.html', {'companies': companies,'companies1':companies1})

from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render ,redirect

# def adminA_Password_save(request):
#     if request.method == 'POST':
#         user = CustomUser.objects.get(is_superuser=True)
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         if password and password == confirm_password:
#             user.password = make_password(password)
#             user.save()
#         return redirect('adminAdashboard')
#     return render(request,"admin-template/adminA_password.html")


def adminA_Password_save(request):
    if request.method == 'POST':
        superusers = CustomUser.objects.filter(is_superuser=True)
        if superusers.exists():
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password and password == confirm_password:
                for user in superusers:
                    user.password = make_password(password)
                    user.save()
            return redirect('adminAdashboard')
        else:
            return redirect('adminA_password')  
    return render(request, "admin-template/adminA_password.html")




def New_Add_ons(request):
    g1=typeofplans.objects.all()

    shou = admin_drop.objects.filter(show1=0)
    prdrop = project_drop.objects.filter(show1=0)
    screen=screenmon.objects.filter(show1=0)
    # adnav=employnav.objects.filter(show1=0)
    
    shou1= admin_drop.objects.filter(show2=0)
    prdrop1 = project_drop.objects.filter(show2=0)
    screen1=screenmon.objects.filter(show2=0)

    shou2 = admin_drop.objects.filter(show3=0)
    prdrop2 = project_drop.objects.filter(show3=0)
    screen2=screenmon.objects.filter(show3=0)

    plan_type = request.POST.get('plantype')
    if plan_type:
        plan = typeofplans.objects.get(id=plan_type)
        if plan.annual_price == 'Basic Plan':
            shou = admin_drop.objects.filter(show1=0)
            prdrop = project_drop.objects.filter(show1=0)
            screen = screenmon.objects.filter(show1=0)
            # adnav=employnav.objects.filter(show1=0),'adnav':adnav

        elif plan.annual_price == 'Gold Plan':
            shou1 = admin_drop.objects.filter(show2=0)
            prdrop1 = project_drop.objects.filter(show2=0)
            screen1 = screenmon.objects.filter(show2=0)
        elif plan.annual_price == 'Platinum Plan':
            shou2 = admin_drop.objects.filter(show3=0)
            prdrop2 = project_drop.objects.filter(show3=0)
            screen2 = screenmon.objects.filter(show3=0)

    if request.method== "POST":
        name=request.POST.get("name")
        amount=request.POST.get("amount")
        plantype=request.POST.get("plantype")
        k=Addons(name=name,amount=amount,plantype=typeofplans(id=plantype))
        k.save()

    context = {'g1': g1, 'shou': shou, 'prdrop': prdrop, 'prdrop2': prdrop2, 'prdrop1': prdrop1, 'screen': screen, 'screen1': screen1, 'screen2': screen2, 'shou1': shou1, 'shou2': shou2}
    return render(request, "Add_ons1.html", context)



from django.shortcuts import render, redirect
from.models import Addons

def New_Add_ons_table(request):
    p=Addons.objects.all()
    return render(request,"New_Add_ons_table.html",{'p':p})

def Delete_New_Add_ons(request, addon_id):
    addon = Addons.objects.get(id=addon_id)
    addon.delete()
    return redirect('New_Add_ons_table')




def subscription1(request):
  
    k=typeofplans.objects.filter(plans__contains='4')
    k1=typeofplans.objects.filter(plans__contains='5')
    k2=typeofplans.objects.filter(plans__contains='6')
    k3=typeofplans.objects.filter(plans__contains='Based on demand')
    a=typeofplans.objects.filter(plans__contains='4')
    a1=typeofplans.objects.filter(plans__contains='5')
    a2=typeofplans.objects.filter(plans__contains='6')
    a3=typeofplans.objects.filter(plans__contains='Based on demand')
    b=typeofplans.objects.filter(plans__contains='4')
    b1=typeofplans.objects.filter(plans__contains='5')
    b2=typeofplans.objects.filter(plans__contains='6')
    b3=typeofplans.objects.filter(plans__contains='Based on demand')
    c=typeofplans.objects.filter(plans__contains='4')
    c1=typeofplans.objects.filter(plans__contains='5')
    c2=typeofplans.objects.filter(plans__contains='6')
    c3=typeofplans.objects.filter(plans__contains='Based on demand')
    d=typeofplans.objects.filter(plans__contains='4')
    d1=typeofplans.objects.filter(plans__contains='5')
    d2=typeofplans.objects.filter(plans__contains='6')
    d3=typeofplans.objects.filter(plans__contains='Based on demand')
    plans_list=typeofplans.objects.all()
    features_list=featurestypes.objects.filter(show1=1)
    features_list1=featurestypes.objects.filter(show2=1)
    features_list2=featurestypes.objects.filter(show3=1)  
    features_list3=featurestypes.objects.all()
    s=typeofplans.objects.filter(plans__contains='4').first()
    s1=typeofplans.objects.filter(plans__contains='5').first()
    s2=typeofplans.objects.filter(plans__contains='6').first()

    selected_plans = SelectedPlan.objects.all()
    newplan=Addons.objects.filter(plantype=1)
    newplan1=Addons.objects.filter(plantype=2)
    newplan2=Addons.objects.filter(plantype=3)
    newplan3=Addons.objects.filter(plantype=4)
    faq_items = FAQItem.objects.all()   
    if request.method == "POST":
        planamount=request.POST.get('planamount')
        amount=int(planamount)*100
        planType=request.POST['planType']
        client = razorpay.Client(auth=("rzp_test_wKlbQmRzj5wB13", "Rj5Q5P45QqYj3xWVn6ItDpSc"))
        payment = client.order.create({'amount':amount, 'currency': 'INR', 'payment_capture': '1'})
        request.session['form_data1'] = {'planamount': planamount, 'planType':planType,'addon':1,'order_id':payment['id']}
        return render(request, "loader.html", {'payment': payment})
    context = {'s':s,'s1':s1,'s2':s2,'d':d,'d1':d1,'d2':d2,'d3':d3,'k':k,'k1':k1,'k2':k2,'k3':k3,'a':a,'a1':a1,'a2':a2,'a3':a3,'b':b,'b1':b1,'b2':b2,'b3':b3,'c':c,'c1':c1,'c2':c2,'c3':c3,'faq_items':faq_items,'selected_plans':selected_plans,'newplan':newplan,'newplan1':newplan1,'newplan2':newplan2,'newplan3':newplan3,'plans_list': plans_list, 'features_list': features_list, 'features_list1':features_list1,'features_list2':features_list2,'features_list3':features_list3, "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID}
    return render(request, "plan3.html", context=context)   

def planexpire_payment(request):
    url = "https://api.cashfree.com/pg/orders"

    headers = {
            "X-Client-Id": "65027036b36cd7d08b4c5d7b33072056",
            "X-Client-Secret": "cfsk_ma_prod_e9af870c9a9b8b0880ec4ed0617d7b98_2651c73f",
            "x-api-version": "2023-08-01",
        }
        
    order_id = uuid.uuid4().hex
    customer_id = uuid.uuid4().hex
    email1=request.session.get('email_2')
    request.session['order_idpex']=order_id
    data = Companys.objects.filter(email=email1).first()
    email=data.email
    Mobile=data.phone_number
    username=data.organizationname
    if data:
       data1 = data.plantype
       newplan = typeofplans.objects.filter(id=data1).first()
    else:
         messages.error(request, "You Don't have Acces to do Payment Operations")
         return HttpResponseRedirect("/planexpireauthentication/")

    selected_plans = []
    selected_amounts = []
    

    if request.method == "POST":
        planamount=request.POST.get('planamount')
        amount = planamount
        planType=request.POST.get('planType')
        payload = {
            "order_id": order_id,
            "order_amount": amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": customer_id,
                "customer_name": username,
                "customer_email": email,
                "customer_phone": Mobile,
            },
             "order_meta":{
                "return_url":"https://buglegal.com/planupdate/?order_id=order_id"

            }
        }

        request.session['form_data1'] = {'planamount': planamount, 'planType':planType,'addon':1,'order_id':order_id}
        response = requests.post(url=url, headers=headers, json=payload)
        payment_ses=response.json()
        return render(request,"loader.html",{'response':response,'payment_ses':payment_ses})
    return render(request, "planexpire_payment.html", {'data': data, 'newplan': newplan, 'selected_plans': selected_plans, "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID})




def planupdate(request):
    email1=request.session.get('email_2')
    data = Companys.objects.filter(email=email1).first()
    data1=data.id
    form_data1 = request.session.get('form_data1')

    if form_data1:
        order_id=form_data1['order_id']
        url = f"https://api.cashfree.com/pg/orders/{order_id}"

        headers = {
            "X-Client-Id": "65027036b36cd7d08b4c5d7b33072056",
            "X-Client-Secret": "cfsk_ma_prod_e9af870c9a9b8b0880ec4ed0617d7b98_2651c73f",
            "x-api-version": "2023-08-01",
            "x-request-id":"4dfb9780-46fe-11ee-be56-0242ac120002",
            "x-idempotency-key":"47bf8872-46fe-11ee-be56-0242ac120002"
        }
        response = requests.post(url=url, headers=headers)
        payment_ses=response.json()
        order_status = payment_ses.get('order_status')
        if order_status == "PAID":
            date=datetime.now()
            compid=Companys.objects.get(id=data1)
            compid.date=date
            compid.freetraile=0
            compid.save()
            del request.session['form_data1']
            return render(request, "payment_success.html")
        else:
            return render(request, "payment_fail.html")
    else:
        messages.error(request, "Form data not found.")
        return redirect('/')  



from.models import freetraildays

def homes(request):
    if request.method == "POST":
        freedays=request.POST['freedays']
        monthly=request.POST['monthly']
        yearly=request.POST['yearly']
        k=freetraildays(freedays=freedays,monthly=monthly,yearly=yearly)
        k.save()
        return HttpResponseRedirect(reverse('homes'))
    return render(request,"ac.html")
def freetrailtable(request):
    k=freetraildays.objects.all()
    return render(request,"freetrailtable.html",{'k':k})

def freetrailedit(request,id):
     ks=freetraildays.objects.get(id=id)
     return render(request,"freetrailupdate.html",{'ks':ks})

def freetrailupdate(request,id):
    ks=freetraildays.objects.filter(id=id).first()
    if request.method == "POST":
        freedays=request.POST['freedays']
        monthly=request.POST['monthly']
        yearly=request.POST['yearly']
        k=freetraildays.objects.get(id=id)
        k.freedays=freedays
        k.monthly=monthly
        k.yearly=yearly
       
        k.save()
        return redirect("/freetrailtable")
    return render(request,"freetrailupdate.html",{'ks':ks})


def addonsedit(request,id):
     ks=Addons.objects.get(id=id)
     return render(request,"addonsupdate.html",{'ks':ks})

def addonsupdate(request,id):
    ks=Addons.objects.filter(id=id).first()
   
    if request.method == "POST":
        amount = request.POST.get("amount")

        
        k = Addons.objects.get(id=id)
        k.amount = amount
        k.save()

        return redirect("/New_Add_ons_table")
    return render(request, "addonsupdate.html", {'ks':ks})


from .models import about

def aboutuspage(request):
    k=about.objects.all()
    return render(request,"aboutus.html",{'k':k})


def aboutus(request):
    if request.method=='POST':
        content=request.POST.get('content')
        images=request.FILES.get('images')
        content1=request.POST.get('content1')
        c1=request.POST.get('c1')
        c2=request.POST.get('c2')
        c3=request.POST.get('c3')
        images1=request.FILES.get('images1')
        content2=request.POST.get('content2')
        images2=request.FILES.get('images2')
        c4=request.POST.get('c4')
        c5=request.POST.get('c5')
        c6=request.POST.get('c6')
        c7=request.POST.get('c7')
        c8=request.POST.get('c8')
        c9=request.POST.get('c9')
        images3=request.FILES.get('images3')
        images4=request.FILES.get('images4')
        content3=request.POST.get('content3')
        images5=request.FILES.get('images5')
        content44=request.POST.get('content44')
        images6=request.FILES.get('images6')
        content55=request.POST.get('content55')
        images7=request.FILES.get('images7')
        content6=request.POST.get('content6')
        images8=request.FILES.get('images8')
        content7=request.POST.get('content7')

        k=about(content=content,images=images,content1=content1,c1=c1,c2=c2,c3=c3,images1=images1,content2=content2,images2=images2,c4=c4,c5=c5,c6=c6,c7=c7,c8=c8,c9=c9,images3=images3,images4=images4,content3=content3,
          images5=images5,content44=content44,images6=images6,content55=content55,images7=images7,content6=content6,
             images8=images8,content7=content7     )
        k.save()
    return render(request,"aboutinsert.html")

def aboutdisplay(request):
    if request.method=="GET":
        k=about.objects.all()
    return render(request,"aboutdisplay.html",{'k':k})

def about_edit(request,id):
    instance=about.objects.get(id=id)
    return render(request,"aboutupdate.html",{'instance':instance})

def aboutupdate(request,id):
    if request.method=='POST':
        content=request.POST.get('content')
        images=request.FILES.get('images')
        content1=request.POST.get('content1')
        c1=request.POST.get('c1')
        c2=request.POST.get('c2')
        c3=request.POST.get('c3')
        images1=request.FILES.get('images1')
        content2=request.POST.get('content2')
        images2=request.FILES.get('images2')
        c4=request.POST.get('c4')
        c5=request.POST.get('c5')
        c6=request.POST.get('c6')
        c7=request.POST.get('c7')
        c8=request.POST.get('c8')
        c9=request.POST.get('c9')
        images3=request.FILES.get('images3')
        images4=request.FILES.get('images4')
        content3=request.POST.get('content3')
        images5=request.FILES.get('images5')
        content44=request.POST.get('content44')
        images6=request.FILES.get('images6')
        content55=request.POST.get('content55')
        images7=request.FILES.get('images7')
        content6=request.POST.get('content6')
        images8=request.FILES.get('images8')
        content7=request.POST.get('content7')
        k=about.objects.get(id=id)
        k.content=content
        k.images=images
        k.content1=content1
        k.c1=c1
        k.c2=c2
        k.c3=c3
        k.images1=images1
        k.content2=content2
        k.images2=images2
        k.c4=c4
        k.c5=c5
        k.c6=c6
        k.c7=c7
        k.c8=c8
        k.c9=c9
        k.images3=images3
        k.images4=images4
        k.content3=content3
        k.images5=images5
        k.content44=content44
        k.images6=images6
        k.content55=content55
        k.images7=images7
        k.content6=content6
        k.images8=images8
        k.content7=content7
        k.save()
        return redirect('/aboutdisplay')

    return render(request,"aboutupdate.html")

def aboutdelete(request, id):
        mn=about.objects.get(id=id)
        mn.delete()
        return redirect('/aboutdisplay')  


from .models import *
from .forms import *
from notifications.signals import notify 
from notifications.models import Notification

def contact(request):
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    contact_info2 = ContactInfo2.objects.first() 
    fd=termsandconditions1.objects.all()

    context = {
                 'links':links,'services':services,'contact_info':contact_info,'social':social,'contact_info2': contact_info2,'fd':fd
        }
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact_message = ContactMessage(name=name, email=email, subject=subject, message=message)
        contact_message.save()
        

        superuser = CustomUser.objects.filter(is_superuser=1).first()
        if superuser:
            notify.send(sender=contact_message, recipient=superuser, verb='Contact', description=f"{name} has messaged.")


        return redirect('success_page')  # Redirect to a success page
    else:
        return render(request, 'contact.html',context)
       

def success_page(request):
        return render(request,'contactsuccess.html')

def create_contact_info(request):
    if request.method == 'POST':
        form = ContactInfo2Form(request.POST)  # Assuming you have a form for validation
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = ContactInfo2Form()
    context = {'form': form}
    return render(request, 'create_contact_info.html', context)

def view_contact_info(request):
    contact_info2 = ContactInfo2.objects.first()  # Adjust for multi-record retrieval if needed
    context = {'contact_info2': contact_info2}
    return render(request, 'view_contact_info.html', context)

def update_contact_info(request, pk):  # Assuming a primary key for identification
    try:
        contact_info2 = ContactInfo2.objects.get(pk=pk)
    except ContactInfo2.DoesNotExist:
        raise Http404("Contact information not found")

    if request.method == 'POST':
        form = ContactInfo2Form(request.POST, instance=contact_info2)
        if form.is_valid():
            form.save()
            return redirect('view_contact_info')
    else:
        form = ContactInfo2Form(instance=contact_info2)
    context = {'form': form}
    return render(request, 'update_contact_info.html', context)

def delete_contact_info(request, pk):  # Assuming a primary key for identification
    try:
        contact_info2 = ContactInfo2.objects.get(pk=pk)
    except ContactInfo2.DoesNotExist:
        raise Http404("Contact information not found")

    if request.method == 'POST':
        contact_info2.delete()
        return redirect('contact_list')  # Redirect to a list of contact information
    else:
        context = {'contact_info2': contact_info2}
        return render(request, 'delete_contact_info.html', context)
    

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import ContactMessage

def retrieve_contact_messages(request):
    contact_messages = ContactMessage.objects.all().order_by('-timestamp')
    items_per_page = 10
    paginator = Paginator(contact_messages, items_per_page)
    page = request.GET.get('page')
    try:
        contact_messages = paginator.page(page)
    except PageNotAnInteger:
        contact_messages = paginator.page(1)
    except EmptyPage:
        contact_messages = paginator.page(paginator.num_pages)
    context = {'contact_messages': contact_messages}
    return render(request, 'retrive_contact.html', context)

def reply_message(request, message_id):
    message = ContactMessage.objects.get(id=message_id)

    if request.method == 'POST':
        reply_content = request.POST.get('reply_content')
        send_mail(
            subject='Re: ' + message.subject,
            message=reply_content,
            from_email=settings.DEFAULT_FROM_EMAIL,  # Adjust as needed
            recipient_list=[message.email],
        )
        return redirect('retrieve_contact_messages')  # Redirect to message list

    return render(request, 'reply_message_form.html', {'message': message})

from django.shortcuts import render, redirect
from .models import ContactMessage

def delete_selected_messages(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('selected_messages')
        ContactMessage.objects.filter(id__in=selected_messages).delete()
    return redirect('retrieve_contact_messages')
    


def subscription2(request):
    k=typeofplans.objects.filter(plans__contains='4')
    k1=typeofplans.objects.filter(plans__contains='5')
    k2=typeofplans.objects.filter(plans__contains='6')
    k3=typeofplans.objects.filter(plans__contains='Based on demand')
    a=typeofplans.objects.filter(plans__contains='4')
    a1=typeofplans.objects.filter(plans__contains='5')
    a2=typeofplans.objects.filter(plans__contains='6')
    a3=typeofplans.objects.filter(plans__contains='Based on demand')
    b=typeofplans.objects.filter(plans__contains='4')
    b1=typeofplans.objects.filter(plans__contains='5')
    b2=typeofplans.objects.filter(plans__contains='6')
    b3=typeofplans.objects.filter(plans__contains='Based on demand')
    c=typeofplans.objects.filter(plans__contains='4')
    c1=typeofplans.objects.filter(plans__contains='5')
    c2=typeofplans.objects.filter(plans__contains='6')
    c3=typeofplans.objects.filter(plans__contains='Based on demand')
    d=typeofplans.objects.filter(plans__contains='4')
    d1=typeofplans.objects.filter(plans__contains='5')
    d2=typeofplans.objects.filter(plans__contains='6')
    d3=typeofplans.objects.filter(plans__contains='Based on demand')
    plans_list=typeofplans.objects.all()
    features_list=featurestypes.objects.filter(show1=1)
    features_list1=featurestypes.objects.filter(show2=1)
    features_list2=featurestypes.objects.filter(show3=1)  
    features_list3=featurestypes.objects.all()
    s=typeofplans.objects.filter(plans__contains='4').first()
    s1=typeofplans.objects.filter(plans__contains='5').first()
    s2=typeofplans.objects.filter(plans__contains='6').first()

    selected_plans = SelectedPlan.objects.all()
    newplan=Addons.objects.filter(plantype=1)
    newplan1=Addons.objects.filter(plantype=2)
    newplan2=Addons.objects.filter(plantype=3)
    newplan3=Addons.objects.filter(plantype=4)
    faq_items = FAQItem.objects.all()   
    if request.method == "POST":
        planamount=request.POST.get('planamount')
        amount=int(planamount)*100
        planType=request.POST['planType']
        client = razorpay.Client(auth=("rzp_test_wKlbQmRzj5wB13", "Rj5Q5P45QqYj3xWVn6ItDpSc"))
        payment = client.order.create({'amount':amount, 'currency': 'INR', 'payment_capture': '1'})
        request.session['form_data1'] = {'planamount': planamount, 'planType':planType,'addon':1,'order_id':payment['id']}
        return render(request, "loader2.html", {'payment': payment})
    context = {'s':s,'s1':s1,'s2':s2,'d':d,'d1':d1,'d2':d2,'d3':d3,'k':k,'k1':k1,'k2':k2,'k3':k3,'a':a,'a1':a1,'a2':a2,'a3':a3,'b':b,'b1':b1,'b2':b2,'b3':b3,'c':c,'c1':c1,'c2':c2,'c3':c3,'faq_items':faq_items,'selected_plans':selected_plans,'newplan':newplan,'newplan1':newplan1,'newplan2':newplan2,'newplan3':newplan3,'plans_list': plans_list, 'features_list': features_list, 'features_list1':features_list1,'features_list2':features_list2,'features_list3':features_list3, "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID}
    return render(request, "plan4.html", context=context)

def planexpire_payment1(request):

    url = "https://api.cashfree.com/pg/orders"

    headers = {
            "X-Client-Id": "65027036b36cd7d08b4c5d7b33072056",
            "X-Client-Secret": "cfsk_ma_prod_e9af870c9a9b8b0880ec4ed0617d7b98_2651c73f",
            "x-api-version": "2023-08-01",
        }
    order_id = uuid.uuid4().hex
    request.session['order_idpex1']=order_id
    customer_id = uuid.uuid4().hex
    email1=request.session.get('email_2')
    data = Companys.objects.filter(email=email1).first()
    email=data.email
    Mobile=data.phone_number
    username=data.organizationname
    if data:
       data1 = data.plantype
       newplan = typeofplans.objects.filter(id=data1).first()
    else:
         messages.error(request, "You Don't have Acces to do Payment Operations")
         return HttpResponseRedirect("/planexpireauthentication1/")

    selected_plans = []
    selected_amounts = []

    if request.method == "POST":
        planamount=request.POST.get('planamount')
        amount = planamount
        planType=request.POST.get('planType')
        payload = {
            "order_id": order_id,
            "order_amount": amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": customer_id,
                "customer_name": username,
                "customer_email": email,
                "customer_phone": Mobile,
            },
             "order_meta":{
                "return_url":"https://buglegal.com/planupdate1/?order_id=order_id"

            }
        }

        request.session['form_data1'] = {'planamount': planamount, 'planType':planType,'addon':1,'order_id':order_id}
        response = requests.post(url=url, headers=headers, json=payload)
        payment_ses=response.json()
        return render(request,"loader2.html",{'response':response,'payment_ses':payment_ses})
    return render(request, "planexpire_payment1.html", {'data': data, 'newplan': newplan, 'selected_plans': selected_plans})




def planupdate1(request):
    email1=request.session.get('email_2')
    data = Companys.objects.filter(email=email1).first()
    data1=data.id
    form_data1 = request.session.get('form_data1')
    if form_data1:
        order_id=form_data1['order_id']
        url = f"https://api.cashfree.com/pg/orders/{order_id}"

        headers = {
            "X-Client-Id": "65027036b36cd7d08b4c5d7b33072056",
            "X-Client-Secret": "cfsk_ma_prod_e9af870c9a9b8b0880ec4ed0617d7b98_2651c73f",
            "x-api-version": "2023-08-01",
            "x-request-id":"4dfb9780-46fe-11ee-be56-0242ac120002",
            "x-idempotency-key":"47bf8872-46fe-11ee-be56-0242ac120002"
        }
        response = requests.post(url=url, headers=headers)
        payment_ses=response.json()
        order_status = payment_ses.get('order_status')
        if order_status == "PAID":
            date=datetime.now()
            compid=Companys.objects.get(id=data1)
            compid.date=date
            compid.freetraile=2
            compid.save()
            del request.session['form_data1']
            return render(request, "payment_success.html")
        else:
            return render(request, "payment_fail.html")

    else:
        messages.error(request, "Form data not found.")
        return redirect('/')         
def planexpireauthentication1(request):
    if request.method == "POST":
        user=authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user is not None:
            request.session['email_2']=user.email;
            request.session['password']=user.password
            if user:
                return HttpResponseRedirect('/planexpire_payment1/')
            else:
                return HttpResponse("you Don't have any active Plan")
        else:
            messages.error(request,"Invalid Username or Password")
    return render(request,"addonauthentication.html")   



def upload_image(request):
    if request.method=="POST":
        image=request.FILES.get('image')
        ading=adminphoto.objects.first()
        if ading:
            ading.image=image
            ading.save()
        else:
            pho=adminphoto(image=image)
            pho.save()
        messages.success(request,"your Profile Pic is saved successfully")  
        return redirect("/admin_profile3")
    return render(request,"admin-template/upload_image.html")


def plandatas(request):
    if request.method == "POST":
        type1=request.POST['type1']
        type2=request.POST['type2']
        type3=request.POST['type3']
        type4=request.POST['type4']

        k=plandata(type1=type1,type2=type2,type3=type3,type4=type4)
        k.save()
    return render(request,"plandata.html")

from django.http import HttpResponse


        
from django.shortcuts import redirect
from django.http import JsonResponse

from django.http import JsonResponse
from .models import Companys

def plandataupdate(request, pk):
    plan = get_object_or_404(plandata, pk=pk)

    if request.method == "POST":
        plan.type1 = request.POST["type1"]
        plan.type2 = request.POST["type2"]
        plan.type3 = request.POST["type3"]
        plan.type4 = request.POST["type4"]
        plan.save()
        return redirect("/plandataretrive")

    return render(request, "plandataupdate.html", {"plan": plan})   
 
def plandataretrive(request):
    plans = plandata.objects.all()
    return render(request, "plandataretrive.html", {"plans": plans})


def plandatadelete(request, pk):
    plan = get_object_or_404(plandata, pk=pk)    
    if request.method == "POST":
        plan.delete()
        return redirect("plandataretrive")
    return render(request, "plandatadelete.html", {"plan": plan})


 

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render
from .models import service

def send_msg(number, message, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    api = "NRvfwbSioQCdmu4B18zHDX9rTaF7xpjVkJ2YgUc3tsALKEZnqMgOSwY0HuKL1GVcAzXNIDW6Qq3Jfedt"
    querystring = {"authorization": api, "sender_id": "TEERDHA", "message": message, "language": "english", "route": "otp", "numbers": number, "variables_values": otp, "flash": "0"}
    headers = {'cache-control': "no-cache"}
    return requests.get(url, headers=headers, params=querystring)

def store_phone_number1(request):
    if request.method == 'POST':
        contactno = request.POST.get('contactno')
        request.session['contactno'] = contactno
        response_data = {'success': True}
        return JsonResponse(response_data)

def send_otp1(request):
    if request.method == 'POST':
        contactno = request.session.get('contactno')

        if contactno:
            otp = random.randint(1000, 9999)
            request.session['generated_otp'] = otp

            response = send_msg(contactno, "Your OTP is: {}".format(otp), otp)

            if response.status_code == 200:
                response_data = {'success': True}
            else:
                response_data = {'success': False, 'error': 'Failed to send OTP via SMS.'}
        else:
            response_data = {'success': False, 'error': 'Phone number not found in session.'}

        return JsonResponse(response_data)

    return HttpResponseNotAllowed(['POST'])

def resend_otp1(request):
    if request.method == 'POST':
        contactno = request.session.get('contactno')

        if contactno:
            otp = random.randint(1000, 9999)
            request.session['generated_otp'] = otp

            response = send_msg(contactno, "Your OTP is: {}".format(otp), otp)

            if response.status_code == 200:
                response_data = {'success': True}
            else:
                response_data = {'success': False, 'error': 'Failed to send OTP via SMS.'}
        else:
            response_data = {'success': False, 'error': 'Phone number not found in session.'}

        return JsonResponse(response_data)

    return HttpResponseNotAllowed(['POST'])

def verify_otp1(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('generated_otp', '')

        if user_entered_otp == str(generated_otp):
            response_data = {'message': 'OTP is valid.'}
        else:
            response_data = {'message': 'Invalid OTP. Please try again.'}

        return JsonResponse(response_data)


def solution1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        date = request.POST.get('date')
        companyname = request.POST.get('companyname')
        business = request.POST.get('business')
        description = request.POST.get('description')
        user_entered_otp = request.POST.get("otp")
        generated_otp = request.session.get('generated_otp', '')

        if user_entered_otp == str(generated_otp):
            service_instance=service.objects.create(
                name=name,
                companyname=companyname,
                email=email,
                date=date,
                business=business,
                contactno=contactno,
                description=description,
                otp=user_entered_otp,
                )
            message = render_to_string("solutionform.html")
            subject = 'Registration Successful'
            subjects = 'Requests For Demo Videos'
            from_email = 'fayaz.mohammed@developtrees.com'
            to_email = 'developtrees28@gmail.com'
            recipient_list = [email]
            plan_list = [business]
            send_mail(subject, message, from_email, recipient_list, html_message=message)
            messages.success(request, "Successfully registered ")
            del request.session['generated_otp']
            recipient_str = ', '.join(recipient_list)
            plan_str = ','.join(plan_list)
            additional_message = f"Customer's Request For The Video : {recipient_str} , plan type : {plan_str} "           
            send_mail(subjects, additional_message, from_email, [to_email])
           
            receiveruser=CustomUser.objects.filter(is_superuser=1).first()
            notify.send(sender=service_instance, recipient=receiveruser, verb='Demo',description=f"{companyname} has registered for the {business}."
            )
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
        return render(request, "reqdmo.html")

    return render(request, "reqdmo.html")
# def solution5(request):
#     post = service.objects.all()
#     items_per_page=10
#     paginator=Paginator(post,items_per_page)
#     page=request.GET.get('page')
#     try:
#         post=paginator.page(page)
#     except PageNotAnInteger:
#         post=paginator.page(1)
#     except EmptyPage:
#         post=paginator.page(paginator.num_pages)
#     return render(request,"solution5.html",{'post':post})

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import service

def solution5(request):
    post = service.objects.all().order_by('-date')
    items_per_page = 10
    paginator = Paginator(post, items_per_page)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    
    return render(request, "solution5.html", {'post': post})


def delete_customer_data(request,id):
    delet=get_object_or_404(service,id=id)
    delet.delete()
    messages.success(request,"Your Data was delete successfully")
    return redirect("/solution5")
def privacy_policy2(request):
     if request.method=="GET":
        sk=privacy_policy.objects.all()
        return render (request,"privacy_policy.html",{'sk':sk})



def terms_conditions2(request):
    
    return render(request,'terms.html')



def Cancellation_policy(request):
    rs=cancellation_policy1.objects.all()
    return render(request,'Cancellation_Policy.html',{'rs':rs})
def terms_conditions1(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        k4=terms_conditions(title=title,description=description)
        k4.save()
        return redirect('/retrive_conditions')

    return render(request,"conditions.html")

def retrive_conditions(request):
        if request.method=="GET":
            k6=terms_conditions.objects.all()
        return render(request,"retrieve_condition.html",{'k6':k6})


def edit_terms_condition(request,id):
  k6=terms_conditions.objects.get(id=id);
  return render(request,"condition_edit.html",{'k6':k6})

def update_terms_condition(request,id):
  if(request.method=="POST"):
    title=request.POST.get('title')
    description=request.POST.get('description')

    k6=terms_conditions.objects.get(id=id);
    k6.title=title;
    k6.description=description;
    
    k6.save();
    return redirect("/retrive_conditions")
  return render(request,"condition_edit.html",{'k6':k6})


def delete_condition(request, id):
    data = get_object_or_404(terms_conditions, id=id)
    if request.method == "POST":
        data.delete()
        return redirect('retrive_conditions')
    return render(request, 'delete_condition_delete.html', {'data': data})

def cancellation_policy_insert(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        k4=cancellation_policy1(title=title,description=description)
        k4.save()
        return redirect('/cancellation_policy_table')

    return render(request,"cancellation_policy_insert.html")

def cancellation_policy_table(request):
        if request.method=="GET":
            k5=cancellation_policy1.objects.all()
        return render(request,"cancellation_policy_table.html",{'k5':k5})


def cancellation_policy_edit(request,id):
    k5=cancellation_policy1.objects.get(id=id);
    return render(request,"cancellation_policy_update.html",{'k5':k5})

def cancellation_policy_update(request,id):
    if(request.method=="POST"):
        description=request.POST.get('description')
        title=request.POST.get('title')
    
        k5=cancellation_policy1.objects.get(id=id);
        k5.title=title;
        k5.description=description;
        
        k5.save();
        return redirect('/cancellation_policy_table')

    return render(request, 'cancellation_policy_update.html',{'k5':k5})


def delete_policy_cancellation(request,id):
    data = get_object_or_404(cancellation_policy1,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('cancellation_policy_table')
    return render(request, 'cancellation_policy_delete.html', {'data': data})


def privacy_policy1(request):
     if request.method=="GET":
        sk=privacy_policy.objects.all()
        return render (request,"privacy_policy1.html",{'sk':sk})

def privacy_policy2(request):
     if request.method=="GET":
        sk=privacy_policy.objects.all()
        return render (request,"privacy_policy.html",{'sk':sk})


def privacy_policy_insert(request):
    if request.method=="POST":
        subtitle=request.POST['subtitle']
        title=request.POST['title']
        content=request.POST ['content']
        point1=request.POST['point1']
        point2=request.POST['point2']
        point3=request.POST['point3']
        point4=request.POST['point4']
        content1=request.POST['content1']

        k=privacy_policy( subtitle= subtitle,title=title,content=content,point1=point1,point2=point2,point3=point3,point4=point4,content1=content1)
        k.save()
        return redirect("/privacy_policy_table")
    return render(request,"privacy_policy_insert.html")
def privacy_policy_edit(request,id):
    k=privacy_policy.objects.get(id=id);
    return render(request,"privacy_policy_update.html",{'k':k})

def privacy_policy_update(request,id):
    if(request.method=="POST"):
        subtitle=request.POST.get('subtitle')
        title=request.POST.get('title')
        content=request.POST.get('content')
        point1=request.POST.get('point1')
        point2=request.POST.get('point2')
        point3=request.POST.get('point3')
        point4=request.POST.get('point4')
        content1=request.POST.get('content1')
    
        k=privacy_policy.objects.get(id=id);
        k.subtitle=subtitle;
        k.title=title;
        k.content=content;


        k.point1=point1;
        
        k.point2=point2;
        k.point3=point3;
        
        k.point4=point4;
        k.content1=content1;
        
        
        k.save();
        return redirect('/privacy_policy_table')

    return render(request, 'privacy_policy_update.html',{'k':k})


    

def privacy_policy_delete(request,id):
    k = get_object_or_404(privacy_policy,id=id)
    
    if request.method == 'POST':
        k.delete()
        return redirect('privacy_policy_table')

    return render(request, 'privacy_policy_delete.html', {'k': k})


def privacy_policy_table(request):
     if request.method=="GET":
        sk=privacy_policy.objects.all()
        return render (request,"policytable.html",{'sk':sk})
     
def team(request):
    if(request.method=="POST"):
        name=request.POST['name'];
        role=request.POST['role'];
        image=request.FILES.get('image');
        description=request.POST['description']
        k=ourteam1(name=name,role=role,image=image,description=description);
        k.save();
    return render(request,'team.html')
def team2(request):
    if(request.method=="POST"):
        name1=request.POST['name1'];
        k1=team1(name1=name1);
        k1.save();
    return render(request,'team2.html')


# def team3(request):
#     b=ourteam1.objects.all();
#     v=team1.objects.all();
#     return render(request,'team1.html',{'b':b,'v':v})
     
def Our_Team(request):
    b1=ourteam1.objects.all()[1:7];
    b2=ourteam1.objects.all()[7:]
    b3=ourteam1.objects.all()[0:1]
    return render(request,'team1.html',{'b1':b1,'b2':b2,'b3':b3})


# screenshot_app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Screenshots
import os
from datetime import datetime
from .models import Monitoring, MonitoringDetails




@csrf_exempt
def capture_screenshot(request):
    if request.method == 'POST':
        try:
            screenshot_file = request.FILES['file']
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            employee_id = request.POST.get('employee_id')
            company_id = request.POST.get('company_id')

            # Get employee and company information
            employee = Employs.objects.get(id=employee_id)
            company = Companys.objects.get(id=company_id)

            # Create directories if they don't exist
            company_directory = os.path.join("media", "screenshots", company.organizationname)
            employee_directory = os.path.join(company_directory, f"{employee.first_name}_{employee.last_name}({employee.empid})")
            date_directory = os.path.join(employee_directory, datetime.now().strftime("%d-%m-%Y"))

            os.makedirs(date_directory, exist_ok=True)

            filename = f"screenshot_{timestamp}.png"
            screenshot = Screenshots(image=os.path.join("screenshots", company.organizationname, f"{employee.first_name}_{employee.last_name}({employee.empid})", datetime.now().strftime("%d-%m-%Y"), filename),
                                     employee_id=employee_id, company_id=company_id)
            screenshot.save()

            save_path = os.path.join(date_directory, filename)

            with open(save_path, 'wb') as f:
                for chunk in screenshot_file.chunks():
                    f.write(chunk)

            return JsonResponse({'message': 'Screenshot received successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})




@csrf_exempt
def record_activity(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        company_id = request.POST.get('company_id')
        active_window_name = request.POST.get('active_window_name')
        total_duration = request.POST.get('total_duration')

        # Assuming Monitoring model has fields: employee_id, company_id, m_title, m_start_time, m_end_time, m_total_duration, m_log_ts
        monitoring_entry = Monitoring(
            employee_id=employee_id,
            company_id=company_id,
            m_title=active_window_name,
            m_start_time=datetime.now(),
            m_end_time=datetime.now(),  # You may want to update this field later when the monitoring stops
            m_total_duration=total_duration,  # You may want to update this field later when the monitoring stops
            m_log_ts=timezone.now(),
        )
        monitoring_entry.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def stop_monitoring(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        company_id = request.POST.get('company_id')
        w = request.POST.get('w')
        t = request.POST.get('t')
        # Assuming MonitoringDetails model has fields: md_title, md_total_time_seconds, md_date, employee_id, company_id
        
        monitoring_details_entry = MonitoringDetails(
            md_title=w,
            md_total_time_seconds=t,
            md_date=datetime.now(),
            employee_id=employee_id,
            company_id=company_id,
        )
        monitoring_details_entry.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def record_system_status(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        company_id = request.POST.get('company_id')
        status_type = request.POST.get('status_type')
        status_message = request.POST.get('status_message')
        timestamp = request.POST.get('timestamp')

        # Assuming SystemStatus model has fields: employee, company, status_type, status_message, timestamp
        system_status_entry = SystemStatus(
            employee_id=employee_id,
            company_id=company_id,
            status_type=status_type,
            status_message=status_message,
            timestamp=timestamp,
        )
        system_status_entry.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
from .models import payroll,payroll1,payroll2

def all_payroll(request):
    pay1 = payroll1.objects.all()
    pay2 = payroll2.objects.all()
    pay = payroll.objects.all()
    return render(request, 'all_payroll.html', {'pay1': pay1, 'pay2': pay2, 'pay': pay})





def Payroll_Feature(request):
    k=payroll1.objects.all()
    d=payroll.objects.all()
    k2=payroll2.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return render(request,"payroll.html",{'d':d,'k':k,'k2':k2,'links':links,'services':services,'contact_info':contact_info,'social':social})



def payroll_form(request):
    if request.method=="POST":
        description1=request.POST.get('description1')
        image1=request.FILES.get('image1')
        title1=request.POST.get('title1')

        payroll.objects.create(
            description1=description1,
            image1=image1,
            title1=title1,

        )
        return redirect('all_payroll')
       

    return render(request,"payrollinsert.html")

def payroll_form1(request):
    if request.method=="POST":
        image1=request.FILES.get('image1')
       
        payroll1.objects.create(
            image1=image1,
           

        )
        return redirect('all_payroll')
       
 
    return render(request,"payrollform1.html")

def payroll_form2(request):
    if request.method=="POST":
        description2=request.POST.get('description2')
        title2=request.POST.get('title2')

        payroll2.objects.create(
            description2=description2,
            title2=title2,

        )
        return redirect('all_payroll')
        

    return render(request,"payrollform2.html")

def edit_payroll1(request, pk):
    data = get_object_or_404(payroll1, pk=pk)
    if request.method == "POST":
        
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        
        data.save()
        return redirect('all_payroll')
      
    return render(request, 'edit_payrollform1', {'data': data})


def delete_payroll1(request, pk):
    data = get_object_or_404(payroll1, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_payroll')
        
    return render(request, 'delete_payrollform1.html', {'data': data})

def display_payroll1(request):
    pay1 = payroll1.objects.all()
    return render(request, 'display_payrollform1.html', {'pay1': pay1})

def edit_payroll2(request, pk):
    data = get_object_or_404(payroll2, pk=pk)
    if request.method == "POST":
        data.title2 = request.POST['title2']
        data.description2 = request.POST['description2']
        data.save()
        return redirect('all_payroll')
      
    return render(request, 'edit_payrollform2.html', {'data': data})


def delete_payroll2(request, pk):
    data = get_object_or_404(payroll2, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_payroll')
      
    return render(request, 'delete_payrollform2.html', {'data': data})


def display_payroll2(request):
    pay2 = payroll2.objects.all()
    return render(request, 'display_payroll2.html', {'pay2': pay2})


def edit_payroll(request, pk):
    data = get_object_or_404(payroll, pk=pk)
    if request.method == "POST":
        data.title1 = request.POST['title1']
        data.description1 = request.POST['description1']
       
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        data.save()
        return redirect('all_payroll')
        
    return render(request, 'edit_payrollform.html', {'data': data})


def delete_payroll(request, pk):
    data = get_object_or_404(payroll, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_payroll')
        
    return render(request, 'delete_payrollform.html', {'data': data})


def display_payroll(request):
    pay = payroll.objects.all()
    return render(request, 'display_payrollform.html', {'pay': pay})

def insert_term(request):
    if request.method == 'POST':
        terms = request.POST.get('terms')
        title = request.POST.get('title')
        content= request.POST.get('content')
        tid = request.POST.get('tid')
        md=termsandconditions1(terms=terms,title=title,content=content,tid=tid)
        md.save()
        return redirect("/terms_display")
    return render(request,"privacy_insert.html")

def edit_term(request,tid):
    mn=termsandconditions1.objects.filter(tid=tid)
    return render(request,"display_privacy.html",{'mn':mn})

def terms_display(request):
    md=termsandconditions1.objects.all()
    return render(request,"privacy_curd.html",{'md':md})

def edit_term1(request,id):
    mn=termsandconditions1.objects.get(id=id)
    return render(request,"privacy_update.html",{'mn':mn})

def update_term(request,id):
    if request.method == 'POST':
        terms = request.POST.get('terms')
        title = request.POST.get('title')
        content= request.POST.get('content')
        tid = request.POST.get('tid')
        md=termsandconditions1.objects.get(id=id)
        md.terms=terms
        md.title=title
        md.content=content
        md.tid=tid
        md.save()
        return redirect("/terms_display")
    return render(request,"privacy_update.html")
def delete_terms(request,id):
    mn=termsandconditions1.objects.get(id=id)
    mn.delete()
    return redirect("/terms_display")
    

from .models import hr_management, peopleandemploy, monitorlog,hr_benefits       
def hr_management_form1(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')



        hr_management.objects.create(
            title=title,
            description=description,
            image1=image1,
            image2=image2,

        )
        return redirect('all_HR_Management')
       

    return render(request,"hrmanagementform1.html")


def hr_management_form3(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        image=request.FILES.get('image')

        peopleandemploy.objects.create(
            title=title,
            description=description,
            image=image,

        )
        return redirect('all_HR_Management')
        
       

    return render(request,"hrmanagementform3.html")

def hr_management_form4(request):
    if request.method=="POST":
        title=request.POST.get('title')
        point1=request.POST.get('point1')
        point2=request.POST.get('point2')
        point3=request.POST.get('point3')
        description1=request.POST.get('description1')
        description2=request.POST.get('description2')
        description3=request.POST.get('description3')
        image=request.FILES.get('image')

        monitorlog.objects.create(
            title=title,
            point1=point1,
            point2=point2,
            point3=point3,
            description1=description1,
            description2=description2,

            description3=description3,
            image=image,

        )
        return redirect('all_HR_Management')

    return render(request,"hrmanagementform4.html")

def hr_management_form2(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')

        hr_benefits.objects.create(
            title=title,
            description=description,

        )
        return redirect('all_HR_Management')
       

    return render(request,"hrmanagementform2.html")

def HR_Management(request):
    management=hr_management.objects.all()
    # reports=hr_report.objects.all()
    people=peopleandemploy.objects.all()
    monitor=monitorlog.objects.all()
    benefit=hr_benefits.objects.all()[:3]
    benefit1=hr_benefits.objects.all()[3:]

    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return render(request,"hrmanagement.html",{'management':management,'people':people,'monitor':monitor, 'benefit':benefit,'benefit1':benefit1, 'links':links,'services':services,'contact_info':contact_info,'social':social})

def edit_HR_Management1(request, pk):
    data = get_object_or_404(hr_management, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.description = request.POST['description']
       
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            data.image2 = request.FILES['image2']
        data.save()
        return redirect('all_HR_Management')
       
    return render(request, 'edit_hrm1.html', {'data': data})

def edit_HR_Management3(request, pk):
    data = get_object_or_404(peopleandemploy, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.description = request.POST['description']
       
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        
        data.save()
        return redirect('all_HR_Management')
        
    return render(request, 'edit_hrm3.html', {'data': data})

def edit_HR_Management4(request, pk):
    data = get_object_or_404(monitorlog, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.point1 = request.POST['point1']
        data.point2 = request.POST['point2']
        data.point3 = request.POST['point3']
        data.description1 = request.POST['description1']
        data.description2 = request.POST['description2']
        data.description3 = request.POST['description3']

       
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        
        data.save()
        return redirect('all_HR_Management')
       
    return render(request, 'edit_hrm4.html', {'data': data})

def edit_HR_Management2(request, pk):
    data = get_object_or_404(hr_benefits, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.description = request.POST['description']
       
       
        data.save()
        return redirect('all_HR_Management')
        
    return render(request, 'edit_hrm2.html', {'data': data})

def delete_HR_Management1(request, pk):
    data = get_object_or_404(hr_management, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_HR_Management')
        
    return render(request, 'delete_hrm1.html', {'data': data})

def delete_HR_Management2(request, pk):
    data = get_object_or_404(hr_benefits, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_HR_Management')
      
    return render(request, 'delete_hrm2.html', {'data': data})

def delete_HR_Management3(request, pk):
    data = get_object_or_404(peopleandemploy, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_HR_Management')
      
    return render(request, 'delete_hrm3.html', {'data': data})

def delete_HR_Management4(request, pk):
    data = get_object_or_404(monitorlog, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_HR_Management')
       
    return render(request, 'delete_hrm4.html', {'data': data})

def display_HR_Management1(request):
    management = hr_management.objects.all()
    return render(request, 'display_hrm1.html', {'management': management})

def display_HR_Management2(request):
    bene = hr_benefits.objects.all()
    return render(request, 'display_hrm2.html', {'bene': bene})

def display_HR_Management3(request):
    peoples = peopleandemploy.objects.all()
    return render(request, 'display_hrm3.html', {'peoples': peoples})

def display_HR_Management4(request):
    moni = monitorlog.objects.all()
    return render(request, 'display_hrm4.html', {'moni': moni})

def all_HR_Management(request):
    management = hr_management.objects.all()
    benefit = hr_benefits.objects.all()
    people = peopleandemploy.objects.all()
    monitoring = monitorlog.objects.all()

    return render(request, 'all_hr_management.html', {'management': management, 'benefit': benefit, 'people': people,'monitoring':monitoring})


from django.shortcuts import render,redirect
from .models import teamlead,teamlead1
from django.http import HttpResponse
# Create your views here.
def reg_tl_management(request):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        content2=request.POST['content2']
        image1=request.FILES.get('image1')
        k=teamlead(title1=title1,content1=content1,content2=content2,image1=image1)
        k.save()
        return redirect('table_tl_management')
    return render(request,"reg.html")
        
        
    
def Team_lead_Management(request):
    
    k=teamlead.objects.all()
    k1=teamlead1.objects.all()
    return render(request,"a1.html",{'k':k,'k1':k1})
    
def table_tl_management(request):
    
    k=teamlead.objects.all()
    k1=teamlead1.objects.all()
    return render(request,"table.html",{'k':k,'k1':k1})


def edit_tl_management(request,id):
    k1=teamlead.objects.get(id=id)
    return render(request,"up.html",{'k1':k1})
def update_tl_management(request,id):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        content2=request.POST['content2']
        image1=request.FILES.get('image1')
        k=teamlead.objects.get(id=id)
        k.title1=title1
        k.content1=content1
        k.content2=content2
        k.image1=image1
        k.save()
        return redirect('table_tl_management')
        
    return render(request,"up.html")
def delete_tl_management(request,id):
    data = get_object_or_404(teamlead,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('table_tl_management')
        
    return render(request,'teamlead_delete.html', {'data': data})

def teamlead_form1(request):
    if request.method=="POST":
        image2=request.FILES.get('image2')
        k=teamlead1(image2=image2)
        k.save()
        return redirect('table_tl_management')
    return render(request,"teamlead_form1.html")
def teamlead_edit1(request,id):
    k1=teamlead1.objects.get(id=id)
    return render(request,"teamlead_update1.html",{'k1':k1})
def teamlead_update1(request,id):
    if request.method=="POST":
        image2=request.FILES.get('image2')
        k=teamlead1.objects.get(id=id)
        k.image2=image2
        k.save()
        return redirect('table_tl_management')
    return render(request,"teamlead_update1.html")
def teamlead_delete1(request,id):
    data = get_object_or_404(teamlead1,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('table_tl_management')
    return render(request,'teamlead_delete1.html', {'data': data})




from django.shortcuts import render,redirect
from .models import empperformance,empperformance1
from django.http import HttpResponse
# Create your views here.
def reg_employee_performance(request):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        k=empperformance(title1=title1,content1=content1,image1=image1)
        k.save()
        return redirect('table_employee_performance')
        
    return render(request,"reg1.html")
def Employee_Performance(request):
    
    k=empperformance.objects.all()
    k1=empperformance1.objects.all()
    return render(request,"a2.html",{'k':k,'k1':k1})
def table_employee_performance(request):
    
    k=empperformance.objects.all()
    k1=empperformance1.objects.all()
    return render(request,"table1.html",{'k':k,'k1':k1})

def edit_employee_performance(request,id):
    
    k1=empperformance.objects.get(id=id)
    return render(request,"up1.html",{'k1':k1})
def update_employee_performance(request,id):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        k=empperformance.objects.get(id=id)
        k.title1=title1
        k.content1=content1
        k.image1=image1
        k.save()
        return redirect('table_employee_performance')
        
    return render(request,"up1.html")
def delete_employee_performance(request,id):
    data = get_object_or_404(empperformance,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('table_employee_performance')
    
    return render(request, 'empperformnace_delete.html', {'data': data})

def empperformance_form1(request):
    if request.method=="POST":
        image2=request.FILES.get('image2')
        k=empperformance1(image2=image2)
        k.save()
        return redirect('table_employee_performance')
    return render(request,"empperformance_form1.html")


def empperformance_edit1(request,id):
    k1=empperformance1.objects.get(id=id)
    return render(request,"empperformance_update1.html",{'k1':k1})
def empperformance_update1(request,id):
    if request.method=="POST":
        image2=request.FILES.get('image2')
        k=empperformance1.objects.get(id=id)
        k.image2=image2
        k.save()
        return redirect('table_employee_performance')
    return render(request,"empperformance_update1.html")
def empperformance_delete1(request,id):
    data = get_object_or_404(empperformance1,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('table_employee_performance')
    return render(request, 'empperformance_delete1.html', {'data': data})

from django.shortcuts import render,redirect
from .models import leavemanagement,leavemanagement1
from django.http import HttpResponse
# Create your views here.
def reg_leave_management(request):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        k=leavemanagement(title1=title1,content1=content1,image1=image1)
        k.save()
        return render('table_leave_management')
    return render(request,"reg2.html")
def home_leave_management(request):
    
    k=leavemanagement.objects.all()
    k1=leavemanagement1.objects.all()
    return render(request,"a3.html",{'k':k,'k1':k1})
def table_leave_management(request):
    
    k=leavemanagement.objects.all()
    k1=leavemanagement1.objects.all()
    return render(request,"table2.html",{'k':k,'k1':k1})

def edit_leave_management(request,id):
    k1=leavemanagement.objects.get(id=id)
    return render(request,"up2.html",{'k1':k1})
def update_leave_management(request,id):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        k=leavemanagement.objects.get(id=id)
        k.title1=title1
        k.content1=content1
        k.image1=image1
        k.save()
        return render('table_leave_management')     
        
    return render(request,"up2.html")
def delete_leave_management(request,id):
    data = get_object_or_404(leavemanagement,id=id)
    if request.method == "POST":
        data.delete()
        return render('table_leave_management')
       
    return render(request, 'leavemanagement_delete.html', {'data': data})



def leavemanagement_form1(request):
    if request.method=="POST":
        image2=request.FILES.get('image2')
        k=leavemanagement1(image2=image2)
        k.save()
        return redirect('table_leave_management')
    return render(request,"leavemanagement_form1.html")


def leavemanagement_edit1(request,id):
    k1=leavemanagement1.objects.get(id=id)
    return render(request,"leavemanagement_update1.html",{'k1':k1})
def leavemanagement_update1(request,id):
    if request.method=="POST":
        image2=request.FILES.get('image2')
        k=leavemanagement1.objects.get(id=id)
        k.image2=image2
        k.save()
        return redirect("table_leave_management")
    return render(request,"leavemanagement_update1.html")
def leavemanagement_delete1(request,id):
    data = get_object_or_404(leavemanagement1,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('table_leave_management')
    return render(request, 'leavemanagement_delete1.html', {'data': data})



def face_insert(request):
    if request.method=="POST":
        description1=request.POST['description1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        description2=request.POST['description2']
        content2=request.POST['content2']
        image2=request.FILES.get('image2')
        description3=request.POST['description3']
        content3=request.POST['content3']
        image3=request.FILES.get('image3')
        description4=request.POST['description4']
        content4=request.POST['content4']
        image4=request.FILES.get('image4')
        description5=request.POST['description5']
        content5=request.POST['content5']
        image5=request.FILES.get('image5')
        fa=face(description1=description1,content1=content1,image1=image1,description2=description2,content2=content2,image2=image2,description3=description3,content3=content3,image3=image3,description4=description4,content4=content4,image4=image4,description5=description5,content5=content5,image5=image5)
        fa.save()
        return redirect('facereading')
        
    return render(request,"face_insert.html")



def Face_Recognition(request):
    fa=face.objects.all()
    return render(request,"face_display1.html",{'fa':fa})


def face_edit(request,id):
    fa1=face.objects.get(id=id)
    return render(request,"face_update.html",{'fa1':fa1})

def face_update(request,id):
    if request.method=="POST":
        description1=request.POST['description1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        description2=request.POST['description2']
        content2=request.POST['content2']
        image2=request.FILES.get('image2')
        description3=request.POST['description3']
        content3=request.POST['content3']
        image3=request.FILES.get('image3')
        description4=request.POST['description4']
        content4=request.POST['content4']
        image4=request.FILES.get('image4')
        description5=request.POST['description5']
        content5=request.POST['content5']
        image5=request.FILES.get('image5')
        fa=face.objects.get(id=id)
        fa.description1=description1
        fa.content1=content1
        fa.image1=image1
        fa.description2=description2
        fa.content2=content2
        fa.image2=image2
        fa.description3=description3
        fa.content3=content3
        fa.image3=image3
        fa.description4=description4
        fa.content4=content4
        fa.image4=image4
        fa.description5=description5
        fa.content5=content5
        fa.image5=image5
        fa.save()
        return redirect('facereading')
        
    return render(request,"face_update.html")

def face_delete(request,id):
    data = get_object_or_404(leavemanagement1,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('facereading')
        
    return render(request, 'face_delete.html', {'data': data})

       

def facereading(request):
    obj=face.objects.all()
    return render(request,"face.html",{'obj':obj})


def shift_management_form1(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        image1=request.FILES.get('image1')


        shift1.objects.create(
            title=title,
            description=description,
            image=image,
            image1=image1

        )
        return redirect('/all_Shift_Management')

    return render(request,"shift_manage_form1.html")

def shift_management_form2(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
       
        shifcards.objects.create(
            title=title,
            description=description,
           

        )
        return redirect('/all_Shift_Management')

    return render(request,"shift_management.html")

def shift_management_form3(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        image=request.FILES.get('image')


        shift2.objects.create(
            title=title,
            description=description,
            image=image,

        )
        return redirect('/all_Shift_Management')

    return render(request,"shift_manage_form3.html")

def Shift_Management(request):
    shi1=shift1.objects.all()
    shi2=shifcards.objects.all()
    shi3=shift2.objects.all()
   
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return render(request,"shift_manage.html",{'shi1':shi1,'shi2':shi2,'shi3':shi3, 'links':links,'services':services,'contact_info':contact_info,'social':social})

def edit_shift_Management1(request, pk):
    data = get_object_or_404(shift1, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.description = request.POST['description']
       
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        if 'image1' in request.FILES:
            data.image1 = request.FILES['image1']
        data.save()
        return redirect('all_Shift_Management')
    return render(request, 'edit_shift1.html', {'data': data})

def edit_shift_Management2(request, pk):
    data = get_object_or_404(shifcards, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.description = request.POST['description']
       
       
        data.save()
        return redirect('all_Shift_Management')
    return render(request, 'edit_shift2.html', {'data': data})

def edit_shift_Management3(request, pk):
    data = get_object_or_404(shift2, pk=pk)
    if request.method == "POST":
        data.title = request.POST['title']
        data.description = request.POST['description']
       
        if 'image' in request.FILES:
            data.image = request.FILES['image']
      
        data.save()
        return redirect('all_Shift_Management')
    return render(request, 'edit_shift3.html', {'data': data})

def delete_Shift_Management1(request, pk):
    data = get_object_or_404(shift1, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_Shift_Management')
    return render(request, 'delete_shift1.html', {'data': data})

def delete_Shift_Management2(request, pk):
    data = get_object_or_404(shifcards, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_Shift_Management')
    return render(request, 'delete_shift2.html', {'data': data})

def delete_Shift_Management3(request, pk):
    data = get_object_or_404(shift2, pk=pk)
    if request.method == "POST":
        data.delete()
        return redirect('all_Shift_Management')
    return render(request, 'delete_shift3.html', {'data': data})

def display_Shift_Management1(request):
    shiff1 = shift1.objects.all()
    return render(request, 'display_shift1.html', {'shiff1': shiff1})
def display_Shift_Management2(request):
    shiff2 = shifcards.objects.all()
    return render(request, 'display_shift2.html', {'shiff2': shiff2})
def display_Shift_Management3(request):
    shiff3 = shift2.objects.all()
    return render(request, 'display_shift3.html', {'shiff3': shiff3})

def all_Shift_Management(request):
    shif1 = shift1.objects.all()
    shif2 = shifcards.objects.all()
    shif3 = shift2.objects.all()

    return render(request, 'all_Shift_Management.html', {'shif1': shif1, 'shif2': shif2, 'shif3': shif3})



def Terms_and_conditions_insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content= request.POST.get('content')
        md=Terms_and_Conditions1(title=title,content=content)
        md.save()
        return HttpResponse("inserted...")
    return render(request,"Terms_and_conditions_insert.html")

def Privacy_and_Policy_insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content= request.POST.get('content')
        md=Privacy_and_Policy1(title=title,content=content)
        md.save()
        return HttpResponse("inserted...")
    return render(request,"Privacy_and_Policy_insert.html")

def Cancellation_Policy2_insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content= request.POST.get('content')
        md=Cancellation_Policy2(title=title,content=content)
        md.save()
        return HttpResponse("inserted...")
    return render(request,"Cancellation_Policy2_insert.html")

def Terms_and_Conditions(request):
    obj=Terms_and_Conditions1.objects.all()
    return render(request,"Terms_and_Conditions.html",{'obj':obj})


def Privacy_and_Policy(request):
    obj=Privacy_and_Policy1.objects.all()
    return render(request,"Privacy_and_Policy.html",{'obj':obj})

def Cancellation_Policy(request):    
    obj=Cancellation_Policy2.objects.all()
    return render(request,"Cancellation_Policy1.html",{'obj':obj})


def admin_profile3(request):
    k = admin_profile1.objects.all()
    superadminpic = adminphoto.objects.all()
    return render(request, "admin-template/admin_profile1.html", {'k': k, 'superadminpic': superadminpic,
                                                                 'username': request.user.username,
                                                                 'email': request.user.email})

def admin_profile_edit(request, id):
    k5 = admin_profile1.objects.get(id=id)
    return render(request, "admin-template/admin_profile_edit.html", {'k5': k5})

def admin_profile_update(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        contactnumber = request.POST.get('contactnumber')
        dateofbirth = request.POST.get('dateofbirth')
        role = request.POST.get('role')
        designation = request.POST.get('designation')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        status = request.POST.get('status')

        k5 = admin_profile1.objects.get(id=id)
        k5.name = name
        k5.status = status
        k5.dateofbirth = dateofbirth
        k5.contactnumber = contactnumber
        k5.role = role
        k5.designation = designation
        k5.address = address
        k5.gender = gender
        k5.save()
        return redirect('admin_profile3')

    return render(request, 'admin-template/admin_profile_edit.html', {'k5': k5})

def admin_profile_form(request):
    context = {
        'today': timezone.now().date()
    }
    if request.method == 'POST':
        name=request.POST['name']
        contactnumber=request.POST['contactnumber']
        status=request.POST['status']
        role=request.POST['role']
        designation=request.POST['designation']

        dateofbirth=request.POST['dateofbirth']

        address= request.POST['address']
        gender = request.POST['gender']
        k=admin_profile1(name=name,address=address,contactnumber=contactnumber,role=role,designation=designation,dateofbirth=dateofbirth,gender=gender,status=status)
        k.save()
        messages.success(request,"Admin Information was saved successfully")
        return redirect("/adminAdashboard")
    return render(request, "admin-template/admin_profile_form.html", context)



def reg_ourteam(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        name = request.POST['name']
        role = request.POST['role']
        description = request.POST['description']
        o1 = ourteam1(image=image, name=name, role=role, description=description)
        o1.save()
        return redirect("home_ourteam")
    return render(request, "o1.html")

def home_ourteam(request):
    if request.method == "GET":
        o1 = ourteam1.objects.all()
        return render(request, "o2.html", {'o1': o1})

def team_edit(request,id):
    k=ourteam1.objects.get(id=id)
    return render(request,"team4.html",{'k':k})

def team_update(request, id):
    k = get_object_or_404(ourteam1, id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        role = request.POST.get('role')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        
        k.name = name
        k.role = role
        if image:  # Only update the image if a new one is uploaded
            k.image = image
        k.description = description
        k.save()
        return redirect('home_ourteam')
    return render(request, "team4.html", {'k': k})


def team_delete(request,id):
    k = get_object_or_404(ourteam1,id=id)
    
    if request.method == 'POST':
        k.delete()
        return redirect('home_ourteam')

    return render(request, 'aa1.html', {'k': k})
    

from django.shortcuts import render, redirect
from django.contrib.auth import login
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth import get_user_model
from .models import Companys

User = get_user_model()

def company_form_view(request):
    planid=request.session.get("planid")
    username=request.session.get('username')
    email=request.session.get('email')
    backend=request.session.get('backend')
    oldpath=request.session.get('oldpath')
    checkcustum=CustomUser.objects.filter(email=email)
    if request.method == 'POST':
        organizationname=request.POST.get('organizationname')
        phone_number=request.POST.get('phone_number')
        address=request.POST.get('address')
        contact_person = request.POST.get('contact_person')
        password = request.POST.get('password')

        if organizationname and address:
            serialized_sociallogin = request.session.pop('sociallogin', None)
            if serialized_sociallogin:
                sociallogin = SocialLogin.deserialize(serialized_sociallogin)
                user = sociallogin.user
                full_name = sociallogin.account.extra_data.get('name')
                email = sociallogin.account.extra_data.get('email')
                user.username=full_name
                user.save()
                sociallogin.save(request, user)
                company = Companys(usernumber=user,email=email,organizationname=organizationname,address=address,phone_number=phone_number,plantype=planid,password=password,contact_person=contact_person)
                company.save()
                editholidays=editholiday12.objects.create(
                companyid=company,
                sun=1
                )
                halfreason=halfldayvreason.objects.create(
                    companyid=company,
                    halfdaylev=1,
                    reason1=1

                )
                emplenght=employedata.objects.create(
                    companyid=company
                )
                taskdat=task1.objects.create(
                    companyid=company
                )
                payroll1=set_payroll_date.objects.create(
                    companyid=company
                )
                workshift=working_shifts.objects.create(
                    companyid=company,
                    cutoff_time=2,
                    befor_time=10,
                    shift_name="general"
                )
                companydetail=company_details.objects.create(
                    companyid=company
                )
                salarycomponent=['Basic Salary','HRA','LTA']
                percentageofCTC=['50','30','20']
                percentageorfixed=['Percentage','Percentage','Percentage']
            
                salaryid=['1','2','3']
                percentageofCTC1 = [value for value in percentageofCTC if value.strip()]
                percentageofCTC_int = [int(x) for x in percentageofCTC1]
                sum_of_percentageofCTC = sum(percentageofCTC_int)
                if len(salarycomponent) == len(percentageofCTC) == len(salaryid):
                 if sum_of_percentageofCTC == 100:
                    for sal,pectc,pefix,salid in zip(salarycomponent,percentageofCTC,percentageorfixed,salaryid):
                     if sal:
                            preup,persave=salary_struct.objects.get_or_create(salaryid=salid,defaults={'salarycomponent':sal,'percentageofCTC':pectc,'percentageorfixed':pefix},companyid=company)

                registration_link =  "https://rzp.io/i/kvy1M77V2"

                subject = 'Registration Successful'
                context = {'registration_link': registration_link}
                message = render_to_string('sms1_template.html', context)

                from_email = 'developtrees1@gmail.com'  
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list,html_message=message)
                date13 = datetime.now() + timedelta(days=13)
                Thread(target=send_followup_email_after_delay1, args=(email, date13, 'your free trial is expired with in 2 days')).start()  

                date14 = datetime.now() + timedelta(days=14)
                Thread(target=send_followup_email_after_delay2, args=(email, date14, 'your free trial is expired with in 1 days')).start() 

                date15 = datetime.now() + timedelta(days=15)
                Thread(target=send_followup_email_after_delay3, args=(email, date15, 'your free trial is expired today')).start() 

                date16 = datetime.now() + timedelta(days=16)
                Thread(target=send_followup_email_after_delay4, args=(email, date16, 'Your free trial is expired recharge now')).start() 

                date17 = datetime.now() + timedelta(days=17)
                Thread(target=send_followup_email_after_delay5, args=(email, date17,  'your free trial is expired')).start() 

                # Thread(target=send_followup_email_after_delay1, args=(email,180,'your free trial expire soon')).start()  
                # Thread(target=send_followup_email_after_delay2, args=(email, 300,'your free trial expire tommorow')).start() 
                # Thread(target=send_followup_email_after_delay3, args=(email, 360,'your free trial expire today')).start() 
                # Thread(target=send_followup_email_after_delay4, args=(email, 420,'your free trial expired 1day ago')).start() 
                # Thread(target=send_followup_email_after_delay5, args=(email, 480,'your free trial expired 2days ago')).start() 
                scheduler = BackgroundScheduler()
                scheduler.add_job(send_sms_after_15_days, 'date', run_date=datetime.now() + timedelta(days=1), args=[phone_number, message])
                scheduler.start()

                message = f"Registration Successfully"

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')  
        else:
            return render(request, 'company_form.html', {'error': 'All fields are required.'})
    return render(request, 'company_form.html',{'username':username,'checkcustum':checkcustum,'checkcustum':checkcustum,'oldpath':oldpath})

from django.shortcuts import render
from .models import visitorentrance,visitorentrance1,buglegal_qns,IntroContent, Step,help_notificationdata,Trail,managing_data,timeqns,abouttime_data1,abouttime_data2,clock,assignqns3,payrol_qns,payroll_data1,payroll_qns2,payroll_qnsdata3,payroll_qnsdata4,payroll_qnsdata5
from .forms import IntroContentForm, StepForm,TrailForm,InstructionForm,InstructionForm1,InstructionForm2
from django.http import HttpResponse

def reg_visitor_entrance(request):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        k=visitorentrance(title1=title1,content1=content1,image1=image1)
        k.save()
        return HttpResponse("inserted")
    return render(request,"ve1.html")
def main_visitor_entrance1(request):
    if request.method=="POST":
        image2=request.FILES.get('image2')
        k1=visitorentrance1(image2=image2)
        k1.save()
        return HttpResponse("inserted")
    return render(request,"ve5.html")
def home_visitor_entrance(request):
    if request.method=="GET":
        k=visitorentrance.objects.all()
        k1=visitorentrance1.objects.all()
        return render(request,"ve4.html",{'k':k,'k1':k1})
def table_visitor_entrance(request):
    if request.method=="GET":
        k=visitorentrance.objects.all()
        k1=visitorentrance1.objects.all()
        return render(request,"ve2.html",{'k':k,'k1':k1})

def edit_visitor_entrance(request,id):
    if request.method=="GET":
        k1=visitorentrance.objects.get(id=id)
    return render(request,"ve3.html",{'k1':k1})
def update_visitor_entrance(request,id):
    if request.method=="POST":
        title1=request.POST['title1']
        content1=request.POST['content1']
        image1=request.FILES.get('image1')
        k=visitorentrance.objects.get(id=id)
        k.title1=title1
        k.content1=content1
        k.image1=image1
        k.save()
        return redirect("/home_visitor_entrance")
    return render(request,"ve3.html")
def delete_visitor_entrance(request,id):
    if request.method=="GT":
        k1=visitorentrance.objects.get(id=id)
        k1.delete()
        return redirect("/home_visitor_entrance")
from .models import  helptopic,helptopic2

def insertform_help(request):
    if request.method == 'POST':
        icon = request.FILES.get('icon')
        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        
        helpt = helptopic(icon=icon, title=title, description=description, url=url)
        helpt.save()
        
        return redirect('retriev_helpfeature') 
    
    return render(request, 'insert_helpfeature.html')


def retriev_helpfeature(request):
    stt=helptopic.objects.all()
    sdd=helptopic2.objects.all()
    return render(request, 'retriev_helpfeature.html',{'stt':stt,'sdd':sdd})

def editform_help(request, id):
    helpt = get_object_or_404(helptopic, id=id)
    
    if request.method == 'POST':
        icon = request.FILES.get('icon', helpt.icon)
        title = request.POST.get('title', helpt.title)
        description = request.POST.get('description', helpt.description)
        url = request.POST.get('url', helpt.url)
        
        helpt.icon = icon
        helpt.title = title
        helpt.description = description
        helpt.url = url
        helpt.save()
        
        return redirect('retriev_helpfeature') 
    
    return render(request, 'edit_helpfeature.html', {'helpt': helpt})


def insertform_help2(request):
    if request.method == 'POST':
        icon = request.FILES.get('icon')
        title = request.POST.get('title')
        
        help = helptopic2(icon=icon, title=title)
        help.save()
        
        return redirect('retriev_helpfeature') 
    
    return render(request, 'insertform_help2.html')


def buglegal_start1(request):
    card1 = buglegal_qns.objects.filter()
    return render(request, 'buglegal_start1.html', {'card1': card1})


def help_sidebar(request):
    return render(request,"help_sidebar.html")

def insertbuglegal_start1(request):
    if request.method == 'POST':
        qns = request.POST.get('qns', '') 
        title2 = request.POST.get('title2', '')
        discription = request.POST.get('discription', '')  
        link = request.POST.get('link', '')  

    
        new_buglegal_qns = buglegal_qns(qns=qns, title2=title2, discription=discription, link=link)
        new_buglegal_qns.save()

    
        return redirect('buglegal_start1')

    else:
        return render(request, 'insertbuglegal_start1.html')





def edit_buglegalstart1(request, pk):
    ins = get_object_or_404(buglegal_qns, pk=pk)
    
    if request.method == 'POST':
        qns = request.POST.get('qns')
        title2 = request.POST.get('title2')
        discription = request.POST.get('discription')
        link = request.POST.get('link')

        
        ins.qns = qns
        ins.title2 = title2
        ins.discription= discription
        ins.title2 = title2
        ins.link = link


        ins.save()
        
        return redirect('buglegal_start1')  
    
    return render(request, 'edit_buglegal_start1.html', {'ins': ins})



def delete_buglegal_qns(request, pk):
    ins = get_object_or_404(buglegal_qns, pk=pk)
    
    if request.method == 'POST':
        ins.delete()
        return redirect('buglegal_start1')  
    
    return render(request, 'delete_buglegal_qns.html', {'ins': ins})





def create_intro_content(request):
    if request.method == 'POST':
        form = IntroContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_step') 
    else:
        form = IntroContentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'navhelp11insert_form.html', context)

def create_step(request):
    if request.method == 'POST':
        form = StepForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StepForm()
    
    context = {
        'form': form,
    }
    return render(request, 'ress.html', context)




def delete_intro_content(request, id):
    intro_content = get_object_or_404(IntroContent, id=id)
    
    if request.method == 'POST':
        intro_content.delete()
        return redirect('create_intro_content')
    
    context = {
        'intro_content': intro_content,
    }
    return render(request, 'delete_intro_content.html', context)

def delete_step(request, id):
    step = get_object_or_404(Step, id=id)
    
    if request.method == 'POST':
        step.delete()
        return redirect('create_step')
    
    context = {
        'step': step,
    }
    return render(request, 'delete_step.html', context)


    
def edit_intro_content(request, intro_content_id):
    intro_content = get_object_or_404(IntroContent, pk=intro_content_id)
    
    if request.method == 'POST':
        form = IntroContentForm(request.POST, request.FILES, instance=intro_content)
        if form.is_valid():
            form.save()
            return redirect('create_step')
    else:
        form = IntroContentForm(instance=intro_content)
    
    context = {
        'form': form,
    }
    return render(request, 'navhelp11insert_form.html', context)



def edit_step(request, step_id):
    step = get_object_or_404(Step, pk=step_id)
    
    if request.method == 'POST':
        form = StepForm(request.POST, instance=step)
        if form.is_valid():
            form.save()
    else:
        form = StepForm(instance=step)
    
    context = {
        'form': form,
    }
    return render(request, 'ress.html', context)



def retriev_card1(request):
    intro_content = IntroContent.objects.first()  
    steps = Step.objects.filter(intro_content=intro_content)  

    context = {
        'intro_content': intro_content,
        'steps': steps,
    }
    return render(request, 'intro_detail.html', context)

def managingdata_retriev(request):
    qns2 = managing_data.objects.filter()
    return render(request, 'managingdata_retrieve.html', {'qns2': qns2})

def manageqn2_edit(request, id):
    m1 = managing_data.objects.get(id=id)
    
    if request.method == 'POST':
        m1.title1 = request.POST['title1']
        m1.des = request.POST['des']
        m1.subhead1 = request.POST['subhead1']
        m1.des1 = request.POST['des1']
        m1.subhead2 = request.POST['subhead2']
        m1.des2 = request.POST['des2']
        m1.save()
    return render(request, "edit_manage.html", {'m1': m1})


def delete_qns3(request, id):
    m2 = get_object_or_404(managing_data, id=id)
    
    if request.method == 'POST':
        m2.delete()
    
    return render(request, 'delete_manage.html', {'m2': m2})



def retrieve_setupqn3(request):
    q3 = help_notificationdata.objects.all()
    return render(request, 'setupqn3_retrieve.html', {'q3': q3})


def insert_setupqn3(request):
    if request.method == 'POST':
        main_title = request.POST.get('main_title')
        title = request.POST.get('title')
        subhead = request.POST.get('subhead')
        point1 = request.POST.get('point1')
        point2 = request.POST.get('point2')
        des1 = request.POST.get('des1', '')
        des2 = request.POST.get('des2', '')
        point3 = request.POST.get('point3')
        point4 = request.POST.get('point4')
        point5 = request.POST.get('point5')
        point6 = request.POST.get('point6')
        point7 = request.POST.get('point7')

        new_data = help_notificationdata( main_title=main_title,title=title,subhead=subhead,point1=point1,point2=point2,des1=des1,des2=des2,point3=point3,point4=point4,point5=point5,point6=point6,point7=point7)
        new_data.save()

        return redirect('retrieve_setupqn3')

    return render(request, 'insert_setupqn3.html')



def edit_setupqn3(request, id):
    instance = get_object_or_404(help_notificationdata, id=id)

    if request.method == 'POST':
        instance.main_title = request.POST.get('main_title')
        instance.title = request.POST.get('title')
        instance.subhead = request.POST.get('subhead')
        instance.point1 = request.POST.get('point1')
        instance.point2 = request.POST.get('point2')
        instance.des1 = request.POST.get('des1', '')
        instance.des2 = request.POST.get('des2', '')
        instance.point3 = request.POST.get('point3')
        instance.point4 = request.POST.get('point4')
        instance.point5 = request.POST.get('point5')
        instance.point6 = request.POST.get('point6')
        instance.point7 = request.POST.get('point7')
        instance.save()

        return redirect('success_page')

    return render(request, 'edit_setupqn3.html', {'instance': instance})


def delete_setupqn3(request, id):
    m3 = get_object_or_404(help_notificationdata, id=id)
    
    if request.method == 'POST':
        m3.delete()
    
    return render(request, 'delete_setupqn3.html', {'m3': m3})



def add_trail(request):
    if request.method == 'POST':
        form = TrailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('freetrail_retriev')  
    else:
        form = TrailForm()

    return render(request, 'add_trail.html', {'form': form})


def edit_trail(request, trail_id):
    trail = get_object_or_404(Trail, pk=trail_id)
    
    if request.method == 'POST':
        form = TrailForm(request.POST, request.FILES, instance=trail)
        if form.is_valid():
            form.save()
            return redirect('trail_detail', trail_id=trail.id)  
    else:
        form = TrailForm(instance=trail)
    
    return render(request, 'edit_trail.html', {'form': form, 'trail': trail})


def freetrail_retrieve(request):
    trails = Trail.objects.all() 
    
    for trail in trails:
        trail.steps = [step.strip() for step in trail.steps.splitlines() if step.strip()]
    
    return render(request, 'freetrile_retrieve.html', {'trails': trails})

def timetrack_qnsd(request):
    card2 = timeqns.objects.filter()
    return render(request, 'timetrack_qnsd.html', {'card2': card2})


def inserttimetrack_qnsd(request):
    if request.method == 'POST':
        qns = request.POST.get('qns', '') 
        title2 = request.POST.get('title2', '')
        discription = request.POST.get('discription', '')  
        link = request.POST.get('link', '')  

    
        new_timetrack = timeqns(qns=qns, title2=title2, discription=discription, link=link)
        new_timetrack.save()

    
        return redirect('timetrack_qnsd')

    else:
        return render(request, 'inserttimetrack_qnsd.html')


def edittimetrack_qnsd(request, pk):
    ins1 = get_object_or_404(timeqns, pk=pk)
    
    if request.method == 'POST':
        qns = request.POST.get('qns')
        title2 = request.POST.get('title2')
        discription = request.POST.get('discription')
        link = request.POST.get('link')

        
        ins1.qns = qns
        ins1.title2 = title2
        ins1.discription= discription
        ins1.title2 = title2
        ins1.link = link


        ins1.save()
        
        return redirect('timetrack_qnsd')  
    
    return render(request, 'edittimetrack_qnsd.html', {'ins1': ins1})



def deletetimetrack_qnsd(request, pk):
    ins2 = get_object_or_404(timeqns, pk=pk)
    
    if request.method == 'POST':
        ins2.delete()
        return redirect('timetrack_qnsd')  
    
    return render(request, 'deletetimetrack_qnsd.html', {'ins2': ins2})


def abouttime_qns1(request):
    card2=abouttime_data1.objects.all()
    card41=abouttime_data2.objects.all()
    return render(request,"abouttime_qns1.html",{'card2': card2, 'card41':card41})



def aboutedit_qns1(request, pk):
    instance = get_object_or_404(abouttime_data1, pk=pk)
    
    if request.method == 'POST':
        
        instance.main_title = request.POST.get('maintitle', instance.main_title)
        instance.des1 = request.POST.get('des1', instance.des1)
        instance.subhead = request.POST.get('subhead', instance.subhead)
        instance.point1 = request.POST.get('point1', instance.point1)
        
        instance.point2 = request.POST.get('point2', instance.point2)
        instance.subhead2 = request.POST.get('subhead2', instance.subhead2)
        instance.point3 = request.POST.get('point3', instance.point3)
        instance.point4 = request.POST.get('point4', instance.point4)
        instance.point5 = request.POST.get('point5', instance.point5)
        
        instance.save()
        return redirect('abouttime_qns1')
    
    return render(request, 'aboutedit_form.html', {'instance': instance})


def aboutdelete_dataans1(request, pk):
    instance = get_object_or_404(abouttime_data1, pk=pk)
    
    if request.method == 'POST':
        instance.delete()
        return redirect('abouttime_qns1')  
    
    return render(request, 'aboutdelete_confirmqns.html', {'instance': instance})


def aboutedit_qns2(request, pk):
    instance = get_object_or_404(abouttime_data2, pk=pk)
    
    if request.method == 'POST':

        instance.subhead3 = request.POST.get('subhead3', instance.subhead3)
        instance.point6 = request.POST.get('point6', instance.point6)
        instance.point7 = request.POST.get('point7', instance.point7)
        instance.point11 = request.POST.get('point11', instance.point11)
        
        instance.subhead4 = request.POST.get('subhead4', instance.subhead4)
        instance.des2 = request.POST.get('des2', instance.des2)
        instance.point8 = request.POST.get('point8', instance.point8)
        instance.point9 = request.POST.get('point9', instance.point9)
        instance.point10 = request.POST.get('point10', instance.point10)
        
        instance.save()
        return redirect('abouttime_qns1')
    
    return render(request, 'aboutedit_form1.html', {'instance': instance})


def aboutdelete_dataans2(request, pk):
    instance = get_object_or_404(abouttime_data2, pk=pk)
    
    if request.method == 'POST':
        instance.delete()
        return redirect('abouttime_qns1')  # Redirect to a relevant URL
    
    return render(request, 'aboutdelete_confirmqns1.html', {'instance': instance})


def insert_clockqns2(request):
    if request.method == 'POST':
        form = InstructionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = InstructionForm()
    
    return render(request, 'insert_clockqns2.html', {'form': form})

def retriev_clock(request):
    instructions = clock.objects.all()
    for instruction in instructions:
        instruction.steps = [step.strip() for step in instruction.steps.splitlines() if step.strip()]
    return render(request, 'retriev_clock_template.html', {'instructions': instructions})


def edit_clock(request, id):
    c1 = get_object_or_404(clock, pk=id)

    if request.method == 'POST':
        title = request.POST['title']
        des1 = request.POST['des1']
        des2 = request.POST['des2']
        steps = request.POST['steps']

        c1.title = title
        c1.des1 = des1
        c1.des2 = des2
        c1.steps = steps
        c1.save()

        return redirect('retriev_clock') 

    return render(request, 'edit_clock.html', {'c1': c1})

def delete_clock(request, id):
    c2 = get_object_or_404(clock, pk=id)

    if request.method == 'POST':
        c2.delete()
        return redirect('retriev_clock') 

    return render(request, 'delete_clock.html', {'c2': c2})

def insert_assignqns3(request):
    if request.method == 'POST':
        form = InstructionForm1(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = InstructionForm()
    
    return render(request, 'insert_assignqns3.html', {'form': form})


def retriev_assignans3(request):
    qns3 = assignqns3.objects.all()
    for instruction in qns3:
        instruction.steps = [step.strip() for step in instruction.steps.splitlines() if step.strip()]
    return render(request, 'retriev_assignanqns3.html', {'qns3': qns3})



def edit_assignqns3(request, id):
    c2 = get_object_or_404(assignqns3, pk=id)

    if request.method == 'POST':
        title = request.POST['title']
        des1 = request.POST['des1']
        des2 = request.POST['des2']
        steps = request.POST['steps']

        c2.title = title
        c2.des1 = des1
        c2.des2 = des2
        c2.steps = steps
        c2.save()

        return redirect('retriev_assignans3')

    return render(request, 'edit_assignqns3.html', {'c2': c2})


def delete_assign3(request, id):
    c3 = get_object_or_404(assignqns3, pk=id)

    if request.method == 'POST':
        c3.delete()
        return redirect('retriev_assignans3') 

    return render(request, 'delete_assign3.html', {'c3': c3})



def insert_breaksqns4(request):
    if request.method == 'POST':
        form = InstructionForm2(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = InstructionForm()
    
    return render(request, 'insert_breaksqns4.html', {'form': form})


def retriev_breaksqns4(request):
    qns4 = breaksqns4.objects.all()
    for breaks in qns4:
        breaks.steps = [step.strip() for step in breaks.steps.splitlines() if step.strip()]
    return render(request, 'retriev_breaksqns4.html', {'qns4': qns4})


def edit_abreaksqns4(request, id):
    c3 = get_object_or_404(breaksqns4, pk=id)

    if request.method == 'POST':
        title = request.POST['title']
        des1 = request.POST['des1']
        des2 = request.POST['des2']
        steps = request.POST['steps']

        c3.title = title
        c3.des1 = des1
        c3.des2 = des2
        c3.steps = steps
        c3.save()

        return redirect('retriev_breaksqns4')

    return render(request, 'edit_breaksqns4.html', {'c3': c3})

def delete_breaksqns4(request, id):
    c4 = get_object_or_404(breaksqns4, pk=id)

    if request.method == 'POST':
        c4.delete()
        return redirect('retriev_breaksqns4')

    return render(request, 'delete_breaksqns4.html', {'c4': c4})

def insert_faq5(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        des = request.POST.get('des')

        question = request.POST.get('question')
        answer = request.POST.get('answer')
        
        faq = faq5(title=title,des=des, question=question, answer=answer)
        faq.save()
        
    
    return render(request, 'insert_faq5.html')


def retriev_faq5(request):
    faq = faq5.objects.all()
    return render(request, 'retriev_faq5.html', {'faq': faq})


def edit_faq5(request, id):
    faq = get_object_or_404(faq5, pk=id)
    
    if request.method == 'POST':
        faq.title = request.POST.get('title')
        faq.des = request.POST.get('des')

        faq.question = request.POST.get('question')
        faq.answer = request.POST.get('answer')
        faq.save()
        return redirect('retriev_faq5') 
    else:
        return render(request, 'edit_faq5.html', {'faq': faq})


def delete_faq5(request, id):
    faq = get_object_or_404(faq5, pk=id)
    
    if request.method == 'POST':
        faq.delete()
        return redirect('retriev_faq5')  
    
    return render(request, 'delete_faq5.html', {'faq': faq})


def table_card2(request):
    qns = abouttime_data1.objects.all()
    qns1 = abouttime_data2.objects.all()
    assignqns3_list = assignqns3.objects.all()
    instructions = clock.objects.all()

    for instruction in instructions:
        instruction.steps = [step.strip() for step in instruction.steps.splitlines() if step.strip()]

    qns4 = breaksqns4.objects.all()
    for breaks in qns4:
        breaks.steps = [step.strip() for step in breaks.steps.splitlines() if step.strip()]

    faqs = faq5.objects.all() 



    return render(request, 'table_detai2.html', {'qns':qns,'qns1':qns1,'instructions': instructions,'assignqns3_list':assignqns3_list,'qns4':qns4,'faqs':faqs})



def payrol_qnsd(request):
    card3 = payrol_qns.objects.filter()
    return render(request, 'payroll_qnsd.html', {'card3': card3})


def insert_payrolqnsd(request):
    if request.method == 'POST':
        qns = request.POST.get('qns', '') 
        title2 = request.POST.get('title2', '')
        discription = request.POST.get('discription', '')  
        link = request.POST.get('link', '')  

    
        new_payroll = payrol_qns(qns=qns, title2=title2, discription=discription, link=link)
        new_payroll.save()

    
        return redirect('payrol_qnsd')

    else:
        return render(request, 'insert_payrolqnsd.html')



def edit_payrolqnsd(request, pk):
    ins3 = get_object_or_404(payrol_qns, pk=pk)
    
    if request.method == 'POST':
        qns = request.POST.get('qns')
        title2 = request.POST.get('title2')
        discription = request.POST.get('discription')
        link = request.POST.get('link')

        
        ins3.qns = qns
        ins3.title2 = title2
        ins3.discription= discription
        ins3.title2 = title2
        ins3.link = link


        ins3.save()
        
        return redirect('payrol_qnsd')  
    
    return render(request, 'edit_payrolqnsd.html', {'ins3': ins3})



def delete_payrolqnsd(request, pk):
    ins3 = get_object_or_404(payrol_qns, pk=pk)
    
    if request.method == 'POST':
        ins3.delete()
        return redirect('payrol_qnsd')  
    
    return render(request, 'delete_payrolqnsd.html', {'ins3': ins3})

def insert_payroll1(request):
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        des = request.POST.get('des')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        new_payroll_data = payroll_data1.objects.create( maintitle=maintitle, des=des, title=title,steps=steps)
        
        new_payroll_data.save()
        
        return redirect('retriev_payroll1') 
        
    else:
        return render(request, 'insert_payroll1.html')



def retriev_payroll1(request):
    pay1 = payroll_data1.objects.all()
    for instruction in pay1:
        instruction.steps = [step.strip() for step in instruction.steps.splitlines() if step.strip()]
    return render(request, 'retriev_payroll1.html', {'pay1': pay1})






def edit_payrollqns1(request, pk):
    data = get_object_or_404(payroll_data1, pk=pk)
    
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        des = request.POST.get('des')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        # Update the object with new data
        data.maintitle = maintitle
        data.des = des
        data.title = title
        data.steps = steps
        data.save()
        
        return redirect('retriev_payroll1')  # Redirect to list view after update
    
    return render(request, 'edit_payrollqns1.html', {'data': data})



def delete_payrollqns1(request, id):
    data = get_object_or_404(payroll_data1, id=id)
    
    if request.method == 'POST':
        data.delete()
        return redirect('retriev_payroll1')
    
    return render(request, 'delete_payroll1.html', {'data': data})

def insert_addempqns2(request):
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        addemp_data = payroll_qns2.objects.create( maintitle=maintitle,  title=title,steps=steps)
        
        addemp_data.save()
        
        return redirect('retriev_addempqns2') 
        
    else:
        return render(request, 'insert_addempqns1.html')


def retriev_addempqns2(request):
    emp1 = payroll_qns2.objects.all()
    for multi in emp1:
        multi.steps = [step.strip() for step in multi.steps.splitlines() if step.strip()]
    return render(request, 'retriev_addempqns2.html', {'emp1': emp1})


def edit_addempqns2(request, id):
    data1 = get_object_or_404(payroll_qns2, id=id)
    
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        data1.maintitle = maintitle
        data1.title = title
        data1.steps = steps
        data1.save()
        
        return redirect('retriev_addempqns2')
    
    return render(request, 'edit_addempqns2.html', {'data1': data1})

def delete_addempqns2(request, id):
    data2 = get_object_or_404(payroll_qns2, id=id)
    
    if request.method == 'POST':
        data2.delete()
        return redirect('retriev_addempqns2')
    
    return render(request, 'delete_addempqns2.html', {'data2': data2})

def insert_Reimbursementqns3 (request):
    if request.method == 'POST':
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        addans3_data = payroll_qnsdata3.objects.create(title=title,steps=steps)
        
        addans3_data.save()
        
        return redirect('retriev_reimbursementqns3') 
        
    else:
        return render(request, 'insert_Reimbursementqns3.html')


def retriev_reimbursementqns3(request):
    rrr = payroll_qnsdata3.objects.all()
    for remb1 in rrr:
        remb1.steps = [step.strip() for step in remb1.steps.splitlines() if step.strip()]
    return render(request, 'retriev_reimbursementqns3.html', {'rrr': rrr})


def edit_reimbursementqns3(request, id):
    data2 = get_object_or_404(payroll_qnsdata3, id=id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        data2.title = title
        data2.steps = steps
        data2.save()
        
        return redirect('retriev_reimbursementqns3')
    
    return render(request, 'edit_reimbursementqns3.html', {'data2': data2})


def delete_reimbursementqns3(request, id):
    data3 = get_object_or_404(payroll_qnsdata3, id=id)
    
    if request.method == 'POST':
        data3.delete()
        return redirect('retriev_reimbursementqns3')
    
    return render(request, 'delete_reimbursementqns3.html', {'data3': data3})


def insert_requestqns4(request):
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        req_data = payroll_qnsdata4.objects.create( maintitle=maintitle,  title=title,steps=steps)
        
        req_data.save()
        
        return redirect('retriev_requestqns4') 
        
    else:
        return render(request, 'insert_requestqns5.html')



def retriev_requestqns4(request):
    req4 = payroll_qnsdata4.objects.all()
    for  aprove in req4:
        aprove.steps = [step.strip() for step in aprove.steps.splitlines() if step.strip()]
    return render(request, 'retriev_requestqns4.html', {'req4': req4})


def edit_requestqns4(request, id):
    data5 = get_object_or_404(payroll_qnsdata4, id=id)
    
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        data5.maintitle = maintitle
        data5.title = title
        data5.steps = steps
        data5.save()
        
        return redirect('retriev_requestqns4')
    
    return render(request, 'edit_requestqns4.html', {'data5': data5})


def delete_requestqns4(request, id):
    data6 = get_object_or_404(payroll_qnsdata4, id=id)
    
    if request.method == 'POST':
        data6.delete()
        return redirect('retriev_reimbursementqns3')
    
    return render(request, 'delete_requestqns4.html', {'data6': data6})



def insert_advanceqns5(request):
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        des1 = request.POST.get('des1')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        ad5_data = payroll_qnsdata5.objects.create( maintitle=maintitle,des1=des1,title=title,steps=steps)
        
        ad5_data.save()
        
        return redirect('retriev_advanceqns5') 
        
    else:
        return render(request, 'insert_advanceqns5.html')


def retriev_advanceqns5(request):
    qns5 = payroll_qnsdata5.objects.all()
    for  advance in qns5:
        advance.steps = [step.strip() for step in advance.steps.splitlines() if step.strip()]
    return render(request, 'retriev_advanceqns5.html', {'qns5': qns5})



def edit_advanceqns5(request, id):
    data6 = get_object_or_404(payroll_qnsdata5, id=id)
    
    if request.method == 'POST':
        maintitle = request.POST.get('maintitle')
        des1 = request.POST.get('des1')
        title = request.POST.get('title')
        steps = request.POST.get('steps')
        
        data6.maintitle = maintitle
        data6.des1 = des1
        data6.title = title
        data6.steps = steps
        data6.save()
        
        return redirect('retriev_advanceqns5')
    
    return render(request, 'edit_advanceqns5.html', {'data6': data6})


def delete_advanceqns5(request, id):
    data7 = get_object_or_404(payroll_qnsdata5, id=id)
    
    if request.method == 'POST':
        data7.delete()
        return redirect('retriev_advanceqns5')
    
    return render(request, 'delete_advanceqns5.html', {'data7': data7})

def table_card1(request):
    intro_content = IntroContent.objects.first()
    steps = Step.objects.filter(intro_content=intro_content)
    qns2 = managing_data.objects.all()
    print("Number of managing_data objects:", qns2.count())

    context = {
        'intro_content': intro_content,
        'steps': steps,
        'qns2':qns2,
    }
    
    return render(request, 'table_detail.html', context)

def table_card3(request):
    pay1 = payroll_data1.objects.all()
    for instruction in pay1:
        instruction.steps = [step.strip() for step in instruction.steps.splitlines() if step.strip()]

    emp1 = payroll_qns2.objects.all()
    for multi in emp1:
        multi.steps = [step.strip() for step in multi.steps.splitlines() if step.strip()]

    rrr = payroll_qnsdata3.objects.all()
    for remb1 in rrr:
        remb1.steps = [step.strip() for step in remb1.steps.splitlines() if step.strip()]

    ads1 = payroll_qnsdata4.objects.all()
    for remb2 in ads1:
        remb2.steps = [step.strip() for step in remb2.steps.splitlines() if step.strip()]

    last_qns = payroll_qnsdata5.objects.all()
    for  mpt in last_qns:
        mpt.steps = [step.strip() for step in mpt.steps.splitlines() if step.strip()]

    return render(request, 'table_card3.html', {'pay1': pay1,'emp1':emp1,'rrr':rrr,'ads1':ads1,'last_qns':last_qns})

from .models import documents_qa,documents_qa1,documents_qa2,documents_qa3,documents_qa4
from .models import documents_qa5,documents_qa6,documents_qa7,documents_qa8,documents_qa9

def documents_card(request):
    card4=documents_qns.objects.all()
    return render(request,"documents_card.html",{'card4': card4 })


def insert_documents(request):
    if request.method == "POST":
        qns=request.POST['qns']
        link= request.POST['link']  
        k=documents_qns(qns=qns,link=link)
        k.save()
        return HttpResponse("Question Inserted Successfully")
    return render(request,"insert_documents.html")


def edit_documents(request, id):
    d1 =documents_qns.objects.get(id=id)
    if request.method == 'POST':
        d1.qns=request.POST['qns']
        d1.link=request.POST['link'] 
        d1.save()
    return render(request, "edit_documents.html", {'d1': d1})

def delete_documents(request, id):
    d2 = get_object_or_404(documents_qns, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documents.html', {'d2': d2})


def retrive_documents(request):
    d3=documents_qns.objects.all()
    doc1=documents_qa.objects.all()
    doc2=documents_qa1.objects.all()
    doc3=documents_qa2.objects.all()
    doc4=documents_qa3.objects.all()
    doc5=documents_qa4.objects.all()
    doc6=documents_qa5.objects.all()
    doc7=documents_qa6.objects.all()
    doc8=documents_qa7.objects.all()
    doc9=documents_qa8.objects.all()
    doc10=documents_qa9.objects.all()
    return render(request,"retrive_documents.html",{ 'd3': d3,'doc1': doc1,'doc2': doc2,'doc3': doc3,'doc4': doc4,'doc5': doc5,'doc6': doc6,'doc7': doc7,'doc8': doc8,'doc9': doc9,'doc10': doc10 })


def documents(request):
    doc=documents_qa.objects.all()
    return render(request,"help20.html",{ 'doc': doc })


def insert_documentsqn1(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        line9=request.POST['line9']
        line10=request.POST['line10']
        line11=request.POST['line11']
        line12=request.POST['line12']
        line13=request.POST['line13']
        line14=request.POST['line14']
        line15=request.POST['line15']
        line16=request.POST['line16']
        line17=request.POST['line17']
        line18=request.POST['line18']
        line19=request.POST['line19']
        line20=request.POST['line20']
        line21=request.POST['line21']
        image=request.FILES.get('image')
        k=documents_qa(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,line12=line12,line13=line13,line14=line14,line15=line15,line16=line16,line17=line17,line18=line18,line19=line19,line20=line20,line21=line21,image=image)
        k.save()
    return render(request,"insert_documentsqn1.html")

def edit_documentsqn1(request, id):
    d1 =documents_qa.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.line8=request.POST['line8']
        d1.line9=request.POST['line9']
        d1.line10=request.POST['line10']
        d1.line11=request.POST['line11']
        d1.line12=request.POST['line12']
        d1.line13=request.POST['line13']
        d1.line14=request.POST['line14']
        d1.line15=request.POST['line15']
        d1.line16=request.POST['line16']
        d1.line17=request.POST['line17']
        d1.line18=request.POST['line18']
        d1.line19=request.POST['line19']
        d1.line20=request.POST['line20']
        d1.line21=request.POST['line21']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn1.html", {'d1': d1})

def delete_documentsqn1(request, id):
    d2 = get_object_or_404(documents_qa, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn1.html', {'d2': d2})

def documents1(request):
    doc1=documents_qa1.objects.all()
    return render(request,"help21.html",{ 'doc1': doc1 })

    
def insert_documentsqn2(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa1(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn2.html")

def edit_documentsqn2(request, id):
    d1 =documents_qa1.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn2.html", {'d1': d1})

def delete_documentsqn2(request, id):
    d2 = get_object_or_404(documents_qa1, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn2.html', {'d2': d2})

def documents2(request):
    doc2=documents_qa2.objects.all()
    return render(request,"help22.html",{ 'doc2': doc2 })


def insert_documentsqn3(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa2(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn3.html")

def edit_documentsqn3(request, id):
    d1 =documents_qa2.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn3.html", {'d1': d1})

def delete_documentsqn3(request, id):
    d2 = get_object_or_404(documents_qa2, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn3.html', {'d2': d2})

def documents3(request):
    doc3=documents_qa3.objects.all()
    return render(request,"help23.html",{ 'doc3': doc3 })

    
def insert_documentsqn4(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa3(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn4.html")

def edit_documentsqn4(request, id):
    d1 =documents_qa3.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn4.html", {'d1': d1})

def delete_documentsqn4(request, id):
    d2 = get_object_or_404(documents_qa3, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn4.html', {'d2': d2})

def documents4(request):
    doc4=documents_qa4.objects.all()
    return render(request,"help24.html",{ 'doc4': doc4 })


def insert_documentsqn5(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa4(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn5.html")

def edit_documentsqn5(request, id):
    d1 =documents_qa4.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn5.html", {'d1': d1})

def delete_documentsqn5(request, id):
    d2 = get_object_or_404(documents_qa4, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn5.html', {'d2': d2})



def documents5(request):
    doc5=documents_qa5.objects.all()
    return render(request,"help25.html",{ 'doc5': doc5 })


def insert_documentsqn6(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa5(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn6.html")

def edit_documentsqn6(request, id):
    d1 =documents_qa5.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn6.html", {'d1': d1})

def delete_documentsqn6(request, id):
    d2 = get_object_or_404(documents_qa5, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn6.html', {'d2': d2})

def documents6(request):
    doc6=documents_qa6.objects.all()
    return render(request,"help26.html",{ 'doc6': doc6 })


def insert_documentsqn7(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa6(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn7.html")

def edit_documentsqn7(request, id):
    d1 =documents_qa6.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn7.html", {'d1': d1})

def delete_documentsqn7(request, id):
    d2 = get_object_or_404(documents_qa6, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn7.html', {'d2': d2})

def documents7(request):
    doc7=documents_qa7.objects.all()
    return render(request,"help27.html",{ 'doc7': doc7 })


def insert_documentsqn8(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa7(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn8.html")

def edit_documentsqn8(request, id):
    d1 =documents_qa7.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn8.html", {'d1': d1})

def delete_documentsqn8(request, id):
    d2 = get_object_or_404(documents_qa7, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn8.html', {'d2': d2})

def documents8(request):
    doc8=documents_qa8.objects.all()
    return render(request,"help28.html",{ 'doc8': doc8 })

    
def insert_documentsqn9(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa8(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn9.html")

def edit_documentsqn9(request, id):
    d1 =documents_qa8.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn9.html", {'d1': d1})

def delete_documentsqn9(request, id):
    d2 = get_object_or_404(documents_qa8, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn9.html', {'d2': d2})

def documents9(request):
    doc9=documents_qa9.objects.all()
    return render(request,"help29.html",{ 'doc9': doc9 })


def insert_documentsqn10(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=documents_qa9(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_documentsqn10.html")

def edit_documentsqn10(request, id):
    d1 =documents_qa9.objects.get(id=id)
    if request.method == 'POST':
        d1.question=request.POST['question']
        d1.start=request.POST['start']
        d1.intro=request.POST['intro']
        d1.line1=request.POST['line1']
        d1.line2=request.POST['line2']
        d1.line3=request.POST['line3']
        d1.line4=request.POST['line4']
        d1.line5=request.POST['line5']
        d1.line6=request.POST['line6']
        d1.line7=request.POST['line7']
        d1.image=request.FILES.get('image')
        d1.save()
    return render(request, "edit_documentsqn10.html", {'d1': d1})

def delete_documentsqn10(request, id):
    d2 = get_object_or_404(documents_qa9, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_documentsqn10.html', {'d2': d2})

def organization_card(request):
    card6=organization_qns.objects.all()
    return render(request,"organization_card.html",{'card6': card6 })

    
def insert_organization(request):
    if request.method == "POST":
        qns=request.POST['qns']
        link= request.POST['link']  
        k=organization_qns(qns=qns,link=link)
        k.save()
    return render(request,"insert_organization.html")

def edit_organization(request, id):
    d1 =organization_qns.objects.get(id=id)
    org1=organization_qa.objects.all()
    if request.method == 'POST':
       d1.qns=request.POST['qns']
       d1.link= request.POST['link'] 
       d1.save()
    return render(request, "edit_organization.html", {'d1': d1,'org1': org1})

def delete_organization(request, id):
    d2 = get_object_or_404(organization_qns, id=id)
    if request.method == 'POST':
        d2.delete()
    return render(request, 'delete_organization.html', {'d2': d2})
    
def retrive_organization(request):
    o3=organization_qns.objects.all()
    org1=organization_qa.objects.all()
    org2=organization_qa1.objects.all()
    org3=organization_qa2.objects.all()
    org4=organization_qa3.objects.all()
    org5=organization_qa4.objects.all()
    org6=organization_qa5.objects.all()
    org7=organization_qa6.objects.all()
    org8=organization_qa7.objects.all()
    org9=organization_qa8.objects.all()
    org10=organization_qa9.objects.all()
    return render(request,"retrive_organization.html",{ 'o3': o3,'org1': org1,'org2': org2,'org3': org3,'org4': org4,'org5': org5,'org6': org6,'org7': org7,'org8': org8,'org9': org9,'org10': org10 })

from .models import organization_qa,organization_qa1,organization_qa2,organization_qa3,organization_qa4
from .models import organization_qa5,organization_qa6,organization_qa7,organization_qa8,organization_qa9

def organization(request):
    org=organization_qa.objects.all()
    return render(request,"help10.html",{ 'org': org })

def insert_organizationqn1(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        line9=request.POST['line9']
        line10=request.POST['line10']
        image=request.FILES.get('image')
        k=organization_qa(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,image=image)
        k.save()
    return render(request,"insert_organizationqn1.html")

def edit_organizationqn1(request, id):
    o1 =organization_qa.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.line9=request.POST['line9']
        o1.line10=request.POST['line10']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn2.html", {'o1': o1})

def delete_organizationqn1(request, id):
    o2 = get_object_or_404(organization_qa, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn1.html', {'o2': o2})

def organization1(request):
    org1=organization_qa1.objects.all()
    return render(request,"help11.html",{ 'org1': org1 })

def insert_organizationqn2(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        line9=request.POST['line9']
        line10=request.POST['line10']
        line11=request.POST['line11']
        line12=request.POST['line12']
        image=request.FILES.get('image')
        k=organization_qa1(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,line12=line12,image=image)
        k.save()
    return render(request,"insert_organizationqn1.html")

def edit_organizationqn2(request, id):
    o1 =organization_qa1.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.line9=request.POST['line9']
        o1.line10=request.POST['line10']
        o1.line11=request.POST['line11']
        o1.line12=request.POST['line12']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn2.html", {'o1': o1})

def delete_organizationqn2(request, id):
    o2 = get_object_or_404(organization_qa1, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn2.html', {'o2': o2})

def organization2(request):
    org2=organization_qa2.objects.all()
    return render(request,"help12.html",{ 'org2': org2 })
    
def insert_organizationqn3(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        line9=request.POST['line9']
        line10=request.POST['line10']
        line11=request.POST['line11']
        line12=request.POST['line12']
        image=request.FILES.get('image')
        k=organization_qa2(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,line12=line12,image=image)
        k.save()
    return render(request,"insert_organizationqn3.html")

def edit_organizationqn3(request, id):
    o1 =organization_qa2.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.line9=request.POST['line9']
        o1.line10=request.POST['line10']
        o1.line11=request.POST['line11']
        o1.line12=request.POST['line12']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn3.html", {'o1': o1})

def delete_organizationqn3(request, id):
    o2 = get_object_or_404(organization_qa2, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn3.html', {'o2': o2})

def organization3(request):
    org3=organization_qa3.objects.all()
    return render(request,"help13.html",{ 'org3': org3 })

def insert_organizationqn4(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        line9=request.POST['line9']
        line10=request.POST['line10']
        line11=request.POST['line11']
        line12=request.POST['line12']
        image=request.FILES.get('image')
        k=organization_qa3(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,line12=line12,image=image)
        k.save()
    return render(request,"insert_organizationqn4.html")

def edit_organizationqn4(request, id):
    o1 =organization_qa3.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.line9=request.POST['line9']
        o1.line10=request.POST['line10']
        o1.line11=request.POST['line11']
        o1.line12=request.POST['line12']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn4.html", {'o1': o1})

def delete_organizationqn4(request, id):
    o2 = get_object_or_404(organization_qa3, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn4.html', {'o2': o2})

def organization4(request):
    org4=organization_qa4.objects.all()
    return render(request,"help14.html",{ 'org4': org4 })
   
def insert_organizationqn5(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        line9=request.POST['line9']
        line10=request.POST['line10']
        line11=request.POST['line11']
        line12=request.POST['line12']
        image=request.FILES.get('image')
        k=organization_qa4(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,line12=line12,image=image)
        k.save()
    return render(request,"insert_organizationqn5.html")

def edit_organizationqn5(request, id):
    o1 =organization_qa4.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.line9=request.POST['line9']
        o1.line10=request.POST['line10']
        o1.line11=request.POST['line11']
        o1.line12=request.POST['line12']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn5.html", {'o1': o1})

def delete_organizationqn5(request, id):
    o2 = get_object_or_404(organization_qa4, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn5.html', {'o2': o2})


def organization5(request):
    org5=organization_qa5.objects.all()
    return render(request,"help15.html",{ 'org5': org5 })
    
def insert_organizationqn6(request):
    if request.method == "POST":
        question=request.POST['question']
        start1=request.POST['start1']
        start2=request.POST['start2']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        image=request.FILES.get('image')
        k=organization_qa5(question=question,start1=start1,start2=start2,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,image=image)
        k.save()
    return render(request,"insert_organizationqn6.html")

def edit_organizationqn6(request, id):
    o1 =organization_qa5.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start1=request.POST['start1']
        o1.start2=request.POST['start2']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn6.html", {'o1': o1})

def delete_organizationqn6(request, id):
    o2 = get_object_or_404(organization_qa5, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn6.html', {'o2': o2})

def organization6(request):
    org6=organization_qa6.objects.all()
    return render(request,"help16.html",{ 'org6': org6 })
   
def insert_organizationqn7(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        image=request.FILES.get('image')
        k=organization_qa6(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,image=image)
        k.save()
    return render(request,"insert_organizationqn7.html")

def edit_organizationqn7(request, id):
    o1 =organization_qa6.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn7.html", {'o1': o1})

def delete_organizationqn7(request, id):
    o2 = get_object_or_404(organization_qa6, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn7.html', {'o2': o2})


def organization7(request):
    org7=organization_qa7.objects.all()
    return render(request,"help17.html",{ 'org7': org7 })
    
def insert_organizationqn8(request):
    if request.method == "POST":
        question=request.POST['question']
        start1=request.POST['start1']
        start2=request.POST['start2']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        image=request.FILES.get('image')
        k=organization_qa7(question=question,start1=start1,start2=start2,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,image=image)
        k.save()
    return render(request,"insert_organizationqn8.html")

def edit_organizationqn8(request, id):
    o1 =organization_qa7.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start1=request.POST['start1']
        o1.start2=request.POST['start2']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn8.html", {'o1': o1})

def delete_organizationqn8(request, id):
    o2 = get_object_or_404(organization_qa7, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn8.html', {'o2': o2})

def organization8(request):
    org8=organization_qa8.objects.all()
    return render(request,"help18.html",{ 'org8': org8 })
    
def insert_organizationqn9(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        line8=request.POST['line8']
        line9=request.POST['line9']
        line10=request.POST['line10']
        line11=request.POST['line11']
        image=request.FILES.get('image')
        k=organization_qa8(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,image=image)
        k.save()
    return render(request,"insert_organizationqn9.html")

def edit_organizationqn9(request, id):
    o1 =organization_qa8.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.line8=request.POST['line8']
        o1.line9=request.POST['line9']
        o1.line10=request.POST['line10']
        o1.line11=request.POST['line11']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn9.html", {'o1': o1})

def delete_organizationqn9(request, id):
    o2 = get_object_or_404(organization_qa8, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn9.html', {'o2': o2})

def organization9(request):
    org9=organization_qa9.objects.all()
    return render(request,"help19.html",{ 'org9': org9 })

def insert_organizationqn10(request):
    if request.method == "POST":
        question=request.POST['question']
        start=request.POST['start']
        intro=request.POST['intro']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']
        line7=request.POST['line7']
        image=request.FILES.get('image')
        k=organization_qa9(question=question,start=start,intro=intro,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,image=image)
        k.save()
    return render(request,"insert_organizationqn10.html")

def edit_organizationqn10(request, id):
    o1 =organization_qa9.objects.get(id=id)
    if request.method == 'POST':
        o1.question=request.POST['question']
        o1.start=request.POST['start']
        o1.intro=request.POST['intro']
        o1.line1=request.POST['line1']
        o1.line2=request.POST['line2']
        o1.line3=request.POST['line3']
        o1.line4=request.POST['line4']
        o1.line5=request.POST['line5']
        o1.line6=request.POST['line6']
        o1.line7=request.POST['line7']
        o1.image=request.FILES.get('image')
        o1.save()
    return render(request, "edit_organizationqn10.html", {'o1': o1})

def delete_organizationqn10(request, id):
    o2 = get_object_or_404(organization_qa9, id=id)
    if request.method == 'POST':
        o2.delete()
    return render(request, 'delete_organizationqn10.html', {'o2': o2})


from .models import helpdata7card,helpdata8card,helpdata9card,helpdata71,helpdata72,helpdata73,helpdata74,helpdata75,helpdata76,helpdata77,helpdata81,helpdata82,helpdata83,helpdata84,helpdata91,helpdata92,helpdata93,helpdata94,helpdata95,helpdata96,helpdata97

def help_page_card7(request):
    obj=helpdata7card.objects.all()
    return render(request,"help_page_card7.html",{'obj':obj})

def help_page_card8(request):
    obj=helpdata8card.objects.all()
    return render(request,"help_page_card8.html",{'obj':obj})

def help_page_card9(request):
    obj=helpdata9card.objects.all()
    return render(request,"help_page_card9.html",{'obj':obj})




def card7create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        link=request.POST['link']

        card7=helpdata7card(sno=sno,cardtitle=cardtitle,qns=qns,link=link)
        card7.save()
        return redirect('card7list')
        
    return render(request,"help_page_card7create.html")

def card7list(request):
    card7=helpdata7card.objects.all()
    return render(request,"help_page_card7get.html",{'card7':card7})


def card7update(request,id):
    k1=get_object_or_404(helpdata7card, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        link=request.POST.get('link')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.link=link
        k1.save()
        return redirect('card7list')
        
    return render(request,"help_page_card7update.html",{'k1':k1})



def card7delete(request,id):
    data = get_object_or_404(helpdata7card,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card7list')
        
    return render(request, 'help_page_card7delete.html', {'data': data})

#card8 crud
def card8create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        link=request.POST['link']

        card8=helpdata8card(sno=sno,cardtitle=cardtitle,qns=qns,link=link)
        card8.save()
        return redirect('card8list')
        
    return render(request,"help_page_card8create.html")

def card8list(request):
    card8=helpdata8card.objects.all()
    return render(request,"help_page_card8get.html",{'card8':card8})


def card8update(request,id):
    k1=get_object_or_404(helpdata8card, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        link=request.POST.get('link')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.link=link
        k1.save()
        return redirect('card8list')
        
    return render(request,"help_page_card8update.html",{'k1':k1})



def card8delete(request,id):
    data = get_object_or_404(helpdata8card,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card8list')
        
    return render(request, 'help_page_card8delete.html', {'data': data})

#card9 crud

def card9create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        link=request.POST['link']

        card9=helpdata9card(sno=sno,cardtitle=cardtitle,qns=qns,link=link)
        card9.save()
        return redirect('card9list')
        
    return render(request,"help_page_card9create.html")

def card9list(request):
    card9=helpdata9card.objects.all()
    return render(request,"help_page_card9get.html",{'card9':card9})


def card9update(request,id):
    k1=get_object_or_404(helpdata9card, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        link=request.POST.get('link')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.link=link
        k1.save()
        return redirect('card9list')
        
    return render(request,"help_page_card9update.html",{'k1':k1})



def card9delete(request,id):
    data = get_object_or_404(helpdata9card,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card9list')
        
    return render(request, 'help_page_card9delete.html', {'data': data})

def help_page_7_1(request):
    obj=helpdata71.objects.all()
    return render(request,"help_page_7_1.html",{'obj':obj})

def card71create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        

        card71=helpdata71(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3)
        card71.save()
        return redirect('card71list')
        
    return render(request,"help_page71create.html")

def card71list(request):
    card71=helpdata71.objects.all()
    return render(request,"help_page71get.html",{'card71':card71})


def card71update(request,id):
    k1=get_object_or_404(helpdata71, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.save()
        return redirect('card71list')
        
    return render(request,"help_page71update.html",{'k1':k1})


def card71delete(request,id):
    data = get_object_or_404(helpdata71,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card71list')
        
    return render(request, 'help_page71delete.html', {'data': data})


    
def help_page_7_2(request):
    obj=helpdata72.objects.all()
    return render(request,"help_page_7_2.html",{'obj':obj})

def card72create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        

        card72=helpdata72(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4)
        card72.save()
        return redirect('card72list')
        
    return render(request,"help_page72create.html")

def card72list(request):
    card72=helpdata72.objects.all()
    return render(request,"help_page72get.html",{'card72':card72})


def card72update(request,id):
    k1=get_object_or_404(helpdata72, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.save()
        return redirect('card72list')
        
    return render(request,"help_page72update.html",{'k1':k1})


def card72delete(request,id):
    data = get_object_or_404(helpdata72,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card72list')
        
    return render(request, 'help_page72delete.html', {'data': data})


def help_page_7_3(request):
    obj=helpdata73.objects.all()
    return render(request,"help_page_7_3.html",{'obj':obj})

def card73create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        

        card73=helpdata73(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3)
        card73.save()
        return redirect('card73list')
        
    return render(request,"help_page73create.html")

def card73list(request):
    card73=helpdata73.objects.all()
    return render(request,"help_page73get.html",{'card73':card73})


def card73update(request,id):
    k1=get_object_or_404(helpdata73, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.save()
        return redirect('card73list')
        
    return render(request,"help_page73update.html",{'k1':k1})


def card73delete(request,id):
    data = get_object_or_404(helpdata73,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card73list')
        
    return render(request, 'help_page73delete.html', {'data': data})



def help_page_7_4(request):
    obj=helpdata74.objects.all()
    return render(request,"help_page_7_4.html",{'obj':obj})

def card74create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        
        

        card74=helpdata74(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3)
        card74.save()
        return redirect('card74list')
        
    return render(request,"help_page74create.html")

def card74list(request):
    card74=helpdata74.objects.all()
    return render(request,"help_page74get.html",{'card74':card74})


def card74update(request,id):
    k1=get_object_or_404(helpdata74, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.save()
        return redirect('card74list')
        
    return render(request,"help_page74update.html",{'k1':k1})


def card74delete(request,id):
    data = get_object_or_404(helpdata74,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card74list')
        
    return render(request, 'help_page74delete.html', {'data': data})


def help_page_7_5(request):
    obj=helpdata75.objects.all()
    return render(request,"help_page_7_5.html",{'obj':obj})

def card75create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        

        card75=helpdata75(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3)
        card75.save()
        return redirect('card75list')
        
    return render(request,"help_page75create.html")

def card75list(request):
    card75=helpdata75.objects.all()
    return render(request,"help_page75get.html",{'card75':card75})


def card75update(request,id):
    k1=get_object_or_404(helpdata75, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.save()
        return redirect('card75list')
        
    return render(request,"help_page75update.html",{'k1':k1})


def card75delete(request,id):
    data = get_object_or_404(helpdata75,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card75list')
        
    return render(request, 'help_page75delete.html', {'data': data})

    
def help_page_7_6(request):
    obj=helpdata76.objects.all()
    return render(request,"help_page_7_6.html",{'obj':obj})

def card76create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        

        card76=helpdata76(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5)
        card76.save()
        return redirect('card76list')
        
    return render(request,"help_page76create.html")

def card76list(request):
    card76=helpdata76.objects.all()
    return render(request,"help_page76get.html",{'card76':card76})


def card76update(request,id):
    k1=get_object_or_404(helpdata76, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        line5=request.POST.get('line5')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.line5=line5
        k1.save()
        return redirect('card76list')
        
    return render(request,"help_page76update.html",{'k1':k1})


def card76delete(request,id):
    data = get_object_or_404(helpdata76,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card76list')
        
    return render(request, 'help_page76delete.html', {'data': data})


def help_page_7_7(request):
    obj=helpdata77.objects.all()
    return render(request,"help_page_7_7.html",{'obj':obj})

def card77create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        
        

        card77=helpdata77(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5)
        card77.save()
        return redirect('card77list')
        
    return render(request,"help_page77create.html")

def card77list(request):
    card77=helpdata77.objects.all()
    return render(request,"help_page77get.html",{'card77':card77})


def card77update(request,id):
    k1=get_object_or_404(helpdata77, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        line5=request.POST.get('line5')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.line5=line5
        k1.save()
        return redirect('card77list')
        
    return render(request,"help_page77update.html",{'k1':k1})


def card77delete(request,id):
    data = get_object_or_404(helpdata77,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card77list')
        
    return render(request, 'help_page77delete.html', {'data': data})


def help_page_7_8(request):
    obj=helpdata78.objects.all()
    return render(request,"help_page_7_8.html",{'obj':obj}) 

def card78create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        
        

        card78=helpdata78(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5)
        card78.save()
        return redirect('card78list')
        
    return render(request,"help_page78create.html")

def card78list(request):
    card78=helpdata78.objects.all()
    return render(request,"help_page78get.html",{'card78':card78})


def card78update(request,id):
    k1=get_object_or_404(helpdata78, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        line5=request.POST.get('line5')
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.line5=line5
        k1.save()
        return redirect('card78list')
        
    return render(request,"help_page78update.html",{'k1':k1})


def card78delete(request,id):
    data = get_object_or_404(helpdata78,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card78list')
        
    return render(request, 'help_page78delete.html', {'data': data})



def help_page_8_1(request):
        obj=helpdata81.objects.all()
        return render(request,"help_page_8_1.html",{'obj':obj})

def card81create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']

        card81=helpdata81(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4)
        card81.save()
        return redirect('card81list')
        
    return render(request,"help_page81create.html")

def card81list(request):
    card81=helpdata81.objects.all()
    return render(request,"help_page81get.html",{'card81':card81})


def card81update(request,id):
    k1=get_object_or_404(helpdata81, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.save()
        return redirect('card81list')
        
    return render(request,"help_page81update.html",{'k1':k1})


def card81delete(request,id):
    data = get_object_or_404(helpdata81,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card81list')
        
    return render(request, 'help_page81delete.html', {'data': data})



def help_page_8_2(request):
        obj=helpdata82.objects.all()
        return render(request,"help_page_8_2.html",{'obj':obj})

def card82create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']

        card82=helpdata82(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4)
        card82.save()
        return redirect('card82list')
        
    return render(request,"help_page82create.html")

def card82list(request):
    card82=helpdata82.objects.all()
    return render(request,"help_page82get.html",{'card82':card82})


def card82update(request,id):
    k1=get_object_or_404(helpdata82, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.save()
        return redirect('card82list')
        
    return render(request,"help_page82update.html",{'k1':k1})


def card82delete(request,id):
    data = get_object_or_404(helpdata82,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card82list')
        
    return render(request, 'help_page82delete.html', {'data': data})




def help_page_8_3(request):
        obj=helpdata83.objects.all()
        return render(request,"help_page_8_3.html",{'obj':obj})

def card83create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']

        card83=helpdata83(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4)
        card83.save()
        return redirect('card83list')
        
    return render(request,"help_page83create.html")

def card83list(request):
    card83=helpdata83.objects.all()
    return render(request,"help_page83get.html",{'card83':card83})


def card83update(request,id):
    k1=get_object_or_404(helpdata83, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.save()
        return redirect('card83list')
        
    return render(request,"help_page83update.html",{'k1':k1})


def card83delete(request,id):
    data = get_object_or_404(helpdata83,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card83list')
        
    return render(request, 'help_page83delete.html', {'data': data})




def help_page_8_4(request):
        obj=helpdata84.objects.all()
        return render(request,"help_page_8_4.html",{'obj':obj})


def card84create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
    

        card84=helpdata84(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3)
        card84.save()
        return redirect('card84list')
        
    return render(request,"help_page84create.html")

def card84list(request):
    card84=helpdata84.objects.all()
    return render(request,"help_page84get.html",{'card84':card84})


def card84update(request,id):
    k1=get_object_or_404(helpdata84, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.save()
        return redirect('card84list')
        
    return render(request,"help_page84update.html",{'k1':k1})


def card84delete(request,id):
    data = get_object_or_404(helpdata84,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card84list')
        
    return render(request, 'help_page84delete.html', {'data': data})






def help_page_9_1(request):
    obj=helpdata91.objects.all()
    return render(request,"help_page_9_1.html",{'obj':obj})

def card91create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
     

        card91=helpdata91(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1)
        card91.save()
        return redirect('card91list')
        
    return render(request,"help_page91create.html")

def card91list(request):
    card91=helpdata91.objects.all()
    return render(request,"help_page91get.html",{'card91':card91})


def card91update(request,id):
    k1=get_object_or_404(helpdata91, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
    
        k1.save()
        return redirect('card91list')
        
    return render(request,"help_page91update.html",{'k1':k1})


def card91delete(request,id):
    data = get_object_or_404(helpdata91,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card91list')
        
    return render(request, 'help_page91delete.html', {'data': data})




def help_page_9_2(request):
    obj=helpdata92.objects.all()
    return render(request,"help_page_9_2.html",{'obj':obj})

def card92create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']

        card92=helpdata92(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6)
        card92.save()
        return redirect('card92list')
        
    return render(request,"help_page92create.html")

def card92list(request):
    card92=helpdata92.objects.all()
    return render(request,"help_page92get.html",{'card92':card92})


def card92update(request,id):
    k1=get_object_or_404(helpdata92, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        line5=request.POST.get('line5')
        line6=request.POST.get('line6')
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.line5=line5
        k1.line6=line6
        k1.save()
        return redirect('card92list')
        
    return render(request,"help_page92update.html",{'k1':k1})


def card92delete(request,id):
    data = get_object_or_404(helpdata92,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card92list')
        
    return render(request, 'help_page92delete.html', {'data': data})



def help_page_9_3(request):
    obj=helpdata93.objects.all()
    return render(request,"help_page_9_3.html",{'obj':obj})

def card93create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        

        card93=helpdata93(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3)
        card93.save()
        return redirect('card93list')
        
    return render(request,"help_page93create.html")

def card93list(request):
    card93=helpdata93.objects.all()
    return render(request,"help_page93get.html",{'card93':card93})


def card93update(request,id):
    k1=get_object_or_404(helpdata93, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        
        k1.save()
        return redirect('card93list')
        
    return render(request,"help_page93update.html",{'k1':k1})


def card93delete(request,id):
    data = get_object_or_404(helpdata93,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card93list')
        
    return render(request, 'help_page93delete.html', {'data': data})



def help_page_9_4(request):
    obj=helpdata94.objects.all()
    return render(request,"help_page_9_4.html",{'obj':obj})

def card94create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']

        card94=helpdata94(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6)
        card94.save()
        return redirect('card94list')
        
    return render(request,"help_page94create.html")

def card94list(request):
    card94=helpdata94.objects.all()
    return render(request,"help_page94get.html",{'card94':card94})


def card94update(request,id):
    k1=get_object_or_404(helpdata94, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        line5=request.POST.get('line5')
        line6=request.POST.get('line6')
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.line5=line5
        k1.line6=line6
        k1.save()
        return redirect('card94list')
        
    return render(request,"help_page94update.html",{'k1':k1})


def card94delete(request,id):
    data = get_object_or_404(helpdata94,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card94list')
        
    return render(request, 'help_page94delete.html', {'data': data})



def help_page_9_5(request):
    obj=helpdata95.objects.all()
    return render(request,"help_page_9_5.html",{'obj':obj})

def card95create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        

        card95=helpdata95(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5)
        card95.save()
        return redirect('card95list')
        
    return render(request,"help_page95create.html")

def card95list(request):
    card95=helpdata95.objects.all()
    return render(request,"help_page95get.html",{'card95':card95})


def card95update(request,id):
    k1=get_object_or_404(helpdata95, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        line5=request.POST.get('line5')
       
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.line5=line5
        
        k1.save()
        return redirect('card95list')
        
    return render(request,"help_page95update.html",{'k1':k1})


def card95delete(request,id):
    data = get_object_or_404(helpdata95,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card95list')
        
    return render(request, 'help_page95delete.html', {'data': data})



def help_page_9_6(request):
    obj=helpdata96.objects.all()
    return render(request,"help_page_9_6.html",{'obj':obj})



def card96create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        line5=request.POST['line5']
        line6=request.POST['line6']

        card96=helpdata96(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6)
        card96.save()
        return redirect('card96list')
        
    return render(request,"help_page96create.html")

def card96list(request):
    card96=helpdata96.objects.all()
    return render(request,"help_page96get.html",{'card96':card96})


def card96update(request,id):
    k1=get_object_or_404(helpdata96, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        line5=request.POST.get('line5')
        line6=request.POST.get('line6')
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.line5=line5
        k1.line6=line6
        k1.save()
        return redirect('card96list')
        
    return render(request,"help_page96update.html",{'k1':k1})


def card96delete(request,id):
    data = get_object_or_404(helpdata96,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card96list')
        
    return render(request, 'help_page96delete.html', {'data': data})


def help_page_9_7(request):
    obj=helpdata97.objects.all()
    return render(request,"help_page_9_7.html",{'obj':obj})  
    
def card97create(request):
    if request.method=="POST":
        sno=request.POST['sno']
        cardtitle=request.POST['cardtitle']
        qns=request.POST['qns']
        line1=request.POST['line1']
        line2=request.POST['line2']
        line3=request.POST['line3']
        line4=request.POST['line4']
        

        card97=helpdata97(sno=sno,cardtitle=cardtitle,qns=qns,line1=line1,line2=line2,line3=line3,line4=line4)
        card97.save()
        return redirect('card97list')
        
    return render(request,"help_page97create.html")

def card97list(request):
    card97=helpdata97.objects.all()
    return render(request,"help_page97get.html",{'card97':card97})


def card97update(request,id):
    k1=get_object_or_404(helpdata97, id=id)

    if request.method=="POST":
        sno=request.POST.get('sno')
        cardtitle=request.POST.get('cardtitle')
        qns=request.POST.get('qns')
        line1=request.POST.get('line1')
        line2=request.POST.get('line2')
        line3=request.POST.get('line3')
        line4=request.POST.get('line4')
        
        
        k1.sno=sno
        k1.cardtitle=cardtitle
        k1.qns=qns
        k1.line1=line1
        k1.line2=line2
        k1.line3=line3
        k1.line4=line4
        k1.save()
        return redirect('card97list')
        
    return render(request,"help_page97update.html",{'k1':k1})


def card97delete(request,id):
    data = get_object_or_404(helpdata97,id=id)
    if request.method == "POST":
        data.delete()
        return redirect('card97list')
        
    return render(request, 'help_page97delete.html', {'data': data})

from django.shortcuts import render
from .models import AdditionalFormData,Recruitment,Recruitment2

def recruitment_companys_data(request):
    form_data = AdditionalFormData.objects.all()
    k = Recruitment.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    k1= Recruitment2.objects.all()

    return render(request, 'recruitment_companys.html', {'form_data': form_data,'k':k,'links':links,'services':services,'contact_info':contact_info,'social':social,'k1':k1})





from .models import Recruitment

def recruitment_insert(request):
    k=Recruitment.objects.all()

    if request.method=="POST":
        heading=request.POST['heading']
        description1=request.POST.get('description1')
        description2=request.POST.get('description2')
        image=request.FILES.get('image')      
        k=Recruitment(heading=heading,description1=description1,description2=description2,image=image)
        k.save()
        return redirect('recruitment_companys_data')

    return render(request, "recruitment_insert.html")





def Recuitment_table(request):
    if request.method=="GET":
        k=Recruitment.objects.all()
    return render(request, "Recuitment_table.html",{'k':k})    


def recruitment_update(request, pk):
    recruitment = get_object_or_404(Recruitment, pk=pk)

    if request.method == "POST":
        recruitment.heading = request.POST.get('heading')
        recruitment.description1 = request.POST.get('description1')
        recruitment.description2 = request.POST.get('description2')
        if 'image' in request.FILES:
            recruitment.image = request.FILES['image']
        recruitment.save()
        return redirect('recruitment_companys_data')

    return render(request, "Recuitment_update.html", {'recruitment': recruitment})


from django.shortcuts import redirect, get_object_or_404
from .models import Recruitment

def recruitment_delete(request, pk):
    recruitment = get_object_or_404(Recruitment, pk=pk)
    if request.method == "POST":
        recruitment.delete()
        return redirect('recruitment_companys_data')


 
from .models import Recruitment2
def recruitment_insert2(request):
    k=Recruitment2.objects.all()
    if request.method=="POST":
        title=request.POST['title']
        description=request.POST.get('description')
        image=request.FILES.get('image')
        title1=request.POST['title1']
        description1=request.POST.get('description1')
        image1=request.FILES.get('image1')
        title2=request.POST['title2']
        description2=request.POST.get('description2')
        image2=request.FILES.get('image2')

        k=Recruitment2(title=title,description=description,image=image,title1=title1,description1=description1,image1=image1,title2=title2,description2=description2,image2=image2)
        k.save()
        return redirect('recruitment_companys_data')
    return render(request, "Recruitment2_insert.html")   



def Recuitment2_table(request):
    if request.method=="GET":
        k=Recruitment2.objects.all()
    return render(request, "Recuitment2_table.html",{'k':k}) 



        
def recruitment2_update(request, pk):
    recruitment2 = get_object_or_404(Recruitment2, pk=pk)

    if request.method == "POST":
        recruitment2.title = request.POST.get('title')
        recruitment2.description = request.POST.get('description')
        recruitment2.title1 = request.POST.get('title1')
        recruitment2.description1 = request.POST.get('description1')
        recruitment2.title2 = request.POST.get('title2')
        recruitment2.description2 = request.POST.get('description2')
        if 'image' in request.FILES:
            recruitment2.image = request.FILES['image']
        if 'image1' in request.FILES:
            recruitment2.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            recruitment2.image2 = request.FILES['image2']
        recruitment2.save()
        return redirect('recruitment_companys_data')

    return render(request, "Recuitment2_update.html", {'recruitment2': recruitment2})





from django.shortcuts import redirect, get_object_or_404
from .models import Recruitment

def recruitment2_delete(request, pk):
    recruitment2 = get_object_or_404(Recruitment2, pk=pk)
    if request.method == "POST":
        recruitment2.delete()
        return redirect('recruitment_companys_data')
        
        
        
        


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Companys, AdditionalFormData, Applicant, CustomUser

def job_application(request, companyid):
    company = get_object_or_404(Companys, id=companyid)
    job_listings = AdditionalFormData.objects.filter(companyid=company)

    if not job_listings.exists():
        return render(request, 'admin-template/error.html', {'message': 'No job listings found for this company.'})

    job_listing = job_listings.first()  
    skills_list = job_listing.skills.split(',') 
    education_list = job_listing.education.split(',') 
    work_experience_list = job_listing.work_experience.split(',') 
    branch_list = job_listing.branch.split(',') 


    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter')
        education = request.POST.get('education')
        branch = request.POST.get('branch')

        work_experience = request.POST.get('work_experience')
        skills = request.POST.get('skills')

        if full_name and email and phone_number and resume and cover_letter and education and work_experience and skills:
            applicant = Applicant(
                company_id=company,  
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                resume=resume,
                cover_letter=cover_letter,
                education=education,
                branch=branch,
                work_experience=work_experience,
                skills=skills,
                job_listing=job_listing  
            )

            applicant.save()
            messages.success(request, "You are Successfully applied for this job application")

            send_mail(
                'Thank You for Your Application',
                f'''
                Dear {full_name},

                Thank you for applying for the position at {job_listing.companyid.organizationname}.

                We have received your application and our team is currently reviewing it. If your qualifications match our requirements, we will reach out to you to discuss the next steps in the hiring process.

                In the meantime, if you have any questions or need further information, please do not hesitate to contact us.

                Thank you again for your interest in joining our team. We appreciate the time and effort you put into your application.

                Best regards,
                {job_listing.companyid.organizationname}

                Contact Information:
                Phone: {job_listing.companyid.phone_number}
                Email: {job_listing.companyid.email}
                Website: {job_listing.companyid.organizationname}
                ''',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return redirect('/recruitment_companys_data')
        else:
            error_message = "Please fill in all required fields."
    else:
        error_message = None

    context = {
        'job_listing': job_listing,
        'error_message': error_message,
        'skills_list': skills_list,
        'education_list': education_list,
        'work_experience_list': work_experience_list,
        'branch_list': branch_list

    }

    return render(request, 'job_application.html', context)


def planintroinst(request):
    if request.method == "POST":
        getapl=request.POST['getapl']
        rightplan=request.POST['rightplan']
        forcont=request.POST['forcont']
        freetrails=request.POST['freetrails']

        k=priceingintro(getapl=getapl,rightplan=rightplan,forcont=forcont,freetrails=freetrails)
        k.save()
        return redirect("/plan_intro_retrive")
    return render(request,"plan_intro_inst.html")

def planintroupdate(request, pk):
    pint = get_object_or_404(priceingintro, pk=pk)

    if request.method == "POST":
        pint.getapl = request.POST["getapl"]
        pint.rightplan = request.POST["rightplan"]
        pint.forcont = request.POST["forcont"]
        pint.freetrails = request.POST["freetrails"]
        pint.save()
        return redirect("/plan_intro_retrive")

    return render(request, "planintroupdate.html", {"pint": pint})   
 
def plan_intro_retrive(request):
    pints = priceingintro.objects.all()
    return render(request, "plan_intro_retrive.html", {"pints": pints})


def planintrodelete(request, pk):
    pint = get_object_or_404(priceingintro, pk=pk)    
    if request.method == "POST":
        pint.delete()
        return redirect("plan_intro_retrive")
    return render(request, "planintrodelete.html", {"plnt": pint})
  
def retrive_helpcards(request):
    d3=documents_qns.objects.all()
    o3=organization_qns.objects.all()
    return render(request,"retrive_helpcards.html",{ 'd3': d3,'o3' : o3 })