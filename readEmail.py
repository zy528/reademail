#-*- encoding: utf-8 -*-
import imaplib
import email
import datetime,time
import re
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_DIR = BASE_DIR + '/file'

PORT_ID = 'port'
HOST_NAME = 'host'
USER = 'user'
PASSWORD = 'password'
TODAY = datetime.date.today()

def getemail(portid = None, hostname = None,user = None,password = None):
    if portid == None:
        portid = PORT_ID
    if hostname == None:
        hostname = HOST_NAME
    if user == None:
        user = USER
    if password == None:
        password = PASSWORD
    conn = imaplib.IMAP4_SSL(port=portid, host=hostname)
    filename = ''
    try:
        conn.login(user, password)
    except:
        print 'login failed'
    conn.select("INBOX")
    type, data = conn.search(None, '(UNSEEN)')
    msgList = data[0].split()
    size = len(msgList)
    msg1 = ''
    fromemail = 'mickeyliu@easyhin.com'
    if size > 0:
        for i in range(size):
            type1, data1 = conn.fetch(msgList[size - (i + 1)], '(RFC822)')
            msg = email.message_from_string(data1[0][1])
            codemsg = email.Header.decode_header(msg['From'])[0][0]
            if re.findall(r"<(.+?)>", codemsg)[0] == fromemail:
                msg1 = msg
                break

    if msg1 != '':
        for part in msg1.walk():
            if not part.is_multipart():
                filename = part.get_filename()
                charset = part.get_charset()
                if filename:
                    h = email.Header.Header(filename)
                    dh = email.Header.decode_header(h)
                    fname = dh[0][0]
                    encodeStr = dh[0][1]
                    if encodeStr != None:
                        if charset == None:
                            fname = fname.decode(encodeStr, 'gbk')
                        else:
                            fname = fname.decode(encodeStr, charset)
                    if fname:
                        try:
                            data = part.get_payload(decode=True)
                            sfname = str(TODAY) + '_' + fname
                            dstdir = FILE_DIR + "/" + sfname
                            f = open(dstdir, 'wb')
                            f.write(data)
                            f.close()
                            filename = sfname
                        except:
                            print 'save failed'
    conn.close()
    conn.logout()
    return filename

if __name__ == "__main__":
   print getemail(PORT_ID,HOST_NAME,USER,PASSWORD)