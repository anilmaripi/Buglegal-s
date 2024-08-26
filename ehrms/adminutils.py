
from datetime import datetime, timedelta,date
from calendar import HTMLCalendar
from datetime import date, timedelta
import datetime
from .models import checkin,checkout,LeaveReportEmploy,Employs
import calendar

def get_empid(request):
    email=request.session.get('email_2');
    return email


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
                eid=get_empid(request)
                q=checkin.objects.filter(date=date(self.year, self.month, day),empid=eid) 
                k=LeaveReportEmploy.objects.filter(leave_date=date(self.year, self.month, day))
                l=LeaveReportEmploy.objects.filter(to_date=date(self.year, self.month, day))
                # k.(leave_date=date(self.year, self.month, day))
                for i in k:
                    if date(self.year, self.month, day)== i.leave_date and i.leave_status==0:					
                        return f"<td class='datepresent' ><span >{day}</span></td>"
                    else:
                        if date(self.year, self.month, day)== i.leave_date and i.leave_status==1:					
                
                            return f"<td class='datepresent1' ><span >{day}</span></td>"
                for i in q:
                    if date(self.year, self.month, day)==i.date and i.status=="present":
                        return f"<td  ><span class='datepresent1' >{day}</span></td>"
                for i in l:
                    if date(self.year, self.month, day)== i.to_date and i.leave_status==0:					
                        return f"<td class='datepresent' ><span >{day}</span></td>"
                    else:
                        if date(self.year, self.month, day)== i.to_date and i.leave_status==1:					
                            return f"<td class='datepresent1' ><span >{day}</span></td>"
                    
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
    return f'<h1 style="color:white; font-size:24px;">Attendence</h1><p style="color:white; font-size:14px;">To apply for leaves, or to update your attendance data, please click on the edit button next to a date. To apply for many leaves together, <a href="employ_apply_leave"> click here.</a></p>'

def caltable(self,year,month):
    today=date(int(year),int(month),1)
    year = today.year
    month= today.month
    num_days = calendar.monthrange(year, month)[1]
    days = [date(year, month, day) for day in range(1, num_days+1)]
    days_list = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">{head()}<th>Date</th><th>Status</th><th></th><th>Check inn</th><th>Check out</th><th>Duration</th><th>Remarks</th></tr>'
    for days in days:
        days_str = f"<tr><td>{days.strftime(' %d/ %m/ %Y')}</td><td>{data(self.request,days)}</td><td></td><td>{im(self.request,days)}</td><td>{out(self.request,days)}</td><td>{dur(self.request,days)}</td><td>-NA-</td></tr>"
        if days.strftime('%A')=="Sunday" or days.strftime('%A')=="Saturday":
            days_str = days.strftime(' %d/ %m/ %Y  ')
            days_list+=f'<tr><td>{days_str}</td><td colspan="6" style="background-color: black;font-size:20px;">weekend</td></tr>'
        else:
            days_list+=f'{days_str}'
    return days_list


def data(request,tds):
    eid=get_empid(request)
    k=checkin.objects.filter(date=tds,empid=eid)
    p=LeaveReportEmploy.objects.filter(leave_date=tds)
    s=LeaveReportEmploy.objects.filter(to_date=tds)
    for i in p:
        if i.leave_date==tds:
            s=i.leave_status==1
            if i.leave_status:
                return "Leave"
            else:
                return "leave"
            return s
    for i in s:
        if i.to_date==tds:
            s=i.leave_status==0
            if i.leave_status:
                return "Leave"
            else:
                return "leave"
            return s

    for i in k:
        if i.date==tds:
            p=i.status
            return p
    return "-NA-"
    return "-NA-"

def im(request,tds):
    eid=get_empid(request)
    k=checkin.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"

def out(request,tds):
    eid=get_empid(request)
    k=checkout.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"
def dur(request,tds):
    eid=get_empid(request)
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
                q=checkin.objects.filter(date=date(self.year, self.month, day),empid=eid) 
                k=LeaveReportEmploy.objects.filter(leave_date=date(self.year, self.month, day))
                l=LeaveReportEmploy.objects.filter(to_date=date(self.year, self.month, day))
                # k.(leave_date=date(self.year, self.month, day))
                for i in k:
                    if date(self.year, self.month, day)== i.leave_date and i.leave_status==0:					
                        return f"<td class='datepresent' ><span >{day}</span></td>"
                    else:
                        if date(self.year, self.month, day)== i.leave_date and i.leave_status==1:					
                
                            return f"<td class='datepresent1' ><span >{day}</span></td>"
                for i in q:
                    if date(self.year, self.month, day)==i.date and i.status=="present":
                        return f"<td  ><span class='datepresent1' >{day}</span></td>"
                for i in l:
                    if date(self.year, self.month, day)== i.to_date and i.leave_status==0:					
                        return f"<td class='datepresent' ><span >{day}</span></td>"
                    else:
                        if date(self.year, self.month, day)== i.to_date and i.leave_status==1:					
                            return f"<td class='datepresent1' ><span >{day}</span></td>"
                    
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
    return f'<h1 style="color:white; font-size:24px;">Attendence</h1><p style="color:white; font-size:14px;">To apply for leaves, or to update your attendance data, please click on the edit button next to a date. To apply for many leaves together, <a href="employ_apply_leave">please</a> click here.</p>'

def caltable(self,year,month):
    today=date(int(year),int(month),1)
    year = today.year
    month= today.month
    num_days = calendar.monthrange(year, month)[1]
    days = [date(year, month, day) for day in range(1, num_days+1)]
    days_list = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">{head()}<th>Date</th><th>Status</th><th></th><th>Check inn</th><th>Check out</th><th>Duration</th><th>Remarks</th></tr>'
    for days in days:
        days_str = f"<tr><td>{days.strftime(' %d/ %m/ %Y')}</td><td>{data(self.request,days)}</td><td></td><td>{im(self.request,days)}</td><td>{out(self.request,days)}</td><td>{dur(self.request,days)}</td><td>-NA-</td></tr>"
        if days.strftime('%A')=="Sunday" or days.strftime('%A')=="Saturday":
            days_str = days.strftime(' %d/ %m/ %Y  ')
            days_list+=f'<tr><td>{days_str}</td><td colspan="6" style="background-color: black;font-size:20px;">weekend</td></tr>'
        else:
            days_list+=f'{days_str}'
    return days_list


def data(request,tds):
    eid=get_empid(request)
    k=checkin.objects.filter(date=tds,empid=eid)
    p=LeaveReportEmploy.objects.filter(leave_date=tds)
    s=LeaveReportEmploy.objects.filter(to_date=tds)
    for i in p:
        if i.leave_date==tds:
            s=i.leave_status==1
            if i.leave_status:
                return "Leave"
            else:
                return "leave"
            return s
    for i in s:
        if i.to_date==tds:
            s=i.leave_status==0
            if i.leave_status:
                return "Leave"
            else:
                return "leave"
            return s

    for i in k:
        if i.date==tds:
            p=i.status
            return p
    return "-NA-"
    return "-NA-"

def im(request,tds):
    eid=get_empid(request)
    k=checkin.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"

def out(request,tds):
    eid=get_empid(request)
    k=checkout.objects.filter(date=tds,empid=eid)
    for i in k:
        d=i.date
        l=i.time
        h= l.strftime('%R')
        return h
    return "-NA-"
def dur(request,tds):
    eid=get_empid(request)
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
    current_month = datetime.now().month
    current_month_holidays = {
        date: name for date, name in holidays.items()
        if date.month == current_month
    }
    return current_month_holidays

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

