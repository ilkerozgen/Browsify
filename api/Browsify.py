import json
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from frontend.Styles import BrowsifyStyles

class Browsify(QMainWindow):
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

        # Set styles
        self.setStyleSheet(BrowsifyStyles().getStyles())

        # Back Button
        back_btn = QAction(QIcon('visual/icons/back.png'), 'Back', self)
        back_btn.setStatusTip('Back to previous page')
        back_btn.triggered.connect(self.current_browser().back)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction(QIcon('visual/icons/forward.png'), 'Forward', self)
        forward_btn.setStatusTip('Forward to the next page')
        forward_btn.triggered.connect(self.current_browser().forward)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction(QIcon('visual/icons/reload.png'), 'Reload', self)
        reload_btn.setStatusTip('Reload page')
        reload_btn.triggered.connect(self.current_browser().reload)
        navbar.addAction(reload_btn)

        # Stop Button
        stop_btn = QAction(QIcon('visual/icons/stop.png'), 'Stop', self)
        stop_btn.setStatusTip('Stop loading the current page')
        stop_btn.triggered.connect(self.current_browser().stop)
        navbar.addAction(stop_btn)

        # Home Button
        home_btn = QAction(QIcon('visual/icons/home.png'), 'Home', self)
        home_btn.setStatusTip('Go home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # New Tab Button
        new_tab_btn = QAction(QIcon('visual/icons/newtab.png'), 'New Tab', self)
        new_tab_btn.setStatusTip('Open a new tab')
        new_tab_btn.triggered.connect(self.add_new_tab_action)
        navbar.addAction(new_tab_btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        self.url_bar.mousePressEvent = self.urlbar_mousePressEvent
        self.tabs.currentChanged.connect(self.update_urlbar_on_tab_change)

        # Updating URL bar
        self.current_browser().urlChanged.connect(lambda qurl: self.update_urlbar(qurl, self.current_browser()))

        # Status Bar
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Add Bookmark Button
        add_bookmark_btn = QAction(QIcon('visual/icons/add.png'), 'Add Bookmark', self)
        add_bookmark_btn.setStatusTip('Bookmark current page')
        add_bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(add_bookmark_btn)

        # Remove Bookmark Button
        remove_add_bookmark_btn = QAction(QIcon('visual/icons/remove.png'), 'Remove Bookmark', self)
        remove_add_bookmark_btn.setStatusTip('Remove selected bookmark')
        remove_add_bookmark_btn.triggered.connect(self.remove_bookmark)
        navbar.addAction(remove_add_bookmark_btn)

        # Show Bookmarks ComboBox
        self.bookmarks_combo = QComboBox()
        self.bookmarks_combo.activated.connect(self.navigate_to_bookmark)
        navbar.addWidget(self.bookmarks_combo)

       # Sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        # Add Bookmarks Sidebar Button
        toggle_sidebar_btn = QAction(QIcon('visual/icons/sidebar.png'), 'Toggle Sidebar', self)
        toggle_sidebar_btn.setStatusTip('Toggle Bookmarks Sidebar')
        toggle_sidebar_btn.triggered.connect(self.toggle_sidebar)
        navbar.addAction(toggle_sidebar_btn)

        # Add the sidebar to the main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tabs)

        main_layout.addWidget(self.sidebar)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initially, hide the sidebar
        self.sidebar.hide()

        # Bookmarks
        self.bookmarks = {}
        self.bookmarks_combo.addItem('No Bookmarks Selected')

        try:
            with open("db/bookmarks.json", 'r') as file:
                self.bookmarks = json.load(file)
        except FileNotFoundError:
            # Handle the case where the file is not found (e.g., first run)
            pass

        # Set window properties
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("Browsify")

        # Initially, show bookmarks
        self.show_bookmarks()

    # Add the toggle_sidebar method
    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            self.sidebar.show()

    # Function to select text in the URL bar when clicked
    def urlbar_mousePressEvent(self, event):
        self.url_bar.selectAll()

    # Handler for add new tab
    def add_new_tab_action(self):
        self.add_new_tab()

    # Function to add a new tab
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

    # Function to return the current browser
    def current_browser(self):
        return self.tabs.currentWidget()

    # Function to update toolbar
    def update_urlbar(self, q, browser=None):
        if browser and browser == self.current_browser():
            self.url_bar.setText(q.toString())
            self.url_bar.setCursorPosition(0)

    # Function to navigate to home page
    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://www.google.com"))

    # Function to navigate to specified URL
    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.current_browser().setUrl(q)

    # Function to save bookmarks to a JSON file
    def save_bookmarks_to_file(self, filename='db/bookmarks.json'):
        with open(filename, 'w') as file:
            json.dump(self.bookmarks, file)

    # Function to load bookmarks from a JSON file
    def load_bookmarks_from_file(self, filename='db/bookmarks.json'):
        try:
            with open(filename, 'r') as file:
                self.bookmarks = json.load(file)
        except FileNotFoundError:
            # Handle the case where the file is not found (e.g., first run)
            pass

    # Function to add bookmark
    def add_bookmark(self):
        current_url = self.current_browser().url().toString()

        # Prompt the user for a bookmark name
        name, ok = QInputDialog.getText(self, 'Add Bookmark', 'Enter a name for the bookmark:')

        if ok and name:
            if current_url not in self.bookmarks:
                self.bookmarks[current_url] = name
                self.bookmarks_combo.addItem(name)
                QMessageBox.information(self, 'Bookmark Added', f'Bookmark added: {name}')

             # Save bookmarks to file
            self.save_bookmarks_to_file()

    # Function to remove a bookmark
    def remove_bookmark(self):
        current_index = self.bookmarks_combo.currentIndex()

        if current_index >= 0 and current_index < self.bookmarks_combo.count():
            bookmark_name = self.bookmarks_combo.itemText(current_index)
            url = self.get_url_from_bookmark_name(bookmark_name)
            
            if url:
                del self.bookmarks[url]
                self.bookmarks_combo.removeItem(current_index)
                QMessageBox.information(self, 'Bookmark Removed', f'Bookmark removed: {bookmark_name}')

                # Save bookmarks to file
                self.save_bookmarks_to_file()
            else:
                QMessageBox.warning(self, 'Error', 'Bookmark not found.')

    # Function to update URL bar when the current tab changes
    def update_urlbar_on_tab_change(self, index):
        current_browser = self.tabs.widget(index)
        if current_browser:
            self.update_urlbar(current_browser.url(), current_browser)

    # Function to get the URL of a bookmark
    def get_url_from_bookmark_name(self, bookmark_name):
        for url, name in self.bookmarks.items():
            if name == bookmark_name:
                return url
        return ""

    # Modify the show_bookmarks method
    def show_bookmarks(self):
        # Clear existing items
        self.bookmarks_combo.clear()

        # Add "No Bookmarks Selected" to the combo box
        self.bookmarks_combo.addItem('No Bookmarks Selected')

        # Add bookmarks to the combo box
        for name in self.bookmarks.values():
            self.bookmarks_combo.addItem(name)
            # Also add bookmarks to the sidebar
            sidebar_label = QLabel(name)
            sidebar_label.mousePressEvent = lambda event, url=self.get_url_from_bookmark_name(name): self.navigate_to_url_sidebar(url)
            self.sidebar_layout.addWidget(sidebar_label)

    # Function to navigate to the selected bookmark
    def navigate_to_bookmark(self, index):
        bookmark_name = self.bookmarks_combo.itemText(index)
        if bookmark_name == 'No Bookmarks Selected':
            self.navigate_home()
        else:
            url = [key for key, value in self.bookmarks.items() if value == bookmark_name]
            if url:
                self.current_browser().setUrl(QUrl(url[0]))

    # Function to close a tab
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    # Function to update the tab title
    def update_tab_title(self, index, title):
        self.tabs.setTabText(index, title)

    # Function to navigate to specified URL from the sidebar
    def navigate_to_url_sidebar(self, url):
        q = QUrl(url)
        if q.scheme() == "":
            q.setScheme("http")

        self.current_browser().setUrl(q)