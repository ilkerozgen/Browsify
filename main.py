import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Create a new tab with the initial page
        self.add_new_tab(QUrl("http://www.google.com"), "Home")

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Set styles for the tabs
        self.setStyleSheet("""
            QTabBar::tab {
                background: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 100px;
                padding: 8px;
                margin: 0;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                border: 1px solid #cccccc;
            }
                           
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
                           
            QToolBar QToolButton:hover {
                background-color: #e0e0e0;
            }
        """)

        # Back Button with Icon
        back_btn = QAction(QIcon('icons/back.png'), 'Back', self)
        back_btn.setStatusTip('Back to previous page')
        back_btn.triggered.connect(self.current_browser().back)
        navbar.addAction(back_btn)

        # Forward Button with Icon
        forward_btn = QAction(QIcon('icons/forward.png'), 'Forward', self)
        forward_btn.setStatusTip('Forward to the next page')
        forward_btn.triggered.connect(self.current_browser().forward)
        navbar.addAction(forward_btn)

        # Reload Button with Icon
        reload_btn = QAction(QIcon('icons/reload.png'), 'Reload', self)
        reload_btn.setStatusTip('Reload page')
        reload_btn.triggered.connect(self.current_browser().reload)
        navbar.addAction(reload_btn)

        # Home Button with Icon
        home_btn = QAction(QIcon('icons/home.png'), 'Home', self)
        home_btn.setStatusTip('Go home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Bookmark Button with Icon
        bookmark_btn = QAction(QIcon('icons/add.png'), 'Add Bookmark', self)
        bookmark_btn.setStatusTip('Bookmark current page')
        bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(bookmark_btn)

        # Remove Bookmark Button with Icon
        remove_bookmark_btn = QAction(QIcon('icons/remove.png'), 'Remove Bookmark', self)
        remove_bookmark_btn.setStatusTip('Remove selected bookmark')
        remove_bookmark_btn.triggered.connect(self.remove_bookmark)
        navbar.addAction(remove_bookmark_btn)

        # New Tab Button with Icon
        new_tab_btn = QAction(QIcon('icons/newtab.png'), 'New Tab', self)
        new_tab_btn.setStatusTip('Open a new tab')
        new_tab_btn.triggered.connect(self.add_new_tab_action)
        navbar.addAction(new_tab_btn)

        # Show Bookmarks ComboBox
        self.bookmarks_combo = QComboBox()
        self.bookmarks_combo.activated.connect(self.navigate_to_bookmark)
        navbar.addWidget(self.bookmarks_combo)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Updating URL bar
        self.current_browser().urlChanged.connect(lambda qurl: self.update_urlbar(qurl, self.current_browser()))

        # Status Bar
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Bookmarks
        self.bookmarks = {}

        # Set window properties
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle("Simple Browser")

        # Initially, show bookmarks
        self.show_bookmarks()

    def add_new_tab_action(self):
        self.add_new_tab()

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl("http://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)
        self.tabs.setTabToolTip(i, qurl.host())

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.titleChanged.connect(lambda title, index=i: self.update_tab_title(index, title))

    def current_browser(self):
        return self.tabs.currentWidget()

    def update_urlbar(self, q, browser=None):
        if browser and browser == self.current_browser():
            self.url_bar.setText(q.toString())
            self.url_bar.setCursorPosition(0)

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.current_browser().setUrl(q)

    def add_bookmark(self):
        current_url = self.current_browser().url().toString()

        # Prompt the user for a bookmark name
        name, ok = QInputDialog.getText(self, 'Add Bookmark', 'Enter a name for the bookmark:')

        if ok and name:
            if current_url not in self.bookmarks:
                self.bookmarks[current_url] = name
                self.bookmarks_combo.addItem(name)
                QMessageBox.information(self, 'Bookmark Added', f'Bookmark added: {name}')

    def remove_bookmark(self):
        current_index = self.bookmarks_combo.currentIndex()
        if current_index >= 0 and current_index < self.bookmarks_combo.count():
            bookmark_name = self.bookmarks_combo.itemText(current_index)
            url = self.get_url_from_bookmark_name(bookmark_name)
            
            if url:
                del self.bookmarks[url]
                self.bookmarks_combo.removeItem(current_index)
                QMessageBox.information(self, 'Bookmark Removed', f'Bookmark removed: {bookmark_name}')
            else:
                QMessageBox.warning(self, 'Error', 'Bookmark not found.')

    def get_url_from_bookmark_name(self, bookmark_name):
        for url, name in self.bookmarks.items():
            if name == bookmark_name:
                return url
        return ""

    def show_bookmarks(self):
        if not self.bookmarks:
            self.bookmarks_combo.addItem('No Bookmarks Selected')
        else:
            self.bookmarks_combo.addItems(self.bookmarks.values())

    def navigate_to_bookmark(self, index):
        bookmark_name = self.bookmarks_combo.itemText(index)
        if bookmark_name == 'No Bookmarks Selected':
            self.navigate_home()
        else:
            url = [key for key, value in self.bookmarks.items() if value == bookmark_name]
            if url:
                self.current_browser().setUrl(QUrl(url[0]))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def update_tab_title(self, index, title):
        self.tabs.setTabText(index, title)

app = QApplication(sys.argv)
QApplication.setApplicationName("Simple Browser")
window = Browser()
window.show()
app.exec_()
