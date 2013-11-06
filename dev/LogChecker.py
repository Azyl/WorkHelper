#-------------------------------------------------------------------------------
# Name:        Excel Export Checker
# Purpose:
#
# Author:      Tataru Andrei Emanuel
#
# Created:     06-11-2013
# Copyright:   (c) Tataru Andrei Emanuel 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import glob


class Record(object):
    __slots__= "requestKey", "logFile", "started", "stopped" , "logLevel", "date", "time", "logEntryType","msgInfo"

    def items(self):
        "dict style items"
        return [
            (field_name, getattr(self, field_name))
            for field_name in self.__slots__]

    def __iter__(self):
        "iterate over fields tuple/list style"
        for field_name in self.__slots__:
            yield getattr(self, field_name)

    def __getitem__(self, index):
        "tuple/list style getitem"
        return getattr(self, self.__slots__[index])

def setDirectory(workingDir):
    curentDirectoryPath=os.getcwd()
    logsDirectoryPath=curentDirectoryPath+"\\"+workingDir
    os.chdir(logsDirectoryPath)
    return logsDirectoryPath

def getLogsFiles():
    logFiles=[]
    for files in glob.glob("*.log.*"):
        logFiles.append(files)
    print logFiles
    return logFiles


def getExcelExportsLines(filename,excelExportsDict):
    with open(filename) as f:
        for line in f:
            if "excel" in line:
                started=False
                stopped=False

                requestKey=line[line.index("[")+1:line.index("]")] #user + id
                logLevel,date,time,logEntryType=line[:line.index("[")-2].replace("  "," ").split(" ")
                msgInfo=line[line.index("]")+2:]


                if "Export excel for" in line[line.index("]")+1:].replace("  "," "):
                    started=True
                if "Finished excel export" in line[line.index("]")+1:].replace("  "," "):
                    stopped=True

                if requestKey in excelExportsDict:
                    if started == True and excelExportsDict[requestKey].started== False:
                        excelExportsDict[requestKey].started=True
                    if stopped == True and excelExportsDict[requestKey].stopped== False:
                        excelExportsDict[requestKey].stopped=True
                    for msg in excelExportsDict[requestKey].msgInfo:
                        if msg<>msgInfo:
                            excelExportsDict[requestKey].msgInfo.append(msgInfo)
                else:
                    r= Record()
                    r.started=started
                    r.stopped=stopped
                    r.requestKey=requestKey
                    r.logFile=filename
                    r.logLevel=logLevel
                    r.date=date
                    r.time=time
                    r.logEntryType=logEntryType
                    r.msgInfo=[msgInfo]
                    excelExportsDict.update({requestKey:r})

def getUnfinishedExports(excelExportsDict):
    failedRequestKeys=[]
    for key,values in excelExportsDict.items():
        if values.started==True and values.stopped==False:
            failedRequestKeys.append(values.requestKey)
            print values.items()
    return failedRequestKeys

def printFailedJobsFound(failedRequestKeys,excelExportsDict):

    if len(failedRequestKeys) > 0:
        print "The following Excel export Jobs have failed to stop:"
        for failedRequest in failedRequestKeys:
            print "Log File <<"+ excelExportsDict[failedRequest].logFile+ ">> Job ID <<" +excelExportsDict[failedRequest].requestKey + ">> started at <<" +excelExportsDict[failedRequest].date+ " " +excelExportsDict[failedRequest].time + ">> -- " + '[%s]' % ', '.join(map(str, excelExportsDict[failedRequest].msgInfo))

def main():
    logDirectoryPath=setDirectory("logs")
    logFiles=getLogsFiles()
    excelExports={}
    for log in logFiles:
        getExcelExportsLines(log,excelExports)
    failedRequest=getUnfinishedExports(excelExports)
    printFailedJobsFound(failedRequest,excelExports)

if __name__ == '__main__':
    main()
