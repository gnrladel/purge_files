#!/usr/bin/env python
import sys
import os
import re
import datetime
import logging
import shutil
import xmltodict
import gzip
try:
   import xml.etree.ElementTree as ET
except ImportError:
    sys.exit("Module ElementTree is not installed")

sys.tracebacklimit = 0
ConfigFile='/home/gnrladel/gnrladel_purge_script/ocpurge_logs.cfg.xml'
logging.basicConfig(filename='/tmp/file.log',level=logging.DEBUG, format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
try:
    tree = ET.parse(ConfigFile)
except IOError:
    logging.error('Xml config file does not exist')
    sys.exit("Xml config file does not exist")
except:
    logging.error('Xml config file is invalid')
    sys.exit("Xml config file is invalid")


with open(ConfigFile) as xml:
    dictionary = xmltodict.parse(xml.read())
    logging.debug('xml file converted correctly to dictionary')

def GetConfigParams(param):
        path = dictionary['FilesConfig']['Types']['Type'][param]['LocalDir']
        filename = dictionary['FilesConfig']['Types']['Type'][param]['FileNameRegEx']
        recuflags = dictionary['FilesConfig']['Types']['Type'][param]['RecursiveFlag']
        leavefiles = dictionary['FilesConfig']['Types']['Type'][param]['LeaveLastFilesNum']
        compression = dictionary['FilesConfig']['Types']['Type'][param]['Compression']
        if compression['@enable'] == '1':
            skipcompressionfile = compression['SkipCompressFiles']
            return path, filename, recuflags, leavefiles, compression['SkipCompressFiles']

        else:
            return path, filename, recuflags, leavefiles

def compress(log_path):
    with open(log_path, 'rb') as f_in, gzip.open(log_path+'.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(log_path)

def check_regex(file):
    return re.match(GetConfigParams(i)[1], file)

def purge_files(path,file):
    return os.path.join(path, os.path.basename(file.pop(0)))

def uncompress(file):
    return os.path.join(GetConfigParams(i)[0], os.path.basename(file.pop(0)))

def list_files(path):
    files=[]
    for  root, directories, filenames in os.walk(path):
        file = [ filename for filename in filenames]
        return file

def list_dirs(path):
    for  root, directories, filenames in os.walk(path):
        directory = [directoryname for directoryname in directories]
        return directory

def purge_main():
    path = os.path.join(GetConfigParams(i)[0])
    try:
        uncomp_files=GetConfigParams(i)[4]
        files = sorted(list_files(path))
        for file in files[:-int(uncomp_files)]:
            if check_regex(file):
                log_path=os.path.join(path, os.path.basename(file))
                compress(log_path)
                logging.info('{} compressed'.format(file))
            else:
                logging.debug('file {} not compatible with configured regular expression'.format(file))
        if int(GetConfigParams(i)[3]) < 0:
            logging.error("Invalid parameter 'LeaveLastFilesNum={}', it must be a positive number".format(int(GetConfigParams(i)[3])))
            sys.exit("Invalid parameter 'LeaveLastFilesNum={}', it must be a positive number".format(int(GetConfigParams(i)[3])))
        elif int(GetConfigParams(i)[3]) < len(files):
            for num in range(len(files) - int(GetConfigParams(i)[3])):
                files2 = sorted(list_files(path))[:-int(uncomp_files)]
                os.remove(purge_files(path,files2))

    except IndexError:
        files = sorted(list_files(path))
        if int(GetConfigParams(i)[3]) < len(files):
            for num in range(len(files) - int(GetConfigParams(i)[3])):
                os.remove(purge_files(path,files))
                logging.info('outdated file {} deleted'.format(purge_files(path,file)))

def purge_recursive():
    dirs = list_dirs(GetConfigParams(i)[0])
    for Dir in dirs:
        path = os.path.join(GetConfigParams(i)[0], os.path.basename(Dir))
        try:
            uncomp_files=GetConfigParams(i)[4]
            files = sorted(list_files(path))
            for file in files[:-int(uncomp_files)]:
                if check_regex(file):
                    log_path=os.path.join(path, os.path.basename(file))
                    compress(log_path)
                    logging.info('{} compressed'.format(file))
                else:
                    logging.debug('file {} not compatible with configured regular expression'.format(file))
            if int(GetConfigParams(i)[3]) < 0:
                logging.error("Invalid parameter 'LeaveLastFilesNum={}', it must be a positive number".format(int(GetConfigParams(i)[3])))
                sys.exit("Invalid parameter 'LeaveLastFilesNum={}', it must be a positive number".format(int(GetConfigParams(i)[3])))
            elif int(GetConfigParams(i)[3]) < len(files):
                for num in range(len(files) - int(GetConfigParams(i)[3])):
                    files2 = sorted(list_files(path))
                    os.remove(purge_files(path,files2))
                    logging.info('outdated file {} deleted'.format(purge_files(path,file)))
        except IndexError:
            files = sorted(list_files(path))
            if int(GetConfigParams(i)[3]) < len(files):
                for num in range(len(files) - int(GetConfigParams(i)[3])):
                    os.remove(purge_files(path,files))
                    logging.info('outdated file {} deleted'.format(purge_files(path,file)))

if __name__ == '__main__':
    for i in range(len(dictionary['FilesConfig']['Types']['Type'])):
        if GetConfigParams(i)[2]=='0':
            purge_main()
        elif GetConfigParams(i)[2]=='1':
            purge_main()
            purge_recursive()
        else:
            logging.error("Invalid parameter 'RecursiveFlag={}', it must be '0' or '1'".format(GetConfigParams(i)[3]))
            sys.exit("Invalid parameter 'RecursiveFlag={}', it must be '0' or '1'".format(GetConfigParams(i)[3]))
