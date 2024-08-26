import datetime
from typing import Any
from django.contrib.auth import logout
from ehrms.models import Companys,Employs,Addonsuser,freetraildays,working_shifts
from django.utils import timezone
from datetime import datetime,timedelta
import pytz
class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get free trial days configuration
        free = freetraildays.objects.first()
        if free:
            freeday = free.freedays
            month = free.monthly
            year = free.yearly
        else:
            freeday = 15
            month = 20
            year = 35
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            companys = Companys.objects.filter(usernumber=request.user.id).first()
            loginemploy = Employs.objects.filter(admin=request.user.id).first()
            current_date1 = datetime.now(pytz.utc)
            addonu = None
            
            if loginemploy:
                compid = Companys.objects.filter(id=loginemploy.companyid.id).first()
            
            if companys:
                plandate = companys.date
                fretraile = companys.freetraile
                addonu = Addonsuser.objects.filter(companyid=companys).first()
            
            elif loginemploy:
                plandate = compid.date
                fretraile = compid.freetraile
            
            else:
                addonu = None
                plandate = None
            
            # Handle addonu object
            if addonu:
                addondate = addonu.date
                addondelete = datetime.combine(addondate, datetime.min.time(), tzinfo=pytz.utc)
            else:
                addondate = None
            
            # Handle plandate object
            if plandate:
                logindate_datetime = datetime.combine(plandate, datetime.min.time(), tzinfo=pytz.utc)
            else:
                logindate_datetime = None
            
            # Check expiration conditions and logout if necessary
            if plandate and (current_date1 - logindate_datetime).days > freeday and fretraile == 1:
                logout(request)
            elif plandate and (current_date1 - logindate_datetime).days > month and fretraile == 0:
                logout(request)
            elif plandate and (current_date1 - logindate_datetime).days > year and fretraile == 2:
                logout(request)
            
            # Check addon expiration and delete if necessary
            if addondate and (current_date1 - addondelete).days > 30:
                addonu.delete()
        
        # Continue with the response
        response = self.get_response(request)
        return response    

from .utils import *
class emppresent:
     def __init__(self,get_response):
           self.get_response=get_response
     def __call__(self,request):
        data=Employs.objects.filter(admin=request.user.id).first()
        if data:
               compid=data.companyid
               wekk=data.working12
               email=data.email
               today = datetime.now().date()
               yesterday=datetime.now().date()-timedelta(days=1)
               tdelta = dursec(request,today)
               ddd=working_shifts.objects.filter(companyid=compid,shift_name=wekk)
               checkincheck=checkin.objects.filter(empid=email,date=today)
               checkoutcheck=checkout.objects.filter(empid=email,date=today)
               checkincheckyesterday=checkin.objects.filter(empid=email,date=yesterday)
               checkoutcheckyesterday=checkout.objects.filter(empid=email,date=yesterday)
               if checkincheck:
                    checkup=checkin.objects.get(empid=email,date=today)
                    total_leavetime = sum([leave.get_shift_duration() for leave in ddd])
                    toatalhalf=total_leavetime/2
                    if checkoutcheck:
                         if total_leavetime <= tdelta:
                              checkup.status="present"
                              checkup.save()
                         elif toatalhalf <= tdelta:
                              checkup.status="Halfday"
                              checkup.save()
                         elif toatalhalf >= tdelta:
                                   checkup.status="Absent"
                                   checkup.save()
               if checkincheckyesterday:
                    checkupyesterday=checkin.objects.get(empid=email,date=yesterday)
                    if checkincheckyesterday and not checkoutcheckyesterday:
                         checkupyesterday.status="Absent"
                         checkupyesterday.save()   
        response = self.get_response(request)
        return response

from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve
from ehrms import adminviews,Employviews
class Logincheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_path = request.path
        resolved_view = resolve(request.path)
        superadmin_required_views = ['adminAdashboard','company_list1','company_list2','company_list3','company_list4','adminA_Password_save','upload_image','display_plans','company_list','update_plan','delete_plan','formdeatiles','delete_company_list1','retrieve_contact_messages','delete_selected_messages','solution5','delete_customer_data','all_employmonitring','edit_employee_index','delete_employee_index','employeemonitoring2','edit_employeeindex1','delete_employeeindex1','employeemonitoring3','edit_employeeindex2','delete_employeeindex2','timetracking1_create','timetracking1_update','timetracking_all_projects','timetracking1_delete','timetracking2_create','timetracking2_update','timetracking2_delete','timetracking3_create','timetracking3_update','timetracking3_delete','timetracking4_create','timetracking4_update','timetracking4_delete','timeattendance_all_projects','timeattendance1_create','timeattendance1_update','timeattendance1_delete','timeattendance2_create','timeattendance2_update','timeattendance2_delete','timeattendance3_create','timeattendance3_update','timeattendance3_delete','timeattendance4_create','timeattendance4_update','timeattendance4_delete','productivity_all_projects','productivity1_update','productivity1_delete','productivity2_update','productivity2_delete','productivity3_update','productivity3_delete','productivity4_update','productivity4_delete','screenmonitoring_all_projects','screenmonitoring1_update','screenmonitoring1_delete','screenmonitoring2_update','screenmonitoring2_delete',
                                     'screenmonitoring3_update','screenmonitoring3_delete','all_activemonitring','projectmanagement_create','edit_monitoring_data','delete_monitoring_data','edit_monitoring2_data','delete_monitoring2_data','edit_monitoring3_data','delete_monitoring3_data','edit_monitoring4_data','delete_monitoring4_data','officework_all_projects','officework1_create','officework1_update','officework1_delete','officework2_create','officework2_update','officework2_delete','officework3_create','officework3_update','officework3_delete','officework4_create','officework4_update','officework4_delete','all_projects','projectmanagement_create','projectmanagement_update','projectmanagement_delete','projectmanagement2_create','projectmanagement2_update','projectmanagement2_delete','projectmanagement3_create','projectmanagement3_update','projectmanagement3_delete','regprivacy','inserted','privacyedit','deletepri','home_ac','insert_ac','edit_ac','delete_ac',
                                     'admincontrol','admincontrol2','admincontrol3','New_Add_ons','New_Add_ons_table','addonsupdate','Delete_New_Add_ons','freetrailtable','freetrailupdate','plandataretrive','plandatas','plandataupdate','plandatadelete','retrive_conditions','terms_conditions1','edit_terms_condition','delete_condition','privacy_policy_table','privacy_policy_insert','privacy_policy_edit','privacy_policy_delete','cancellation_policy_table','cancellation_policy_insert','cancellation_policy_edit','delete_policy_cancellation',]
        view_name = resolved_view.func.__name__
        log_not = ['/', '/show_login/', '/doLogin', '/employeemonitoring/', '/timetracking/', '/timeattendance/',
                   '/productivity/', '/screenmonitoring/', '/activitymonitoring/', '/officework/', '/projectmanagment/',
                   '/displayprivacy/', '/display_ac/','/Admin_Control/','/Productivity_Monitoring/', '/subscription/', '/register_company/1/', '/register_company/2/',
                   '/register_company/3/', '/register_company/4/', '/terms_conditions2/', '/privacy_policy2/','/documents/','/documents1/','/documents2/','/documents3/','/documents4/','/documents5/','/documents6/','/documents7/','/documents8/','/documents9/',
                   '/Cancellation_policy/', '/solution1/', '/addonauthentication/', '/Our_Team', '/aboutuspage/','/home_visitor_entrance/','/help_page_card7/','/help_page_card8/','/help_page_card9/','/help_page_7_1/','/help_page_7_2/','/help_page_7_3/','/help_page_7_4/','/help_page_7_5/','/help_page_7_6/','/help_page_7_7/','/help_page_7_8/','/help_page_8_1/','/help_page_8_2/','/help_page_8_3/','/help_page_8_4/','/help_page_9_1/','/help_page_9_2/','/help_page_9_3/','/help_page_9_4/','/help_page_9_5/','/help_page_9_6/','/help_page_9_7/','/recruitment_companys_data/',
                   '/contact/','/retriev_helpfeature/' ,'/buglegal_start1/',  '/retriev_card1/', '/managingdata_retriev/', '/retrieve_setupqn3/','/documents_card/', '/abouttime_qns1/', '/retriev_clock/','/retriev_assignans3/','/retriev_breaksqns4/','/retriev_faq5/','/freetrail_retrieve/','/organization_card/', '/timetrack_qnsd/','/payrol_qnsd/','contact/success/', '/ehrms/password_reset/', '/store_phone_number/', '/send_otp/','/ehrms/password_reset/done/','/check_username_existadmin/','/check_email_existadmin/','/accounts/login/','/accounts/inactive/','/accounts/signup/','/accounts/reauthenticate/','/accounts/email/','/accounts/confirm-email/','/planupdate/',
                   '/company-form/','/social_login_complete/','/handle_payment/','/retriev_payroll1/','/retriev_addempqns2/','/retriev_reimbursementqns3/','/retriev_requestqns4/','/retriev_advanceqns5/','/organization/','/organization1/','/organization2/','/organization3/','/organization4/','/organization5/','/organization6/','/organization7/','/organization8/','/organization9/',
                   '/resend_otp/', '/verify_otp/','/planexpireauthentication1/','/planexpireauthentication/','/planexpire_payment/','/planexpire_payment1/','/addonfectures/','/record_system_status/','/client_record_activity/','/client_stop_monitoring/','/client_capture/','/get_employee_and_company/','/check_launch/','/planupdate1/','/edit_term/1001','/edit_term/1002','/edit_term/1003','/face_display/','/Face_Recognition/','/face_insert/','/facereading/','/Payroll_Feature/','/home_employee_performance/','/Employee_Performance/','/home_leave_management/','/home_tl_management/','/Team_lead_Management/','/HR_Management/','/Shift_Management/',
                   '/Terms_and_Conditions/','/Privacy_and_Policy/','/Cancellation_Policy/']

        if self.is_exempted_path(current_path,request):
            return self.get_response(request)
        
        if current_path.startswith('/accounts/'):
             return self.get_response(request)
    
        
        if current_path == '/admin/login/' or current_path.startswith('/admin/'):
            return self.get_response(request)   

        if current_path not in log_not:
            if not request.user.is_authenticated:
                return redirect("/show_login/")
        if request.user.is_authenticated:
            if request.user.user_type == "1":
                if resolved_view.func.__module__ == adminviews.__name__:
                    return self.get_response(request)
                elif resolved_view.func.__module__ == Employviews.__name__:
                    return redirect("/admin_home")
                elif view_name in superadmin_required_views:
                    return redirect("/admin_home")
            elif request.user.user_type == "2":
                if resolved_view.func.__module__ == Employviews.__name__:
                    return self.get_response(request)
                elif resolved_view.func.__module__ == adminviews.__name__:
                    return redirect("/Employ_home/")
                elif view_name in superadmin_required_views:
                    return redirect("/Employ_home/")
            if request.user.is_superuser:
                  if view_name in superadmin_required_views:
                       return self.get_response(request)
                  elif resolved_view.func.__module__ == adminviews.__name__:
                    return redirect("/adminAdashboard/")
                  elif resolved_view.func.__module__ == Employviews.__name__:
                    return redirect("/adminAdashboard/")

        response = self.get_response(request)
        return response

    def is_exempted_path(self, path,request):
        planexp1=request.session.get('order_idpex1')
        planexp=request.session.get('order_idpex')
        planex=request.session.get('order_idpex2')



        exempted_urls = [
            'https://cdn.jsdelivr.net/',
            'https://cdnjs.cloudflare.com/ajax/libs/',
            'https://code.jquery.com/',
            'https://unpkg.com/',
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js",
            "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js",
            "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js",
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.10.1/gsap.min.js",
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css",
            "https://unpkg.com/swiper/swiper-bundle.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap",
            "https://www.yudiz.com/codepen/animation-form/banner.jpg",
            'https://api.cashfree.com/pg/orders',
            'https://sdk.cashfree.com/js/v3/cashfree.js',
            f'https://buglegal.com/planupdate1/?order_id={planexp1}',
            f"https://api.cashfree.com/pg/orders/{planexp1}",
            f'https://buglegal.com/planupdate/?order_id={planexp}',
            f"https://api.cashfree.com/pg/orders/{planexp}",
            f'https://buglegal.com/handle_payment/?order_id={planexp}',
            f"https://api.cashfree.com/pg/orders/{planexp}",
            'https://buglegal.com/record_system_status/',
            'https://buglegal.com/client_record_activity/',
            'https://buglegal.com/client_stop_monitoring/',
            'https://buglegal.com/client_capture/',
            'https://buglegal.com/get_employee_and_company/',
            'https://buglegal.com/check_launch/',
            settings.MEDIA_URL,  
            settings.STATIC_URL, 
        ]
        for url in exempted_urls:
            if path.startswith(url):
                return True
            
        exempted_extensions = ['.css', '.png', '.js','.ico','.jpg']
        for ext in exempted_extensions:
            if path.endswith(ext):
                return True
        return False


from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from notifications.signals import notify
from .models import Employs, checkin, checkout, working_shifts, ExtraTimeSlot
class AutoCheckoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            data = Employs.objects.filter(admin=request.user.id).first()
            if not data:
                return

            email = data.email
            today = datetime.now().date()
            now = datetime.now()
            check_in = checkin.objects.filter(date=today, empid=email).first()
            check_out = checkout.objects.filter(date=today, empid=email).first()
            workings = working_shifts.objects.filter(shift_name=data.working12, companyid=data.companyid).first()
            extra_time_slots = ExtraTimeSlot.objects.filter(employees=data)
            if workings:
                starting_time = workings.starting_time
                extra_time1 = workings.extra_time1
                ending_time = workings.ending_time
                ending_datetime = datetime.combine(today, ending_time)
                default_extra_time = timedelta(minutes=extra_time1)
                assigned_extra_time = sum(slot.duration for slot in extra_time_slots)
                extra_time_from_slots = timedelta(minutes=assigned_extra_time)
                total_extra_time = default_extra_time + extra_time_from_slots
                auto_checkout_time = ending_datetime + total_extra_time
                reminder_time = auto_checkout_time - timedelta(minutes=2)  
                if now >= reminder_time and now < auto_checkout_time:
                    notify.send(
                        sender=request.user,
                        recipient=data.admin,
                        verb='Checkout Reminder',
                        description='Please remember to check out. You will be automatically checked out as absent in 2 minutes.'
                    )
                    messages.info(request, 'Reminder: Please remember to check out.')
                if check_in and not check_out and now > auto_checkout_time:
                    checkout.objects.create(
                        date=today,
                        time=now.time(),
                        empid=email,
                        shift_name=workings.shift_name,
                        date_value=1,
                        companyid=data.companyid,
                        is_employee="1"
                    )
                    check_in.status = 'absent'
                    check_in.save()
                    messages.success(request, 'You have been automatically checked out as absent.')
                    total_extra_time_used = (now - ending_datetime).total_seconds() // 60
                    remaining_extra_time = max(assigned_extra_time - total_extra_time_used, 0)
                    data.extra_time = remaining_extra_time
                    data.save()