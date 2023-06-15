# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#########-------Register user function

def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")
    
    while new_username in username_password.keys():     #loop until user will provide new username
        print("Username already exist.")
        new_username = input("New Username: ")      #asking again for not duplicated use name 

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

#########-------Register user function end 
#########-------Add task function
def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

########--------Add task function end 
########--------view all 
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

########--------view_all function end
########--------view_mine
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    question = input("Which task do you want to see?(-1 for back to menu) ")
    if int(question) == -1:     #user decide to get back to menu 
        print("Going back")
    else:
        ticket_nr = 1       #starting numeration for tasks
        for t in task_list:
            
            if t['username'] == curr_user and ticket_nr == int(question) :
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Ticket number: \t {ticket_nr}\n"      #generating ticket number
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                disp_str += f"Completed: \n {t['completed']}\n"
                print(disp_str)
                # decision about what modification should be done 
                modify_task = input('''Task modification:
c - mark the task as completed
e - edit task
any key to exit
: ''').lower()
                if modify_task == "c": #user want mark this task as close
                    task_list[ticket_nr-1]['completed'] = "Yes"          #marking task as completed
                
                elif modify_task == "e":
                    if t['completed'] == False:
                        task_list[ticket_nr-1] = edit_task(t)
                    else:
                        print("Sorry, this task can't be edited. It is already complited.")
            ticket_nr += 1
        # function that is saving tasks into the file
        save_task_list()
        
            
    

########--------view_mine function end
def generate_report_task():
    f = open("task_overview.txt", "w")
    #define emtpy statistics
    completed_task = 0
    uncompleted_task = 0
    overdue_tasks = 0
    all_tasks = len(task_list)
    today = datetime.today()
    for t in task_list:
        if t['completed'] == True:
            completed_task += 1
        else:
            uncompleted_task += 1
            if t['due_date'] < today:
                overdue_tasks += 1
    
    f.write("Number of all tasks: " + str(all_tasks) + "\n")
    f.write("Number of completed tasks: " + str(completed_task)+ "\n")
    f.write("Number of uncompleted task: " + str(uncompleted_task)+ "\n")
    f.write("Number of overdue tasks: " + str(overdue_tasks)+ "\n")
    f.write("Percentage completed: " + str((completed_task / all_tasks) *100) + "%\n")
    f.write("Percentage overdue: " + str((overdue_tasks / all_tasks) *100) + "%\n")
    f.close()

########## generate user report 
def generate_report_user():
    f = open("user_overview.txt", "w")

    all_tasks = len(task_list) #calculating all tasks in file
    f.write("Number of all tasks: " + str(all_tasks) + "\n\n")
    today = datetime.today() # generating today date
    for user in user_data:
        username, password = user.split(';')
        #clearning statistics for every user
        completed_task = 0
        uncompleted_task = 0
        overdue_tasks = 0
        for t in task_list:
            if t['completed'] == True and t['username'] == username:  # completed user tasks
                completed_task += 1
            elif t['completed'] == False and t['username'] == username: # uncompleted user tasks
                uncompleted_task += 1
                if t['due_date'] < today: #uncompleted and overdue user tasks
                    overdue_tasks += 1
        all_tasks_assigned_to_user = completed_task + uncompleted_task # count all user tasks
        if all_tasks_assigned_to_user == 0: # if username has no tasks, we are not calculating percentages
            f.write("Username: " + username + "\n"
                    + "All tasks: " + str(completed_task + uncompleted_task) + "\n\n"
                    )
        else:
            f.write("Username: " + username + "\n"
                    + "All tasks: " + str(completed_task + uncompleted_task) + "\n"
                    + "Percentage of all tasks: " + str(all_tasks_assigned_to_user/all_tasks*100) + "%\n" 
                    + "Percentage of completed tasks: " + str(completed_task/all_tasks_assigned_to_user*100)+ "%\n"
                    + "Percentage of uncompleted tasks: " + str(uncompleted_task/all_tasks_assigned_to_user*100)+ "%\n"
                    + "Percentage of overdue tasks: " + str(overdue_tasks/all_tasks_assigned_to_user*100)+ "%\n\n"
                    )
    
    f.close()

########## edit task
def edit_task(task):
    print()
    edit = input('''Select what do you want change in this task:
u - edit owner of the task
d - edit due date
any key to exit
: ''').lower()
    if edit == "u":
        print("User assignt to task is: " + task['username'])
        new_username = input("Give me new username for this task: ")
        task['username'] = new_username #overwriting username assigned to task
    elif edit == "d":
        print("Current due_date is: " + task['due_date'].strftime(DATETIME_STRING_FORMAT))
        new_date = input("Give me new due date for this task: ")
        task['due_date'] = datetime.strptime(new_date, '%Y-%m-%d') #changing due date
    else:
        print("Nothing to edit")
    return task #returning modified task to previous call
        
########## edit task END

def save_task_list():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - genarate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
       reg_user()

    elif menu == 'a':
       add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr': #run two separate functions for clear visibility
        generate_report_task()
        generate_report_user()
        
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------") 

        try: #try to catch error if the file does not exists
            tasks_report = open("task_overview.txt", "r")
        except:
            generate_report_task() #generating the report
            tasks_report = open("task_overview.txt", "r")
        
        try: #try to catch error if the file does not exists
            user_report = open("user_overview.txt", "r")
        except:
            generate_report_user()  #generating the report
            user_report = open("user_overview.txt", "r")

        print(tasks_report.read()) 
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print("-----------------------------------")
        print(user_report.read())

        user_report.close()
        tasks_report.close()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")