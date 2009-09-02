#!/usr/bin/env python2.5
import os
import sys
import crypt
import string
import cgi
import Cookie
import xmlrpclib
import cgitb
cgitb.enable()

salt = 'ab'
max_age = 30*60 # 30 minutes maximum age
relative_path = '/~james'

# Get variables from request
form = cgi.FieldStorage()
name = form.getvalue('username')
pln_password = form.getvalue('password')
password = crypt.crypt(pln_password,salt)

auth = xmlrpclib.ServerProxy('https://localhost:8082/auth')
res = auth.validateUser(name, password)
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
