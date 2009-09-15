#!/usr/bin/env python2.6
# Add a new user
import xmlrpclib
import cgi
import cgitb
import crypt
cgitb.enable()

# Configuration values
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('server_settings.conf')
listen_port = config.getint('Server Settings', 'rpc_listen_port')

form = cgi.FieldStorage()
uname = form.getvalue('create_name')
passwd = form.getvalue('create_password')
passwd2 = form.getvalue('verify_password')
if passwd == passwd2:
    hsh_pw = crypt.crypt(passwd, 'ab')
else:
    print 'Content-type: text/html'
    print
    print '<html><head><title>User exists checking</title></head>'
    print '<body>'
    print '<p>Passwords don\'t match</p>'
    print '</body></html>'   
    
fname = form.getvalue('fname')
lname = form.getvalue('lname')

auth = xmlrpclib.ServerProxy('https://localhost:8082/auth')
res = auth.userExists(uname)

if not res:
    added = auth.createUser(uname, hsh_pw, fname, lname)

print 'Content-type: text/html'
print
print '<html><head><title>User exists checking</title></head>'
print '<body>'
if res:
    print '<p>User already exsits</p>'
elif added:
    print '<p>Successfully added %s %s (%s)</p>' % (fname, lname, uname)
else:
    print '<p>Something went wrong there: userExists returned '+ str(added)  +'</p>'
print '</body></html>'   
