import authController
from utils import validate_email, validate_password, validate_phone_number, validate_date_format, validate_dates
from projectController import (
    create_project, view_projects, update_project, 
    delete_project, search_projects_by_date, view_user_projects
)

class Application:
    def __init__(self):
        self.current_user = None

    def register(self):
        print("\n=== User Registration ===")
        
        # First Name validation
        while True:
            first_name = input("First name: ").strip()
            if first_name:
                break
            print("Error: First name cannot be empty!")

        # Last Name validation
        while True:
            last_name = input("Last name: ").strip()
            if last_name:
                break
            print("Error: Last name cannot be empty!")

        # Email validation
        while True:
            email = input("Email: ").strip()
            if validate_email(email):
                break
            print("Error: Invalid email format! Please use a valid email address.")

        # Password validation
        while True:
            password = input("Password: ").strip()
            if validate_password(password):
                while True:
                    confirm_password = input("Confirm password: ").strip()
                    if password == confirm_password:
                        break
                    print("Error: Passwords do not match! Please try again.")
                break
            print("Error: Password must be at least 8 characters long and contain at least one letter and one number!")

        # Phone number validation
        while True:
            phone_number = input("Phone number: ").strip()
            if validate_phone_number(phone_number):
                break
            print("Error: Invalid Egyptian phone number! Format should be: 01xxxxxxxxx, +20xxxxxxxxxx, or 0020xxxxxxxxxx")

        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'phone_number': phone_number
        }
            
        response = authController.register(new_user)
        print(response.get("message", response.get("error")))
        
        # Auto-login after successful registration
        if response.get("user"):
            self.current_user = response.get("user")

    def login(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        data = authController.login(email, password)
        if data.get("message"):
            self.current_user = data.get("user")
            print(data.get("message"))
        else:
            print(data.get("error"))

    def logout(self):
        if self.current_user:
            print(f"See You, {self.current_user.get('first_name')} {self.current_user.get('last_name')}")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    def show_menu(self):
        print("\n=== Crowdfunding Console Application ===")
        if self.current_user:
            print(f"\nWelcome, {self.current_user.get('first_name')} {self.current_user.get('last_name')}")
            print("\nProject Management:")
            print("1. Create Project")
            print("2. View All Projects")
            print("3. View My Projects")
            print("4. Update Project")
            print("5. Delete Project")
            print("6. Search Projects by Date")
            print("\nAccount:")
            print("7. Logout")
            print("8. Exit")
        else:
            print("\nAuthentication:")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

    def create_project(self):
        print("\n=== Create New Project ===")
        
        # Title validation
        while True:
            title = input("Project title: ").strip()
            if title:
                break
            print("Error: Project title cannot be empty!")

        # Details validation
        while True:
            details = input("Project details: ").strip()
            if details:
                break
            print("Error: Project details cannot be empty!")

        # Total target validation
        while True:
            total_target = input("Total target (EGP): ").strip()
            try:
                total_target = float(total_target)
                if total_target > 0:
                    break
                print("Error: Total target must be greater than zero!")
            except ValueError:
                print("Error: Please enter a valid number for total target!")

        # Start date validation
        while True:
            start_time = input("Start time (YYYY-MM-DD): ").strip()
            if validate_date_format(start_time):
                break
            print("Error: Invalid date format! Please use YYYY-MM-DD format.")

        # End date validation
        while True:
            end_time = input("End time (YYYY-MM-DD): ").strip()
            if not validate_date_format(end_time):
                print("Error: Invalid date format! Please use YYYY-MM-DD format.")
                continue
            
            if validate_dates(start_time, end_time):
                break
            print("Error: End date must be after start date!")

        project_data = {
            'title': title,
            'details': details,
            'total_target': total_target,
            'start_time': start_time,
            'end_time': end_time
        }
        
        response = create_project(project_data, self.current_user)
        print(response.get("message", response.get("error")))

    def view_projects(self):
        print("\n=== All Projects ===")
        projects = view_projects()
        self._display_projects(projects)

    def view_my_projects(self):
        print("\n=== My Projects ===")
        projects = view_user_projects(self.current_user['id'])
        self._display_projects(projects)

    def update_project(self):
        print("\n=== Update Project ===")
        self.view_my_projects()
        
        while True:
            project_id = input("\nEnter project ID to update (or press Enter to cancel): ").strip()
            if not project_id:
                return
            
            # Verify project exists and belongs to user
            projects = view_user_projects(self.current_user['id'])
            if any(p['id'] == project_id for p in projects):
                break
            print("Error: Invalid project ID or you don't have permission to edit this project!")

        print("\nLeave blank to keep current value:")
        updated_data = {}

        # Title update
        new_title = input("New title: ").strip()
        if new_title:
            updated_data['title'] = new_title

        # Details update
        new_details = input("New details: ").strip()
        if new_details:
            updated_data['details'] = new_details

        # Total target update
        while True:
            new_target = input("New total target (EGP): ").strip()
            if not new_target:
                break
            try:
                target = float(new_target)
                if target > 0:
                    updated_data['total_target'] = target
                    break
                print("Error: Total target must be greater than zero!")
            except ValueError:
                print("Error: Please enter a valid number for total target!")

        # Dates update
        while True:
            new_start = input("New start date (YYYY-MM-DD): ").strip()
            if not new_start:
                break
            if validate_date_format(new_start):
                updated_data['start_time'] = new_start
                break
            print("Error: Invalid date format! Please use YYYY-MM-DD format.")

        while True:
            new_end = input("New end date (YYYY-MM-DD): ").strip()
            if not new_end:
                break
            if not validate_date_format(new_end):
                print("Error: Invalid date format! Please use YYYY-MM-DD format.")
                continue
            
            start_time = updated_data.get('start_time', projects[0]['start_time'])
            if validate_dates(start_time, new_end):
                updated_data['end_time'] = new_end
                break
            print("Error: End date must be after start date!")

        if not updated_data:
            print("No changes were made.")
            return

        response = update_project(project_id, updated_data, self.current_user)
        print(response.get("message", response.get("error")))

    def delete_project(self):
        print("\n=== Delete Project ===")
        self.view_my_projects()
        
        while True:
            project_id = input("\nEnter project ID to delete (or press Enter to cancel): ").strip()
            if not project_id:
                return
            
            # Verify project exists and belongs to user
            projects = view_user_projects(self.current_user['id'])
            if any(p['id'] == project_id for p in projects):
                break
            print("Error: Invalid project ID or you don't have permission to delete this project!")

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete this project? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            return

        response = delete_project(project_id, self.current_user)
        print(response.get("message", response.get("error")))

    def search_projects(self):
        print("\n=== Search Projects by Date ===")
        
        while True:
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            if validate_date_format(date_str):
                break
            print("Error: Invalid date format! Please use YYYY-MM-DD format.")

        projects = search_projects_by_date(date_str)
        if isinstance(projects, dict) and projects.get("error"):
            print(projects["error"])
        else:
            self._display_projects(projects)

    def _display_projects(self, projects):
        if not projects:
            print("No projects found.")
            return
        
        for project in projects:
            print("\n-------------------")
            print(f"ID: {project['id']}")
            print(f"Title: {project['title']}")
            print(f"Details: {project['details']}")
            print(f"Target: {project['total_target']} EGP")
            print(f"Duration: {project['start_time']} to {project['end_time']}")
