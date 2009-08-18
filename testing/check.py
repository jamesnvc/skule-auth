#!/usr/bin/env python2.5
import xmlrpclib
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
name = form.getvalue('new_username')

auth = xmlrpclib.ServerProxy('https://localhost:8082/auth')
res = auth.userExists(name)

print 'Content-type: text/html'
print
print '<html><head><title>User exists checking</title></head>'
print '<body>'
if res:
    print "<p>User exists: uid = %d</p>" % res
else:
    print '<p>No user by that name</p>'
print '</body></html>'
