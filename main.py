import sys
from PyQt5.QtWidgets import *
from api.Browsify import Browsify

def main():
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Browsify")
    window = Browsify()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
