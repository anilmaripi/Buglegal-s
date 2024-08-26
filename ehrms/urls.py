from django.urls import include, re_path
from ehrms import Employviews,adminviews

app_name = 'ehrms'
urlpatterns = [

    re_path(r'^calendar/$', Employviews.CalendarView.as_view(), name='calendar'),
    re_path(r'^secondcalendar/$', Employviews.SecondCalendarView.as_view(), name='secondcalendar'),
    re_path('employ_apply_leave/', Employviews.employ_apply_leave, name='employ_apply_leave'),
    re_path(r'^calendar1/$', adminviews.CalendarView_1.as_view(), name='calendar1'),
    re_path(r'^calendar2/$', adminviews.CalendarView_2.as_view(), name='calendar2'),
    # re_path(r'^calendar2/$', Employviews.CalendarView1.as_view(), name='calendar2'),


]