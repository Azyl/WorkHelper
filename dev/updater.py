#!/usr/bin/env python
'''
Created on Jan 29, 2014

@author: EVR6486
'''



import sys, os, re, ftplib
import hashlib
from optparse import OptionParser

#config = os.path.expanduser('~/.nftprc')
config = os.path.expanduser('./updater.config')
r_field = re.compile(r'(?s)([^\n:]+): (.*?)(?=\n[^ \t]|\Z)')

def getConfig(name=None):
    # Find the config file
    home = os.path.expanduser('~/')
    nftp_conf = os.getenv('NFTP_CONF')
    if nftp_conf is not None: 
        s = open(config).read()
    elif os.path.exists(config): 
        s = open(config).read()
    elif os.path.exists('.nftprc'): 
        s = open('.nftprc').read()
    elif os.path.exists('nftp.conf'): 
        s = open('nftp.conf').read()
    elif os.path.exists(home + 'nftp.conf'): 
        s = open(home + 'nftp.conf').read()
    else:
        return {}
    conf = {}
    s = s.replace('\r\n', '\n')
    s = s.replace('\r', '\n')
    for item in s.split('\n\n'): 
        meta = dict(r_field.findall(item.strip()))
        if meta.has_key('name'): 
            fname = meta['name']
            del meta['name']
            conf[fname] = meta
        else: raise 'ConfigError', 'Must include a name'

    if name is not None: 
        return conf[name]
    else: return conf

def getFtp(meta): 
    ftp = ftplib.FTP(meta['host'], meta['username'], meta['password'])
    print 'Changing remote dir (ftp) to: ' + meta['remotedir']
    ftp.cwd(meta['remotedir'])
    return ftp

def getMD5(file):
    hash = hashlib.md5(file.read()).hexdigest()
    return hash

def checkDirectory(meta):
    ftp=getFtp(meta)
    #files = ftp.dir()
    #print files
    
    filelist=ftp.nlst()
    print "files in the remote folder: "
    for file in filelist:
        print "    "+file
        print "checking if the file exists in the localdirectory:"
        try:
            with open(meta['localdir']+'\\' +file) as f:
                
                localMD5 = getMD5(f)
                print ('file '+file+' exists locally')
                print '    local file MD5:  '+localMD5
                filetmp = open(meta['localdir']+'\\' + file + '.tmp', 'wb')
                ftp.retrbinary('RETR '+meta['remotedir']+'/' + file, filetmp.write);
                filetmp.close()
                filex=open(meta['localdir']+'\\' + file + '.tmp', 'r')
                remoteMD5 = getMD5(filex)
                filex.close()
                print '    remote file MD5: '+remoteMD5
                if localMD5==remoteMD5:
                    print 'file '+file+' is up to date'
                    os.remove(meta['localdir']+'\\' + file + '.tmp')
                else:
                    os.remove(meta['localdir']+'\\' + file)
                    os.rename(meta['localdir']+'\\' + file + '.tmp', meta['localdir']+'\\' + file)
        except IOError:
            print 'file ' +file+' does not exist locally'
            filetmp = open(meta['localdir']+'\\' + file, 'wb')
            ftp.retrbinary('RETR '+meta['remotedir']+'/' + file, filetmp.write);
            filetmp.close()
            print 'file '+file+ ' downloaded'
        
        
        
        
     
   
    

def getFile(meta,filename,tmp):
    ftp=getFtp(meta)
    file = open(meta['localdir']+'\\' + filename + tmp, 'wb')
    print 'Opening local file ' 
    ftp.retrbinary('RETR '+meta['remotedir']+'/' + filename, file.write);
    print 'Closing file ' + filename
    ftp.quit()

def main(argv=None):
    #meta={'host':'ftp.crisoft.ro','username':'lemet','password':'lemetftp1','remotedir':'/HealthCheck/updater'}
    #meta={'host':['ftp.crisoft.ro'],'username':['lemet'],'password':['lemetftp1'],'remotedir':['/HealthCheck/updater']}
    
    #getFtp(meta)
    #get('Install.sql','/HealthCheck/updater')
    
    #meta = getConfig('example')
    
    meta=getConfig()
    print "the following directories have been configured:"
    for key in meta:
        print " -- " + key
        for k,v in meta[key].iteritems():
            print k+":"+v
    
    for key in meta:
        print " ++ " + key
        #getFile(meta[key],'Install.sql')
        checkDirectory(meta[key])
        
        
        
    #print meta
    #getFtp(meta['example'])
    #get('example','/HealthCheck/updater')

if __name__=="__main__": 
    main()
