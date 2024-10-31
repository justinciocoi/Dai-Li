# tasks.py
# Justin Ciocoi 2023/10/23

import json
import os
import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QListWidgetItem, QCheckBox
from PyQt5.QtCore import QTimer



class TaskManager:
    ## Constructor for Task Manager Class
    def __init__(self, tab1, tab2, tab3, parent):

        self.data_directory_path = os.path.join(os.path.expanduser('~'), ".myAppData", "Dai-Li", "data")
        self.task_file_path = os.path.join(self.data_directory_path, "tasks.json")
        self.log_file_path = os.path.join(self.data_directory_path, "log.json")
        self.tab1 = tab1
        self.tab2 = tab2
        self.tab3 = tab3
        self.parent = parent
        self.selected_item = None
        self.current_tab = 0

        self.initialize_tasks_json()

        self.timer = QTimer()
        with open(self.task_file_path, "r") as file:
            tasks = json.load(file)

        self.timer.timeout.connect(self.check_reset)
        self.timer.start(60000) # Checks once per minute, change to 60000 to 1000 to check every second instead


        self.check_reset_at_launch(tasks)
        



    ## Function to handle placing entered text into the task list
    def add_task(self):
        # Get the current tab's task input and task list directly
        if self.current_tab == 0:
            task_input = self.tab1.task_input
            task_list = self.tab1.task_list
        elif self.current_tab == 1:
            task_input = self.tab2.task_input
            task_list = self.tab2.task_list
        elif self.current_tab == 2:
            task_input = self.tab3.task_input
            task_list = self.tab3.task_list

        task_text = task_input.text()

        if task_text:
            # Create a new QListWidgetItem
            item = QListWidgetItem()
            
            # Make the list item expand to fit the content
            
            task_list.addItem(item)

            # Create a new QCheckBox
            checkbox = QCheckBox(task_text)
            checkbox.stateChanged.connect(self.save_tasks)
            
            

            # Associate the QCheckBox with the QListWidgetItem
            task_list.setItemWidget(item, checkbox)

            # Clear the input field after adding the task
            task_input.clear()

            # Save the tasks to the JSON file after adding
            self.save_tasks()



    ##Saves task data to json
    def save_tasks(self):
        # Retrieve current tasks
        tasks = {
            "daily": self.get_tasks(self.tab1.task_list),
            "weekly": self.get_tasks(self.tab2.task_list),
            "monthly": self.get_tasks(self.tab3.task_list),
        }

        try:
            # Load the entire JSON data
            with open(self.task_file_path, "r+") as file:
                data = json.load(file)
                data["tasks"] = tasks  # Update only the tasks section

                # Write back the updated data
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()  # Ensure old content is cleared if file size shrinks

        except FileNotFoundError:
            # Initialize JSON structure if file is missing
            with open(self.task_file_path, "w") as file:
                json.dump({
                    "tasks": tasks,
                    "last_reset": {"daily": "", "weekly": "", "monthly": ""}
                }, file, indent=4)



    ##Saves reset data to json
    def save_reset_time(self, period):
        with open(self.task_file_path, "r+") as file:
            data = json.load(file)
            now = datetime.now()

            if period == "daily":
                data["last_reset"]["daily"] = now.strftime("%Y-%m-%d")
            elif period == "weekly":
                data["last_reset"]["weekly"] = now.strftime("%Y-%m-%d")
            elif period == "monthly":
                data["last_reset"]["monthly"] = now.strftime("%Y-%m")

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()



    ##Function which gets data from app to json
    def get_tasks(self, task_list):
        tasks = []
        for index in range(task_list.count()):
            item = task_list.item(index)
            checkbox = task_list.itemWidget(item)  # Get the widget (QCheckBox) associated with the item

            if checkbox is not None:
                task_text = checkbox.text()  # Get the task text
                checked = checkbox.isChecked()  # Get whether the task is checked
                tasks.append({"task": task_text, "checked": checked})  # Add task to list without removing it
            else:
                print(f"Warning: No checkbox found for item at index {index}")
        #print(f"get_tasks() result: {tasks}")  # Debug output for all tasks
        return tasks



    ## Function which loads in tasks
    def load_tasks(self):
        if not os.path.exists(self.task_file_path):
            return
        
        with open(self.task_file_path, "r") as file:
            tasks = json.load(file)

        self.populate_tasks(self.tab1.task_list, tasks.get("tasks", {}).get("daily", []))
        self.populate_tasks(self.tab2.task_list, tasks.get("tasks", {}).get("weekly", []))
        self.populate_tasks(self.tab3.task_list, tasks.get("tasks", {}).get("monthly", []))

        #print(f"get_tasks() result: {tasks}")  # Debug output for all tasks



    ## Function which populates items and passes them to load_tasks()
    def populate_tasks(self, task_list, tasks):
        for task in tasks:
            # Create a new QListWidgetItem for each task
            item = QListWidgetItem()
            task_list.addItem(item)

            # Create a new QCheckBox and set its text and checked state
            checkbox = QCheckBox(task["task"])
            checkbox.setChecked(task["checked"])  # Properly set the checked state

            # Connect stateChanged signal to save the task when checked/unchecked
            checkbox.stateChanged.connect(self.save_tasks)
            # checkbox.clicked.connect(lambda: self.parent.item_selected(item))
            # Add the checkbox to the QListWidgetItem
            task_list.setItemWidget(item, checkbox)



    ## Function to continuously check for reset while the app runs
    def check_reset(self, now=None):
        if now is None:
            now = datetime.now()

        if now.hour == 0 and now.minute == 0:
            self.log_data("daily")
            self.reset_tasks("daily")
        #else:
            #print("No Daily Reset this Minute", now.strftime("%Y/%d/%m || %H:%M:%S"))

        if now.weekday() == 6 and now.hour == 0 and now.minute == 0:
            self.log_data("weekly")
            self.reset_tasks("weekly")
        #else:
            #print("No Weekly Reset this Minute", now.strftime("%Y/%d/%m || %H:%M:%S"))

        if now.day == 1 and now.hour == 0 and now.minute == 0:
            self.log_data("monthly")
            self.reset_tasks("monthly")
        #else:
            #print("No Monthly Reset this Minute", now.strftime("%Y/%d/%m || %H:%M:%S"))



    ## Function to check if a reset is warranted for any tab at app launch
    def check_reset_at_launch(self, tasks):
        now = datetime.now()

        # Check if a daily reset is needed
        last_daily_reset = tasks.get("last_reset", {}).get("daily", "")
        if last_daily_reset:
            last_daily_reset_date = datetime.strptime(last_daily_reset, "%Y-%m-%d")
            if now.date() > last_daily_reset_date.date():
                self.log_data("daily")
                self.reset_tasks("daily")  # Reset daily tasks
                
            #else:
                #print("No Daily Reset at Launch")

        # Check if a weekly reset is needed
        last_weekly_reset = tasks.get("last_reset", {}).get("weekly", "")
        if last_weekly_reset:
            last_weekly_reset_date = datetime.strptime(last_weekly_reset, "%Y-%m-%d")
            
            # Calculate the most recent Sunday midnight
            last_sunday = now - timedelta(days=now.weekday() + 1)  # Get last Sunday
            last_sunday_midnight = datetime(last_sunday.year, last_sunday.month, last_sunday.day)  # Set to midnight
            
            # Check if last Sunday midnight is later than the last weekly reset
            if last_sunday_midnight > last_weekly_reset_date:
                self.log_data("weekly")
                self.reset_tasks("weekly")  # Reset weekly tasks in JSON
          
               

        # Check if a monthly reset is needed
        last_monthly_reset = tasks.get("last_reset", {}).get("monthly", "")
        if last_monthly_reset:
            last_monthly_reset_date = datetime.strptime(last_monthly_reset, "%Y-%m")
            # Reset if it's a new month
            if now.year > last_monthly_reset_date.year or now.month > last_monthly_reset_date.month:
                self.log_data("monthly")
                self.reset_tasks("monthly")  # Reset monthly tasks
                
            #else:
                #print("No Monthly Reset at Launch")



    ## Function which resets task completion status
    def reset_tasks(self, period):
        """
        Reset tasks directly in the JSON file by unchecking them, rather than updating the UI first.
        """
        try:
            # Load the JSON data
            with open(self.task_file_path, "r+") as file:
                data = json.load(file)
                
                # Access the specified period's tasks and reset checked status
                tasks_to_reset = data.get("tasks", {}).get(period, [])
                for task in tasks_to_reset:
                    task["checked"] = False  # Uncheck the task in the JSON data
                
                # Update the last reset timestamp for this period
                now = datetime.now()
                if "last_reset" not in data:
                    data["last_reset"] = {}
                data["last_reset"][period] = now.strftime("%Y-%m-%d") if period != "monthly" else now.strftime("%Y-%m")
                
                # Write the modified data back to the file
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            print(f"{period.capitalize()} tasks have been reset in JSON.")
            #self.log_data()
        except FileNotFoundError:
            print("tasks.json file not found. Unable to reset tasks.")



    ## Function for initializing json file when not found
    def initialize_tasks_json(self):
        import os
        original_dir = os.getcwd()
        os.chdir(self.data_directory_path)
        if not os.path.exists("tasks.json"):
            
            with open("tasks.json", "w") as file:
                json.dump({
                    "tasks": {"daily": [], "weekly": [], "monthly": []},
                    "last_reset": {"daily": "1900-1-1", "weekly": "1900-1-1", "monthly": "1900-1"}
                }, file, indent=4)

        if not os.path.exists("log.json"):
            with open("log.json", "w") as file:
                json.dump({

                }, file, indent=4)
        
        os.chdir(original_dir)

            



    ## Convers tasks.json to 
    def convert_to_log_form(self, period):
        with open(self.task_file_path, "r") as file:
            task_data = json.load(file)

        # Attempt to load existing log data, or initialize a new structure
        try:
            with open("data/successRates.json", "r") as file:
                log_data = json.load(file)
        except FileNotFoundError:
            log_data = {"daily": {}, "weekly": {}, "monthly": {}}

        # Ensure the period (e.g., "daily", "weekly", "monthly") exists in log_data
        if period not in log_data:
            log_data[period] = {}

        current_date = datetime.now().strftime("%Y-%m-%d")

        for task in task_data["tasks"].get(period, []):
            task_name = task["task"]
            task_status = task.get("checked", False)

            # Initialize task entry in log_data if not already present
            if task_name not in log_data[period]:
                log_data[period][task_name] = {
                    "successes": 0,
                    "failures": 0,
                    "last_update": None
                }

            # Update successes or failures based on the task's status
            if task_status:
                log_data[period][task_name]["successes"] += 1
            else:
                log_data[period][task_name]["failures"] += 1

            # Update the last_update date
            log_data[period][task_name]["last_update"] = current_date

        return log_data


    def log_data(self, period):
        data = self.convert_to_log_form(period)
        with open("data/successRates.json", "w") as file:
            json.dump(data, file, indent=4)











    ## clears log.json and reinitializes it
    #def clear_logs(self):


    
    ## clears tasks for current tab
    #def clear_tasks(self, period):
