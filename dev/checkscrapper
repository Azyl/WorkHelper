'''
Created on Apr 15, 2014

@author: azyl
'''

from bs4 import BeautifulSoup
import datetime
import logging



def parseURL(URL):
        # if URL is not None:
        f = open(URL, 'r')
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
    parseURL(URL='./output/check335.html')
