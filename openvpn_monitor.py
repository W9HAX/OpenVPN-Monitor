#!/usr/bin/python
#OpenVPN Alert Generator - A @W9HAX production in conjuction with @curi0usjack

import sys
import datetime
import socket,re
from smtplib import SMTP
# add this to crontab:
#*/5 *    * * *  /usr/bin/python /etc/openvpn/openvpn_status.py
ignorefile = "/var/log/vpnignoreusers.txt"
entryfile = "/var/log/vpnactivity.log"
global constatus
s = socket.socket()
server_address = ('localhost', 1196)
s.connect(server_address)
s.send("status 2\r\n")
vpndata = s.recv(4096)
#print vpndata
s.close()
date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
def sendmail( userid, ip, vpnip, vpndate, constatus, connected):
    smtp = SMTP()
    smtp.set_debuglevel(1)
    smtp.connect('MAIL_SERVER_IP', 587)
    #smtp.login('USERNAME@DOMAIN', 'PASSWORD')
    from_addr = "Sender-EMAIL-HERE"
    to_addr = "Recipent-EMAIL-HERE"
    subj = "VPN01 - A VPN Client has been Detected"
    strmessage_text = """
A new VPN Client has been detected:
    
UserID:		%s
IP: 		%s
VPN IP:		%s
Date: 		%s
Information: 	%s

Verbose OpenVPN Status (Connected Clients):

%s
    """
    message = strmessage_text % ( userid, ip, vpnip, vpndate, constatus, connected)
    
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s"  % ( from_addr, to_addr, subj, vpndate, message )
    smtp.sendmail(from_addr, to_addr, msg)
    print "Message successfully sent"
    smtp.quit()
def checkuser( userid, ip, vpndate):
    ignore = open(ignorefile, "r")
    if userid in ignore.read():
        print "{0} shall be ignored. User was found in the ignore file.".format(userid)
        return True
    else:
        #if user is in vpnactivity log return true, else add to file and return false
        checkuser = open(entryfile, "r")
        checkdate = open(entryfile, "r")
        if userid in checkuser.read():
            print "{0} will be ignored. User in entry log already.".format(userid)
            if vpndate in checkdate.read():
                print "{0} will be ignored. Established connection exists.".format(userid)
                return True
            else:
                entry = open(entryfile, "a")
                entry.write("{0} - UserID: {1}. IP Address: {2}\n".format(vpndate, userid, ip))
                global constatus
                constatus = "Existing connection - Client Re-established"
                return False
        else:
            entry = open(entryfile, "a")  
            entry.write("{0} - UserID: {1}. IP Address: {2}\n".format(vpndate, userid, ip))
            global constatus
            constatus = "This is a new connection"
            return False
    
connected = vpndata.split("\r\n")         
for x in vpndata.split('\n'):
    if x.find("CLIENT_LIST") != -1 and x.find("HEADER") == -1:
        splstr = x.split(',')
        userid = splstr[1]
        ip = splstr[2]
        vpnip = splstr[3]
        vpndate = splstr[6]
        if checkuser(userid, ip, vpndate) == False:
            sendmail( userid, ip, vpnip, vpndate, constatus, connected)
