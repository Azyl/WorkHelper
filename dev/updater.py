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

        # logging:
        self.lgr = logging.getLogger('updater')
        self.lgr.setLevel(logging.DEBUG)
        # fh = logging.FileHandler('./myapp.log')
        self.fh = logging.StreamHandler()
        self.fh.setLevel(logging.DEBUG)
        frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(frmt)
        self.lgr.addHandler(self.fh)

        # config:
        self.meta = self.getConfig()

    def getConfig(self, name = None):

        # config = os.path.expanduser('~/.nftprc')
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


        # header = self.checkHeader(config)
        # for i in header:
            # print i

        s = s.splitlines(True)
        s = s[6:]


        s = ''.join(s)

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

    def checkVHeader(self, textFile):
        for line in textFile:
            if 'REM @(#)' in line:
                yield line

    def checkHeader(self, textFile):
        header = self.checkVHeader(textFile)
        revision = ''
        date = ''
        author = ''
        for line in list(header):
            if '$Revision:' in line:
                revision = line.replace('REM @(#)', '').replace('$', '').replace('Revision:', '').replace('\n', '').replace('  ', '').replace(' ', '').strip()
                # self.lgr.debug(revision)
            elif '$Date:' in line:
                date = line.replace('REM @(#)', '').replace('$', '').replace('Date:', '').replace('\n', '').replace('  ', '').replace(' ', '').strip()
                # self.lgr.debug(date)
            elif '$Author:' in line:
                author = line.replace('REM @(#)', '').replace('$', '').replace('Author:', '').replace('\n', '').replace('  ', '').replace(' ', '').strip()
                # self.lgr.debug(author)
        return {'revision':revision, 'date':date, 'author':author}




    def getFtp(self, meta):
        ftp = ftplib.FTP(meta['host'], meta['username'], meta['password'])
        ftp.sendcmd("TYPE i")  # Switch to Binary mode
        self.lgr.info('Changing remote dir (ftp) to: ' + meta['remotedir'])
        ftp.cwd(meta['remotedir'])
        return ftp

    def getMD5(self, file):
        hash = hashlib.md5(file.read()).hexdigest()
        return hash

    def is_file(self, ftp, filename):
        ftp.sendcmd("TYPE i")  # Switch to Binary mode
        try:
            ftp.size(filename) is not None
            return True
        except ftplib.error_perm:
            return False

    def checkDirectory(self, meta):
        ftp = self.getFtp(meta)
        # files = ftp.dir()
        # print files

        filelist = ftp.nlst()
        self.lgr.info('files in the remote folder: ')
        for file in filelist:
            if self.is_file(ftp, file):
                self.lgr.info('    ' + file)
                self.lgr.info('checking if the file exists in the localdirectory:')
                try:
                    with open(meta['localdir'] + self.osPathDelim() + file) as f:
                        last_pos = f.tell()
                        localMD5 = self.getMD5(f)
                        f.seek(last_pos)
                        localVheader = self.checkHeader(f)
                        self.lgr.info('file ' + file + ' exists locally')
                        self.lgr.info('    local file MD5:  ' + localMD5)
                        filetmp = open(meta['localdir'] + self.osPathDelim() + file + '.tmp', 'wb')
                        ftp.retrbinary('RETR ' + meta['remotedir'] + '/' + file, filetmp.write);
                        filetmp.close()
                        filex = open(meta['localdir'] + self.osPathDelim() + file + '.tmp', 'r')
                        last_pos = filex.tell()
                        remoteMD5 = self.getMD5(filex)
                        filex.seek(last_pos)
                        remoteVheader = self.checkHeader(filex)
                        filex.close()
                        self.lgr.info('    remote file MD5: ' + remoteMD5)
                        f.close()
                        if localMD5 == remoteMD5:
                            self.lgr.info('file ' + file + ' is up to date')
                            os.remove(meta['localdir'] + self.osPathDelim() + file + '.tmp')
                        else:
                            self.lgr.info('!! files do not match -- checking the version number from the header of the file')
                            self.lgr.debug('localfile vheader ' + ''.join(localVheader['revision']))
                            self.lgr.debug('remotefile vheader ' + ''.join(remoteVheader['revision']))

                            doUpdate = False
                            rValid = False
                            lVaild = False

                            try:
                                int(remoteVheader['revision'])
                                rValid = True
                            except ValueError:
                                self.lgr.debug('remoteVheader is not a valid number or is missing ' + remoteVheader['revision'])

                            try:
                                int(localVheader['revision'])
                                rValid = True
                            except ValueError:
                                self.lgr.debug('localVheader is not a valid number or is missing ' + localVheader['revision'])

                            if rValid and lVaild:
                                if int(remoteVheader['revision']) > int(localVheader['revision']):
                                    doUpdate = True
                            elif rValid and not lVaild:
                                doUpdate = True
                            else:
                                self.lgr.debug('remote file version cannot be determined not updating the local file')


                            if doUpdate == True:
                                os.remove(meta['localdir'] + self.osPathDelim() + file)
                                os.rename(meta['localdir'] + self.osPathDelim() + file + '.tmp', meta['localdir'] + '\\' + file)
                                self.lgr.debug('local file updated')

                except IOError:
                    self.lgr.info('file ' + file + ' does not exist locally')
                    filetmp = open(meta['localdir'] + self.osPathDelim() + file, 'wb')
                    ftp.retrbinary('RETR ' + meta['remotedir'] + '/' + file, filetmp.write);
                    filetmp.close()
                    self.lgr.info('file ' + file + ' downloaded')
            else:
                self.lgr.info('Changing remote dir (ftp) to: ' + meta['remotedir'] + '/' + file)
                ftp.cwd(meta['remotedir'] + '/' + file)
                self.lgr.info('Checking if the local folder exists: ' + meta['localdir'] + self.osPathDelim() + file)
                self.ensure_dir(meta['localdir'] + self.osPathDelim() + file)
                meta1 = meta.copy()
                meta1['remotedir'] = meta['remotedir'] + '/' + file
                meta1['localdir'] = meta['localdir'] + self.osPathDelim() + file
                self.checkDirectory(meta1)

    def osPathDelim(self):
        if os.name in ('posix', 'mac', 'os2', 'ce', 'java', 'riscos'):
            return '/'
        else:
            return '\\'  # 'nt'

    def ensure_dir(self, folder):
        # directory = os.path.dirname(folder)
        self.lgr.debug('Path:  ' + folder)
        if not os.path.exists(folder):
            os.makedirs(folder)
            self.lgr.info('local directory does not exist, created : ' + folder)

    def getFile(self, meta, filename, tmp):
        ftp = self.getFtp(meta)
        file = open(meta['localdir'] + self.osPathDelim() + filename + tmp, 'wb')
        print 'Opening local file '
        ftp.retrbinary('RETR ' + meta['remotedir'] + '/' + filename, file.write);
        print 'Closing file ' + filename
        # file.close()
        ftp.quit()

def main(argv = None):

    Refresher = updater()
    Refresher.lgr.info('the following directories have been configured:')
    for key in Refresher.meta:
        Refresher.lgr.info(" -- " + key)
        for k, v in Refresher.meta[key].iteritems():
            Refresher.lgr.info(k + ":" + v)


    for key in Refresher.meta:
        Refresher.lgr.info(" ++ " + key)
        if key <> 'main':
            Refresher.checkDirectory(Refresher.meta[key])


if __name__ == "__main__":
    main()
