#!/usr/bin/env python
'''
Created on Jan 29, 2014

@author: EVR6486
'''


import sys, os, re, ftplib
import hashlib
import logging
from optparse import OptionParser




class updater():
    def __init__(self):
        
        #logging:
        self.lgr = logging.getLogger('updater')
        self.lgr.setLevel(logging.DEBUG)
        #fh = logging.FileHandler('./myapp.log')
        self.fh = logging.StreamHandler()
        self.fh.setLevel(logging.DEBUG)
        frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(frmt)
        self.lgr.addHandler(self.fh)
     
        #config:
        self.meta=self.getConfig()
    
    def getConfig(self,name=None):
        
        #config = os.path.expanduser('~/.nftprc')
        config = os.path.expanduser('./updater.config')
        r_field = re.compile(r'(?s)([^\n:]+): (.*?)(?=\n[^ \t]|\Z)')
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
            else:
                raise 'ConfigError', 'Must include a name'
                self.lgr.error('Config error, Config file does not conatin a name field')
        if name is not None: 
            return conf[name]
        else: return conf

    def getFtp(self,meta): 
        ftp = ftplib.FTP(meta['host'], meta['username'], meta['password'])
        self.lgr.info('Changing remote dir (ftp) to: ' + meta['remotedir'])
        ftp.cwd(meta['remotedir'])
        return ftp        

    def getMD5(self,file):
        hash = hashlib.md5(file.read()).hexdigest()
        return hash

    def checkDirectory(self,meta):
        ftp=self.getFtp(meta)
        #files = ftp.dir()
        #print files
    
        filelist=ftp.nlst()
        self.lgr.info('files in the remote folder: ')
        for file in filelist:
            self.lgr.info('    '+file)
            self.lgr.info('checking if the file exists in the localdirectory:')
            try:
                with open(meta['localdir']+'\\' +file) as f:
                    localMD5 = self.getMD5(f)
                    self.lgr.info('file '+file+' exists locally')
                    self.lgr.info('    local file MD5:  '+localMD5)
                    filetmp = open(meta['localdir']+'\\' + file + '.tmp', 'wb')
                    ftp.retrbinary('RETR '+meta['remotedir']+'/' + file, filetmp.write);
                    filetmp.close()
                    filex=open(meta['localdir']+'\\' + file + '.tmp', 'r')
                    remoteMD5 = self.getMD5(filex)
                    filex.close()
                    self.lgr.info('    remote file MD5: '+remoteMD5)
                    if localMD5==remoteMD5:
                        self.lgr.info('file '+file+' is up to date')
                        os.remove(meta['localdir']+'\\' + file + '.tmp')
                    else:
                        os.remove(meta['localdir']+'\\' + file)
                        os.rename(meta['localdir']+'\\' + file + '.tmp', meta['localdir']+'\\' + file)
            except IOError:
                self.lgr.info('file ' +file+' does not exist locally')
                filetmp = open(meta['localdir']+'\\' + file, 'wb')
                ftp.retrbinary('RETR '+meta['remotedir']+'/' + file, filetmp.write);
                filetmp.close()
                self.lgr.info('file '+file+ ' downloaded')

        
    def getFile(self,meta,filename,tmp):
        ftp=self.getFtp(meta)
        file = open(meta['localdir']+'\\' + filename + tmp, 'wb')
        print 'Opening local file ' 
        ftp.retrbinary('RETR '+meta['remotedir']+'/' + filename, file.write);
        print 'Closing file ' + filename
        ftp.quit()

def main(argv=None):

    Refresher = updater()
    Refresher.lgr.info('the following directories have been configured:')
    for key in Refresher.meta:
        Refresher.lgr.info(" -- " + key)
        for k,v in Refresher.meta[key].iteritems():
            Refresher.lgr.info(k+":"+v)

    
    for key in Refresher.meta:
        Refresher.lgr.info(" ++ " + key)
        Refresher.checkDirectory(Refresher.meta[key])


if __name__=="__main__": 
    main()
