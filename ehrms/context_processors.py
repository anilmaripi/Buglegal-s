
from pyexpat.errors import messages
from tkinter.messagebox import NO

from ehrms.Employviews import Employ_home
from .models import CustomUser, employnav,Employs,NotificationEmploy,companylogo,NavbarItem,Footer1,Companys,company_details,Addonsuser,adminnav,admin_drop,project_drop,FooterLink,FooterService,ContactInfo,SocialLink
from.models import *

def member_logged(request):
    try:
        mem_employee123 = Employs.objects.filter(admin=request.user.id).first()
        mem_role = mem_employee123.role
        mem_hroptions = mem_employee123.hroptions
        mem_projectmanagerop = mem_employee123.projectmanagerop
        mem_team_lead_ext = TeamMember.objects.filter(employee=mem_employee123, is_team_lead=True).exists()
    except:
        mem_employee123 = 0
        mem_role = None
        mem_hroptions = None
        mem_projectmanagerop = None
        mem_team_lead_ext = 0

        
    return{'mem_team_lead_ext': mem_team_lead_ext,
             'mem_role':mem_role,
             'mem_hroptions': mem_hroptions,
             'mem_projectmanagerop': mem_projectmanagerop}


def dynamic_nav(request):
    # Retrieve the navigation items
    try:
        a=companylogo.objects.all()
        s=employnav.objects.all()
        employ_obj=Employs.objects.get(admin=request.user.id)
        

        notification1=NotificationEmploy.objects.filter(employ_id=employ_obj.id)
        notifications1=NotificationEmploy.objects.filter(employ_id=employ_obj.id).count()
    # You can perform any additional logic or filtering here if needed
    except Employs.DoesNotExist:
        # Handle the case where the Employ object doesn't exist
        employ_obj = None
        notifications1 = 0
        notification1 = 0
    # Return the navigation items in a dictionary
    return {'s': s,'notifications1':notifications1,'notification1':notification1,'a':a}


def navbar(request):
    navbar_items = NavbarItem.objects.filter(parent=None)
    footer_item=Footer1.objects.all()
    var1=(request.path)
    allurls=['/all_employmonitring/','/timetracking_all_projects/','/timeattendance_all_projects/','/productivity_all_projects/','/screenmonitoring_all_projects/','/all_activemonitring/','/officework_all_projects/','/all_projects/','/regprivacy/','/home_ac/']
    planurls=['/admincontrol2/','/admincontrol3/','/admincontrol/','/New_Add_ons/','/New_Add_ons_table/','/freetrailtable/','/plandataretrive/']

    for item in navbar_items:
        item.is_active = item.is_active(request.path)
    return {'navbar_items':navbar_items,'footer_item':footer_item,'var1':var1,'allurls':allurls,'planurls':planurls}
def footer(request):
    footer_item=Footer1.objects.all()
    links = FooterLink.objects.all()
    services = FooterService.objects.all()
    contact_info = ContactInfo.objects.first()
    social = SocialLink.objects.all()
    return {'footer_item':footer_item,'links':links,'services':services,'contact_info':contact_info,'social':social}

from django.db.models import Q

def sidenav(request):
   loginuse=CustomUser.objects.filter(id=request.user.id).first()
   if loginuse:
      logusertype=loginuse.user_type
   else:
       logusertype=None
   palnid=None
   organization=None
   data=None
   s=None
   a=None
   admin_drops=None
   addon_drops=None
   complan=None
   addon=None
   palnid=None
   organization_name=None
   projects_drops=None
   teamleadop=None
   checkcheckin=None
   checkcheckout=None
   
   if logusertype == "1":
        organization_name=None
        projects_drops=None
        palnid=None
        data = Companys.objects.filter(usernumber=request.user.id).first()
        if data:
           organization=data.organizationname
           complan=data.plantype
        else:
            organization=None
            complan=None
        a=company_details.objects.filter(companyid=data).first()
        cef_url = adminaddnav.objects.filter(admin_add_option=1)
        cef=cafeteria_allowance.objects.filter(companyid=data,check_field='Enabled')
  
        addon=Addonsuser.objects.filter(companyid=data).values_list('plan', flat=True)
        if complan=="1":    
          s=adminnav.objects.all()
          if addon:
              admin_drops=admin_drop.objects.filter(Q(parent_category=None,show1 = 1) | Q(parent_category=None,name__in=addon)).order_by('id')
          else:
             admin_drops=admin_drop.objects.filter(parent_category=None,show1 = 1).order_by('id')
              
        elif complan== "2":
            s=adminnav.objects.all()
            if addon:
              admin_drops=admin_drop.objects.filter(Q(parent_category=None,show2 = 1) | Q(parent_category=None,name__in=addon)).order_by('id')
            else:
             admin_drops=admin_drop.objects.filter(parent_category=None,show2 = 1).order_by('id')
     
        elif complan== "3":
            s=adminnav.objects.all()
            if addon:
              admin_drops=admin_drop.objects.filter(Q(parent_category=None,show3 = 1) | Q(parent_category=None,name__in=addon)).order_by('id')
            else:
             admin_drops=admin_drop.objects.filter(parent_category=None,show3 = 1).order_by('id')
    
        else:
            s=adminnav.objects.all()
            admin_drops=admin_drop.objects.filter(parent_category=None,show=1).order_by('id')
   elif logusertype == "2":
       organization=None
       complan=None
       addon=None
       data=Employs.objects.filter(admin=request.user.id).first()
       compid = data.companyid
       cef_url = adminaddnav.objects.filter(employ_add_option=1)
       cef=cafeteria_allowance.objects.filter(companyid=compid,check_field='Enabled')


       if data:
            data1=data.id
            data2=data.hroptions
            project_manager=data.projectmanagerop
            receptionist=data.receptionist_option

            compid=data.companyid
            email=data.email
            today=datetime.today()
            regname=Companys.objects.filter(id=data.companyid.id).first()
            organization_name=regname.organizationname
            a=company_details.objects.filter(companyid=compid).first()
            findcompid=Companys.objects.filter(id=data.companyid.id).first()
            palnid=findcompid.plantype
            checkcheckin=checkin.objects.filter(empid=email,date=today)
            checkcheckout=checkout.objects.filter(empid=email,date=today)
            hr_cont=hr_controls.objects.filter(employ_name=data1).values_list('field_name',flat=True)
            teamleadop= TeamMember.objects.filter(employee=data1,is_team_lead=1)
            monitoring=['screen monitoring','detailed monitoring','powerlogs','screenshots']
            addoncheck=Addonsuser.objects.filter(companyid=compid,plan__in=monitoring)
            if palnid == "1":
                if data2:
                    s=employnav.objects.filter(is_name_exist=1,hr_options=1,show1=1).exclude(url="/calendar/")
                elif project_manager:
                    s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show1=1).exclude(url="/calendar/")

                elif receptionist:
                    s=employnav.objects.filter(is_name_exist=1,recepionist_option=1,show1=1).exclude(url="/calendar/")

                elif teamleadop:
                    s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show1=1).exclude(url="/calendar/")

                else:
                    s=employnav.objects.filter(is_name_exist=1,employ_options=1,show1=1).exclude(url="/calendar/")
                projects_drops=project_drop.objects.filter(parent_category=None,show1=1).order_by('id')
                if hr_cont:
                      admin_drops=employ_drop.objects.filter(parent_category=None,show1=1,name__in=hr_cont).order_by('id')
                else:
                    admin_drops=None
            elif palnid == "2":
                # if data2:
                #     s=employnav.objects.filter(is_name_exist=1,hr_options=1,show2=1)

                # elif project_manager:
                #     s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show2=1)

                # elif receptionist:
                #     s=employnav.objects.filter(is_name_exist=1,receptionist_option=1,show2=1)

                # elif teamleadop:
                #     s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show2=1)
                
            
                # else:
                #     s=employnav.objects.filter(is_name_exist=1,employ_options=1,show2=1)
                if data2:
                    if addoncheck: 
                        s=employnav.objects.filter(is_name_exist=1,hr_options=1,show2=1).exclude(url="/secondcalendar/")
                    else:
                        s=employnav.objects.filter(is_name_exist=1,hr_options=1,show2=1).exclude(url="/calendar/")

                elif project_manager:
                    if addoncheck:
                        s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show2=1).exclude(url="/secondcalendar/")
                    else:
                        s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show2=1).exclude(url="/calendar/")

                    
                elif receptionist:
                    if addoncheck:
                        s=employnav.objects.filter(is_name_exist=1,receptionist_option=1,show2=1).exclude(url="/secondcalendar/")
                    else:
                        s=employnav.objects.filter(is_name_exist=1,receptionist_option=1,show2=1).exclude(url="/calendar/")



                elif teamleadop:
                    if addoncheck:
                        s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show2=1).exclude(url="/secondcalendar/")
                    else:
                        s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show2=1).exclude(url="/calendar/")
            
                else:
                    if addoncheck:
                        s=employnav.objects.filter(is_name_exist=1,employ_options=1,show2=1).exclude(url="/secondcalendar/")
                    else:
                        s=employnav.objects.filter(is_name_exist=1,employ_options=1,show2=1).exclude(url="/calendar/")
                # if data2:
                #      if addoncheck:
                #          s=employnav.objects.filter (is_name_exist=1,hr_options=1,show2=1)  and  employnav.objects.exclude(url="/calendar2/")  | employnav.objects.filter(is_name_exist=1,hr_options=1,plantype=0,)
                #      else:
                #          s=employnav.objects.filter(is_name_exist=1,hr_options=1,show2=1)
                # elif project_manager:
                #     if addoncheck:
                #         s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show2=1) and employnav.objects.exclude(url="/calendar2/")  | employnav.objects.filter(is_name_exist=1,projectmanager_options=1,plantype=0,)
                #     else:
                #         s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show2=1) 
                # elif teamleadop:
                #     if addoncheck:
                #         s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show2=1)  and  employnav.objects.exclude(url="/calendar2/")  | employnav.objects.filter(is_name_exist=1,is_tl_option=1,plantype=0,)
                #     else:
                #         s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show2=1) 
            
                # else:
                #     if addoncheck:
                #        s=employnav.objects.filter(is_name_exist=1,employ_options=1,show2=1)  and  employnav.objects.exclude(url="/calendar2/")  | employnav.objects.filter(is_name_exist=1,employ_options=1,plantype=0,)
                #     else:
                #        s=employnav.objects.filter(is_name_exist=1,employ_options=1,show2=1) 


                projects_drops=project_drop.objects.filter(parent_category=None,show2=1).order_by('id')
                if hr_cont:
                       admin_drops=employ_drop.objects.filter(parent_category=None,show2=1,name__in=hr_cont).order_by('id')
                else:
                       admin_drops=None                
            elif palnid == "3":
                if data2:
                    s=employnav.objects.filter(is_name_exist=1,hr_options=1,show3=1).exclude(url="/secondcalendar/")

                elif project_manager:
                    s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show3=1).exclude(url="/secondcalendar/")

                elif receptionist:
                    s=employnav.objects.filter(is_name_exist=1,receptionist_option=1,show3=1).exclude(url="/secondcalendar/")


                elif teamleadop:
                    s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show3=1).exclude(url="/secondcalendar/")

                else:
                    s=employnav.objects.filter(is_name_exist=1,employ_options=1,show3=1).exclude(url="/secondcalendar/")
                projects_drops=project_drop.objects.filter(parent_category=None,show3=1).order_by('id')
                if hr_cont:
                      admin_drops=employ_drop.objects.filter(parent_category=None,show3=1,name__in=hr_cont).order_by('id')
                else:
                      admin_drops=None

            
            else:
                if data2:
                    s=employnav.objects.filter(is_name_exist=1,hr_options=1).exclude(url="/secondcalendar/")
                elif project_manager:
                    s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1).exclude(url="/secondcalendar/")
                elif receptionist:
                    s=employnav.objects.filter(is_name_exist=1,receptionist_option=1).exclude(url="/secondcalendar/")


                elif teamleadop:
                    s=employnav.objects.filter(is_name_exist=1,is_tl_option=1).exclude(url="/secondcalendar/")
                

                else:
                    s=employnav.objects.filter(is_name_exist=1,employ_options=1).exclude(url="/secondcalendar/")
                    
                projects_drops=project_drop.objects.filter(parent_category=None,show3=1).order_by('id')
                if hr_cont:
                    admin_drops=employ_drop.objects.filter(parent_category=None,name__in=hr_cont).order_by('id')
                else:
                    admin_drops=None
            
       
    
   else:
                organization=None
                data=None
                s=None
                a=None
                admin_drops=None
                addon_drops=None
                complan=None
                addon=None
                palnid=None
                organization_name=None
                projects_drops=None
                teamleadop=None
                checkcheckin=None
                checkcheckout=None
                cef_url=None
                cef=None
                addoncheck=None
   return{'organization':organization,'checkcheckin':checkcheckin,'checkcheckout':checkcheckout,'palnid':palnid,'organization_name':organization_name,'projects_drops':projects_drops,  'data':data, 's':s,'a':a,'admin_drops':admin_drops,'complan':complan,'addon':addon,'teamleadop':teamleadop, 'logusertype':logusertype,'cef_url':cef_url,'cef':cef}


def supadminprofilepic(request):
    try:
      supcheck=CustomUser.objects.filter(id=request.user.id,is_superuser=1).first()
      if supcheck:
        superadminpic=adminphoto.objects.all()
      else:
          superadminpic=None
    except CustomUser.DoesNotExist:
        supcheck=None
    return{'superadminpic':superadminpic}


# def employeesidenav(request):
#     try:
#        data=Employs.objects.filter(admin=request.user.id).first()
#        palnid=None
#        organization_name=None
#        a=None
#        s=None
#         projects_drops=None
#         admin_drops=None
#        if data:
#             data1=data.id
#             data2=data.hroptions
#             project_manager=data.projectmanagerop
#             compid=data.companyid
#             regname=Companys.objects.filter(id=data.companyid.id).first()
#             organization_name=regname.organizationname
#             a=company_details.objects.filter(companyid=compid).first()
#             findcompid=Companys.objects.filter(id=data.companyid.id).first()
#             palnid=findcompid.plantype
#             teamleadop= TeamMember.objects.filter(employee=data1,is_team_lead=1)
#             if palnid == "1":
#                 if data2:
#                     s=employnav.objects.filter(is_name_exist=1,hr_options=1,show1=1)
#                 elif project_manager:
#                     s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show1=1)
#                 elif teamleadop:
#                     s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show1=1)
#                 else:
#                     s=employnav.objects.filter(is_name_exist=1,employ_options=1,show1=1)
#                 projects_drops=project_drop.objects.filter(parent_category=None,show1=1).order_by('id')
#                 admin_drops=employ_drop.objects.filter(parent_category=None,show1=1).order_by('id')
#             elif palnid == "2":
#                 if data2:
#                     s=employnav.objects.filter(is_name_exist=1,hr_options=1,show2=1)

#                 elif project_manager:
#                     s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show2=1)


#                 elif teamleadop:
#                     s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show2=1)
            
#                 else:
#                     s=employnav.objects.filter(is_name_exist=1,employ_options=1,show2=1)
#                 projects_drops=project_drop.objects.filter(parent_category=None,show2=1).order_by('id')
#                 admin_drops=employ_drop.objects.filter(parent_category=None,show2=1).order_by('id')
                
#             elif palnid == "3":
#                 if data2:
#                     s=employnav.objects.filter(is_name_exist=1,hr_options=1,show3=1)

#                 elif project_manager:
#                     s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1,show3=1)

#                 elif teamleadop:
#                     s=employnav.objects.filter(is_name_exist=1,is_tl_option=1,show3=1)

#                 else:
#                     s=employnav.objects.filter(is_name_exist=1,employ_options=1,show3=1)
#                 projects_drops=project_drop.objects.filter(parent_category=None,show3=1).order_by('id')
#                 admin_drops=employ_drop.objects.filter(parent_category=None,show3=1).order_by('id')
#             else:
#                 if data2:
#                     s=employnav.objects.filter(is_name_exist=1,hr_options=1)
#                 elif project_manager:
#                     s=employnav.objects.filter(is_name_exist=1,projectmanager_options=1)

#                 elif teamleadop:
#                     s=employnav.objects.filter(is_name_exist=1,is_tl_option=1)

#                 else:
#                     s=employnav.objects.filter(is_name_exist=1,employ_options=1)
                    
#                 projects_drops=project_drop.objects.filter(parent_category=None,show3=1).order_by('id')
#                 admin_drops=employ_drop.objects.filter(parent_category=None,show3=1).order_by('id')
#     except Employs.DoesNotExist:
#         data1=None
#         data2=None
#         organization_name=None
#         project_manager=None
#         compid=None
#         a=None
#         s=None
#         projects_drops=None
#         admin_drops=None
#         palnid=None

#     return{'palnid':palnid,'organization_name':organization_name,'a':a,'s':s,'projects_drops':projects_drops,'admin_drops':admin_drops}




          
      



    


