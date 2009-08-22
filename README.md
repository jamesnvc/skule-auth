README
==============

This is the authentication backend that will be used by the Skule student website

To run this on your own server, simply install Twisted, then run
"rpc\_auth\_server.py".  Included in the "testing" directory is a sample of the
usage of this system.

Note that to use SSL, you will also have to generate SSL certs, change the
paths to them in "rpc\_auth\_server", and configure Apache and mod_ssl
appropriately.

Generating SSL Certs
--------------------

<code>
$ openssl genrsa -des3 -out server.key 1024
$ openssl req -new -key server.key -out server.csr
$ cp server.key server.key.org
$ openssl rsa -in server.key.org -out server.key
$ openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
</code>

Then, you'll want to notify Apache of this:
<code>
$ cp server.crt /etc/apache2/server.crt
$ cp server.key /etc/apache2/server.key
</code>

and add lines to your Apache configuration, probably something along the line of
<code>
SSLCertificateFile "/etc/apache2/server.crt"
SSLCertificateKeyFile "/etc/apache2/server.key"
</code>
	