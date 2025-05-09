from utils import save_data, load_data
import bcrypt
import uuid
from User import User

def register(new_user):
    users = load_data('users')
    
    if any(user.get('email') == new_user['email'] for user in users):
        return {"error": "Email already registered!"}
    
    try:
        hashed_password = bcrypt.hashpw(new_user['password'].encode(), bcrypt.gensalt()).decode()
        
        user = User(
            id=str(uuid.uuid4()),
            first_name=new_user['first_name'],
            last_name=new_user['last_name'],
            email=new_user['email'],
            password=hashed_password,
            phone_number=new_user['phone_number']
        )
        
        user_dict = user.to_dict()
        users.append(user_dict)
        save_data('users', users)
        
        return {"message": "Registration successful", "user": user_dict}
    except Exception as e:
        return {"error": f"Registration failed: {str(e)}"}

def login(email, password):
    users = load_data('users')
    for user in users:
        if user['email'] == email:
            if bcrypt.checkpw(password.encode(), user['password'].encode()):
                return {"message": "Login successful", "user": user}
    return {"error": "Invalid email or password"}

def logout(current_user):
    if current_user:
        return {"message": "Logout successful"}
    return {"error": "No user is currently logged in"}

