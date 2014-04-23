'''
Created on Apr 15, 2014

@author: azyl
'''

from bs4 import BeautifulSoup
import datetime
import logging
import glob

IMPORT_dir='./'
EXPORT_dir='./output/'
FILE_extension='.lst'


def table1(Startdate,hostname,tablestr):
    rows = tablestr.findAll(lambda tag: tag.name=='tr')
    r={}
    ReportStatus=0
    for row in rows:
        if row.contents[7].name <> 'th':
            respct = float(str(row.contents[7].string).strip())/float(str(row.contents[9].string).strip())
            #print "%.2f" % (respct)
            if respct > 0.95:
                ReportStatus=2
            elif respct > 0.85:
                ReportStatus=1
            
            rep={}
            rep[row.contents[1].string]=respct
            r.update(rep)
    
    if ReportStatus==0:                     
        print "UPDATE dailyreport set T1SESsIONS=%d, T1PROCESSES=%d, T1LOCKS=%d, T1MAXROLLBACK=%d WHERE Repdate = '%s';" % (r['sessions'],r['processes'],r['enqueue_locks'],r['max_rollback_segments'],Startdate)
    else:
        print "UPDATE dailyreport set T1SESsIONS=%d, T1PROCESSES=%d, T1LOCKS=%d, T1MAXROLLBACK=%d, REPORTSTATUS=%s WHERE Repdate = '%s';" % (r['sessions'],r['processes'],r['enqueue_locks'],r['max_rollback_segments'],ReportStatus,Startdate)

def table2(Startdate,hostname,tablestr):

        # table 2 
        t2 = tablestr
        #print 't2 --> '+str(t2)
        over10=0
        maxval=0
        rows = t2.findAll(lambda tag: tag.name=='tr')
        #r={}
        ReportStatus=0
        for row in rows:
            if row.contents[7].name <> 'th':
                #print row.contents[7].name
                #print row.contents[7].string
                if float(row.contents[7].string)>0:
                    over10=over10+1
                if float(row.contents[7].string)>maxval:
                    maxval=float(row.contents[7].string)
                
        if maxval>10:
            ReportStatus=1
            print "UPDATE dailyreport set T2OVER10MIN=%d, T2MAX=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (over10,maxval,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T2OVER10MIN=%d, T2MAX=%s WHERE Repdate = '%s';" % (over10,maxval,Startdate)
       

def table3(Startdate,hostname,tablestr):
    # table 3 
    t3 = tablestr
    #print t3
    over10=0
    maxval=0
    rows = t3.findAll(lambda tag: tag.name=='tr')
    #r={}
    ReportStatus=0
    for row in rows:
        if row.contents[7].name <> 'th':
            #print row.contents[15].name
            #print row.contents[15].string
            try:
                if float(row.contents[15].string)>0:
                    over10=over10+1
                if float(row.contents[15].string)>maxval:
                    maxval=float(row.contents[15].string)
            except ValueError:
                if float(row.contents[17].string)>0:
                    over10=over10+1
                if float(row.contents[17].string)>maxval:
                    maxval=float(row.contents[17].string)
                
    if maxval>10:
        ReportStatus=1
        print "UPDATE dailyreport set T3OVER10MIN=%d, T3MAX=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (over10,maxval,ReportStatus,Startdate)
    else:
        print "UPDATE dailyreport set T3OVER10MIN=%d, T3MAX=%s WHERE Repdate = '%s';" % (over10,maxval,Startdate)

def table4(Startdate,hostname,tablestr):
    # table 4 
    t4 = tablestr
    #print t4
    over10=0
    maxval=0
    rows = t4.findAll(lambda tag: tag.name=='tr')
    #r={}
    ReportStatus=0
    try:
        for row in rows:
            #print row.contents[11].name
            #print row.contents[11].string
            if row.contents[1].name <> 'th':
                #print row.contents[13].name
                #print row.contents[13].string
                duration2=row.contents[13].string.split(':')[0]
                #print 'duration2 ->' + duration2
                try:
                    t=int(duration2)
                except ValueError:
                    t=duration2.split(' ')[0]
                
                if t>24:
                    over10=over10+1
                if t>maxval:
                    maxval=t
                    
        if maxval>24:
            ReportStatus=1
            print "UPDATE dailyreport set T4OVER1DAY=%d, T4MAX=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (over10,maxval,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T4OVER1DAY=%d, T4MAX=%s WHERE Repdate = '%s';" % (over10,maxval,Startdate)
    except IndexError:
        logging.error("malformed table -> T4")



def table5(Startdate,hostname,tablestr):
    # table 5 
    t5 = tablestr
    #print t5
    rows = t5.findAll(lambda tag: tag.name=='tr')
    countobj=len(rows)-1
    #print countobj
                
    if countobj>0:
        ReportStatus=1
        print "UPDATE dailyreport set T5DEADLOCK=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countobj,ReportStatus,Startdate)
    else:
        print "UPDATE dailyreport set T5DEADLOCK=%s WHERE Repdate = '%s';" % (countobj,Startdate)
        
def table6(Startdate,hostname,tablestr):
    # table 6 
    t6 = tablestr
    #print t6
    count=0
    countSin=0
    countOthers=0
    rows = t6.findAll(lambda tag: tag.name=='tr')
    #r={}
    ReportStatus=0
    for row in rows:
        if row.contents[7].name <> 'th':
            #print row.contents[5].name
            #print row.contents[5].string
            
            if row.contents[5].string=="SYNONYM":
                countSin=countSin+1
            else:
                countOthers=countOthers+1
            count=count+1
            
    if countOthers>0:
        ReportStatus=1
        print "UPDATE dailyreport set T6PUBSYNINVALID=%s, T6USEROBJINVALID=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countSin,countOthers,ReportStatus,Startdate)
    else:
        print "UPDATE dailyreport set T6PUBSYNINVALID=%s, T6USEROBJINVALID=%s WHERE Repdate = '%s';" % (countSin,countOthers,Startdate)

def table7(Startdate,hostname,tablestr):
    # table 7 
    t7 = tablestr
    #print t7
    rows = t7.findAll(lambda tag: tag.name=='tr')
    
    ReportStatus=0
    for row in rows:
        if row.contents[3].name <> 'th':
            #print row.contents[9].name
            #print row.contents[9].string
            
            
            tablespaceName=row.contents[1].string
            try:
                freeperc=float(row.contents[11].string)
            except IndexError:
                freeperc=float(row.contents[9].string)
            if freeperc<15:
                ReportStatus=2
                print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                print "INSERT into dailyreportt7 (CLIENT,DBLINK,REPDATE,TABLESPACENAME,MAXFREEPCT) values (%s,%s,%s,%s,%d);" % (hostname,'dblink',Startdate,tablespaceName,freeperc)
            elif freeperc<20:
                ReportStatus=1
                print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                print "INSERT into dailyreportt7 (CLIENT,DBLINK,REPDATE,TABLESPACENAME,MAXFREEPCT) values (%s,%s,%s,%s,%d);" % (hostname,'dblink',Startdate,tablespaceName,freeperc)
            else:
                print "INSERT into dailyreportt7 (CLIENT,DBLINK,REPDATE,TABLESPACENAME,MAXFREEPCT) values (%s,%s,%s,%s,%d);" % (hostname,'dblink',Startdate,tablespaceName,freeperc)

def table10(Startdate,hostname,tablestr):
    # table 10 
    t10 = tablestr
    #print t5
    rows = t10.findAll(lambda tag: tag.name=='tr')
    countobj=len(rows)-1
    #print countobj
                
    if countobj>0:
        ReportStatus=1
        print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countobj,ReportStatus,Startdate)
    else:
        print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s WHERE Repdate = '%s';" % (countobj,Startdate)

def table11(Startdate,hostname,tablestr):
    # table 11 
    t11 = tablestr
    #print t11
    rows = t11.findAll(lambda tag: tag.name=='tr')
   
    ReportStatus=0
    for row in rows:
        if row.contents[3].name <> 'th':
            #print row.contents[9].name
            #print row.contents[9].string
            
            USERNAME=row.contents[1].string
            try:
                FAILURECOUNT=int(row.contents[7].string)
            except ValueError:
                FAILURECOUNT=int(row.contents[5].string)
            try:
                daterun=datetime.datetime.strptime(row.contents[11].string,'%d-%b-%Y %H:%M')
            except ValueError:
                daterun=datetime.datetime.strptime(row.contents[9].string,'%d-%b-%y')
            datecheck=datetime.datetime.strptime(Startdate,'%d-%b-%y')
            diff=daterun-datecheck
            
            
            #print daterun.strftime('%d-%b-%Y %H:%M')
            #print datecheck.strftime('%d-%b-%Y %H:%M')
            #print diff.days
            
            if diff.days==0:
                STATRUN=1
            else:
                STATRUN=0
            
            if FAILURECOUNT>0 or STATRUN<>1:
                ReportStatus=1
                print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
            print "INSERT into dailyreportt11 (CLIENT,DBLINK,REPDATE,USERNAME,STATRUN,FAILURECOUNT) values (%s,%s,%s,%s,%s,%s);" % (hostname,'dblink',Startdate,USERNAME,STATRUN,FAILURECOUNT)

def table12(Startdate,hostname,tablestr):
    # table 12 
    t12 = tablestr
    #print t12
    rows = t12.findAll(lambda tag: tag.name=='tr')
    countobj=len(rows)-1
    #print countobj
                
    if countobj>0:
        ReportStatus=1
        print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countobj,ReportStatus,Startdate)
    else:
        print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s WHERE Repdate = '%s';" % (countobj,Startdate)
                                           

def table14(Startdate,hostname,tablestr):
    rows = tablestr.findAll(lambda tag: tag.name=='tr')

        
    ReportStatus=0
    for row in rows:
        if row.contents[3].name <> 'th':
            driveName=row.contents[0].string
            drivedescr=row.contents[1].string
            freeperc=float(row.contents[4].string)
            if freeperc<15:
                ReportStatus=2
                print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                print "INSERT into dailyreportt14 (CLIENT,DBLINK,REPDATE,DRIVENAME,DRIVEDESCR,FREEPERC) values (%s,%s,%s,%s,%s,%d) ;" % (hostname,'dblink',Startdate,driveName,drivedescr,freeperc)
            elif freeperc<20:
                ReportStatus=1
                print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                print "INSERT into dailyreportt14 (CLIENT,DBLINK,REPDATE,DRIVENAME,DRIVEDESCR,FREEPERC) values (%s,%s,%s,%s,%s,%d) ;" % (hostname,'dblink',Startdate,driveName,drivedescr,freeperc)
            else:
                print "INSERT into dailyreportt14 (CLIENT,DBLINK,REPDATE,DRIVENAME,DRIVEDESCR,FREEPERC) values (%s,%s,%s,%s,%s,%d) ;" % (hostname,'dblink',Startdate,driveName,drivedescr,freeperc)
                        

def writeFile(fileName,check):
    fo=open(fileName,"w")
    fo.write(check)
    fo.close()

def dataPreprocesing(InputFolder,OutputFolder):
    FILES=glob.glob(InputFolder+"*"+FILE_extension)
    logging.info("Files to be processed: "+', '.join(map(str, FILES)))
    for lstfile in FILES:
        logging.info("Processing file : "+lstfile)
        fo = open(lstfile,"r")
        s = fo.read()
        fo.close()
        array = s.split("<<<<%%%%>>>>")
        i=0
        j=0
        for check in array:
            if 'Health Check on' in check:
                fileName=OutputFolder+str(lstfile).replace(InputFolder,'')+'HC'+str(i)+".html"
                writeFile(fileName=fileName,check=check)
                logging.info('Check html file created -> '+fileName)
                i=i+1
            elif 'Disk Usage Check on' in check:
                fileName=OutputFolder+str(lstfile).replace(InputFolder,'')+'DC'+str(j)+".html"
                writeFile(fileName=fileName,check=check)
                logging.info('Check html file created -> '+fileName)
                j=j+1
            else:
                #logging.warning('Unrecognized check: '+check)
                pass
        logging.info("File "+str(lstfile).replace(InputFolder,'')+" processed")
        
def dataProcesing(InputFolder):
    FILES=glob.glob(InputFolder+"*")
    logging.info("Files to be processed: "+', '.join(map(str, FILES)))
    for lstfile in FILES:
        fileName=str(lstfile).replace(InputFolder,'')
        if 'HC' in fileName:
            logging.info("Processing HealthCheck file : "+fileName)
            parseHealthCheck(file=lstfile)
        elif 'DC' in fileName:
            logging.info("Processing DiskCheck file : "+fileName)
            parseDiskCheck(file=lstfile)



            
def parseDiskCheck(file):
        f = open(file, 'r')
        doc = BeautifulSoup(f.read())
        f.close()
        #print doc
        texts = doc.findAll(text=True)
        #print texts
        hoststring = texts[6].replace('Disk Usage Check on ', '').replace(' at','')
        hostname = hoststring.split(' ')[0]
        #print 'hostname= '+hostname
        Startdate=texts[0]
        #print 'Startdate= '+Startdate
        tables = doc.findAll(lambda tag: tag.name=='table')
        #print tables
        t14 = tables[0]
        
        #
        #
        table14(Startdate=Startdate,hostname=hostname,tablestr=t14)
        
def parseHealthCheck(file):
    f = open(file, 'r')
    doc = BeautifulSoup(f.read())
    f.close()
    #print doc
    texts = doc.findAll(text=True)
    #print texts
    hoststring = texts[6].replace('Disk Usage Check on ', '').replace(' at','')
    hostname = hoststring.split(' ')[0]
    #print 'hostname= '+hostname
    Startdate=texts[0]
    #print 'Startdate= '+Startdate
    tables = doc.findAll(lambda tag: tag.name=='table')
    #print tables
    
    #
    #
    if 'Table 1: Resource usage' in str(tables[0]):
        table1(Startdate=Startdate,hostname=hostname,tablestr=tables[0])
    else:
        logging.error("unknown table -> T1")
    
    if 'Table 2: TOP 10 programs by cpu time' in str(tables[1]):
        table2(Startdate=Startdate,hostname=hostname,tablestr=tables[1])
    else:
        logging.error("unknown table -> T2")
            
    if 'Table 3: TOP 10 long operations' in str(tables[2]):
        table3(Startdate=Startdate,hostname=hostname,tablestr=tables[2])
    else:
        logging.error("unknown table -> T3")
        
    if 'Table 4: TOP 10 IDLE Sesions' in str(tables[4]):
        table4(Startdate=Startdate,hostname=hostname,tablestr=tables[4])
    elif 'Table 4: TOP 10 IDLE Sesions' in str(tables[3]):
        table4(Startdate=Startdate,hostname=hostname,tablestr=tables[3])
    else:       
        logging.error("unknown table -> T4")
        
    
    if 'Table 5: DeadLocks' in str(tables[5]):
        table5(Startdate=Startdate,hostname=hostname,tablestr=tables[5])
    elif 'Table 5: DeadLocks' in str(tables[4]):
        table5(Startdate=Startdate,hostname=hostname,tablestr=tables[4])
    else:       
        logging.error("unknown table -> T5")
       
    if 'Table 6: Invalid Objects' in str(tables[6]):
        table6(Startdate=Startdate,hostname=hostname,tablestr=tables[6])
    elif 'Table 6: Invalid Objects' in str(tables[5]):
        table6(Startdate=Startdate,hostname=hostname,tablestr=tables[5])
    else:       
        logging.error("unknown table -> T6")    
    
    if 'Table 7: Tablespace utilization' in str(tables[7]):
        table7(Startdate=Startdate,hostname=hostname,tablestr=tables[7])
    elif 'Table 7: Tablespace utilization' in str(tables[6]):
        table7(Startdate=Startdate,hostname=hostname,tablestr=tables[6])
    else:       
        logging.error("unknown table -> T7")
        
        
    if 'Table 10: Unextendable Objects' in str(tables[10]):
        table10(Startdate=Startdate,hostname=hostname,tablestr=tables[10])
    elif 'Table 10: Unextendable Objects' in str(tables[9]):
        table10(Startdate=Startdate,hostname=hostname,tablestr=tables[9])
    else:       
        logging.error("unknown table -> T10") 
        
    if 'Table 11: Statistics job Status' in str(tables[11]):
        table11(Startdate=Startdate,hostname=hostname,tablestr=tables[11])
    elif 'Table 11: Statistics job Status' in str(tables[10]):
        table11(Startdate=Startdate,hostname=hostname,tablestr=tables[10])
    else:       
        logging.error("unknown table -> T11")
        
    
    if 'Table 12: RMAN BackUP job Status' in str(tables[12]):
        table12(Startdate=Startdate,hostname=hostname,tablestr=tables[12])
    elif 'Table 12: RMAN BackUP job Status' in str(tables[11]):
        table12(Startdate=Startdate,hostname=hostname,tablestr=tables[11])
    else:       
        logging.error("unknown table -> T12")       
    
    
    
    
def parseFile(File):
        # if URL is not None:
        f = open(File, 'r')
        doc = BeautifulSoup(f.read())
        f.close()
        print doc
        texts = doc.findAll(text=True)
        print texts
        
        hoststring = texts[6].replace('Health Check on ', '').replace(' at','')
        hostname = hoststring.split(' ')[0]
        print hostname
        Startdate=texts[0]

        
        tables = doc.findAll(lambda tag: tag.name=='table')
       
       
        # table 1
        t1 = tables[0]
        rows = t1.findAll(lambda tag: tag.name=='tr')
        r={}
        ReportStatus=0
        for row in rows:
            if row.contents[7].name <> 'th':
                respct = float(str(row.contents[7].string).strip())/float(str(row.contents[9].string).strip())
                #print "%.2f" % (respct)
                if respct > 0.95:
                    ReportStatus=2
                elif respct > 0.85:
                    ReportStatus=1
                
                rep={}
                rep[row.contents[1].string]=respct
                r.update(rep)
        
        if ReportStatus==0:                     
            print "UPDATE dailyreport set T1SESsIONS=%d, T1PROCESSES=%d, T1LOCKS=%d, T1MAXROLLBACK=%d WHERE Repdate = '%s';" % (r['sessions'],r['processes'],r['enqueue_locks'],r['max_rollback_segments'],Startdate)
        else:
            print "UPDATE dailyreport set T1SESsIONS=%d, T1PROCESSES=%d, T1LOCKS=%d, T1MAXROLLBACK=%d, REPORTSTATUS=%s WHERE Repdate = '%s';" % (r['sessions'],r['processes'],r['enqueue_locks'],r['max_rollback_segments'],ReportStatus,Startdate)
            
            
        # table 2 
        t2 = tables[1]

        over10=0
        maxval=0
        rows = t2.findAll(lambda tag: tag.name=='tr')
        #r={}
        ReportStatus=0
        for row in rows:
            if row.contents[7].name <> 'th':
                #print row.contents[7].name
                #print float(row.contents[7].string)
                if float(row.contents[7].string)>0:
                    over10=over10+1
                if float(row.contents[7].string)>maxval:
                    maxval=float(row.contents[7].string)
                
        if maxval>10:
            ReportStatus=1
            print "UPDATE dailyreport set T2OVER10MIN=%d, T2MAX=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (over10,maxval,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T2OVER10MIN=%d, T2MAX=%s WHERE Repdate = '%s';" % (over10,maxval,Startdate)
       
        # table 3 
        t3 = tables[2]
        #print t3
        over10=0
        maxval=0
        rows = t3.findAll(lambda tag: tag.name=='tr')
        #r={}
        ReportStatus=0
        for row in rows:
            if row.contents[7].name <> 'th':
                #print row.contents[15].name
                #print float(row.contents[15].string)
                if float(row.contents[15].string)>0:
                    over10=over10+1
                if float(row.contents[15].string)>maxval:
                    maxval=float(row.contents[15].string)
                    
        if maxval>10:
            ReportStatus=1
            print "UPDATE dailyreport set T3OVER10MIN=%d, T3MAX=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (over10,maxval,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T3OVER10MIN=%d, T3MAX=%s WHERE Repdate = '%s';" % (over10,maxval,Startdate)
        
        
        
        # table 4 
        t4 = tables[4]
        #print t4
        over10=0
        maxval=datetime.timedelta(seconds=0)
        zi=datetime.timedelta(days=1)
        rows = t4.findAll(lambda tag: tag.name=='tr')
        initialTime= datetime.datetime.strptime('00:00:00','%H:%M:%S')
        #r={}
        ReportStatus=0
        for row in rows:
            if row.contents[7].name <> 'th':
                #print row.contents[13].name
                #print row.contents[13].string
                duration = datetime.datetime.strptime(row.contents[13].string,'%H:%M:%S')
                diff  = duration - initialTime
                #print "%.2f" % (diff.seconds/60)
                
                
                
                if diff>zi:
                    over10=over10+1
                if diff>maxval:
                    maxval=diff
                    
        if maxval>zi:
            ReportStatus=1
            print "UPDATE dailyreport set T4OVER1DAY=%d, T4MAX=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (over10,maxval,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T4OVER1DAY=%d, T4MAX=%s WHERE Repdate = '%s';" % (over10,maxval,Startdate)
        
        
        # table 5 
        t5 = tables[5]
        #print t5
        rows = t5.findAll(lambda tag: tag.name=='tr')
        countobj=len(rows)-1
        #print countobj
                    
        if countobj>0:
            ReportStatus=1
            print "UPDATE dailyreport set T5DEADLOCK=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countobj,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T5DEADLOCK=%s WHERE Repdate = '%s';" % (countobj,Startdate)
            
         
        # table 6 
        t6 = tables[6]
        #print t6
        count=0
        countSin=0
        countOthers=0
        rows = t6.findAll(lambda tag: tag.name=='tr')
        #r={}
        ReportStatus=0
        for row in rows:
            if row.contents[7].name <> 'th':
                #print row.contents[5].name
                #print row.contents[5].string
                
                if row.contents[5].string=="SYNONYM":
                    countSin=countSin+1
                else:
                    countOthers=countOthers+1
                count=count+1
                
        if countOthers>0:
            ReportStatus=1
            print "UPDATE dailyreport set T6PUBSYNINVALID=%s, T6USEROBJINVALID=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countSin,countOthers,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T6PUBSYNINVALID=%s, T6USEROBJINVALID=%s WHERE Repdate = '%s';" % (countSin,countOthers,Startdate)
                
                
        # table 7 
        t7 = tables[7]
        rows = t7.findAll(lambda tag: tag.name=='tr')
       
        ReportStatus=0
        for row in rows:
            if row.contents[3].name <> 'th':
                
                tablespaceName=row.contents[1].string
                freeperc=float(row.contents[11].string)
                if freeperc<15:
                    ReportStatus=2
                    print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                    print "INSERT into dailyreportt7 (CLIENT,DBLINK,REPDATE,TABLESPACENAME,MAXFREEPCT) values (%s,%s,%s,%s,%d);" % (hostname,'dblink',Startdate,tablespaceName,freeperc)
                elif freeperc<20:
                    ReportStatus=1
                    print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                    print "INSERT into dailyreportt7 (CLIENT,DBLINK,REPDATE,TABLESPACENAME,MAXFREEPCT) values (%s,%s,%s,%s,%d);" % (hostname,'dblink',Startdate,tablespaceName,freeperc)
                else:
                    print "INSERT into dailyreportt7 (CLIENT,DBLINK,REPDATE,TABLESPACENAME,MAXFREEPCT) values (%s,%s,%s,%s,%d);" % (hostname,'dblink',Startdate,tablespaceName,freeperc)
   


    
        
            
            
        # table 10 
        t10 = tables[10]
        #print t5
        rows = t10.findAll(lambda tag: tag.name=='tr')
        countobj=len(rows)-1
        #print countobj
                    
        if countobj>0:
            ReportStatus=1
            print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countobj,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s WHERE Repdate = '%s';" % (countobj,Startdate)



        
        # table 11 
        t11 = tables[11]
        #print t11
        rows = t11.findAll(lambda tag: tag.name=='tr')
       
        ReportStatus=0
        for row in rows:
            if row.contents[3].name <> 'th':
                USERNAME=row.contents[1].string
                FAILURECOUNT=int(row.contents[7].string)
                daterun=datetime.datetime.strptime(row.contents[11].string,'%d-%b-%Y %H:%M')
                datecheck=datetime.datetime.strptime(Startdate,'%d-%b-%y')
                diff=daterun-datecheck
                
                
                #print daterun.strftime('%d-%b-%Y %H:%M')
                #print datecheck.strftime('%d-%b-%Y %H:%M')
                #print diff.days
                
                if diff.days==0:
                    STATRUN=1
                else:
                    STATRUN=0
                
                if FAILURECOUNT>0 or STATRUN<>1:
                    ReportStatus=1
                    print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                print "INSERT into dailyreportt11 (CLIENT,DBLINK,REPDATE,USERNAME,STATRUN,FAILURECOUNT) values (%s,%s,%s,%s,%s,%s);" % (hostname,'dblink',Startdate,USERNAME,STATRUN,FAILURECOUNT)
                    
               


        # table 12 
        t12 = tables[12]
        #print t12
        rows = t12.findAll(lambda tag: tag.name=='tr')
        countobj=len(rows)-1
        #print countobj
                    
        if countobj>0:
            ReportStatus=1
            print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s, REPORTSTATUS=%s WHERE Repdate = '%s';" % (countobj,ReportStatus,Startdate)
        else:
            print "UPDATE dailyreport set T10UNEXTENDCOUNT=%s WHERE Repdate = '%s';" % (countobj,Startdate)
        






        # table 14 
        t14 = tables[14]
        rows = t14.findAll(lambda tag: tag.name=='tr')

        
        ReportStatus=0
        for row in rows:
            if row.contents[3].name <> 'th':
                driveName=row.contents[0].string
                drivedescr=row.contents[1].string
                freeperc=float(row.contents[4].string)
                if freeperc<15:
                    ReportStatus=2
                    print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                    print "INSERT into dailyreportt14 (CLIENT,DBLINK,REPDATE,DRIVENAME,DRIVEDESCR,FREEPERC) values (%s,%s,%s,%s,%s,%d) ;" % (hostname,'dblink',Startdate,driveName,drivedescr,freeperc)
                elif freeperc<20:
                    ReportStatus=1
                    print "UPDATE dailyreport set REPORTSTATUS=%s WHERE Repdate = '%s';" % (ReportStatus,Startdate)
                    print "INSERT into dailyreportt14 (CLIENT,DBLINK,REPDATE,DRIVENAME,DRIVEDESCR,FREEPERC) values (%s,%s,%s,%s,%s,%d) ;" % (hostname,'dblink',Startdate,driveName,drivedescr,freeperc)
                else:
                    print "INSERT into dailyreportt14 (CLIENT,DBLINK,REPDATE,DRIVENAME,DRIVEDESCR,FREEPERC) values (%s,%s,%s,%s,%s,%d) ;" % (hostname,'dblink',Startdate,driveName,drivedescr,freeperc)
                


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info("Scrape started")
    
    '''
    fo = open("testlemetprod.lst","r")
    s = fo.read()
    fo.close()
    array = s.split("<<<<%%%%>>>>")
    #print array[10]
    #print array[11]
    #print array[12]
    #print array[13]
    i=0
    for check in array:
        #if i%2<>0:
        fo=open("./output/check"+str(i)+".html","w")
        fo.write(check)
        fo.close()
        i=i+1     
    '''
    dataPreprocesing(InputFolder=IMPORT_dir,OutputFolder=EXPORT_dir)
    dataProcesing(InputFolder=EXPORT_dir)
    
    #parseURL(URL='./output/check335.html')
