
from PyQt5 import QtCore, QtGui, QtWidgets
from MultiHex.objects import Entity, Mobile

import os
art_dir = os.path.join( os.path.dirname(__file__),'..','Artwork')
from glob import glob

class Entity_Dialog(object):
    def __init__(self, mode=0, entity=None):
        """
        Modes 
            0 - New Entity Mode
            1 - New Mobile Mode
            2 - Edit Entity Mode
            3 - View Mode 
        """
        if not isinstance(mode, int):
            raise TypeError("Mode must be {}, not {}".format(int, type(mode)))
        if mode not in [0,1,2,3]:
            raise ValueError("Unrecognized mode: {}".format(mode))
        self._mode = mode

        if mode in [2,3]:
            if entity is None:
                raise ValueError("Entity must be specified in Edit/View mode")
            if not isinstance(entity,Entity):
                raise TypeError("Arg 'entity' must be {}, not {}".format(Entity, type(entity)))

        # not protecting this, we'll be changing it!
        self.entity = entity

        if mode==1 or isinstance(entity, Mobile):
            self.art_dir = os.path.join(art_dir, 'mobiles')
        else:
            self.art_dir = os.path.join(art_dir, 'map_icons')

    @property
    def mode(self):
        return(self._mode)


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # build the name label depending on the mode this is being built in
        font = QtGui.QFont()
        font.setPointSize(24)
        if self.mode!=3:
            self.entity_name = QtWidgets.QLineEdit(self.centralwidget)
        else:
            self.entity_name = QtWidgets.QLabel(self.centralwidget)
        self.entity_name.setObjectName("entity_name")
        self.entity_name.setFont(font)
        if self.mode==2 or self.mode==3:
            self.entity_name.setText(self.entity_name)
        elif self.mode==1:
            self.entity_name.setText("New Mobile")
        else:
            self.entity_name.setText("New Entity")
        self.verticalLayout.addWidget(self.entity_name)
        self.central_panes = QtWidgets.QHBoxLayout()
        self.left_pane = QtWidgets.QFormLayout()
        line = 0
        if self.mode==1 or isinstance(self.entity, Mobile):
            self.speed_lbl = QtWidgets.QLabel(self.centralwidget)
            self.speed_lbl.setObjectName("speed_lbl")
            self.speed_lbl.setText("Speed:")
            self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.speed_lbl) #FieldRole SpanningRole
            self.speed_edit = QtWidgets.QDoubleSpinBox(self.centralwidget)
            self.speed_edit.setObjectName("speed_edit")
            self.speed_edit.setMinimum(0)
            self.speed_edit.setSingleStep(0.1)
            self.speed_edit.setDecimals(1)
            self.speed_edit.setMaximum(100.)
            if self.mode==2 or self.mode==3:
                self.speed_edit.setValue(entity.speed)
            else:
                self.speed_edit.setValue(1.0)
            if self.mode==3:
                self.speed_edit.setEnabled(False)
            self.left_pane.setWidget(line, QtWidgets.QFormLayout.FieldRole, self.speed_edit)
            line+=1
        self.description_lbl = QtWidgets.QLabel(self.centralwidget)
        self.description_lbl.setObjectName("description_lbl")
        self.description_lbl.setText("Description: \n")
        self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.description_lbl)
        line+=1
        self.description_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.description_edit.setObjectName("description_edit")
        if self.mode==2 or self.mode==3:
            self.description_edit.setText(entity.description)
        if self.mode==3:
            self.description_edit.setEnabled(False)
        self.left_pane.setWidget(line, QtWidgets.QFormLayout.SpanningRole, self.description_edit)

        self.right_pane = QtWidgets.QVBoxLayout()
        if self.mode!=3:
            self.icon_combo = QtWidgets.QComboBox(self.centralwidget)
            self.icon_combo.setObjectName("icon_combo")
            self.pictures = glob(os.path.join(self.art_dir, "*.svg"))
            for each in self.pictures:
                name = os.path.basename(each)
                self.icon_combo.addItem( QtGui.QIcon(QtGui.QPixmap(each)), name )

            self.right_pane.addWidget(self.icon_combo)
        self.picture_box = QtWidgets.QLabel(self.centralwidget)
        self.picture_box.setObjectName("picture_box")
        self.picture_box.setPixmap(QtGui.QPixmap(os.path.join(self.art_dir,self.pictures[self.icon_combo.currentIndex()])).scaledToWidth(400))
        self.right_pane.addWidget(self.picture_box)
        # Picture spot

        self.central_panes.addItem(self.left_pane)
        self.central_panes.addItem(self.right_pane)
        self.verticalLayout.addItem(self.central_panes)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        if self.mode==3:
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        else:
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.icon_combo.currentIndexChanged.connect(self.combo_change)

        Dialog.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.centralwidget)
        #self.buttonBox.accepted.connect(Dialog.accept)
        #self.buttonBox.rejected.connect(Dialog.reject)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Entity Dialog"))


    def combo_change(self):
        self.picture_box.setPixmap(QtGui.QPixmap(os.path.join(self.art_dir,self.pictures[self.icon_combo.currentIndex()])).scaledToWidth(400))


class whatevs(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(whatevs, self).__init__(parent)
        self.ui = Entity_Dialog()
        self.ui.setupUi(self)

import sys
app = QtWidgets.QApplication(sys.argv)
app_instance = whatevs()

if __name__=="__main__":
    # make sure the base saves folder exists 
    app_instance.show()
    sys.exit(app.exec_())
