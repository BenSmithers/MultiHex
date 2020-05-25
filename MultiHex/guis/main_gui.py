from PyQt5 import QtCore, QtGui, QtWidgets

import os
art_dir = os.path.join( os.path.dirname(__file__),'..','Artwork','buttons')

class main_gui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", "MultiHex"))

        # define the primary areas on the GUI
        #    the tool pane
        #    the screen
        #    the context pane

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # the tool pane! Icons should be added to this
        self.toolPane = QtWidgets.QVBoxLayout()
        self.toolPane.setObjectName("toolPane")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.toolPane.addItem(spacerItem)

        # define the screen
        # self.horizontalLayout.addLayout(self.verticalLayout)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget) # <--- this is the screen
        self.graphicsView.setObjectName("graphicsView") 
        self.horizontalLayout.addWidget(self.graphicsView)

        # this is the contextPane
        self.contextPane = QtWidgets.QToolBox(self.centralwidget)
        self.contextPane.setMinimumSize(QtCore.QSize(250,0))
        self.contextPane.setMaximumSize(QtCore.QSize(250, 16777215))
        self.contextPane.setObjectName("contextPane")
        self.horizontalLayout.addWidget(self.contextPane)

        # and nest it! 
        MainWindow.setCentralWidget(self.centralwidget)

        # self.toolBox.setItemText(self.toolBox.indexOf(self.paneItem), _translate("MainWindow", "Detailer"))

        # and then the menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1109, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHeatmaps = QtWidgets.QMenu(self.menubar)
        self.menuHeatmaps.setObjectName("menuHeatmaps")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout_MultiHex = QtWidgets.QAction(MainWindow)
        self.actionAbout_MultiHex.setObjectName("actionAbout_MultiHex")
        self.actionTemperature = QtWidgets.QAction(MainWindow)
        self.actionTemperature.setCheckable(False)
        self.actionTemperature.setObjectName("actionTemperature")
        self.actionAltitude = QtWidgets.QAction(MainWindow)
        self.actionAltitude.setObjectName("actionAltitude")
        self.actionRainfall = QtWidgets.QAction(MainWindow)
        self.actionRainfall.setObjectName("actionRainfall")
        self.actionBiome_Names = QtWidgets.QAction(MainWindow)
        self.actionBiome_Names.setCheckable(True)
        self.actionBiome_Names.setObjectName("actionBiome_Names")
        self.actionBiome_Borders = QtWidgets.QAction(MainWindow)
        self.actionBiome_Borders.setCheckable(True)
        self.actionBiome_Borders.setObjectName("actionBiome_Borders")
        self.actionRivers = QtWidgets.QAction(MainWindow)
        self.actionRivers.setCheckable(True)
        self.actionRivers.setObjectName("actionRivers")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout_MultiHex)
        self.menuHeatmaps.addAction(self.actionAltitude)
        self.menuHeatmaps.addAction(self.actionRainfall)
        self.menuHeatmaps.addAction(self.actionTemperature)
        self.menuView.addAction(self.actionBiome_Names)
        self.menuView.addAction(self.actionBiome_Borders)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionRivers)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHeatmaps.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())