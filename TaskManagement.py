import datetime

# Define Task class
class Task:
    def __init__(self, title, description, due_date, priority="Medium", category="General", status="Pending"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.status = status
    
    def update_status(self, new_status):
        self.status = new_status
    
    def __str__(self):
        return f"[ {self.status} ] {self.title} | Due: {self.due_date} | Priority: {self.priority} | Category: {self.category}\nDescription: {self.description}\n"

# Define User class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
    
    def update_task_status(self, title, new_status):
        for task in self.tasks:
            if task.title == title:
                task.update_status(new_status)
                return True
        return False
    
    def get_tasks(self, sort_by="due_date"):
        return sorted(self.tasks, key=lambda t: getattr(t, sort_by))
    
    def search_tasks(self, keyword):
        return [task for task in self.tasks if keyword.lower() in task.title.lower()]

# User Management
class TaskManager:
    def __init__(self):
        self.users = {}
        self.current_user = None
    
    def register(self):
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty!")
            return
        
        password = input("Enter password: ").strip()
        if not password:
            print("Password cannot be empty!")
            return
        
        if username in self.users:
            print("Username already exists!")
        else:
            self.users[username] = User(username, password)
            print("User registered successfully!")
    
    def login(self):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Welcome, {username}!")
        else:
            print("Invalid credentials!")
    
    def add_task(self):
        if not self.current_user:
            print("You must be logged in!")
            return
        
        title = input("Task title: ").strip()
        if not title:
            print("Task title cannot be empty!")
            return
        
        desc = input("Description: ").strip()
        due_date = input("Due date (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD.")
            return
        
        priority_options = ["High", "Medium", "Low"]
        priority = input("Priority (High/Medium/Low): ").strip().capitalize()
        if priority not in priority_options:
            print("Invalid priority! Choose from High, Medium, or Low.")
            return
        
        category = input("Category: ").strip()
        
        task = Task(title, desc, due_date, priority, category)
        self.current_user.add_task(task)
        print("Task added successfully!")

    def view_tasks(self):
        if not self.current_user:
            print("You must be logged in!")
            return
        tasks = self.current_user.get_tasks()
        if not tasks:
            print("No tasks available.")
            return
        for task in tasks:
            print(task)

    def delete_task(self):
        if not self.current_user:
            print("You must be logged in!")
            return
        
        tasks = self.current_user.get_tasks()
        if not tasks:
            print("No tasks available to delete.")
            return
        
        print("\nSelect a task to delete:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.title} (Due: {task.due_date})")
        
        try:
            choice = int(input("Enter the task number: ").strip())
            if 1 <= choice <= len(tasks):
                task_title = tasks[choice - 1].title
                self.current_user.delete_task(task_title)
                print(f"Task '{task_title}' deleted successfully!")
            else:
                print("Invalid selection!")
        except ValueError:
            print("Please enter a valid number!")

    def update_task(self):
        if not self.current_user:
            print("You must be logged in!")
            return
        
        tasks = self.current_user.get_tasks()
        if not tasks:
            print("No tasks available to update.")
            return
        
        print("\nSelect a task to update:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.title} (Status: {task.status})")
        
        try:
            choice = int(input("Enter the task number: ").strip())
            if 1 <= choice <= len(tasks):
                task_title = tasks[choice - 1].title
                status_options = ["Pending", "In Progress", "Completed"]
                
                print("\nSelect new status:")
                for idx, status in enumerate(status_options, start=1):
                    print(f"{idx}. {status}")
                
                status_choice = int(input("Enter the status number: ").strip())
                if 1 <= status_choice <= len(status_options):
                    new_status = status_options[status_choice - 1]
                    self.current_user.update_task_status(task_title, new_status)
                    print(f"Task '{task_title}' updated to '{new_status}' successfully!")
                else:
                    print("Invalid status selection!")
            else:
                print("Invalid task selection!")
        except ValueError:
            print("Please enter a valid number!")

    def search_tasks(self):
        if not self.current_user:
            print("You must be logged in!")
            return
        
        keyword = input("Search keyword: ").strip()
        if not keyword:
            print("Search keyword cannot be empty!")
            return
        
        results = self.current_user.search_tasks(keyword)
        if not results:
            print("No matching tasks found.")
            return
        for task in results:
            print(task)

    def menu(self):
        while True:
            print("\nTASK MANAGER\n1. Register\n2. Login\n3. Exit")
            choice = input("Select an option: ").strip()
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
                if self.current_user:
                    self.user_dashboard()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice!")

    def user_dashboard(self):
        while True:
            print("\nUSER DASHBOARD\n1. Add Task\n2. View Tasks\n3. Update Task\n4. Delete Task\n5. Search Tasks\n6. Logout")
            choice = input("Select an option: ").strip()
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.search_tasks()
            elif choice == "6":
                print("Logging out...")
                self.current_user = None
                break
            else:
                print("Invalid choice!")

# Run application
if __name__ == "__main__":
    app = TaskManager()
    app.menu()
