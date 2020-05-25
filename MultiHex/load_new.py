from MultiHex.guis.new_load_gui import new_load_gui

import sys
from PyQt5.QtWidgets import QDialog

class new_load_dialog(QDialog):
    def __init__(self, parent):
        super(new_load_dialog, self).__init__(parent)
        self.ui = new_load_gui()
        self.ui.setupUi(self)

        self.ui.new_map_button.clicked.connect(self.button_new)
        self.ui.load_map_button.clicked.connect(self.button_load)
        self.ui.quit_button.clicked.connect(self.button_quit)
        self.parent = parent

    def button_new(self):
        """
        Tells the parent Window to try making a new map. This will launch the New Map Interface
        """
        self.parent.new()
        self.accept()

    def button_load(self):
        """
        This tells the parent window to load a map. Opens the open file dialog! 
        """
        self.parent.load()
        self.accept()

    def button_quit(self):
        sys.exit()