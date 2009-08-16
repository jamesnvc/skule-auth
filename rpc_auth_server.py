# Authentication server for Skule.ca
from twisted.web import server, xmlrpc
from twisted.enterprise import adbapi

class AuthXmlRpc(xmlrpc.XMLRPC):
    """XML/RPC authentication server for skule.ca
    """

    def __init__(self, dbconn):
        """
        Initialize server
        Arguments:
        - `dbconn`: Database connection to autheticate users against
        """
        self.dbconn = dbconn
        self.allowNone = True

    def xmlrpc_validateUser(self,username,hsh_pw):
        """Validate the given username/password

        Arguments:
        - `username`: Username to validate
        - `hsh_pw`: Hashed password for the user
        """
        return self.dbconn.runQuery(
            "select userid, password from user where username = ? and password = ?",
            (username, hsh_pw)).addCallback(
            self._gotValidateQueryResults, hsh_pw
            )

    def _gotValidateQueryResults(self, rows, pw):
        """Callback to process successful retrieval of user info from database

        Arguments:
        - `rows`: Results
        - `pw`: Hash of password from the user
        """
        if rows:
            userid, password = rows[0]
            if password == pw:
                return (userid, password)
            else:
                return False # wrong password
        else:
            return False # No such user

    def xmlrpc_userExists(self, username):
        """Check if a user with the given name exists in the database.
        Returns the userid if so, false otherwise.
        
        Arguments:
        - `username`: Name to check
        """
        return self.dbconn.runQuery(
            "select userid from user where username = ?", (username,)).addCallback(
            self._gotExistsQueryResults)

    def _gotExistsQueryResults(self, rows):
        """Callback to process successful retrieval of username from database
        
        Arguments:
        - `rows`: results
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
        """
        return self.dbconn.runOperation(
            "insert into user (username, password, firstname, lastname) values (?, ?, ?, ?)" ,
            (username, passwd, fname, lname)).addCallback(
            self._addedUser).addErrback(self._anError)

    def _addedUser(self, arg):
        """Callback after successfully adding a user
        
        Arguments:
        - `arg`:  None
        """
        return True

    def _anError(self, *args):
        """
        
        Arguments:
        - `args`:
        """
        return False
        
        
        

DB_DRIVER = "sqlite3"
DB_ARGS = {
    'db': 'test.db',
    'user': 'tester',
    'passwd': 'tester',
    }

if __name__ == "__main__":
    from twisted.internet import reactor
    from twisted.web import resource
    connection = adbapi.ConnectionPool(DB_DRIVER, 'test.db')
    root = resource.Resource()
    root.putChild('auth', AuthXmlRpc(connection))
    reactor.listenTCP(8082, server.Site(root))
    reactor.run()
