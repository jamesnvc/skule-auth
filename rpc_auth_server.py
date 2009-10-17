# Authentication server for Skule.ca
import auth_lib
import os
import string
import time
import hashlib
from twisted.web import server, xmlrpc
from twisted.enterprise import adbapi
from twisted.internet import task

class AuthXmlRpc(xmlrpc.XMLRPC):
    """XML/RPC authentication server for skule.ca
    """

    def __init__(self, dbconn, userTimeout):
        """Initialize server
        
        Arguments:
        - `dbconn`: Database connection to autheticate users against
        """
        self.sessions = {}
        self.dbconn = dbconn
        self.allowNone = True
        self.timeout = userTimeout

    def xmlrpc_validateUser(self,username,pln_pw):
        """Validate the given username/password

        Arguments:
        - `username`: Username to validate
        - `pln_pw`: Entered password
        Returns:
        - A deferred (_gotValidateQueryResults(row, pln_pw))
        """
        return self.dbconn.runQuery(
            "SELECT userid, password, salt FROM user WHERE username = ?",
            (username, )).addCallback(
            self._gotValidateQueryResults, pln_pw
            ).addErrback(self._anError)

    def _gotValidateQueryResults(self, rows, pw):
        """Callback to process successful retrieval of user info from database

        Arguments:
        - `rows`: Results
        - `pw`: Password from the user
        Returns:
        - `(userid, sid)`: if the password is correct, false otherwise
        """
        if rows:
            userid, password, salt = rows[0]
            hsh_pw = hashlib.sha1(pw+salt).hexdigest()
            if password == hsh_pw:
                # Generating a random session cookie
                sid = rand_string(20)
                self.sessions[userid] = sid
                def sessionTimeout(): del self.sessions[userid]
                d = task.deferLater(reactor, self.timeout, sessionTimeout)

                # Additional debugging information
                def timedOut(*args): print "%d: The session for user %d has expired" % (time.time(), userid)
                d.addCallback(timedOut)
                
                return (userid, sid)
            else:
                return False # wrong password
        else:
            return False # No such user

    def xmlrpc_userExists(self, username):
        """Check if a user with the given name exists in the database.
        Returns the userid if so, false otherwise.
        
        Arguments:
        - `username`: Name to check
        Returns:
        - A deferred (see `_gotExistsQueryResults`)
        """
        return self.dbconn.runQuery(
            "SELECT userid FROM user WHERE username = ?", (username,) ).addCallback(
            self._gotExistsQueryResults).addErrback(self._anError)

    def _gotExistsQueryResults(self, rows):
        """Callback to process successful retrieval of username from database
        
        Arguments:
        - `rows`: results
        Returns: The userid of the user if exisits, False otherwise
        """
        if rows:
            return rows[0][0]
        else:
            return False

    def xmlrpc_createUser(self, username, passwd, fname, lname):
        """Adds a user named `username` to the database, with the hashed password `passwd`, 
		   first name `fname`, last name `lname`
        
        Arguments:
        - `username`: username to add
        - `passwd`: Hash of password for new user
        - `fname`: First name
        - `lname`: Last name
        Returns:
        - True on successful insertion, False otherwise
        """
        return self.dbconn.runOperation(
            "INSERT INTO user (username, password, firstname, lastname, salt) VALUES (?, ?, ?, ?, ?)" ,
            (username, passwd, fname, lname, auth_lib.rand_string(10))).addCallback(
            self._addedUser).addErrback(self._anError)

    def _addedUser(self, arg):
        """Callback after successfully adding a user
        
        Arguments:
        - `arg`:  None
        """
        return True

    def _anError(self, *args):
        """Callback in case of an error adding a user
        
        Arguments:
        - `args`: None
        """
        return False
    
    def xmlrpc_checkUserSession(self, userid, sid):
        """Checks that the session id of the user with id `userid` is equivalent to the supplied session id
        
        Arguments:
        - `userid`: User id to check 
        - `sid`: Session id to verify
        Returns: True if matches, false otherwise
        """
        return (userid in self.sessions) and (self.sessions[userid] == sid)


if __name__ == "__main__":
    from twisted.web import resource
    from twisted.internet import reactor, ssl
    # Configuration values
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read('server_settings.conf')
    timeout_seconds = config.getfloat('Server Settings', 'cookie_timeout_minutes') * 60
    db_driver = config.get('Server Settings', 'db_driver')
    db_name = config.get('Server Settings', 'db_name')
    listen_port = config.getint('Server Settings', 'rpc_listen_port')
    ssl_key = config.get('Server Settings', 'ssl_key')
    ssl_cert = config.get('Server Settings', 'ssl_cert')
    
    connection = adbapi.ConnectionPool(db_driver, db_name)
    root = resource.Resource()
    root.putChild('auth', AuthXmlRpc(connection, timeout_seconds))
    sslContext = ssl.DefaultOpenSSLContextFactory(ssl_key, ssl_cert)
    reactor.listenSSL(listen_port, server.Site(root), sslContext)
    
    print "Starting server on port %s, using %s database %s." % (listen_port, db_driver, db_name)
    print "Using %s and %s for SSL." % (ssl_key, ssl_cert)
    print "Using a timeout of %f seconds" % (timeout_seconds)
    print "^C to stop the server"
    try:
        reactor.run()
    finally:
        connection.close()
