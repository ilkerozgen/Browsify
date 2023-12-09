import json
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QDateTime, Qt

from frontend.Styles import BrowsifyStyles
from controller import controller_script as control

class Browsify(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setAlignment(Qt.AlignTop) 
        self.sidebar.setLayout(self.sidebar_layout)

        # Show Bookmarks ComboBox
        self.bookmarks_combo = QComboBox()
        self.bookmarks_combo.activated.connect(self.navigate_to_bookmark)

        # Bookmarks
        self.bookmarks = {}
        self.bookmarks_combo.addItem('No Bookmarks Selected')
        try:
            with open("db/bookmarks.json", 'r') as file:
                self.bookmarks = json.load(file)
        except FileNotFoundError:
            self.bookmarks = {}

        # Load default bookmarks
        self.default_bookmarks = {}
        try:
            with open("db/default_bookmarks.json", 'r') as file:
                self.default_bookmarks = json.load(file)
        except FileNotFoundError:
            self.default_bookmarks = {}

        if len(self.default_bookmarks) == 0:
            # Create a new tab with the initial page
            self.add_new_tab(QUrl("http://www.google.com"), "Home")
        else:
            # Open default bookmarks in new tabs
            for url in self.default_bookmarks:
                self.add_new_tab(QUrl(url), "Default Bookmark")

         # Visits
        self.visits = {}
        try:
            with open("db/visits.json", 'r') as file:
                self.visits = json.load(file)
        except FileNotFoundError:
            self.visits = {}

        # History
        self.history = {}
        try:
            with open("db/history.json", 'r') as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = {}            

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
        self.url_bar.returnPressed.connect(self.navigate_to_url())
        navbar.addWidget(self.url_bar)
        self.url_bar.mousePressEvent = self.urlbar_mousePressEvent
        self.tabs.currentChanged.connect(self.update_urlbar_on_tab_change)

        # Updating URL bar
        self.current_browser().urlChanged.connect(self.handleURL())

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

        # Add History Button
        history_btn = QAction(QIcon('visual/icons/history.png'), 'Search History', self)
        history_btn.setStatusTip('View Search History')
        history_btn.triggered.connect(self.show_history_popup)
        navbar.addAction(history_btn)

        # Add Bookmarks Sidebar Button
        toggle_sidebar_btn = QAction(QIcon('visual/icons/bookmarks.png'), 'My Bookmarks', self)
        toggle_sidebar_btn.setStatusTip('My Bookmarks')
        toggle_sidebar_btn.triggered.connect(self.toggle_sidebar)
        navbar.addAction(toggle_sidebar_btn)

        # Search Bookmarks Button
        bookmarks_btn = QAction(QIcon('visual/icons/search.png'), 'Search Bookmarks', self)
        bookmarks_btn.setStatusTip('Search Bookmarks')
        bookmarks_btn.triggered.connect(self.show_bookmarks_popup)
        navbar.addAction(bookmarks_btn)

        # Add the sidebar to the main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.sidebar)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.sidebar.hide()

        # Load the state of checked checkboxes
        self.checked_state = control.load_checked_state()

        # Set window properties
        self.setGeometry(100, 100, 1400, 850)
        self.setWindowTitle("Browsify")

        # Initially, show bookmarks
        self.show_bookmarks()

        # Store the original unfiltered bookmarks
        self.original_bookmarks = self.bookmarks.copy()

    ########################
    ### Toggle Functions ###
    ########################
    # Function to open the sidebar
    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            self.sidebar.show()

    ######################
    ### Event Handlers ###
    ######################
    # Function to select text in the URL bar when clicked
    def urlbar_mousePressEvent(self, event):
        self.url_bar.selectAll()

    # Fucntion to handle add new tab
    def add_new_tab_action(self):
        self.add_new_tab()

    # Function to handle URL change
    def handleURL(self):
        return lambda qurl: self.update_urlbar(qurl, self.current_browser())

    #####################
    ### Add Functions ###
    #####################
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

    # Function to add a bookmark
    def add_bookmark(self):
        current_url = self.current_browser().url().toString()

        # Prompt the user for a bookmark name
        name, ok = QInputDialog.getText(self, 'Add Bookmark', 'Enter a name for the bookmark:')

        if ok and name:
            if name in self.bookmarks.values():
                QMessageBox.warning(self, 'Bookmark Exists', f'A bookmark with the name "{name}" already exists.')
            else:
                if current_url not in self.bookmarks:
                    self.bookmarks[current_url] = name
                    self.show_bookmarks()  # Update bookmarks in both combo box and sidebar
                    QMessageBox.information(self, 'Bookmark Added', f'Bookmark added: {name}')

                    # Save bookmarks to file
                    control.save_bookmarks_to_file(self)

                    # Sort bookmarks by visit count in the sidebar after adding a bookmark
                    self.sort_bookmarks_by_visits()

    # Function to add URL to history
    def add_to_history(self, url):
        # Get the current date and time with a custom format
        current_datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")

        # Add the URL and the formatted date of access to the history
        self.history[url] = current_datetime

        # Update the visit count for the URL
        self.update_visit_count(url)

        # Save the updated history to the file
        control.save_history_to_file(self)

    ########################
    ### Remove Functions ###
    ########################
    # Function to remove a bookmark
    def remove_bookmark(self):
        bookmark_names = list(self.bookmarks.values())

        if not bookmark_names:
            QMessageBox.warning(self, 'No Bookmarks', 'There are no bookmarks to remove.')
            return

        # Prompt the user to select a bookmark to remove
        bookmark_name, ok = QInputDialog.getItem(self, 'Remove Bookmark', 'Select a bookmark to remove:', bookmark_names, 0, False)

        if ok and bookmark_name:
            url = self.get_url_from_bookmark_name(bookmark_name)

            if url:
                del self.bookmarks[url]
                self.show_bookmarks()  # Update bookmarks in both combo box and sidebar
                QMessageBox.information(self, 'Bookmark Removed', f'Bookmark removed: {bookmark_name}')

                # Save bookmarks to file
                control.save_bookmarks_to_file(self)

                # Sort bookmarks by visit count in the sidebar after adding a bookmark
                self.sort_bookmarks_by_visits()
            else:
                QMessageBox.warning(self, 'Error', 'Bookmark not found.')

    ################################
    ### Browser Utiliy Functions ###
    ################################
    # Function to return the current browser
    def current_browser(self):
        return self.tabs.currentWidget()

    # Function to update toolbar
    def update_urlbar(self, q, browser=None):
        if browser and browser == self.current_browser():
            self.url_bar.setText(q.toString())
            self.url_bar.setCursorPosition(0)
            self.add_to_history(q.toString())

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

    # Function to show the bookmarks
    def show_bookmarks(self):
        # Clear existing items in both combo box and sidebar
        self.bookmarks_combo.clear()
        for i in reversed(range(self.sidebar_layout.count())):
            self.sidebar_layout.itemAt(i).widget().setParent(None)

        # Add "No Bookmarks Selected" to the combo box
        self.bookmarks_combo.addItem('No Bookmarks Selected')

        # Sort bookmarks by name
        sorted_bookmarks = sorted(self.bookmarks.items(), key=lambda x: x[1])

        # Add bookmarks to the combo box and sidebar
        for url, name in sorted_bookmarks:
            self.bookmarks_combo.addItem(name)
            # Also add bookmarks to the sidebar
            sidebar_label = QLabel(f"{name} ({self.visits.get(url, 0)} visits)")
            sidebar_label.mousePressEvent = lambda event, url=url: self.navigate_to_url_sidebar(url)
            self.sidebar_layout.addWidget(sidebar_label)

        # Sort bookmarks by visit count in the sidebar
        self.sort_bookmarks_by_visits()

    # Function to close a tab
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    # Function to update the tab title
    def update_tab_title(self, index, title):
        self.tabs.setTabText(index, title)

    # Function to show bookmarks popup
    def show_bookmarks_popup(self):
        popup = QDialog(self)
        popup.setWindowTitle("Bookmarks")
        popup.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Create a new QLineEdit for the search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search Bookmarks")

        # Sort bookmarks by name
        sorted_bookmarks = sorted(self.bookmarks.items(), key=lambda x: x[1])

        bookmarks_list = QListWidget()

        # Create a mapping to store QListWidgetItem and corresponding checkbox
        checkbox_mapping = {}

        # Load the state of checked checkboxes
        checked_state = control.load_checked_state()

        def update_bookmarks_list():
            bookmarks_list.clear()
            for row, (url, name) in enumerate(sorted_bookmarks):
                if search_bar.text().lower() in name.lower():
                    checkbox = QCheckBox(name)
                    item = QListWidgetItem(bookmarks_list)
                    bookmarks_list.setItemWidget(item, checkbox)
                    checkbox_mapping[row] = checkbox
                    checkbox.setChecked(checked_state.get(url) == "True")
                    

        update_bookmarks_list()

        search_bar.textChanged.connect(update_bookmarks_list)

        bookmarks_list.itemClicked.connect(self.navigate_to_bookmark_from_popup)

        layout.addWidget(search_bar)
        layout.addWidget(bookmarks_list)

        popup.setLayout(layout)

        # Add a button to set default bookmarks
        set_default_button = QPushButton("Set Default")
        set_default_button.clicked.connect(lambda: self.set_default_bookmarks(checkbox_mapping))
        layout.addWidget(set_default_button)

        popup.exec_()

    # Function to filter the bookmarks in the search window
    def filter_bookmarks(self, text):
        if not text:
            # If the search bar is empty, restore the original bookmarks
            filtered_bookmarks = self.original_bookmarks
        else:
            # Filter bookmarks based on the entered text
            filtered_bookmarks = {url: name for url, name in self.original_bookmarks.items() if text.lower() in name.lower()}

            # Check if the entered text matches any existing bookmark names
            if not filtered_bookmarks:
                # If no matches are found, add a placeholder entry
                filtered_bookmarks[''] = f'No bookmarks found for "{text}"'

        # Update the bookmarks list dynamically
        self.update_bookmarks_list(filtered_bookmarks)

    # Function to update the bookmarks list
    def update_bookmarks_list(self, bookmarks):
        bookmarks_list = self.findChild(QListWidget)
        if bookmarks_list:
            bookmarks_list.clear()
            bookmarks_list.addItems(bookmarks.values())

    # Function to update the visit count
    def update_visit_count(self, url):
        # Increment the visit count for the URL
        self.visits[url] = self.visits.get(url, 0) + 1

        # Save the updated visit counts to the file
        control.save_visits_to_file(self)

        # Update the sidebar to reflect the changes in visit counts
        self.sort_bookmarks_by_visits()

    # Function to show the history popup window
    def show_history_popup(self):
        # Check if the history window is already open
        existing_history_popup = self.findChild(QDialog, "History")

        if existing_history_popup:
            # If the history window is open, update its content
            history_list = existing_history_popup.findChild(QListWidget)
            if history_list:
                history_list.clear()
                history_list.addItems([f"{url} - {date}" for url, date in self.history.items()])
            return

        # If the history window is not open, create a new one
        popup = QDialog(self)
        popup.setObjectName("History")  # Set an object name to identify the window later
        popup.setWindowTitle("History")
        popup.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Create a QListWidget for displaying the history
        history_list = QListWidget()
        history_list.addItems([f"{url} - {date}" for url, date in self.history.items()])

        layout.addWidget(history_list)

        # Add a button to clear the history
        clear_button = QPushButton("Clear History")
        clear_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_button)

        popup.setLayout(layout)
        popup.exec_()

    # Function to clear search history
    def clear_history(self):
        # Check if there are items in the history to clear
        if not self.history:
            QMessageBox.information(self, 'Clear History', 'History is already empty.')
            return

        # Clear the history and visit counts
        self.history = {}
        self.visits = {}

        # Save the empty history and visit counts to the files
        control.save_history_to_file(self)
        control.save_visits_to_file(self)

        # Close the history popup if it's open
        history_popup = self.findChild(QDialog, "History")
        if history_popup:
            history_popup.close()

        # Refresh the history window
        self.show_history_popup()

        # Notify the user that the history has been cleared
        QMessageBox.information(self, 'Clear History', 'History has been cleared.')

    # Function to sort the bookmarks by visit counts
    def sort_bookmarks_by_visits(self):
        # Sort bookmarks by visit count in descending order
        sorted_bookmarks = sorted(self.bookmarks.items(), key=lambda x: self.visits.get(x[0], 0), reverse=True)

        # Clear existing items in the sidebar
        for i in reversed(range(self.sidebar_layout.count())):
            self.sidebar_layout.itemAt(i).widget().setParent(None)

        # Add bookmarks to the sidebar in sorted order
        for url, name in sorted_bookmarks:
            sidebar_label = QLabel(name)
            sidebar_label.mousePressEvent = lambda event, url=url: self.navigate_to_url_sidebar(url)
            self.sidebar_layout.addWidget(sidebar_label)

    # Function to set default bookmarks
    def set_default_bookmarks(self, checkbox_mapping):
        default_bookmarks = []
        checked_state = {}  # To store the state of checked checkboxes

        # Iterate through the checkbox_mapping dictionary
        for row, checkbox in checkbox_mapping.items():
            if checkbox.isChecked():
                # Get the corresponding bookmark URL from the sorted_bookmarks list
                url = sorted(self.bookmarks.items(), key=lambda x: x[1])[row][0]
                default_bookmarks.append(url)
                checked_state[url] = "True"  # Mark the checkbox as checked

        # Save the default bookmarks to the 'default_bookmarks.json' file
        with open('db/default_bookmarks.json', 'w') as file:
            json.dump(default_bookmarks, file)

        # Save the state of checked checkboxes to a file
        control.save_checked_state(checked_state)

        # Show a message box indicating that bookmarks have been set as default
        QMessageBox.information(self, 'Default Bookmarks Set', 'Default bookmarks have been set successfully.')

    ############################
    ### Navigation Functions ###
    ############################
    # Function to navigate to home page
    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://www.google.com"))

    # Function to navigate to URL
    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.current_browser().setUrl(q)

        self.add_to_history(q.toString())
        self.update_visit_count(q.toString())

        return self.navigate_to_url

    # Function to navigate to the selected bookmark
    def navigate_to_bookmark(self, index):
        bookmark_name = self.bookmarks_combo.itemText(index)
        if bookmark_name == 'No Bookmarks Selected':
            self.navigate_home()
        else:
            url = [key for key, value in self.bookmarks.items() if value == bookmark_name]
            if url:
                self.current_browser().setUrl(QUrl(url[0]))
                self.add_to_history(url)

    # Function to navigate to URL from the sidebar
    def navigate_to_url_sidebar(self, url):
        q = QUrl(url)
        if q.scheme() == "":
            q.setScheme("http")

        self.current_browser().setUrl(q)
        self.add_to_history(url)

    # Function to navigate to URL from popup window
    def navigate_to_bookmark_from_popup(self, item):
        bookmark_name = item.text()
        url = self.get_url_from_bookmark_name(bookmark_name)
        if url:
            self.current_browser().setUrl(QUrl(url))
            # Add the visited URL to the history
            self.add_to_history(url)
    

    

    

    

    
