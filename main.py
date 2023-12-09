import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from core.Browsify import Browsify
from controller import controller_script as control

def main():
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Browsify")
    window = Browsify()
    control.load_bookmarks_from_file(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
