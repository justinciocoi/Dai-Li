#helpers.py

from datetime import datetime, timedelta
from PyQt5.QtCore import QFile, QTextStream

##Function to get current date
def getDate():
    dt = datetime.today()
    day = dt.day
    daystring = dt.strftime("%A")
    month = dt.strftime("%B")
    intMonth = dt.month
    year = dt. year

    sunday = dt - timedelta(days=dt.weekday() + 1)

    return day, sunday.day, month, year, intMonth, daystring

def load_stylesheet(file_name):
    file = QFile(file_name)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    return stream.readAll()

