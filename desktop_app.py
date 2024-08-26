from __future__ import print_function
import time
import json
import datetime
import sys

from dateutil import parser
if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto

import comtypes
comtypes.CoInitialize()



# Django API URLs
SYSTEM_STATUS_API = 'https://buglegal.com/record_system_status/'
RECORD_ACTIVITY_API = 'https://buglegal.com/client_record_activity/'
STOP_MONITORING_API = 'https://buglegal.com/client_stop_monitoring/'
CAPTURE_API = 'https://buglegal.com/client_capture/'
GET_EMP_API = 'https://buglegal.com/get_employee_and_company/'



import requests

import pyautogui as pg
from threading import Thread

import certifi

ca_bundle_path = certifi.where()

import httpx

import os


def get_executable_directory():
    # Get the directory of the executable
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # Running as a script
        return os.path.dirname(os.path.abspath(__file__))

# Function to authenticate the secret identifier
def authenticate_secret_identifier(secret_file_path):
    try:
        exe_dir = get_executable_directory()

        secret_file_path = os.path.join(exe_dir, secret_file_path)

       

        # Read the encrypted secret identifier from the secret file
        with open(secret_file_path, 'rb') as secret_file:
            user_identifier_bytes = secret_file.read()
            user_identifier = user_identifier_bytes.decode()

        return user_identifier
    except Exception as e:
        print(f"Error authenticating secret identifier: {str(e)}")
        return None





# Call the authentication function
def authenticate_user():
    secret_file_path = 'secret_user_identifier.txt'
    
    user_identifier = authenticate_secret_identifier(secret_file_path)

    if user_identifier is not None:
        print(f"Authenticated User Identifier: {user_identifier}")
        response = httpx.get(f'{GET_EMP_API}?user_identifier={user_identifier}')

        if response.status_code == 200:
            data = response.json()
            employee_id = data.get('employee_id')
            company_id = data.get('company_id')
            checked_in = data.get('checkin')
            checked_out = data.get('checkout')

            # Now you have employee_id, company_id, check-in, and check-out status
            print(f'Employee ID: {employee_id}, Company ID: {company_id}')
            print(f'Checked In: {checked_in}, Checked Out: {checked_out}')
            

            return employee_id, company_id, checked_in, checked_out
        else:
            print(f'Failed to get employee_id and company_id from the API. Status Code: {response.status_code}')
    else:
        print("Authentication failed.")
    return None, None, None, None


employee_id, company_id ,checked_in, checked_out  = authenticate_user()


stop_monitoring_flag = False


class AcitivyList:
    def __init__(self, activities):
        self.activities = activities

    def initialize_me(self):
        activity_list = AcitivyList([])
        exe_dir = get_executable_directory()
        json_file_path = os.path.join(exe_dir, 'activities.json')
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            activity_list = AcitivyList(
                activities=self.get_activities_from_json(data)
            )

        return activity_list

    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:

            return_list.append(
                Activity(
                    name=activity['name'],
                    time_entries=self.get_time_entires_from_json(activity),
                )
            )
        self.activities = return_list
        return return_list

    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time=parser.parse(entry['start_time']),
                    end_time=parser.parse(entry['end_time']),
                    days=entry['days'],
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list

    def serialize(self):
        return {
            'activities': self.activities_to_json()
        }

    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())

        return activities_


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'name': self.name,
            'time_entries': self.make_time_entires_to_json()
        }

    def make_time_entires_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())

        return time_list


class TimeEntry:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def _get_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def serialize(self):
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }


def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


import sys



def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name




def get_chrome_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        comtypes.CoInitialize()  # Initialize COM
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        
        return 'https://' + edit.GetValuePattern().Value
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)

   

def show_activity():
    b = list()
    d = list()

    # Get the directory of the executable
    exe_dir = get_executable_directory()
    json_file_path = os.path.join(exe_dir, 'activities.json')

    try:
        with open(json_file_path, 'r') as jsonfile:
            a = json.load(jsonfile)
            e = a.get('activities', [])
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON data.")
        return []

    for i in e:
        b.append(i['name'])

    tot = 0

    for i in e:
        sed = 0
        for j in i.get("time_entries", []):
            sed = sed + int(j.get("minutes", 0)) * 60 + int(j.get("seconds", 0)) + int(j.get("hours", 0)) * 3600

            tot = tot + sed
        d.append(sed)

    kek = time.strftime("%H:%M:%S", time.gmtime(tot))
    kek = "Time used: " + kek
    print(b)
    print(d)
    combineBD = zip(b, d)
    zipped_list = list(combineBD)

    return zipped_list

def erase():
    try:
        # Get the directory of the executable
        exe_dir = get_executable_directory()
        json_file_path = os.path.join(exe_dir, 'activities.json')

        # Check if the file exists before trying to erase it
        if os.path.exists(json_file_path):
            open(json_file_path, "w").close()
        else:
            print(f"File not found: {json_file_path}")

    except Exception as e:
        print(f"Error erasing activities.json: {str(e)}")



def record(active_window_name, activity_name, start_time, activeList, first_time):
    try:
        al = activeList.initialize_me()
    except Exception:
        print('No json')

    global stop_monitoring_flag
    try:
        while not stop_monitoring_flag:
            previous_site = ""
            if sys.platform not in ['linux', 'linux2']:
                new_window_name = get_active_window()
                if 'Google Chrome' in new_window_name:
                    new_window_name = url_to_name(get_chrome_url())
            if sys.platform in ['linux', 'linux2']:
                new_window_name = l.get_active_window_x()
                if 'Google Chrome' in new_window_name:
                    new_window_name = l.get_chrome_url_x()

            if active_window_name != new_window_name:
                print(active_window_name)
                activity_name = active_window_name
                al = activity_name
                print(al)
                print(type(al))
                ct = datetime.datetime.now()
                ct1=datetime.datetime.now()
                    # Calculate total duration in seconds
                total_duration = (ct - start_time).seconds
                # Updated SQL query to include start_time and end_time
                requests.post(RECORD_ACTIVITY_API, data={
                    'employee_id': employee_id,
                    'company_id': company_id,
                    'active_window_name': active_window_name,
                    'total_duration':total_duration
                })

                if not first_time:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                    time_entry._get_specific_times()

                    exists = False
                    for activity in activeList.activities:
                        if activity.name == activity_name:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        activity = Activity(activity_name, [time_entry])
                        activeList.activities.append(activity)
                    exe_dir = get_executable_directory()
                    json_file_path = os.path.join(exe_dir, 'activities.json')    
                    with open(json_file_path, 'w') as json_file:
                        json.dump(activeList.serialize(), json_file,
                                  indent=4, sort_keys=True)
                        start_time = datetime.datetime.now()
                first_time = False
                active_window_name = new_window_name

            time.sleep(1)

    except KeyboardInterrupt:
        exe_dir = get_executable_directory()
        json_file_path = os.path.join(exe_dir, 'activities.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(activeList.serialize(), json_file,
                      indent=4, sort_keys=True)



def start_monitoring():
    active_window_name = str()
    activity_name = ""
    start_time = datetime.datetime.now()
    activeList = AcitivyList([])
    first_time = True
    erase()

    record(active_window_name, activity_name, start_time, activeList, first_time)




def stop_monitoring():
    global stop_monitoring_flag
    stop_monitoring_flag = True 
    for w, t in show_activity():
        today = datetime.datetime.now()
        requests.post(STOP_MONITORING_API, data={
            'employee_id': employee_id,
            'company_id': company_id,
            'w':w,
            't':t,
 
        })
        print(f"Recording activity: {w} - {t} seconds")
        requests.post(RECORD_ACTIVITY_API, data={
            'employee_id': employee_id,
            'company_id': company_id,
            'active_window_name': w
        })

    print("Monitoring stopped.")

from psutil import sensors_battery


import time

from pynput import mouse, keyboard

class ScreenshotApp:
    def __init__(self):

        self.running = False
        self.checkin_flag =False

        self.last_input_time = time.time()


    def start_capture(self):
         #Call the authentication function
        authenticate_user() 
        if employee_id is not None and company_id is not None:   
            self.running = True 
            Thread(target=self.capture_loop).start()
            Thread(target=self.monitor_battery_and_idle_status).start()  

            Thread(target=start_monitoring).start()
           
     
        else:
            print("Authentication failed.")

    def monitor_battery_and_idle_status(self):
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click) , \
             keyboard.Listener(on_press=self.on_press, on_release=self.on_release):
            while self.running:
                try:    
                    battery = sensors_battery()
                    
                    if battery:
                        percent = battery.percent
                        power_plugged = battery.power_plugged
                        status_type = 'battery'
                        status_message = f'Battery Level: {percent}%, Power Plugged: {power_plugged}'
                        self.save_system_status(status_type, status_message)

                    if self.is_system_idle():
                        status_type = 'offline'
                        status_message = 'Offline'
                        self.save_system_status(status_type, status_message)
                    else:
                        status_type = 'online'
                        status_message = 'Online'
                        
                        self.save_system_status(status_type, status_message)
                    
                    
                    time.sleep(10)
                except Exception as e:
                        print(f"Error in monitor_battery_and_idle_status: {str(e)}")

    def is_system_idle(self, threshold_seconds=20):
        idle_time = time.time() - self.last_input_time
        return idle_time > threshold_seconds

    def on_move(self, x, y):
        self.last_input_time = time.time()

    def on_click(self, x, y, button, pressed):
        self.last_input_time = time.time()

    def on_press(self, key):
        self.last_input_time = time.time()

    def on_release(self, key):
        self.last_input_time = time.time()


    
    def save_system_status(self, status_type, status_message):
        # Save the system status to the database
        try:
            response = requests.post(SYSTEM_STATUS_API, data={
                'employee_id': employee_id,
                'company_id': company_id,
                'status_type': status_type,
                'status_message': status_message,
                'timestamp': datetime.datetime.now(),
            })

            response.raise_for_status()

            if response.status_code == 200:
                print(f"System status saved successfully: {status_message}")
            else:
                print(f"Failed to save system status. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error saving system status: {str(e)}")





 
    def stop_capture(self):
        self.running = False
        stop_monitoring()
     

        sys.exit()
    
    def process_api_response(self, response_data):
        checkin_command = response_data.get('checkin', False)
        checkout_command = response_data.get('checkout', False)
        
        if checkin_command and not self.checkin_flag:
            self.start_capture()
            self.checkin_flag = True
        elif checkout_command and self.checkin_flag:
            self.stop_capture()
            self.checkin_flag = False


        

    def monitor_server(self):
        while True:
            secret_file_path = 'secret_user_identifier.txt'
            
            user_identifier = authenticate_secret_identifier(secret_file_path)

            if user_identifier is not None:
                response = httpx.get(f'{GET_EMP_API}?user_identifier={user_identifier}')
                if response.status_code == 200:
                    response_data = response.json()
                    self.process_api_response(response_data)

              

                time.sleep(5)  # Adjust the interval as needed
            else:
                print('User not identified.')
                time.sleep(60)

    def capture_loop(self):
        while self.running:
            self.send_screenshot()
            time.sleep(5)


    def send_screenshot(self):
        url = f"{CAPTURE_API}?token="
        
        try:
            screenshot = pg.screenshot()  # Capture screenshot using Pillow (PIL)
            screenshot_path = os.path.join(get_executable_directory(), "screenshot.png")
            screenshot.save(screenshot_path)

            with open(screenshot_path, "rb") as file:
                files = {'file': file}
                data = {
                    'employee_id': employee_id,
                    'company_id': company_id,
                }
                response = requests.post(url, files=files, data=data)

            print(response.json())

        except Exception as e:
            print(f"Error capturing or sending screenshot: {str(e)}")




import win32com.client







def check_registry_entry():
    try:
        reg = win32com.client.Dispatch('WScript.Shell')
        exe_dir = get_executable_directory()

        # Construct absolute paths to the key and secret files
        app_path = os.path.join(exe_dir, 'desktop_app.exe')
        command = rf'"{app_path}" "desktopapp://run" %1'
        def_value=""
        # Check if the default value under 'desktopapp' key is set to 'URL:Buglegal Protocol'
        default_value = reg.RegRead(rf'HKEY_CURRENT_USER\Software\Classes\desktopapp\{def_value}')
        if default_value != 'URL:Buglegal Protocol':
            print("Default value under 'desktopapp' key is incorrect.")
            return False

        # Check if the value for 'URL Protocol' is set
        url_protocol_value = reg.RegRead(r'HKEY_CURRENT_USER\Software\Classes\desktopapp\URL Protocol')
        if url_protocol_value != '':
            print("Value for 'URL Protocol' is set.")
            return False

        # Check if the command value is set correctly under 'shell\open\command'
        cmd_value=""
        command_value = reg.RegRead(rf'HKEY_CURRENT_USER\Software\Classes\desktopapp\shell\open\command\{cmd_value}')
        if command_value != command:
            print("Command value under 'shell\open\command' is incorrect.")
            return False

        print("Registry check completed.")

        return True
    
    
    except Exception as e:
        print(f"Error checking registry: {e}")
        return False



def set_registry_entry():
    key_path = r"Software\Classes\desktopapp\shell\open\command"

    # Construct dynamic paths
    
    exe_dir = get_executable_directory()

        # Construct absolute paths to the key and secret files
    app_path = os.path.join(exe_dir,'desktop_app.exe')
    command = rf'"{app_path}" "desktopapp://run" %1'

    try:
        # Create a new instance of the registry COM object
        reg = win32com.client.Dispatch('WScript.Shell')

        
        
        def_value=""
        reg.RegWrite(rf'HKEY_CURRENT_USER\Software\Classes\desktopapp\{def_value}','URL:Buglegal Protocol', 'REG_SZ')
        # Set value for 'URL Protocol'
        reg.RegWrite(r'HKEY_CURRENT_USER\Software\Classes\desktopapp\URL Protocol', '', 'REG_SZ')
            
        cmd_value=""
        # Set value for 'command' under 'desktopapp\shell\open'
        reg.RegWrite(rf'HKEY_CURRENT_USER\Software\Classes\desktopapp\shell\open\command\{cmd_value}', command, 'REG_SZ')


        
        print(f"Registry entry successfully set.")
    except Exception as e:
        print(f"Error setting registry entry: {e}")





if __name__ == "__main__":

    
    if not check_registry_entry():
        set_registry_entry()

    if len(sys.argv) > 1 and sys.argv[1] == "desktopapp://run":
        # Handle the 'run' action in your application
        print("Running the application.")
        app = ScreenshotApp()
        monitoring_thread = Thread(target=app.monitor_server,daemon=True)
        monitoring_thread.start()
        monitoring_thread.join()

    





