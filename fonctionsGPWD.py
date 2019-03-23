# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Fichier des fonctions du plugin cc
                                 A QGIS plugin
 
                              -------------------
        begin                : 2019-03-21
        copyright            : (C) 2019 by Jean-Christophe Baudin 
        email                : jean-christophe.baudin@ymail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsProject, QgsMapLayer, QgsWkbTypes, QgsPointXY
from qgis.PyQt.QtCore import QFileInfo, QSettings, QCoreApplication
from qgis.PyQt.QtCore import QTranslator, qVersion
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox,QDialog
from osgeo import ogr
from math import sqrt

import csv, sys
import re
import os
import os.path
import unicodedata
 
def twodecimal(number):
    NB=int((number * 100) + 0.5) / 100.0 # Adding 0.5 rounds it up
    return  NB

def vect(p1, p2):
    #Vecteur dit par deux points
    v_x = p2.x() - p1.x()
    v_y = p2.y() - p1.y()
    Vec=QgsPointXY(v_x,v_y)
    return Vec  

def mag(p):
    magn=0.0
    if (p.x(),p.y())==(0.0,0.0):
        return 1
    else:
        # magnitude d'un vecteur point
        magn=sqrt(p.x()**2 + p.y()**2)
    return magn

def Aggregateur(DicoP1):
    cpt_agg=0
    nb=0
    liste_id=[]
    liste_pt=[]
    liste_aggreg_pt=[]
    T=True
    while len(DicoP1)!=0:
        first=True
        QMessageBox.information(None,"debug :",'DicoP1: '+str(DicoP1)+'\n'+'nb: '+str(nb)+'\n'+ 'liste_id: '+'\n'+str(liste_id)+'\n'+'liste_pt: '+'\n'+str(liste_pt)) 
        for keyD1 in list(DicoP1.keys()):
            P1=DicoP1[keyD1][0] 
        if first:
            T=True
            first=False
            nb+=1
            liste_id=[keyD1]
            liste_pt=[P1]
            del DicoP1[keyD1]
        while T:
            for pt in liste_pt:
                compteur_corresP=0
                for keyD1 in list(DicoP1.keys()):
                    #QMessageBox.information(None,"debug :",'DicoP1: '+str(DicoP1)+'\n'+'nb: '+str(nb)+'\n'+ 'liste_id: '+'\n'+str(liste_id)+'\n'+'liste_pt: '+'\n'+str(liste_pt)) 
                    P1=DicoP1[keyD1][0]
                    if mag(vect(pt,P1))<D:
                        compteur_corresId=0
                        for id in liste_id:
                            if keyD1==id:
                                compteur_corresId+=1
                        if compteur_corresId==0:
                            nb+=1
                            liste_id.append(keyD1)
                            liste_pt.append(P1)
                            compteur_corresP+=1
            if compteur_corresP==0:
                T=False
                cpt_agg+=1
                DicoA[cpt_agg]=[nb, liste_id, liste_pt]
                for id in liste_id:
                    for keyD1 in list(DicoP1.keys()):
                        if id==keyD1:
                            del DicoP1[keyD1]
    return DicoA

def getVectorLayerByName(NomCouche):
    layermap=QgsProject.instance().mapLayers()
    for name, layer in layermap.items():
        if layer.type()==QgsMapLayer.VectorLayer and layer.name()==NomCouche:
            if layer.isValid():
               return layer
            else:
               return None
            

