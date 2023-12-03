class BrowsifyStyles:
    def __init__(self):
        self._styles = """
            QTabWidget::pane { 
                border: 1px solid #C4C4C3; 
                top: -1px; 
            }
            
            QTabBar::tab {
                background: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 200px;
                padding: 8px;
                margin: 0;
                font-size: 16px;
                margin-top: 5px;
                margin-left: 5px;
                border-bottom: none;
            }

            QTabBar::close-button:hover {
                background-color: #e31b2f;
            }
            
            QTabBar::close-button {
                background-color: #9fa0a1;
                margin-top: 5px;
                border-radius: 6px;
                image: url(visual/icons/close.png);
            }

            QTabBar::tab:selected {
                background: #ffffff;
                border: 1px solid #cccccc;
                border-bottom: none;
            }

            QTabBar::tab:hover {
                background: #e0e0e0;
            }

            QToolBar {
                height: 40px;
            }

            QToolBar QToolButton {
                height: 40px;
                width: 40px;
                background-color: #f0f0f0;
                border: none;
            }

            QToolBar QToolButton:hover {
                background-color: #e0e0e0;
            }

            QToolBar QComboBox {
                height: 40px;
                font-size: 14px;
            }

            QLineEdit {
                height: 40px;
                border-radius: 4px;
                margin-left: 6px;
                margin-right: 6px;
                margin-top: 3px;
                margin-bottom: 3px;
                font-size: 14px;
            }

            QLineEdit:hover {
                border: 2px solid #2196F3;
            }
        """

    def getStyles(self):
        return self._styles
