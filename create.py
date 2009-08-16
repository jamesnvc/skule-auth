# Add a new user
import xmlrpclib
import cgi
import cgitb
import crypt
cgitb.enable()

form = cgi.FieldStorage()
uname = form.getvalue('create_name')
passwd = form.getvalue('create_password')
hsh_pw = crypt.crypt(passwd, 'ab')
fname = form.getvalue('fname')
lname = form.getvalue('lname')

auth = xmlrpclib.ServerProxy('http://localhost:8082/auth')
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
    print '<p>Something went wrong there...</p>'
print '</body></html>'   
