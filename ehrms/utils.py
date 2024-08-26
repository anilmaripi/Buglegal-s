
from datetime import datetime, timedelta,date
from calendar import HTMLCalendar
from datetime import date, timedelta
import datetime
import email

from .models import checkin,checkout,LeaveReportEmploy,Employs,editholiday12,customholidays,publicholidays,LeaveReportAdmin,Companys
import calendar
from django.http import HttpRequest

def get_empid(request):
    email=request.session.get('email_2');
    return email
def get_people(request):
    std = request.session.get('employ_id')
    if request.path == '/hod_calendar/':
         if std is not None:
            del request.session['employ_id']

    return std
def getcompanyid(request):
    data1= request.session.get['data1']
    return data1

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, day=None):
        self.year = year
        self.month = month
        self.day=day
        super(Calendar, self).__init__()
       
    

    def formatday(self,request, day):
        
        d = ''
       
        if day != 0:
           
             
            if date.today() == date(self.year, self.month, day):
                return f"<td style='border: 2px solid #ffffff;'>{day}</td>"
            else:
                people_id=get_people(request)
                pemail=Employs.objects.filter(admin=people_id).first()
                eid=get_empid(request)
                if people_id:
                    q=checkin.objects.filter(date=date(self.year, self.month, day),empid=pemail.email) 
                    k=LeaveReportEmploy.objects.filter(email_leave=pemail.email)
                else:
                    q=checkin.objects.filter(date=date(self.year, self.month, day),empid=eid) 
                    k=LeaveReportEmploy.objects.filter(email_leave=eid)
                l=LeaveReportEmploy.objects.filter(to_date=date(self.year, self.month, day))
                # k.(leave_date=date(self.year, self.month, day))
                for i in k:
                    if i.leave_date <= date(self.year, self.month, day) <= i.to_date and i.leave_status == 0:
                        return f"<td class='datepresent'><span>{day}</span></td>"
                    elif i.leave_date <= date(self.year, self.month, day) <= i.to_date and i.leave_status == 1:
                        return f"<td class='datepresent1'><span>{day}</span></td>"
                for i in q:
                    if date(self.year, self.month, day)==i.date and i.status=="present":
                        return f"<td  ><span class='datepresent1' >{day}</span></td>"
                    elif date(self.year, self.month, day)==i.date and i.status=="Halfday":
                        return f"<td  ><span class='datepresent2' >{day}</span></td>"
                    elif date(self.year, self.month, day)==i.date and i.status=="Absent":
                        return f"<td  ><span class='datepresent3' >{day}</span></td>"
                # for i in l:
                #     if date(self.year, self.month, day)== i.to_date and i.leave_status==0:					
                #         return f"<td class='datepresent' ><span >{day}</span></td>"
                #     else:
                #         if date(self.year, self.month, day)== i.to_date and i.leave_status==1:					
                #             return f"<td class='datepresent1' ><span >{day}</span></td>"
                    
            return f"<td><span class='date'>{day}</span></td>"
        return '<td></td>'
        



    def formatweek(self,request, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(request,d)
        return f'<tr> {week} </tr>'
    


    def formatmonth(self,request, withyear=True): 

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(request,week)}\n'
        return cal
def head():
    return f'<h1 style="color:white; font-size:24px;">Attendance</h1><p style="color:white; font-size:14px;">To apply for leaves, or to update your attendance data, please click on the edit button next to a date. To apply for many leaves together, <a href=""> click here.</a></p>'
def caltable(self,year,month,request):
    comid=Companys.objects.filter(usernumber=request.user.id).first()
    emid=Employs.objects.filter(admin=request.user.id).first()
    if comid:
       compid=comid.id
    else:
        compid=emid.companyid
        
    editholiday_instance = editholiday12.objects.filter(companyid=compid).first()
    sat1_value = editholiday_instance.sat1
    sat2_value = editholiday_instance.sat2
    sat3_value = editholiday_instance.sat3
    sat4_value = editholiday_instance.sat4
    sat5_value = editholiday_instance.sat5 
    sun_value = editholiday_instance.sun
    mon_value=editholiday_instance.mon
    tue_value=editholiday_instance.tue
    wed_value=editholiday_instance.web
    thu_value=editholiday_instance.thu
    fri_value=editholiday_instance.fri
    allsat=editholiday_instance.alsat
    special_weekends_a = customholidays.objects.filter(companyid=compid)
    public_holidays = publicholidays.objects.filter(companyid=compid)
    today=date(int(year),int(month),1)
    year = today.year
    month= today.month
    num_days = calendar.monthrange(year, month)[1]
    days = [date(year, month, day) for day in range(1, num_days+1)]
    days_list = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">{head(self.request)}<th>Date</th><th>Status</th><th></th><th>Check in</th><th>Check out</th><th>Duration</th></tr>'
    saturdays_encountered = 0
    weekoff_days = []
    weekend_count=0
    for day in days:
        special_weekends = special_weekends_a.filter(date=day).first()
        public_holidaysc = public_holidays.filter(publicholiday_date=day).first()
        day_str = day.strftime(' %d/ %m/ %Y')
        status = data(self.request, day)
        check_in = im(self.request, day)
        check_out = out(self.request, day)
        duration = dur(self.request, day)
        if sun_value == 1 and day.strftime('%A')=="Sunday":
            days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
            weekoff_days.append("Sunday")
            weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Sunday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Sunday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif sun_value !=1 and day.strftime('%A')=="Sunday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if mon_value== 1 and day.strftime('%A')=="Monday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Monday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Monday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Monday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif mon_value !=1 and day.strftime('%A')=="Monday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if tue_value==1 and day.strftime('%A')=="Tuesday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Tuesday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Tuesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Tuesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif tue_value !=1 and day.strftime('%A')=="Tuesday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if wed_value==1 and day.strftime('%A')=="Wednesday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Wednesday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Wednesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Wednesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif wed_value !=1 and day.strftime('%A')=="Wednesday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if thu_value==1 and day.strftime('%A')=="Thursday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Thursday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Thursday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Thursday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif thu_value !=1 and day.strftime('%A')=="Thursday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if fri_value==1 and day.strftime('%A')=="Friday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Friday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Friday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Friday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif fri_value !=1 and day.strftime('%A')=="Friday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if allsat==1 and day.strftime('%A')=="Saturday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Saturday")
               weekend_count += 1
        # elif special_weekends and day.strftime('%A')=="Saturday":
        #        days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
        # elif public_holidaysc and day.strftime('%A')=="Saturday":
        #        days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
        if allsat != 1 and day.strftime('%A') == "Saturday":
           saturdays_encountered += 1
           if sat1_value == 1 and saturdays_encountered == 1 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 1 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 1  :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat1_value !=1 and saturdays_encountered == 1 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat2_value == 1  and saturdays_encountered == 2 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 2 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 2 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat2_value !=1 and saturdays_encountered == 2 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat3_value == 1  and saturdays_encountered == 3 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 3 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 3 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat3_value !=1 and saturdays_encountered == 3 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat4_value == 1  and saturdays_encountered == 4 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 4 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 4 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat4_value !=1 and saturdays_encountered == 4 :
               days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat5_value == 1  and saturdays_encountered == 5 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 5 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 5 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat5_value != 1  and  saturdays_encountered == 5 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"

    return days_list,weekoff_days,weekend_count


def caltablesalary(self,year,month,request):
    comid=Companys.objects.filter(usernumber=request.user.id).first()
    emid=Employs.objects.filter(admin=request.user.id).first()
    if comid:
       compid=comid.id
    else:
        compid=emid.companyid
        
    editholiday_instance = editholiday12.objects.filter(companyid=compid).first()
    sat1_value = editholiday_instance.sat1
    sat2_value = editholiday_instance.sat2
    sat3_value = editholiday_instance.sat3
    sat4_value = editholiday_instance.sat4
    sat5_value = editholiday_instance.sat5 
    sun_value = editholiday_instance.sun
    mon_value=editholiday_instance.mon
    tue_value=editholiday_instance.tue
    wed_value=editholiday_instance.web
    thu_value=editholiday_instance.thu
    fri_value=editholiday_instance.fri
    allsat=editholiday_instance.alsat
    special_weekends_a = customholidays.objects.filter(companyid=compid)
    public_holidays = publicholidays.objects.filter(companyid=compid)
    today=date(int(year),int(month),1)
    today1 = date.today()
    year = today.year
    month= today.month
    num_days = calendar.monthrange(year, month)[1]
    num_days_today = today1.day
    days = [date(year, month, day) for day in range(1, num_days+1)]
    days_list = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">{head(self.request)}<th>Date</th><th>Status</th><th></th><th>Check in</th><th>Check out</th><th>Duration</th></tr>'
    saturdays_encountered = 0
    weekoff_days = []
    weekend_count = 0   
    num_weekends = 0    
    for day in days[:num_days_today]:
        special_weekends = special_weekends_a.filter(date=day).first()
        public_holidaysc = public_holidays.filter(publicholiday_date=day).first()
        day_str = day.strftime(' %d/ %m/ %Y')
        status = data(self.request, day)
        check_in = im(self.request, day)
        check_out = out(self.request, day)
        duration = dur(self.request, day)
        if sun_value == 1 and day.strftime('%A')=="Sunday":
            days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
            weekoff_days.append("Sunday")
            weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Sunday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Sunday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif sun_value !=1 and day.strftime('%A')=="Sunday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if mon_value== 1 and day.strftime('%A')=="Monday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Monday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Monday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Monday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif mon_value !=1 and day.strftime('%A')=="Monday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if tue_value==1 and day.strftime('%A')=="Tuesday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Tuesday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Tuesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Tuesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif tue_value !=1 and day.strftime('%A')=="Tuesday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if wed_value==1 and day.strftime('%A')=="Wednesday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Wednesday")
               weekend_count += 1
        elif special_weekends and day.strftime('%A')=="Wednesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Wednesday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif wed_value !=1 and day.strftime('%A')=="Wednesday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if thu_value==1 and day.strftime('%A')=="Thursday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
               weekoff_days.append("Thursday")
        elif special_weekends and day.strftime('%A')=="Thursday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Thursday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif thu_value !=1 and day.strftime('%A')=="Thursday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if fri_value==1 and day.strftime('%A')=="Friday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
               weekoff_days.append("Friday")
        elif special_weekends and day.strftime('%A')=="Friday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
        elif public_holidaysc and day.strftime('%A')=="Friday":
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
        elif fri_value !=1 and day.strftime('%A')=="Friday":
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
        if allsat==1 and day.strftime('%A')=="Saturday":
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekoff_days.append("Saturday")
               weekend_count += 1
        # elif special_weekends and day.strftime('%A')=="Saturday":
        #        days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
        # elif public_holidaysc and day.strftime('%A')=="Saturday":
        #        days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
        if allsat != 1 and day.strftime('%A') == "Saturday":
           saturdays_encountered += 1
           if sat1_value == 1 and saturdays_encountered == 1 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 1 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 1  :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat1_value !=1 and saturdays_encountered == 1 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat2_value == 1  and saturdays_encountered == 2 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 2 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 2 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat2_value !=1 and saturdays_encountered == 2 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat3_value == 1  and saturdays_encountered == 3 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 3 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 3 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat3_value !=1 and saturdays_encountered == 3 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat4_value == 1  and saturdays_encountered == 4 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 4 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 4 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat4_value !=1 and saturdays_encountered == 4 :
               days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"
           if sat5_value == 1  and saturdays_encountered == 5 :
               days_list+=f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">Weekend</td></tr>'
               weekend_count += 1
           elif special_weekends and saturdays_encountered == 5 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{special_weekends.reason}</td></tr>'
               weekend_count += 1
           elif public_holidaysc and saturdays_encountered == 5 :
               days_list += f'<tr><td>{day_str}</td><td colspan="6" style="background-color: black;font-size:20px;">{public_holidaysc.festival_name}</td></tr>'
               weekend_count += 1
           elif sat5_value != 1  and  saturdays_encountered == 5 :
             days_list += f"<tr><td>{day_str}</td><td>{status}</td><td></td><td>{check_in}</td><td>{check_out}</td><td>{duration}</td><td></td></tr>"

    return days_list,weekoff_days,weekend_count



def data(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
       k=checkin.objects.filter(date=tds,empid=pemail.email)
       p=LeaveReportEmploy.objects.filter(email_leave=pemail.email)
    else:
       k=checkin.objects.filter(date=tds,empid=eid)
       p=LeaveReportEmploy.objects.filter(email_leave=eid)

    for i in p:
        if i.leave_date<= tds <= i.to_date:
           
            if i.leave_status:
                return "Leave"
                    
            else:
                return "Pending"
    # for i in s:
    #     if i.to_date==tds:
    #         s=i.leave_status==0
    #         if i.leave_status:
    #             return "Leave"
    #         else:
    #             return "leave"
    #         return s

    for i in k:
        if i.date==tds:
            p=i.status
            return p
    return "-NA-"
    return "-NA-"

def im(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
       k=checkin.objects.filter(date=tds,empid=pemail.email)
    else:
       k=checkin.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"

def out(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
       k=checkout.objects.filter(date=tds,empid=pemail.email)
    else:
       k=checkout.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"
def dur(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
       k=checkin.objects.filter(date=tds,empid=pemail.email)
    else:
       k=checkin.objects.filter(date=tds,empid=eid)
    p=checkout.objects.filter(date=tds,empid=pemail.email)
    s1,s2="",""
    for i in k:
        d=i.date
        l=i.time
        if d==tds:
            s1=l.strftime('%H:%M:%S')		
    for a in p:
        j=a.time
        d=a.date
        if d==tds:
            s2=j.strftime('%H:%M:%S')
    if s1!="" and s2!="":
        FMT = '%H:%M:%S'
        tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)
        return tdelta
    return "-NA-"





class Calendar1(HTMLCalendar):
    def __init__(self, year=None, month=None, day=None):
        self.year = year
        self.month = month
        self.day=day
        super(Calendar1, self).__init__()
       
    

    def formatday(self,request, day):
        
        d = ''
       
        if day != 0:
           
             
            if date.today() == date(self.year, self.month, day):
                return f"<td style='border: 2px solid #ffffff;'>{day}</td>"
            else:
                eid=get_empid(request)
                people_id=get_people(request)
                pemail=Employs.objects.filter(admin=people_id).first()
                if pemail:
                    emaila=pemail.email
                if people_id:     
                   q=checkin.objects.filter(date=date(self.year, self.month, day),empid=pemail.email)
                   k=LeaveReportEmploy.objects.filter(email_leave=pemail.email)
                else:
                   q=checkin.objects.filter(date=date(self.year, self.month, day),empid=eid)
                   k=LeaveReportEmploy.objects.filter(email_leave=eid)
                l=LeaveReportEmploy.objects.filter(to_date=date(self.year, self.month, day))
                # k.(leave_date=date(self.year, self.month, day))
                for i in k:
                    if i.leave_date <= date(self.year, self.month, day) <= i.to_date and i.leave_status == 0:
                        return f"<td class='datepresent'><span>{day}</span></td>"
                    elif i.leave_date <= date(self.year, self.month, day) <= i.to_date and i.leave_status == 1:
                        return f"<td class='datepresent1'><span>{day}</span></td>"
                for i in q:
                    if date(self.year, self.month, day)==i.date and i.status=="present":
                        return f"<td  ><span class='datepresent1' >{day}</span></td>"
                # for i in l:
                #     if date(self.year, self.month, day)== i.to_date and i.leave_status==0:					
                #         return f"<td class='datepresent' ><span >{day}</span></td>"
                #     else:
                #         if date(self.year, self.month, day)== i.to_date and i.leave_status==1:					
                #             return f"<td class='datepresent1' ><span >{day}</span></td>"
                    
            return f"<td><span class='date'>{day}</span></td>"
        return '<td></td>'
        



    def formatweek(self,request, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(request,d)
        return f'<tr> {week} </tr>'
    


    def formatmonth(self,request, withyear=True): 

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(request,week)}\n'
        return cal
def head(request):
    employid=Employs.objects.filter(admin=request.user.id)
    if employid:
      return f'<h1 style=" font-size:24px;padding:0px; margin:0px; margin-bottom:10px; margin-top:10px;">Attendance</h1><p style="color:black; font-size:14px;font-weight:700px;">To apply for leave, please click on the "click here" button next to a date. To apply for multiple leaves together and also view your leave application history, please <a href="/employ_apply_leave/"><button style="background-color: #006600; color: #e6e6e6;font-weight: 700px; border:none;border-radius:5px;padding:5px;">click here</button></a></p>'
    else:
      return f'<h1 style="color:black; font-size:24px;padding-top:20px;">Attendance</h1><p style="color:black; font-size:14px;">See Attendance Details below</p>'

from datetime import date
import calendar







def data(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
       k=checkin.objects.filter(date=tds,empid=pemail.email)
       p=LeaveReportEmploy.objects.filter(email_leave=pemail.email)
    else:
       k=checkin.objects.filter(date=tds,empid=eid)
       p=LeaveReportEmploy.objects.filter(email_leave=eid)
    s=LeaveReportEmploy.objects.filter(to_date=tds)
    
    for i in p:
        if i.leave_date<= tds <= i.to_date:
           
            if i.leave_status:
                return "Leave"
                    
            else:
                return "Pending"
    # for i in s:
    #     if i.to_date==tds:
    #         s=i.leave_status==0
    #         if i.leave_status:
    #             return "Leave"
    #         else:
    #             return "leave"
    #         return s

    for i in k:
        if i.date==tds:
            p=i.status
            return p
    return "-NA-"
    return "-NA-"

def im(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
       k=checkin.objects.filter(date=tds,empid=pemail.email)
    else:
       k=checkin.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"

def out(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
      k=checkout.objects.filter(date=tds,empid=pemail.email)
    else:
      k=checkout.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"
def dur(request,tds):
    eid=get_empid(request)
    people_id=get_people(request)
    pemail=Employs.objects.filter(admin=people_id).first()
    if people_id:
      k=checkin.objects.filter(date=tds,empid=pemail.email)
      p=checkout.objects.filter(date=tds,empid=pemail.email)
    else:
      k=checkin.objects.filter(date=tds,empid=eid)
      p=checkout.objects.filter(date=tds,empid=eid)
    s1,s2="",""
    for i in k:
        d=i.date
        l=i.time
        if d==tds:
            s1=l.strftime('%H:%M:%S')		
    for a in p:
        j=a.time
        d=a.date
        if d==tds:
            s2=j.strftime('%H:%M:%S')
    if s1!="" and s2!="":
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        return tdelta
    return "-NA-"






from holidays import India
from datetime import datetime

from holidays import India
from datetime import datetime

def get_holidays_for_region(region):
    current_year = datetime.now().year
    india_holidays = India(years=current_year)

    if region == 'india':
        return india_holidays
    elif region == 'telangana':
        # Filter holidays for Telangana based on state code (TS)
        telangana_holidays = {
            date: name for date, name in india_holidays.items()
            if 'TS' in name
        }
        return telangana_holidays
    else:
        return {}

def get_current_month_holidays(region):
    holidays = get_holidays_for_region(region)
    current_year = datetime.now().year
    current_year_holidays = {
        date: name for date, name in holidays.items()
        if date.year == current_year  
    }
    return current_year_holidays

def get_all_month_holidays(region):
    holidays = get_holidays_for_region(region)
    all_month_holidays = holidays  # No filtering based on month
    return all_month_holidays

def get_current_month_holidays_count(region):
    holidays = get_holidays_for_region(region)
    current_month = datetime.now().month
    current_month_holidays_count = sum(
        1 for date in holidays.keys() if date.month == current_month
    )
    return current_month_holidays_count



def dursec(request, tds):
    eid = get_empid(request)
    people_id = get_people(request)
    pemail = Employs.objects.filter(admin=people_id).first()

    if people_id:
        k = checkin.objects.filter(date=tds, empid=pemail.email)
        p = checkout.objects.filter(date=tds, empid=pemail.email)
    else:
        k = checkin.objects.filter(date=tds, empid=eid)
        p = checkout.objects.filter(date=tds, empid=eid)

    s1, s2 = None, None

    for i in k:
        d = i.date
        l = i.time
        if d == tds:
            s1 = datetime.combine(d, l)  
            break  

    for a in p:
        d = a.date
        j = a.time
        if d == tds:
            s2 = datetime.combine(d, j)  
            break  

    if s1 and s2:
        tdelta = (s2 - s1).total_seconds()
        return tdelta

    return "-NA-"
