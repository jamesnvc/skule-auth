#!/usr/bin/env python2.6
import os
import sys
import crypt
import string
import cgi
import Cookie
import xmlrpclib
import cgitb
cgitb.enable()
# Configuration values
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('server_settings.conf')
timeout = config.getfloat('Server Settings', 'cookie_timeout_minutes') * 60
listen_port = config.getint('Server Settings', 'rpc_listen_port')
cookie_path = config.get('Server Settings', 'cookie_path')

salt = 'ab'
max_age = timeout
relative_path = cookie_path

# Get variables from request
form = cgi.FieldStorage()
name = form.getvalue('username')
pln_password = form.getvalue('password')

auth = xmlrpclib.ServerProxy('https://localhost:%d/auth' % listen_port)
res = auth.validateUser(name, pln_password)
if not res:
    print 'Status: 302 Moved Temporarily'
    print "Location: ../testing/test1.php"
    print
    exit
    
uid, sid = res    

loggedinCookie = Cookie.SimpleCookie()
loggedinCookie['username'] = name
loggedinCookie['username']['max-age'] = max_age
loggedinCookie['username']['path'] = relative_path

loggedinCookie['sid'] = sid
loggedinCookie['sid']['max-age'] = max_age
loggedinCookie['sid']['path'] = relative_path

loggedinCookie['uid'] = uid
loggedinCookie['uid']['max-age'] = max_age
loggedinCookie['uid']['path'] = relative_path

print 'Status: 302 Moved Temporarily'
print loggedinCookie
print "Location: ../testing/test1.php"
print
