from MultiHex.guis.about_gui import Ui_Dialog as about_MHX
from PyQt5.QtWidgets import QDialog

class about_dialog(QDialog):
    def __init__(self, parent):
        super(about_dialog, self).__init__(parent)
        self.ui = about_MHX()
        self.ui.setupUi(self)

    