from Application import Application

def main():
    app = Application()
    
    while True:
        app.show_menu()
        choice = input("\nChoose an option: ")
        
        if app.current_user is None:
            if choice == "1":
                app.login()
            elif choice == "2":
                app.register()
            elif choice == "3":
                print("See You!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            if choice == "1":
                app.create_project()
            elif choice == "2":
                app.view_projects()
            elif choice == "3":
                app.view_my_projects()
            elif choice == "4":
                app.update_project()
            elif choice == "5":
                app.delete_project()
            elif choice == "6":
                app.search_projects()
            elif choice == "7":
                app.logout()
            elif choice == "8":
                print("Thanks for using our application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()