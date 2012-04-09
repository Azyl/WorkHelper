#!/usr/local/bin/jython
# -*- coding: utf-8 -*-

"""
WorkHelper
#execfile('test.py')
This aplication is aimed at avoind repeating,
time consuming and boring coding actions.

author: Tataru Andrei Emanuelsw
email: tataru.andrei.emanuel@ipsos.com
last modified: March 2012
"""
from java.awt import Dimension
from java.awt import Color

from java.awt.datatransfer import StringSelection, DataFlavor

from javax.swing import JButton
from javax.swing import SwingConstants
from javax.swing import JFrame
from javax.swing import JLabel
from javax.swing import JTextArea
from javax.swing import BorderFactory
from javax.swing import GroupLayout
from javax.swing import JScrollPane
from javax.swing import JTextField
from javax.swing import JCheckBox
from java.awt import Toolkit
#import os




class WorkHelper(JFrame):

    def __init__(self):
        super(WorkHelper, self).__init__()

        self.clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
        #self.initUI()

    #def initUI(self):

        #panel = JPanel()
        #self.getContentPane().add(panel)
        
#############################################################
# Layout
        layout = GroupLayout(self.getContentPane())
        self.getContentPane().setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)
#############################################################

#############################################################
# Scroll Area Input + Output
        Larea1 = JLabel("InputArea:")
        Larea2 = JLabel("OutputArea:")
        
        Sarea1 = JScrollPane()
        Sarea2 = JScrollPane()
        
        self.area1 = JTextArea()
        self.area1.setToolTipText("Input Area")
        self.area1.setEditable(True)
        self.area1.setBorder(BorderFactory.createLineBorder(Color.gray))
        
        Sarea1.setPreferredSize(Dimension(300,100))
        Sarea1.getViewport().setView((self.area1))
        
        self.area2 = JTextArea()
        self.area2.setToolTipText("Output Area")
        self.area2.setEditable(False)
        self.area2.setBorder(BorderFactory.createLineBorder(Color.gray))
        
        Sarea2.setPreferredSize(Dimension(300,100))
        Sarea2.getViewport().setView((self.area2))
#############################################################

#############################################################
# Buttons

        self.cCurly = JCheckBox("Curly");
        self.cCurly.setToolTipText("When 'Checked' Curly Brackets will surround the Categories")
        self.cCurly.setSelected(1)
        

        self.cCtClipB = JCheckBox("Auto-Copy");
        self.cCtClipB.setToolTipText("When 'Checked' after the Categories are created they will added to the clipboard")
        self.cCtClipB.setSelected(1)

        self.cSemiC = JCheckBox("SemiColumn");
        self.cSemiC.setToolTipText("When 'Checked' after the Categories are created at the end will be a semicolomn")
        self.cSemiC.setSelected(1)        
        
        bRemoveNBSP_L = JButton("Clean LText", actionPerformed=self.bRemoveNBSP_L)
        bRemoveNBSP_L.setToolTipText("Removes Spaces, Tabs from the start of every text line from the input Area")
        bRemoveNBSP_R = JButton("Clean RText", actionPerformed=self.bRemoveNBSP_R)
        bRemoveNBSP_R.setToolTipText("Removes Spaces, Tabs from the end of every text line from the input Area")
        bCopyToInput = JButton("Copy to Input", actionPerformed=self.bCopyToInput)
        bCopyToInput.setToolTipText("Copy the text from the Output Area to the Input Area for further Operations")
        
        bClear = JButton("Clear", actionPerformed=self.bClear)
        bClear.setToolTipText("Clears the text form both Input and Output text Areas")
        
        self.iStart = JTextField(maximumSize=Dimension(40,25))
        self.iStart.setToolTipText("The Start Index for the Making of the Categories")
        
        self.RThis = JTextField()
        self.RThis = JTextField(maximumSize=Dimension(120,25))
        self.RThis.setToolTipText("Text to be replaced or The Starting C_Index")
        
        self.RThat = JTextField()
        self.RThat = JTextField(maximumSize=Dimension(120,25))
        self.RThat.setToolTipText("Text to be placed or The Finish C_Index")
        
        
        bSandReplace = JButton("Replace Text", actionPerformed=self.bSandReplace)
        bSandReplace.setToolTipText("Replace the text from This with Thext from That in the Text from the Input Area and displays it in the Output Area")
        
        bcCat = JButton("CreatCateg", actionPerformed=self.bcCat)
        bcCat.setToolTipText("Create a categorical form starting C_Index to finish C_Index; Use the above text boxes to define the indexes")
        
        
        bC_S = JButton("Create _Series", actionPerformed=self.bC_S)
        bC_S.setToolTipText("Create a series form starting C_Index to finish C_Index; Use the above text boxes to define the indexes; It will create a series for every row in the Input Area")

        
        
        bM_Categories = JButton("Categories", actionPerformed=self.mCategories)
        bM_Categories.setToolTipText("Make Categories using the lines from the Input Area")
        #bM_Categories = JButton(maximumSize=Dimension(40,25))
        # de incercat daca merge cu ; sa grupezi in [dsa] elementele
#############################################################


#############################################################
# Aplication Layout 2 groups one Horizontal and one Vertical
        layout.setHorizontalGroup(layout.createSequentialGroup()
            .addGroup(layout.createParallelGroup()
                .addComponent(Larea1)
                .addComponent(Sarea1)

                .addComponent(Sarea2)
                .addComponent(bCopyToInput)
                .addComponent(Larea2))
            .addGroup(layout.createParallelGroup()
            .addGroup(layout.createSequentialGroup()
                .addComponent(bM_Categories)
                .addComponent(self.iStart))
            .addGroup(layout.createSequentialGroup()
                .addComponent(self.cCurly)
                .addComponent(self.cSemiC)
                .addComponent(self.cCtClipB))
            .addGroup(layout.createSequentialGroup()
                .addComponent(bRemoveNBSP_L)
                .addComponent(bRemoveNBSP_R))
            .addGroup(layout.createSequentialGroup()
                .addComponent(self.RThis)
                .addComponent(self.RThat))
            .addGroup(layout.createSequentialGroup()
                .addComponent(bSandReplace)
                .addComponent(bcCat))
            .addGroup(layout.createSequentialGroup()
                .addComponent(bC_S))
                
                .addComponent(bClear))
            
        )

        layout.setVerticalGroup(layout.createSequentialGroup()
            .addComponent(Larea1)
            
            .addGroup(layout.createParallelGroup()
                .addComponent(Sarea1)
                
                .addGroup(layout.createSequentialGroup()
                    .addGroup(layout.createParallelGroup()
                        .addComponent(bM_Categories)
                        .addComponent(self.iStart))
                    .addGroup(layout.createParallelGroup()
                        .addComponent(self.cCurly)
                        .addComponent(self.cSemiC)
                        .addComponent(self.cCtClipB))
                    .addGroup(layout.createParallelGroup()
                        .addComponent(bRemoveNBSP_L)
                        .addComponent(bRemoveNBSP_R))
                    .addGroup(layout.createParallelGroup()
                        .addComponent(self.RThis)
                        .addComponent(self.RThat))
                    .addGroup(layout.createParallelGroup()   
                        .addComponent(bSandReplace)
                        .addComponent(bcCat))
                    .addGroup(layout.createParallelGroup()
                        .addComponent(bC_S))
                        
                        
                        )
                    )
                
            .addGroup(layout.createParallelGroup()
                .addComponent(bCopyToInput)
                .addComponent(bClear))
            .addComponent(Larea2)
            .addGroup(layout.createParallelGroup()
                .addComponent(Sarea2))
        )
        
        #layout.linkSize(SwingConstants.HORIZONTAL, [ok, bCopyToInput, close, bM_Categories])
        layout.linkSize(SwingConstants.HORIZONTAL, [self.RThis,self.RThat,bRemoveNBSP_L,bRemoveNBSP_R,bCopyToInput,bM_Categories,bSandReplace,bcCat,bC_S])
        
        #layout.linkSize(SwingConstants.HORIZONTAL, [self.cCurly,bM_Categories])
#############################################################

#############################################################
# Aplication Settings
        self.pack()
        #self.setPreferredSize(Dimension(1000, 1000))
        self.setTitle("Workhelper")
        self.setSize(800, 500)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setLocationRelativeTo(None)
        self.setVisible(True)
#############################################################
        
#############################################################
# WorkHelper class methods:
    def onQuit(self, e):
        "@sig public void setExpression(java.lang.String e)"
        System.exit(0)


# def addToClipBoard(self, text):
# "@sig public void setExpression(java.lang.String text)"
# command = 'echo ' + text.strip() + '| clip'
# os.system(command)
# brute method for pasting into clipboard on windows



        
    def mCategories(self, e):
        "@sig public void setExpression(java.lang.String e)"
        """
Takes every line of text form the Input Area and by using a
string composotion it creates the output in the SPSS dimension
categories format.
"""
        try:
            StartIndex = int(self.iStart.getText())
        except ValueError:
            StartIndex=1




        text=self.area1.getText().rstrip()
        
        
        counter=StartIndex
        lastindex=0
        textO=""
        
        for i in range(0,len(text)):
                if text[i]=='\n':
                        textO=textO+("_"+str(counter)+' "'+text[lastindex:i]+'",\n')
                        lastindex=i+1
                        counter=counter+1

        if len(text[lastindex:len(text)])>0:
                textO=textO+("_"+str(counter)+' "'+text[lastindex:len(text)]+'"')


        if len(textO)>0:
            if self.cCurly.isSelected():
                textO = "{\n"+ textO + "\n}"
                if self.cSemiC.isSelected():
                    textO = textO + ";"
            self.copyToClipboard(textO)    
            self.area2.setText(textO)
    
    def copyToClipboard(self, text):
            if self.cCtClipB.isSelected():
                stringSelection = StringSelection(text)
                self.clipboard.setContents(stringSelection, None)
            
        
        
    def bCopyToInput(self, e):
        "@sig public void setExpression(java.lang.String e)"
        """Copy the Text from the Output Area to the input Area for further operations"""
        
        self.area1.setText(self.area2.getText())
    
    def bRemoveNBSP_L(self, e):
        "@sig public void setExpression(java.lang.String e)"
        text=self.area1.getText().rstrip()
        textO=""
        lastindex=0
        
        for i in range(0,len(text)):
            if text[i] == '\n':
                textO = textO+text[lastindex:i].lstrip()+"\n"
                lastindex=i+1
                #print(text[0:i].lstrip()+'\n')
        if len(text[lastindex:len(text)])>0:
                textO=textO+text[lastindex:len(text)].lstrip()
        self.area2.setText(textO)
    
    def bRemoveNBSP_R(self, e):
        "@sig public void setExpression(java.lang.String e)"
        text=self.area1.getText().rstrip()
        textO=""
        lastindex=0
        
        for i in range(0,len(text)):
            if text[i] == '\n':
                textO = textO+text[lastindex:i].rstrip()+"\n"
                lastindex=i+1
                #print(text[0:i].lstrip()+'\n')
        if len(text[lastindex:len(text)])>0:
                textO=textO+text[lastindex:len(text)].rstrip()
        self.area2.setText(textO)
        
    def bClear(self, e):
        "@sig public void setExpression(java.lang.String e)"
        self.area1.setText("")
        self.area2.setText("")
    
    def bcCat(self, e):
        "@sig public void setExpression(java.lang.String e)"
        try:
            StartIndex = int(self.RThis.getText())
        except ValueError:
            StartIndex=1
        
        try:
            FinishIndex = int(self.RThat.getText())
        except ValueError:
            FinishIndex=1
        cCats=""
        for i in range(StartIndex,FinishIndex+1):
            if i<>FinishIndex:
                cCats=cCats+"_"+str(i)+","
            else:
                cCats=cCats+"_"+str(i)
            
        if StartIndex<FinishIndex:
            cCats="{"+cCats+"}"
            self.copyToClipboard(cCats)
            self.area2.setText(cCats)
        
    def bSandReplace(self, e):
        self.area2.setText(self.area1.getText().replace(self.RThis.getText(),self.RThat.getText()))
        
    def bC_S(self, e):
        "@sig public void setExpression(java.lang.String e)"
        try:
            StartIndex = int(self.RThis.getText())
        except ValueError:
            StartIndex=1
        
        try:
            FinishIndex = int(self.RThat.getText())
        except ValueError:
            FinishIndex=1
        
        if StartIndex<FinishIndex:
            text=self.area1.getText().rstrip()
            lastindex=0
            textO=""
            
            for i in range(0,len(text)):
                    if text[i]=='\n':
                        counter=StartIndex
                        for j in range(StartIndex,FinishIndex+1):
                            textO=textO+(text[lastindex:i]+"_"+str(counter)+" ")
                            counter=counter+1
                        lastindex=i+1
                        textO=textO+'\n'

            #if len(text[lastindex:len(text)])>0:
            #        textO=textO+("_"+str(counter)+' "'+text[lastindex:len(text)]+'"')

            if lastindex==0 and len(text)>0:
                counter=StartIndex
                for j in range(StartIndex,FinishIndex+1):
                    textO=textO+(text[lastindex:i]+"_"+str(counter)+" ")
                    counter=counter+1
            
            if len(textO)>0:
                self.copyToClipboard(textO)    
                self.area2.setText(textO)
        
#############################################################

if __name__ == '__main__':
    WorkHelper()