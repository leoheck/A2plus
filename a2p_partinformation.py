#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2018 kbwbe                                              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCADGui,FreeCAD
import Spreadsheet
from PySide import QtGui, QtCore
import os, copy, time, sys, platform
import a2plib
from a2p_partlistglobals import PARTLIST_COLUMN_NAMES

from a2p_partlistglobals import (
    PARTINFORMATION_SHEET_NAME, 
    PARTINFORMATION_SHEET_LABEL
    )



#------------------------------------------------------------------------------
toolTip = \
'''
Create a spreadsheet for ordering or
logistics information.

The created spreadsheet can be found
within the tree view.

Please fill in your information.
This spreadsheet will be read out
by the parts list function of A2plus.
'''

class a2p_CreatePartInformationSheet_Command:
    
    def countLines(self,ss):
        count = 1
        try:
            while True:
                cellAdress = 'A{}'.format(count)
                ss.get(cellAdress)
                count+=1
        except:
            count = count -1
        return count

    def Activated(self):
        doc = FreeCAD.activeDocument()
        if doc == None:
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(),
                                        "No active document found!",
                                        "You have to open a FCStd file first."
                                    )
            return
        
        try:
            found = doc.getObject(PARTINFORMATION_SHEET_NAME)
            if found != None: # object already exists
                numLines = self.countLines(found)
                if numLines != len(PARTLIST_COLUMN_NAMES):
                    flags = QtGui.QMessageBox.StandardButton.Yes | QtGui.QMessageBox.StandardButton.No
                    msg = u"Do you want to update the field names ?"
                    response = QtGui.QMessageBox.information(
                        QtGui.QApplication.activeWindow(),
                        u"field configuration has changed",
                        msg,
                        flags
                        )
                    if response == QtGui.QMessageBox.Yes:
                        for idx,name in enumerate(PARTLIST_COLUMN_NAMES):
                            found.set('A'+str(idx+1),name)
                            found.setBackground(
                                'A1:A'+str(len(PARTLIST_COLUMN_NAMES)),
                                (0.000000,1.000000,0.000000,1.000000)
                                )
                            found.setBackground(
                                'B1:B'+str(len(PARTLIST_COLUMN_NAMES)),
                                (0.85,0.85,0.85,1.000000)
                                )
                        doc.recompute()
                return
        except:
            pass # proceed and create the sheat
        
        # create a spreadsheet with a special reserved name...
        ss = doc.addObject('Spreadsheet::Sheet',PARTINFORMATION_SHEET_NAME)
        ss.Label = PARTINFORMATION_SHEET_LABEL
        
        for idx,name in enumerate(PARTLIST_COLUMN_NAMES):
            ss.set('A'+str(idx+1),name)
            ss.set('B'+str(idx+1),'')
        
        ss.setColumnWidth('A',220)
        ss.setColumnWidth('B',300)
        ss.setBackground('A1:A'+str(len(PARTLIST_COLUMN_NAMES)), (0.000000,1.000000,0.000000,1.000000))
        ss.setBackground('B1:B'+str(len(PARTLIST_COLUMN_NAMES)), (0.85,0.85,0.85,1.000000))
        doc.recompute()

    def GetResources(self):
        return {
            'Pixmap'  :     ':/icons/a2p_PartsInfo.svg',
            'MenuText':     'Create a spreadsheet for ordering or logistics information',
            'ToolTip':      toolTip
            }
        
FreeCADGui.addCommand('a2p_CreatePartInformationSheet_Command', a2p_CreatePartInformationSheet_Command())
#------------------------------------------------------------------------------
