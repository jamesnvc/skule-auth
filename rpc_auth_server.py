# Authentication server for Skule.ca
import os
import string
import time
from twisted.web import server, xmlrpc
from twisted.enterprise import adbapi
from twisted.internet import base

class AuthXmlRpc(xmlrpc.XMLRPC):
    """XML/RPC authentication server for skule.ca
    """

    def __init__(self, dbconn):
        """Initialize server
        
        Arguments:
        - `dbconn`: Database connection to autheticate users against
        """
        self.sessions = {}
        self.dbconn = dbconn
        self.allowNone = True
        self.timeout = 30 * 60

    def xmlrpc_validateUser(self,username,hsh_pw):
        """Validate the given username/password

        Arguments:
        - `username`: Username to validate
        - `hsh_pw`: Hashed password for the user
        Returns:
        - A deferred (_gotValidateQueryResults(row, hsh_pw))
        """
        return self.dbconn.runQuery(
            "SELECT userid, password FROM user WHERE username = ? AND password = ?",
            (username, hsh_pw)).addCallback(
            self._gotValidateQueryResults, hsh_pw
            )

    def _gotValidateQueryResults(self, rows, pw):
        """Callback to process successful retrieval of user info from database

        Arguments:
        - `rows`: Results
        - `pw`: Hash of password from the user
        Returns:
        - `(userid, sid)`: if the password is correct, false otherwise
        """
        if rows:
            userid, password = rows[0]
            if password == pw:
                x = [ ]
                while len(x) < 20:
                    y = os.urandom(1) 
                    if y in (string.letters+string.digits):
                        x += y
                sid = ''.join(x)
                
                # TODO: Set a timeout to erase this after `timeout`
                self.sessions[userid] = sid
                def sessionTimeout(): del self.sessions[userid]
                base.DelayedCall( time.time() + self.timeout, sessionTimeout, [], {}, None, None )
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
            self._gotExistsQueryResults).addErr	

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
            "INSERT INTO user (username, password, firstname, lastname) VALUES (?, ?, ?, ?)" ,
            (username, passwd, fname, lname)).addCallback(
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


DB_DRIVER = "sqlite3"
DB_ARGS = {
    'db': 'test.db',
    'user': 'tester',
    'passwd': 'tester',
    }

if __name__ == "__main__":
    from twisted.web import resource
    from twisted.internet import reactor, ssl
    connection = adbapi.ConnectionPool(DB_DRIVER, 'test.db')
    root = resource.Resource()
    root.putChild('auth', AuthXmlRpc(connection))
    sslContext = ssl.DefaultOpenSSLContextFactory('testing/KeyGen/server.key','testing/KeyGen/server.crt')
    reactor.listenSSL(8082, server.Site(root), sslContext)
    reactor.run()
