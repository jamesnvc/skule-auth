# Authentication server for Skule.ca
# Copyright James Cash 2009

# FIXME: twisted.enterprise is deprecated, replace with something better
from twisted.enterprise import adbapi
from twisted.cred import portal, checkers, credentials, error as credError
from twisted.protocols import basic
from twisted.internet import protocol, reactor, defer
from zope.interface import Interface, implements

class PasswordDictChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, passwords):
        self.passwords = passwords

    def requestAvatarId(self, credentials):
        username = credentials.username
        if self.passwords.has_key(username):
            if credentials.password == self.passwords[username]:
                return defer.succeed(username)
            else:
                return defer.fail(
                    credError.UnauthorizedLogin("Bad password"))
        else:
            return defer.fail(
                credError.UnauthorizedLogin("No such user"))

# TODO: Change this to use sqlalchemy or similiar, instead of just strings
class DbPasswordChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def __init__(self, dbconn):
        self.dbconn = dbconn

    def requestAvatarId(self,credentials):
        """Request the avatar with the given credentials from the database

        Arguments:
        - `credentials`:
        """
        return self.dbconn.runQuery(
            "select userid, password from user where username = ?", (credentials.username,)).addCallback(
            self._gotQueryResults, credentials)

    def _getQueryResults(self, rows, userCredentials):
        """Callback which is called upon successful retrieval of the user's credentials from the database

        Arguments:
        - `rows`:
        - `userCredentials`:
        """
        if rows:
            userid, password = rows[0]
            return defer.maybeDeferred(
                userCredentials.checkPassword, password).addCallback(
                self._checkedPassword, userid)
        else:
            raise credError.UnauthorizedLogin("No such user")

    def _checkedPassword(self, matched, userid):
        """Callback which is called upon successful validation of the user's credentials

        Arguments:
        - `matched`:
        - `userid`:
        """
        if matched:
            return userid
        else:
            raise credError.UnauthorizedLogin("Bad password")

class DbRealm:
    implements(portal.IRealm)

    def __init__(self, dbconn):
        self.dbconn = dbconn

    def requestAvatar(self, avatarId, mind, *interfaces):
        """Return the avatar with the given ID from the database
        
        Arguments:
        - `self`:
        - `avatarId`:
        - `mind`:
        - `*interfaces`:
        """
        if simplecred.INamedUserAvatar in interfaces:
            return self.dbconn.runQuery(
                "select username, firstname, lastname from user where userid = ?",
                (avatarId)).addCallBack(
                self._gotQueryResults)
        else:
            raise KeyError("None of the requested interfaces is supported")
        
    def _getQueryResults(self, rows):
        """Callback called upon successful retrieval of the avatar for the user
        
        Arguments:
        - `self`:
        - `rows`:
        """
        username, firstname, lastname = rows[0]
        fullname = "%s %s" % (firstname, lastname)
        return (simplecred.INamedUserAvatar,
                simplecred.NamedUserAvatar(username, fullname),
                lambda: None)    


class INamedUserAvatar(Interface):
    """Should have attributes `username` and `fullname`"""

class NamedUserAvatar:
    implements(INamedUserAvatar)

    def __init__(self, username, fullname):
        self.username = username
        self.fullname = fullname

class TestRealm:
    implements(portal.IRealm)

    def __init__(self, users):
        self.users = users

    def requestAvatar(self, avatarId, mind, *interfaces):
        if INamedUserAvatar in interfaces:
            fullname = self.users[avatarId]
            logout = lambda: None
            return (INamedUserAvatar,
                    NamedUserAvatar(avatarId, fullname),
                    logout)
        else:
            raise KeyError("None of the requested interfaces are supported.")

class LoginTestProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        cmd = getattr(self, 'handle_'+self.currentCommand)
        cmd(line.strip())

    def connectionMade(self):
        self.transport.write("Username: ")
        self.currentCommand = 'user'

    def handle_user(self, username):
        self.username = username
        self.transport.write("Password: ")
        self.currentCommand = 'pass'

    def handle_pass(self, password):
        creds = credentials.UsernamePassword(self.username, password)
        self.factory.portal.login(creds, None, INamedUserAvatar).addCallback(
            self._loginSucceeded).addErrback(
            self._loginFailed)

    def _loginSucceeded(self, avatarInfo):
        avatarInterface, avatar, logout = avatarInfo
        self.transport.write("Welcome %s!\r\n" % avatar.fullname)
        defer.maybeDeferred(logout).addBoth(self._logoutFinished)

    def _logoutFinished(self, result):
        self.transport.loseConnection()

    def _loginFailed(self, failure):
        self.transport.write("Denied: %s.\r\n" % failure.getErrorMessage())
        self.transport.loseConnection()

class LoginTestFactory(protocol.ServerFactory):
    protocol = LoginTestProtocol

    def __init__(self, portal):
        self.portal = portal

users = { 'foo': 'Foo Bar'}
passwords = {'foo': 'bar'}

DB_DRIVER = "sqlite"
DB_ARGS = {
    'db': 'test.db',
    'user': 'tester',
    'passwd': 'tester',
    }

if __name__ == "__main__":
    connection = adbapi.ConnectionPool(DB_DRIVER, **DB_ARGS)
    p = portal.Portal(DbRealm(connection))
    p.registerChecker(DbPasswordChecker(connection))
    factory = simplecred.LoginTestFactory(p)
    reactor.listenTCP(2323, factory)
    reactor.run()
