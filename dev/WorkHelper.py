#!/usr/local/bin/env jython
# -*- coding: utf-8 -*-

"""
WorkHelper
#execfile('aplication_name.py')
This aplication is aimed at avoind repeating,
time consuming and boring coding actions.

author: Tataru Andrei Emanuelsw
email: tataru.andrei.emanuel@ipsos.com
last modified: April 2012
"""
from java.awt import Dimension
from java.awt import Color

from java.awt.datatransfer import StringSelection
#DataFlavor

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
from javax.swing import JTabbedPane
from javax.swing import JPanel

import os
#import re




class WorkHelper(JFrame):

    def __init__(self):
        super(WorkHelper, self).__init__()
        self.clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()

#############################################################
# Layout:
        layout = GroupLayout(self.getContentPane())
        self.getContentPane().setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)
#############################################################

#############################################################
# Frame Area:
        Larea1 = JLabel("InputArea:")

        Sarea1 = JScrollPane()
        self.area1 = JTextArea()
        self.area1.setToolTipText("Input Area")
        self.area1.setEditable(True)
        self.area1.setBorder(BorderFactory.createLineBorder(Color.gray))
        Sarea1.setPreferredSize(Dimension(300,100))
        Sarea1.getViewport().setView((self.area1))

        bClear = JButton("Clear", actionPerformed=self.bClear)
        bClear.setToolTipText("Clears the text form both Input and Output text Areas")

        bCopyToInput = JButton("Copy to Input", actionPerformed=self.bCopyToInput)
        bCopyToInput.setToolTipText("Copy the text from the Output Area to the Input Area for further Operations")
        
        self.cCtClipB = JCheckBox("Auto-Copy");
        self.cCtClipB.setToolTipText("When 'Checked' after the Categories are created they will added to the clipboard")
        self.cCtClipB.setSelected(1)
        
        Larea2 = JLabel("OutputArea:")
        
        Sarea2 = JScrollPane()
        self.area2 = JTextArea()
        self.area2.setToolTipText("Output Area")
        self.area2.setEditable(False)
        self.area2.setBorder(BorderFactory.createLineBorder(Color.gray))
        Sarea2.setPreferredSize(Dimension(300,100))
        Sarea2.getViewport().setView((self.area2))

#############################################################
# Tabbed Area:
        tabPane = JTabbedPane(JTabbedPane.TOP)
        self.getContentPane().add(tabPane)
        #####################################################
        # Text Edit pane
        panel_TEdit = JPanel()
        layout2 = GroupLayout(panel_TEdit)
        layout2.setAutoCreateGaps(True)
        layout2.setAutoCreateContainerGaps(True)
        panel_TEdit.setLayout(layout2)
        
        bRemoveNBSP_L = JButton("Clean LText", actionPerformed=self.bRemoveNBSP_L)
        bRemoveNBSP_L.setToolTipText("Removes Spaces, Tabs from the start of every text line from the input Area")
        bRemoveNBSP_R = JButton("Clean RText", actionPerformed=self.bRemoveNBSP_R)
        bRemoveNBSP_R.setToolTipText("Removes Spaces, Tabs from the end of every text line from the input Area")
    
        
        self.ReplaceThis = JTextField()
        self.ReplaceThis = JTextField(maximumSize=Dimension(120,25))
        self.ReplaceThis.setToolTipText("Text to be replaced")

        self.ReplaceThat = JTextField()
        self.ReplaceThat = JTextField(maximumSize=Dimension(120,25))
        self.ReplaceThat.setToolTipText("Text to be placed")

        bSandReplace = JButton("Replace Text", actionPerformed=self.bSandReplace)
        bSandReplace.setToolTipText("Replace the text from This with Text from That in the Text from the Input Area and displays it in the Output Area")

        bRemNumbers = JButton("Rem Numbers", actionPerformed=self.RemNumbers)
        bRemNumbers.setToolTipText("Removes numbers from the start of every line")
        #####################################################
        # Dimension pane
        panel_Dimensions = JPanel()
        layout3 = GroupLayout(panel_Dimensions)
        layout3.setAutoCreateGaps(True)
        layout3.setAutoCreateContainerGaps(True)
        panel_Dimensions.setLayout(layout3)
        
        
        self.cCurly = JCheckBox("Curly");
        self.cCurly.setToolTipText("When 'Checked' Curly Brackets will surround the Categories")
        self.cCurly.setSelected(1)

        self.cSemiC = JCheckBox("SemiColumn");
        self.cSemiC.setToolTipText("When 'Checked' after the Categories are created at the end will be a semicolomn")
        self.cSemiC.setSelected(1)

        self.iStart = JTextField(maximumSize=Dimension(40,25))
        self.iStart.setToolTipText("The Start Index for the Making of the Categories")

        self.RThis = JTextField()
        self.RThis = JTextField(maximumSize=Dimension(120,25))
        self.RThis.setToolTipText("The Starting Index used in creating the Categorical")

        self.RThat = JTextField()
        self.RThat = JTextField(maximumSize=Dimension(120,25))
        self.RThat.setToolTipText("The Finish Index used in creating the Categorical")
        
        optioncCategories = JLabel("Options:")
        bcCat = JButton("CreatCateg", actionPerformed=self.bcCat)
        bcCat.setToolTipText("Create a categorical form starting C_Index to finish C_Index; Use the text boxes to define the indexes")

        bM_Categories = JButton("Categories", actionPerformed=self.mCategories)
        bM_Categories.setToolTipText("Make Categories using the lines from the Input Area. Use it to define Categorical questions.")
        #####################################################
        # ConfirmIt pane
        panel_ConfirmIt = JPanel()
        layout4 = GroupLayout(panel_ConfirmIt)
        layout4.setAutoCreateGaps(True)
        layout4.setAutoCreateContainerGaps(True)
        panel_ConfirmIt.setLayout(layout4)
        
        self.PID = JTextField()
        self.PID = JTextField(maximumSize=Dimension(120,25))
        self.PID.setToolTipText("The PID number used for creating links with PID and ids from every line of the Input Area")
        
        bClinks = JButton("Create Links", actionPerformed=self.bClinks)
        bClinks.setToolTipText("Create links for a project using PID and ID, ID`s are read from every line of the Input Area")
        
        bClinksNA = JButton("Create Links NA ", actionPerformed=self.bClinksNA)
        bClinksNA.setToolTipText("Create links for a project using PID and ID`s from the standard sample test for US")
        
        bClinksCA = JButton("Create Links CA", actionPerformed=self.bClinksCA)
        bClinksCA.setToolTipText("Create links for a project using PID and ID`s from the standard sample test for CA")
        
        self.Width = JTextField()
        self.Width = JTextField(maximumSize=Dimension(120,25))
        self.Width.setToolTipText("The Width used in creating the DIV html tag, note the dimension used is in px")
        
        baddDIVt = JButton("Add DIV tag", actionPerformed=self.baddDIVt)
        baddDIVt.setToolTipText("Create a DIV tag for every line in the Input Area")
        #####################################################
        # Statistics pane
        panel_Statistics = JPanel()
        layout5 = GroupLayout(panel_Statistics)
        layout5.setAutoCreateGaps(True)
        layout5.setAutoCreateContainerGaps(True)
        panel_Statistics.setLayout(layout5)         
        
        #####################################################
        # TimeTraking pane
        panel_TimeTraking = JPanel()
        layout6 = GroupLayout(panel_TimeTraking)
        layout6.setAutoCreateGaps(True)
        layout6.setAutoCreateContainerGaps(True)
        panel_TimeTraking.setLayout(layout6)     
        
        #####################################################
        # Tabbed Area Tabs
        tabPane.addTab("Text Edit", panel_TEdit)
        tabPane.addTab("Dimensions", panel_Dimensions)
        tabPane.addTab("ConfirmIt", panel_ConfirmIt)
        tabPane.addTab("Statistics", panel_Statistics)
        tabPane.addTab("TimeTraking", panel_TimeTraking)
        
        
#############################################################




#############################################################
# Aplication Layouts: 2 groups one Horizontal and one Vertical
        
        #############################################################
        # Frame Layout: 2 groups one Horizontal and one Vertical
        layout.setHorizontalGroup(layout.createSequentialGroup()
            .addGroup(layout.createParallelGroup()
                .addComponent(Larea1)
                .addComponent(Sarea1)
                .addComponent(Sarea2)
                .addGroup(layout.createSequentialGroup()
                          .addComponent(bCopyToInput)
                          .addComponent(bClear)
                          .addComponent(self.cCtClipB))
                .addComponent(Larea2))
            .addGroup(layout.createParallelGroup()
                .addComponent(tabPane))
                        )

        layout.setVerticalGroup(layout.createSequentialGroup()
            .addGroup(layout.createParallelGroup()
                      .addGroup(layout.createSequentialGroup()
                          .addComponent(Larea1)
                          .addComponent(Sarea1)
                          .addGroup(layout.createParallelGroup()
                                    .addComponent(bCopyToInput)
                                    .addComponent(bClear)
                                    .addComponent(self.cCtClipB)    )
                          .addComponent(Larea2)
                          .addComponent(Sarea2))
                      .addGroup(layout.createSequentialGroup()
                          .addComponent(tabPane))
                          )
                        )

        #############################################################
        # TEdit Layout: 2 groups one Horizontal and one Vertical
        layout2.setHorizontalGroup(layout2.createSequentialGroup()
            .addGroup(layout2.createParallelGroup()
                .addGroup(layout2.createSequentialGroup()
                    .addComponent(bRemNumbers)
                    .addComponent(bRemoveNBSP_L)
                    .addComponent(bRemoveNBSP_R))
                    .addGroup(layout2.createSequentialGroup()
                    .addComponent(bSandReplace)
                    .addComponent(self.ReplaceThis)
                    .addComponent(self.ReplaceThat))  
                      
                      
                      
                                   ))
        
        layout2.setVerticalGroup(layout2.createSequentialGroup()
            .addGroup(layout2.createParallelGroup()
                .addComponent(bRemNumbers)
                .addComponent(bRemoveNBSP_L)
                .addComponent(bRemoveNBSP_R))
                                 
                .addGroup(layout2.createParallelGroup()
                    .addComponent(bSandReplace)
                    .addComponent(self.ReplaceThis)
                    .addComponent(self.ReplaceThat))  
                                 )
            
            
        #############################################################
        # Dimensions Layout: 2 groups one Horizontal and one Vertical
        layout3.setHorizontalGroup(layout3.createSequentialGroup()
        
         .addGroup(layout3.createParallelGroup()
            .addGroup(layout3.createSequentialGroup()
                .addComponent(bM_Categories)
                .addComponent(self.iStart))
            .addGroup(layout3.createSequentialGroup()
                .addComponent(optioncCategories)
                .addComponent(self.cCurly)
                .addComponent(self.cSemiC)
                )
           
            .addGroup(layout3.createSequentialGroup()
                .addComponent(bcCat)
                .addComponent(self.RThis)
                .addComponent(self.RThat))
            .addGroup(layout3.createSequentialGroup()
                
                )

                )
        )
        
        layout3.setVerticalGroup(layout3.createSequentialGroup()
            .addGroup(layout3.createSequentialGroup()
                    .addGroup(layout3.createParallelGroup()
                        .addComponent(bM_Categories)
                        .addComponent(self.iStart))
                    
                    .addGroup(layout3.createParallelGroup()
                        .addComponent(bcCat)
                        .addComponent(self.RThis)
                        .addComponent(self.RThat))
                    .addGroup(layout3.createParallelGroup()
                        
                    .addGroup(layout3.createParallelGroup()
                        .addComponent(optioncCategories)
                        .addComponent(self.cCurly)
                        .addComponent(self.cSemiC)
                        )
                   
                                )
                        )
            
            )
        #############################################################
        # ConfimIT Layout: 2 groups one Horizontal and one Vertical
        layout4.setHorizontalGroup(layout4.createSequentialGroup()
        
         .addGroup(layout4.createParallelGroup()
            .addGroup(layout4.createSequentialGroup()
                .addComponent(bClinks)
                .addComponent(self.PID)
                )
            .addGroup(layout4.createSequentialGroup()
                .addComponent(bClinksNA)
                .addComponent(bClinksCA)
                )
            .addGroup(layout4.createSequentialGroup()
                .addComponent(baddDIVt)
                .addComponent(self.Width)
                
                )
                
                ))
        
        
        layout4.setVerticalGroup(layout4.createSequentialGroup()
            .addGroup(layout4.createSequentialGroup()
                    .addGroup(layout4.createParallelGroup()
                        .addComponent(bClinks)
                        .addComponent(self.PID))
                    .addGroup(layout4.createParallelGroup()
                        .addComponent(bClinksNA)
                        .addComponent(bClinksCA)
                        )
                    
                    .addGroup(layout4.createParallelGroup()
                        .addComponent(baddDIVt)
                        .addComponent(self.Width)
                        )
                    
                        
                        ))
        
        
        #layout2.linkSize(SwingConstants.HORIZONTAL, [self.cCurly,bM_Categories])
        #layout.linkSize(SwingConstants.HORIZONTAL, [ok, bCopyToInput, close, bM_Categories])
        #layout3.linkSize(SwingConstants.HORIZONTAL, [self.RThis,self.RThat,bRemoveNBSP_L,bRemoveNBSP_R,bM_Categories,bSandReplace,bcCat])

        
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
        os.system.exit(0)


# def addToClipBoard(self, text):
# "@sig public void setExpression(java.lang.String text)"
# command = 'echo ' + text.strip() + '| clip'
# os.system(command)
# brute method for pasting into clipboard on windows




    def mCategories(self, e):
        "@sig public void setExpression(java.lang.String e)"
        """
        Takes every line of text form the Input Area and by using a
        string composition it creates the output in the SPSS dimension
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
        self.area2.setText(self.area1.getText().replace(self.ReplaceThis.getText(),self.ReplaceThat.getText()))
        self.copyToClipboard(self.area2.getText())

    #############################################################
    # Confirmit
    def bClinks(self, e):
    
    
        text=self.area1.getText().rstrip()

        lastindex=0
        textO=""

        for i in range(0,len(text)):
                if text[i]=='\n':
                    textO=textO+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+text[lastindex:i]+'\n'
                    lastindex=i+1

        if len(text[lastindex:len(text)])>0:
                textO=textO+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+text[lastindex:len(text)]

        self.copyToClipboard(textO)
        self.area2.setText(textO)
        
    def bClinksNA(self, e):
        
        
        output=""
        
        for i in range (1,201):
        
            if i<10:
                output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'US9900'+str(i)+'\n'
            else:
                if i<100:
                    output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'US990'+str(i)+'\n'
                else:
                    if i==200:
                        output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'US99'+str(i)
                    else: 
                        output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'US99'+str(i)+'\n'
        
        
        self.area2.setText(output)
        self.copyToClipboard(self.area2.getText())
        
    def bClinksCA(self, e):
        output=""
        
        for i in range (1,201):
        
            if i<10:
                output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'CA9900'+str(i)+'\n'
            else:
                if i<100:
                    output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'CA990'+str(i)+'\n'
                else:
                    if i==200:
                        output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'CA99'+str(i)
                    else: 
                        output=output+'http://surveys.ipsosinteractive.com/surveys2/?pid='+self.PID.getText()+'&id='+'CA99'+str(i)+'\n'
        
        
        self.area2.setText(output)
        self.copyToClipboard(self.area2.getText())
        
    def baddDIVt(self, e):
        
        try:
            Width = int(self.Width.getText())
        except ValueError:
            Width=1
            
        text=self.area1.getText().rstrip()

        lastindex=0
        textO=""

        for i in range(0,len(text)):
            if text[i]=='\n':
                textO=textO+'<div style="width:'+str(Width)+'px">'+text[lastindex:i]+'</div>'+'\n'
                lastindex=i+1

        if len(text[lastindex:len(text)])>0:
            textO=textO+'<div style="width:'+str(Width)+'px">'+text[lastindex:len(text)]+'</div>'
            

        self.copyToClipboard(textO)
        self.area2.setText(textO)
        
    def RemNumbers(self, e):
        text=self.area1.getText().rstrip()

        lastindex=0
        textO=""
        
        
        for i in range(0,len(text)):
            if text[i]=='\n':
                textO=textO+text[lastindex:i].lstrip('1234567890')+'\n'
                lastindex=i+1
        if len(text[lastindex:len(text)])>0:
            textO=textO+text[lastindex:len(text)].lstrip('1234567890')
            

        self.copyToClipboard(textO)
        self.area2.setText(textO)
#############################################################

if __name__ == '__main__':
    WorkHelper()