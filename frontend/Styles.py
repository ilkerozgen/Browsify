class BrowsifyStyles:
    def __init__(self):
        self._styles = """
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
                        
                        QToolBar {
                            height: 40px; /* Set the height of the toolbar */
                        }

                        QToolBar QToolButton {
                            height: 30px; /* Set the height of the toolbar buttons */
                            width: 30px;  /* Set the width of the toolbar buttons */
                        }

                        QToolBar QComboBox {
                            height: 30px; /* Set the height of the combo box in the toolbar */
                        }

                        QLineEdit {
                            height: 30px; /* Set the height of the URL input box */
                        }

                        QToolBar QToolButton:hover {
                            background-color: #e0e0e0;
                        }
                    """
    def getStyles(self):
        return self._styles