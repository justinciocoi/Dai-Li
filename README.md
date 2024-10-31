### Dai-Li Task Manager

Pronounced "daily," Dai-Li is a simple task manager application meant to help keep on track with repeating tasks. The app consists of a simple user interface and three tabs, meant to track your daily, weekly, and monthly tasks or goals.

The app uses the PyQt5 framework for the UI and implements some usage of qss as well for styling.

The app uses json to store persistent data as far as tasks go as well as using a TaskManager class defined in python for managing tasks (i.e. adding, removing, saving, logging, etc.).

Currently, there are two ways to use Dai-Li: either by running it as a python file in a development-like environment or by building it yourself using pyinstaller. 


For either approach you will first clone the repository to your local machine and navigate into its directory, as well as create and activate a virtual environment
- Clone the repository

    ```bash
    git clone https://github.com/justinciocoi/dai-li && cd dai-li
    ```

- Create a virtual environment
    ```bash
    python3 -m venv venv
    ```
- Activate virtual environment
    ```bash
    source venv/bin/activate
    ```

For the python file approach the steps are as follows:



- Install relevant python modules
    ```bash
    pip3 install pyqt5
    ```

- Run the main script
    ```bash
    python3 main.py
    ```

Otherwise, you will have to build your own version of the app using pyinstaller. Once again using a virtual environment, we will follow these steps:
- Install pyinstaller
    ```bash
    pip3 install pyinstaller
    ```

- Run initial pyinstaller command to create Dai-Li.spec file
    ```bash
    pyinstaller --onefile --windowed --icon='icon.icns' --name='Dai-Li' main.py
    ```

- Edit the `Analysis` object in the Dai-Li.spec file to match the following:
    ```spec
    a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('styles.qss', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    )
    ```
    
- And finally run the command:
    ```bash
    pyinstaller Dai-Li.spec
    ```
Your executable will be within the project directory but can be moved anywhere and accessed the same. Json data is stored at ~/.myAppData/Dai-Li/data




KNOWN_BUGS

PLANNED_UPDATES:

- A log view is in the works where each task and period (daily/weekly/monthly) will return statistics relating to task completion over time. The log view will also allow users to specify dates between which statistics should be returned, but by default the entire subset of completion will be considered.

- A configuration file used to change styling, colors, and fonts is going to be added to allow for more user personalization of the application

