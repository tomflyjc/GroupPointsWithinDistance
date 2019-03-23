# -*- coding: utf-8 -*-
# (c) JC BAUDIN 2019 03 21
# import de QGIS
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QVariant
from qgis.PyQt.QtWidgets import     (QMessageBox,
                                    QDialog,
                                    QProgressBar,
                                    QDialogButtonBox,
                                    QAction,
                                    QLabel,
                                    QComboBox,
                                    QPushButton,
                                    QLineEdit,
                                    QDoubleSpinBox,
                                    QInputDialog,
                                    QApplication)

 

from qgis.core import  (QgsProject,
                        QgsMapLayer,
                        QgsWkbTypes,
                       QgsVectorLayer,
                       QgsField,
                       QgsFields,
                       QgsFeature,
                       QgsFeatureSink,
                       QgsFeatureRequest,
                       QgsGeometry,
                       QgsPointXY,
                       QgsPoint,
                       #QgsPolygonXY,
                       QgsWkbTypes,
                       QgsRectangle,
                       QgsFeature,
                       QgsSpatialIndex,
                       QgsCoordinateTransform,
                       QgsFeatureRequest,
                       QgsVector,
                       QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform)
                       
from qgis.utils import iface

import os
import os.path
import fonctionsGPWD
import doAboutGroupPointsWithinDistance

class Ui_Dialog(object):
    """
    def __init__(self, iface):
        self.iface = iface
    """
    def setupUi(self, Dialog):
        self.iface = iface
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,350,250).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setWindowTitle("GroupPointsWithinDistance")
        
        # QLabel lancer recherche
        self.label10 = QLabel(Dialog)
        self.label10.setGeometry(QtCore.QRect(15,15,320,18))
        self.label10.setObjectName("label10")
        self.label10.setText("Select a layer with points to regroup:  ")

        ListeCouchesPoint=[""]
        NbCouches=self.iface.mapCanvas().layerCount()
        if NbCouches==0: QMessageBox.information(None,"information:","No layers ! ")
        else:
            for i in range(0,NbCouches):
                couche=self.iface.mapCanvas().layer(i)
                # 0 pour point
                if couche.geometryType()== 0 or couche.geometryType()==3 :
                    if couche.isValid():
                       ListeCouchesPoint.append(couche.name())
                    else:
                       QMessageBox.information(None,"information:","No layers with points ! ")
                       return None
        self.ComboBoxPoints = QComboBox(Dialog)
        self.ComboBoxPoints.setMinimumSize(QtCore.QSize(320, 25))
        self.ComboBoxPoints.setMaximumSize(QtCore.QSize(320, 25))
        self.ComboBoxPoints.setGeometry(QtCore.QRect(10, 35, 320,25))
        self.ComboBoxPoints.setObjectName("ComboBoxPoints")
        for i in range(len(ListeCouchesPoint)):  self.ComboBoxPoints.addItem(ListeCouchesPoint[i])
         
        # QLabel entrer Enter distance of recherch
        self.labelResearchDistance = QLabel(Dialog)
        self.labelResearchDistance.setGeometry(QtCore.QRect(15,80,240,23))
        self.labelResearchDistance.setObjectName(" ResearchDistance")
        self.labelResearchDistance.setText("Enter distance of research :")

        #Exemple de QDoubleSpinBox
        self.dsbResearchDistance = QDoubleSpinBox(Dialog)
        self.dsbResearchDistance.setMinimumSize(QtCore.QSize(70, 23))
        self.dsbResearchDistance.setMaximumSize(QtCore.QSize(70, 23))
        self.dsbResearchDistance.setGeometry(QtCore.QRect(180,80,70,23))
        self.dsbResearchDistance.setObjectName("dsb")
        #self.dsbResearchDistance.setValue(10.0)
        self.dsbResearchDistance.setDecimals(1)
        self.dsbResearchDistance.setSingleStep(10.0)
        self.dsbResearchDistance.setRange(0,1000000)
        self.dsbResearchDistance.setProperty("value", 100.0)
        
        #self.dsbResearchDistance.valueChanged.connect(self.onValueChanged)
       
        #Exemple de QPushButton
        self.DoButton = QPushButton(Dialog)
        self.DoButton.setMinimumSize(QtCore.QSize(280, 20))
        self.DoButton.setMaximumSize(QtCore.QSize(280, 20))        
        self.DoButton.setGeometry(QtCore.QRect(15,120, 280, 20))
        self.DoButton.setObjectName("DoButton")
        self.DoButton.setText(" Let's make aggregates - being patient !")
 
     
        #Exemple de QLCDNumber
        self.progressBar = QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setMinimumSize(QtCore.QSize(260, 15))
        self.progressBar.setMaximumSize(QtCore.QSize(260, 15))
        self.progressBar.setGeometry(QtCore.QRect(30,155,260,15))
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
            """QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center;}"""
            """QProgressBar::chunk {background-color: #6C96C6; width: 20px;}"""
        )
        #Pose a minima une valeur de la barre de progression / slide contrôle
        self.progressBar.setValue(0)
        
        
        #Exemple de QPushButton
        self.aboutButton = QPushButton(Dialog)
        self.aboutButton.setMinimumSize(QtCore.QSize(70, 20))
        self.aboutButton.setMaximumSize(QtCore.QSize(70, 20))        
        self.aboutButton.setGeometry(QtCore.QRect(30, 195, 70, 23))
        self.aboutButton.setObjectName("aboutButton")
        self.aboutButton.setText(" Read me ")
        
        self.PushButton = QPushButton(Dialog)
        self.PushButton.setMinimumSize(QtCore.QSize(100, 20))
        self.PushButton.setMaximumSize(QtCore.QSize(100, 20))
        self.PushButton.setGeometry(QtCore.QRect(185, 195, 100,20))
        self.PushButton.setObjectName("PushButton")
        self.PushButton.setText("Close")

        self.PushButton.clicked.connect(Dialog.reject)
        self.ComboBoxPoints.activated[str].connect(self.onComboP)
        self.aboutButton.clicked.connect(self.doAbout)
        self.DoButton.clicked.connect(self.Run)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
                                                             
    def onComboP(self):
        global SelectionP
        SelectionP = self.ComboBoxPoints.currentText()
        
    def doAbout(self):
        d = doAboutGroupPointsWithinDistance.Dialog()
        d.exec_()
    
    def Run(self):
        D=0.0
        D=self.dsbResearchDistance.value()
        #QMessageBox.information(None,"information:"," D : "+str(D)) 
        DicoP1={}
        DicoA={}
        counterProgess=0
        compteur_pt=0
        layerP=fonctionsGPWD.getVectorLayerByName(SelectionP)
        # on parcourt la couche de points et on stocke dans les dictionnaire DicoP1  les points
        # the points of the point laye are put into a dictionnary 
        for featP in layerP.getFeatures():
            Point_id = featP.id()
            geomP1=featP.geometry()
            Point1=geomP1.asPoint()
            DicoP1[Point_id]=[Point1]
            compteur_pt+=1
        
        if D==0 :
            QMessageBox.information(None,"information:","Zero is not a value for D !") 
        
        #zdim est le compteur de la progress bar    
        zDim = compteur_pt
        counterProgess=0
        cpt_agg=1
        nb=0
        liste_id=[]
        liste_pt=[]
        liste_aggreg_pt=[]
        DicoSegments={}
        firstDicoSegments=True
        T=True
        while len(DicoP1)!=0:
            first=True
            zPercent = int(100 * counterProgess / zDim)
            self.progressBar.setValue(zPercent)
            nb=0
            for keyD1 in list(DicoP1.keys()):
                P1=DicoP1[keyD1][0] 
            if first:
                # we pick a first point and delete it from the dictionnary we point are stored
                T=True
                first=False
                nb+=1
                liste_id=[keyD1]
                liste_pt=[P1]
                counterProgess+=1
                del DicoP1[keyD1]
            while T:
                # We are generating an aggregates and making it grows
                # by adding points at distance from the point it contains
                # and repeating the research all over again as soon a poitn is added
                # untill none are added
                for pt in liste_pt:
                    compteur_corresP=0
                    for keyD1 in list(DicoP1.keys()):
                        P1=DicoP1[keyD1][0]
                        if fonctionsGPWD.mag(fonctionsGPWD.vect(pt,P1))<D: # one point at distance found
                            compteur_corresId=0
                            for idp in liste_id:
                                if keyD1==idp: # is this point already added in the aggregate
                                    compteur_corresId+=1
                            if compteur_corresId==0: # if not let s add it
                                nb+=1
                                liste_id.append(keyD1)
                                liste_pt.append(P1)
                                compteur_corresP+=1
                                counterProgess+=1
                                # boucle des segments
                                # interpoint line loop
                                idseg='' # a segment as an id made of the points id order ordered id: smallerid-biggerid
                                idseg=str(keyD1)+'-'+str(idp)
                                idseg_reverse=str(idp)+'-'+str(keyD1)
                                if firstDicoSegments:
                                    firstDicoSegments=False
                                    if int(keyD1) > int(idp):
                                        idseg=idseg_reverse
                                        DicoSegments[idseg]=[[pt,P1],idp,keyD1,cpt_agg]
                                    else:
                                        DicoSegments[idseg]=[[P1,pt],keyD1,idp,cpt_agg]
                                else:
                                    for idseg_cheack in list(DicoSegments.keys()):
                                            if idseg==idseg_cheack or idseg_reverse==idseg_cheack: pass
                                            else:
                                                if int(keyD1) > int(idp):
                                                    idseg=idseg_reverse
                                                    DicoSegments[idseg]=[[pt,P1],idp,keyD1,cpt_agg]
                                                else:
                                                    DicoSegments[idseg]=[[P1,pt],keyD1,idp,cpt_agg]
                                
                if compteur_corresP==0: # if no more points are find then we are over with the previous aggregate        
                    T=False
                    
                    DicoA[cpt_agg]=[nb, liste_id, liste_pt,DicoSegments]
                    cpt_agg+=1
                    for id in liste_id:
                        for keyD1 in list(DicoP1.keys()):
                            if id==keyD1:
                                del DicoP1[keyD1]

        # on fabrique un polygone buffer de D/100
        # du convexHull de tous les points de l'agregat
        # pour les operateur Pyqgis
        # voir http://www.qgis.org/api/classQgsGeometry.html#a1699b205d01c365a50ead2d0bf2bbcfb
        DicoP4={}

        for key2 in list (DicoA.keys()):
            list_pt=[]
            list_pt=DicoA[key2][2]    
            nb_pt=0
            nb_pt=DicoA[key2][0]
            Liste_id=[]
            Liste_id=DicoA[key2][1]
            buff=0.0
            first=True
            for pt in list_pt:
                if first:
                    first=False
                    #https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/geometry.html
                    g0=QgsGeometry().fromPointXY(pt)
                else:
                    g0=QgsGeometry().fromPointXY(pt).combine(g0) # combine pour union car union reserve C++
            buff=D/100
            P=g0.convexHull()
            B=P.buffer(buff,5)
            DicoP4[key2]=[B,Liste_id,nb_pt]
            
        zPercent = int(100 * counterProgess / zDim)
        self.progressBar.setValue(zPercent)
        self.iface.mapCanvas().refresh()
        
        
        STATIONS= QgsVectorLayer("MultiPolygon?crs=epsg:2154",  "Polygons_under_AGGREGATES_D"+str(D)+"_OF_"+ str(layerP.name()), "memory")
        QgsProject.instance().addMapLayer(STATIONS)
        prSTATIONS =STATIONS.dataProvider()
        listFieldsS = []
        listFieldsS.append(QgsField("NumAggreg", QVariant.String))   
        listFieldsS.append(QgsField("List_Pts", QVariant.String))  
        listFieldsS.append(QgsField("Nb_Pts", QVariant.Int))
        prSTATIONS.addAttributes(listFieldsS)

        STATIONS.startEditing()
        newfeatSTATIONS=QgsFeature()
        for keyP4 in DicoP4.keys():
            GeomPoly=DicoP4[keyP4][0]   
            newfeatSTATIONS=QgsFeature()
            newfeatSTATIONS.setGeometry(GeomPoly)
            toto=''
            first=True
            for t in DicoP4[keyP4][1]:
                if first:
                    first=False
                    toto= str(t)
                else: toto=toto+' - '+str(t)
            NbObs=DicoP4[keyP4][2]
            ValuesSTATIONS=[keyP4]
            ValuesSTATIONS.append(toto)
            ValuesSTATIONS.append(NbObs)
            newfeatSTATIONS.setAttributes(ValuesSTATIONS)
            prSTATIONS.addFeatures([newfeatSTATIONS])
        STATIONS.commitChanges()
        iface.mapCanvas().refresh()       

        SEGMENTS= QgsVectorLayer("MultiLineString?crs=epsg:2154", "Lines_from_"+ str(layerP.name())+"_Aggregates", "memory")
        QgsProject.instance().addMapLayer(SEGMENTS)
        prSEGMENTS =SEGMENTS.dataProvider()
        listFields = []
        listFields.append(QgsField("NumAgregat", QVariant.String))
        listFields.append(QgsField("Nb_Pts", QVariant.Int))
        prSEGMENTS.addAttributes(listFields)
        SEGMENTS.startEditing()
        newfeatSEGMENTS=QgsFeature()
        attributs=[]
        for keyA in DicoA.keys():
            DicoSeg=DicoA[keyA][3]
            NbObs=DicoA[keyA][0]
            firstSEG=True
            MultiLine=[]
            GeomLine=QgsGeometry
            for keyPair in DicoSeg.keys():
                if DicoSeg[keyPair][3]==keyA:
                    if firstSEG:
                        firstSEG=False
                        MultiLine=[]
                        MultiLine=[DicoSeg[keyPair][0]]
                    else:
                        MultiLine.append(DicoSeg[keyPair][0])
            
            GeomLine=QgsGeometry.fromMultiPolylineXY(MultiLine)
            NumAg=keyA
            newfeatSEGMENTS=QgsFeature()
            newfeatSEGMENTS.setGeometry(GeomLine)
            ValuesSEGMENTS=[NumAg]
            ValuesSEGMENTS.append(NbObs)
            newfeatSEGMENTS.setAttributes(ValuesSEGMENTS)
            prSEGMENTS.addFeatures([newfeatSEGMENTS])
        SEGMENTS.commitChanges()
        iface.mapCanvas().refresh()

        # modification de la table de point initiale pour ajout d un numero d agregat
        # making of the modified point layer with aggregates code
        AGGREGATS= QgsVectorLayer("Point?crs=epsg:2154",  str(layerP.name())+"_with_aggregates", "memory")
        QgsProject.instance().addMapLayer(AGGREGATS)
        prAGGREGATS =AGGREGATS.dataProvider()
        fieldsP=layerP.fields()
        listFields = []
        for f in fieldsP:
                    znameField= f.name()
                    Type= str(f.typeName())
                    if Type == 'Integer':   listFields.append(QgsField( znameField, QVariant.Int))
                    if Type == 'Real':   listFields.append(QgsField( znameField, QVariant.Double))
                    if Type == 'String':    listFields.append(QgsField( znameField, QVariant.String))
                    else :  listFields.append(QgsField( znameField, QVariant.String))
        listFields.append(QgsField("Point_id", QVariant.String))
        listFields.append(QgsField("NumAggreg", QVariant.String))
        listFields.append(QgsField("Nb_Pts", QVariant.Int))
        listFields.append(QgsField("List_Pts", QVariant.String))  
        prAGGREGATS.addAttributes(listFields)
        AGGREGATS.startEditing()
        newfeatAGGREGATS=QgsFeature()
        attributs=[]
        for featP in layerP.getFeatures():
            attributs = featP.attributes()
            Point_id = featP.id()
            geomP1=featP.geometry()
            NbObs=1
            NumAgregat=0
            for keyP4 in DicoP4.keys():
                #GeomPoly=DicoP4[keyP4][0]   
                #if geomP1.intersects(GeomPoly):
                for ptid in DicoP4[keyP4][1] :
                    if  Point_id==ptid:
                        NbObs=DicoP4[keyP4][2]
                        toto=''
                        first=True
                        for t in DicoP4[keyP4][1]:
                            if first:
                                first=False
                                toto= str(t)
                            else: toto=toto+' - '+str(t)
                        list_id=toto
                        NumAgregat=keyP4
            newfeatAGGREGATS=QgsFeature()
            newfeatAGGREGATS.setGeometry(geomP1)
            ValuesAGGREGATS=attributs
            ValuesAGGREGATS.append(Point_id)
            ValuesAGGREGATS.append(NumAgregat)
            ValuesAGGREGATS.append(NbObs)
            ValuesAGGREGATS.append(list_id)
            newfeatAGGREGATS.setAttributes(ValuesAGGREGATS)
            prAGGREGATS.addFeatures([newfeatAGGREGATS])
        AGGREGATS.commitChanges()
        iface.mapCanvas().refresh()
        


