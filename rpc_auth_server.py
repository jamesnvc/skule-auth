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

    def xmlrpc_validateUser(self,username,hsh_pw):
        """Validate the given username/password

        Arguments:
        - `username`: Username to validate
        - `hsh_pw`: Hashed password for the user
        """
        return self.dbconn.runQuery(
            "select userid, password from user where username = ? and password = ?",
            (username, hsh_pw)).addCallback(
            self._gotQueryResults, hsh_pw
            )

    def _gotQueryResults(self, rows, pw):
        """Callback to process successful retrieval of user info from database

        Arguments:
        - `rows`:
        - `pw`:
        """
        if rows:
            userid, password = rows[0]
            if password == pw:
                return (userid, password)
            else:
                return False
        else:
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
