import moni
import json
import sys

json_object = json.loads(sys.argv[1])
employee_id = json_object.get("employee_id")  # Assuming the employee ID is included in the JSON data
company_id =json_object.get("company_id")
moni.mainRecord()