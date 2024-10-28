# main.py
# Justin Ciocoi 2024/10/23
# main script for launching application

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from backend import ui

def main():
    app = QApplication(sys.argv)
    window = ui.WeeklyApp() 
    window.show()

    fonts = QFontDatabase().families()
    for font in fonts:
        with open("output.txt", "a") as file:
            file.write(f"{font}\n")
    

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()