import sys
from PyQt5.QtWidgets import *
from api.browsify import Browsify

def main():
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Browsify")
    window = Browsify()
    window.load_bookmarks_from_file()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
