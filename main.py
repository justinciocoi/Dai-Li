# main.py
# Justin Ciocoi 2024/10/23
# main script for launching application

import sys
from PyQt5.QtWidgets import QApplication
from backend import ui

def main():
    app = QApplication(sys.argv)
    window = ui.WeeklyApp() 
    window.show()
    

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()