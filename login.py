#!/usr/bin/python
import os, sys
import crypt, string
import cgi
import cgitb; cgitb.enable()
import Cookie

salt = 'ab'
max_age = 30*60 # 30 minutes maximum age
relative_path = '/~james'

# Get variables from request
form = cgi.FieldStorage()
name = form.getvalue('username')
pln_password = form.getvalue('password')
password = crypt.crypt(pln_password,salt)

loggedinCookie = Cookie.SimpleCookie()
loggedinCookie['username'] = name
loggedinCookie['username']['max-age'] = max_age
loggedinCookie['username']['path'] = relative_path
# Session ID
x = []
while len(x) < 20:
    y = os.urandom(1) 
    if y in (string.letters+string.digits):
        x += y
sid = ''.join(x)
loggedinCookie['sid'] = sid
loggedinCookie['sid']['max-age'] = max_age
loggedinCookie['sid']['path'] = relative_path

print 'Status: 302 Moved Temporarily'
print loggedinCookie
print "Location: ../testing/test1.php"
print
