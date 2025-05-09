from utils import save_data, load_data, validate_dates
from Project import Project
import uuid

def create_project(project_data, current_user):
    projects = load_data('projects')
    
    try:
        project = Project(
            id=str(uuid.uuid4()),
            title=project_data['title'],
            details=project_data['details'],
            total_target=float(project_data['total_target']),
            start_time=project_data['start_time'],
            end_time=project_data['end_time'],
            owner_id=current_user['id']
        )
        
        project_dict = project.to_dict()
        projects.append(project_dict)
        save_data('projects', projects)
        return {"message": "Project created successfully", "project": project_dict}
    except Exception as e:
        return {"error": f"Failed to create project: {str(e)}"}

def view_projects():
    return load_data('projects')

def view_user_projects(user_id):
    projects = load_data('projects')
    return [p for p in projects if p['owner_id'] == user_id]

def update_project(project_id, updated_data, current_user):
    projects = load_data('projects')
    
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return {"error": "Project not found"}
        
    if project['owner_id'] != current_user['id']:
        return {"error": "You can only edit your own projects"}
        
    project.update(updated_data)
    save_data('projects', projects)
    return {"message": "Project updated successfully", "project": project}

def delete_project(project_id, current_user):
    projects = load_data('projects')
    
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return {"error": "Project not found"}
        
    if project['owner_id'] != current_user['id']:
        return {"error": "You can only delete your own projects"}
        
    projects = [p for p in projects if p['id'] != project_id]
    save_data('projects', projects)
    return {"message": "Project deleted successfully"}

def search_projects_by_date(date_str):
    from datetime import datetime
    projects = load_data('projects')
    try:
        search_date = datetime.strptime(date_str, '%Y-%m-%d')
        return [
            p for p in projects 
            if datetime.strptime(p['start_time'], '%Y-%m-%d') <= search_date <= datetime.strptime(p['end_time'], '%Y-%m-%d')
        ]
    except ValueError:
        return {"error": "Invalid date format"}