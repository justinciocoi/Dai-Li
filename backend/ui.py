# ui.py
# Justin Ciocoi 2024/10

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QTabWidget, QLabel, QLineEdit, QListWidget, QPushButton)
from PyQt5.QtCore import Qt
from backend import helpers
from backend import tasks

## Class to define each tab of the app
class Tab(QWidget):
    def __init__(self, title):
        super().__init__()

        layout = QVBoxLayout() ##Defines the layout of the tab as a vertical layout

        self.title_label = QLabel(f"<h1>{title}</h1>") ## creates var title_label
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label) ## adds title_label to layout

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter new task")

        self.add_button = QPushButton("Add Task")
        self.add_button.setFixedWidth(150)

        #self.history_view_button = QPushButton("History")
        #self.history_view_button.setFixedWidth(100)

        
        ## Connects the signal of enter being pressed in task_input to clicking the add_button
        self.task_input.returnPressed.connect(self.add_button.click)
        #self.history_view_button.clicked.connect(self.show_popup)
        
        ##put the widgets on the layout
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_button, alignment=Qt.AlignHCenter)
        #layout.addWidget(self.history_view_button, alignment=Qt.AlignHCenter)
    
    
        self.setLayout(layout) ##sets tab layout to tab

    def show_popup(self):
        self.popup = LogView()
        self.popup.setWindowTitle("History")
        self.popup.setGeometry(150,150,200,100)

        self.popup.show()

## Class definition for main App
class WeeklyApp(QMainWindow):
    ## constructor
    def __init__(self):
        super().__init__()

        today_day, sunday_day, current_month, current_year, int_month, day_string = helpers.getDate()

        self.setWindowTitle("Dai-Li")
        self.setGeometry(100, 100, 300, 500)

        stylesheet = helpers.load_stylesheet("styling/styles.qss")
        self.setStyleSheet(stylesheet)
        self.spacer = QWidget()
        self.spacer.setGeometry(0,0,300,20)
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.tab_tracker)


        self.tab1 = Tab("Daily")
        self.tab2 = Tab("Weekly")
        self.tab3 = Tab("Monthly")

        self.tab1.title_label.setText(f"<h1>{day_string} {int_month}/{today_day}/{current_year}</h1>")
        self.tab2.title_label.setText(f"<h1>Week of {int_month}/{sunday_day}/{current_year}</h1>")
        self.tab3.title_label.setText(f"<h1>{current_month} {current_year}</h1>")

        self.task_manager = tasks.TaskManager(self.tab1, self.tab2, self.tab3, self)

        self.task_manager.load_tasks()

        self.tab1.add_button.clicked.connect(self.task_manager.add_task)
        self.tab2.add_button.clicked.connect(self.task_manager.add_task)
        self.tab3.add_button.clicked.connect(self.task_manager.add_task)

        self.tab_widget.addTab(self.tab1, "Daily")
        self.tab_widget.addTab(self.tab2, "Weekly")
        self.tab_widget.addTab(self.tab3, "Monthly")

        self.setCentralWidget(self.tab_widget)

        ## Connect currentItemChanged to update selected_item
        self.tab1.task_list.currentItemChanged.connect(self.item_selected)
        self.tab2.task_list.currentItemChanged.connect(self.item_selected)
        self.tab3.task_list.currentItemChanged.connect(self.item_selected)

        self.selected_item = None
        self.current_tab = 0  ## Track the current tab

    # Function to track which tab the user is currently on
    def tab_tracker(self, index):
        self.current_tab = index
        self.task_manager.current_tab = index

    # Function to remove task from list
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace and self.selected_item:
            # Determine which task list is currently active
            if self.current_tab == 0:
                task_list = self.tab1.task_list
            elif self.current_tab == 1:
                task_list = self.tab2.task_list
            elif self.current_tab == 2:
                task_list = self.tab3.task_list
            
            # Get the row of the selected item
            current_row = task_list.row(self.selected_item)
            
            # Remove the selected item from the task list
            task_list.takeItem(current_row)

            # Clear selected_item since it was just removed
            self.selected_item = None

            # Handle the case where other items are still in the list
            if task_list.count() > 0:
                # Try to select the item in the same row (or the previous one if at the end)
                new_row = min(current_row, task_list.count() - 1)
                task_list.setCurrentRow(new_row)
                self.selected_item = task_list.currentItem()

            # Save the tasks to ensure deletion is persistent
            self.task_manager.save_tasks()

        elif event.key() == Qt.Key_Left and self.current_tab > 0:
        # Switch to the previous tab (move left)
            self.current_tab -= 1
            self.tab_widget.setCurrentIndex(self.current_tab)

        elif event.key() == Qt.Key_Right and self.current_tab < 2:
            # Switch to the next tab (move right)
            self.current_tab += 1
            self.tab_widget.setCurrentIndex(self.current_tab)

            self.tab_tracker(self.current_tab)
        
    # Update selected_item whenever the current item changes
    def item_selected(self, current):
        # If there is a current item, update selected_item; otherwise, set it to None
        if current:
            self.selected_item = current
        else:
            self.selected_item = None

    

class LogView(QWidget):
    def __init__(self):
        super().__init__()

        stylesheet = helpers.load_stylesheet("styling/styles.qss")
        self.setStyleSheet(stylesheet)

        layout = QVBoxLayout()

        self.label = QLabel("History")
        layout.addWidget(self.label)

        self.setLayout(layout)

        

        


    

        