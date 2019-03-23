# -*- coding: utf-8 -*-


import os
import os.path
from qgis.core import QgsProject, QgsMapLayer, QgsWkbTypes
from qgis.PyQt.QtCore import QFileInfo, QSettings, QCoreApplication
from qgis.PyQt.QtCore import QTranslator, qVersion
from qgis.PyQt.QtGui import QIcon,QFont,QPalette,QBrush,QColor
from PyQt5 import QtCore
from qgis.PyQt.QtWidgets import QAction, QMessageBox,QDialog, QDialogButtonBox,QAction,QGridLayout,QLabel,QTextEdit,QPushButton,QFrame,QSpacerItem,QSizePolicy,QApplication
# Import libs 

import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,440,660).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        font = QFont()
        font.setPointSize(15) 
        font.setWeight(50) 
        font.setBold(True)
        
        self.label_2 = QLabel(Dialog)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,1,1,2)
         
        self.textEdit = QTextEdit(Dialog)

        palette = QPalette()

        brush = QBrush(QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active,QPalette.Base,brush)

        brush = QBrush(QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive,QPalette.Base,brush)

        brush = QBrush(QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled,QPalette.Base,brush)
        self.textEdit.setPalette(palette)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.width = 320
        self.textEdit.height = 360
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Plain)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
       
        self.gridlayout.addWidget(self.textEdit,2,1,5,2) 

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,4,2,1,1) 

        spacerItem = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,3,1,1,1)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QApplication.translate("Dialog", "GroupPointsWithinDistance", None))
        self.label_2.setText(QApplication.translate("Dialog", "GroupPointsWithinDistance 0.1", None))
        self.textEdit.setHtml(QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><span style=\" font-weight:600;\">"
        " GroupPointsWithinDistance 0.1 :</span>" "  A little QGIS plugin to find and group/aggregate points of a points' layer if they are at a given distance of one another.</b>\n"+
        "                                                                                                                                                                                           \n"+ 
        " <br><b>WARNING:</b><br><b> Work with projected datas only, in other words do not use geographical (long-lat type) reference systems !</b>\n " +
        "                                                                                                                                             \n"+
        "             \n"+
        "This plugin is meant to deal with any points datas (for instance faunistic or floristic observations), nearby from one another, that the user wants to be regrouped/aggregated as a station.\n"+
        "\n"+"                                                                                                                                                                                                                    \n"+
        "The user should appreciate and cheack which distance to use, and - may be - keep the distance chosen as small as possible in order to avoid '"'chains effect'"' and producing too widespread groups .\n"+
        "                                                                                                                                          \n"+
        "The plugin produces a layer of point called '"'input_layer_name_aggregated_with_Distance'"' with 3 mores attributes:                                                          \n"+
        "                                                                                                                                                                                                                    \n"+
        " - Point_id: the point id,                                                                                                                                                              \n"+               

        "                                                                                                                                                                                                                    \n"+
        " - NumAggreg: the '"'aggregates id number'"'                                                                                                                                                              \n"+               
        "                                                                                                                                                                                                                    \n"+
        " - Nb_Pts: the number of regrouped points,                                              \n " +
        "\n"+"                                                                                                                                                                                                                    \n"+
        " - List_Pts: the list of the points ids in the aggregate.                                                                                                                     \n"+
        "\n"+"                                                                                                                                          \n"+
        "                                                                                                                                                          \n"+ "\n"+ 
        " The plugin also produce a line layer, with not all lines connecting points of a same aggregate but showing only the very one of the connections that were made to link the points as part of a same aggregate."
        " the plugin also produces a layer of polygons overlaping the regrouped points within distance with an attribute table with also NumAggreg,Nb_Pts,List_Pts attributes.    \n " +
        "\n"+"                                                                                                                                                                \n"+
        "  The polygons are buffers (D/100) of the convex hull polygons of the aggregated points \n " +
        "                                                                                                                                                          \n"+ "\n"+ 
        "<br><b>WARNING 2:</b><br> The polygons are meant - as the lines - only to show the aggregates but they overlap often points that are not part of the aggregate. The lines can be used for that matter  \n"+
        "<br><b>In order to select point of an aggregate only consider the point table attribute !</b><br>" 
        "                                                                                                                                                          \n"+ "\n"+ 
       
       " <br><b><i>NOTA BENE: all rasters should be unchecked in layer panel or the plugin won't work !</i></b></br>" 
        " This plugin is not a part of Qgis engine and any problems should be reported only to the author. </p></td></tr></table>"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        "                   "
        "<br><b>jeanchristophebaudin@ymail.com</b><br>"
        "<br><br><i>code 0.1 (21 march 2019).</i></p></body></html>", None))
        self.pushButton.setText(QApplication.translate("Dialog", "OK", None))



