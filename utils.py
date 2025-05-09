import os
import json
import re
from datetime import datetime

def save_data(json_file_name, data):
    with open(f'data/{json_file_name}.json', 'w') as file:
        json.dump(data, file, indent=2)

def load_data(json_file_name):
    file_path = f'data/{json_file_name}.json'
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return []
    with open(file_path, 'r') as file:
        return json.load(file)

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password):
    # At least 8 characters, 1 letter, and 1 number
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    return bool(re.match(pattern, password))

def validate_phone_number(phone_number):
    # Egyptian phone numbers format
    pattern = r'^(?:\+20|0020|01)[0-2,5]{1}[0-9]{8}$'
    return bool(re.match(pattern, phone_number))

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_project_title(title):
    return bool(title and len(title.strip()) <= 100)

def validate_project_details(details):
    return bool(details and len(details.strip()) <= 1000)

def validate_project_target(target):
    try:
        target = float(target)
        return target > 0
    except (ValueError, TypeError):
        return False

def validate_dates(start_time, end_time):
    if not all([validate_date_format(start_time), validate_date_format(end_time)]):
        return False
    
    try:
        start = datetime.strptime(start_time, '%Y-%m-%d')
        end = datetime.strptime(end_time, '%Y-%m-%d')
        return start < end
    except ValueError:
        return False

