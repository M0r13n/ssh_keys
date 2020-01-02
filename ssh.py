from twisted.conch import avatar
from twisted.conch.checkers import SSHPublicKeyChecker
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.conch.ssh.transport import SSHServerTransport
from twisted.cred import portal, credentials
from twisted.cred.checkers import ICredentialsChecker
from twisted.cred.credentials import ICredentials
from twisted.cred.error import UnauthorizedLogin
from twisted.internet import reactor, protocol, defer
from twisted.python import log
from twisted.python import components
from zope.interface import implementer
import sys

log.startLogging(sys.stderr)

# Path to RSA SSH keys used by the server.
# They can be generated with $ ckeygen -t rsa -f ssh-keys/ssh_host_rsa_key
SERVER_RSA_PRIVATE = 'ssh_host_rsa_key'
SERVER_RSA_PUBLIC = 'ssh_host_rsa_key.pub'
KEYS = []

MSG = msg = """
    +---------------------------------------------------------------------+
    |                                                                     |
    |  Hello there! :-)                                                   |
    |                                                                     |
    |                                                                     |
    |  This is demo to demonstrate that SSH sends all your public keys    |
    |  by default.                                                        |
    |  The original idea comes from @FiloSottile  and is available here:  |  
    |  https://github.com/FiloSottile/whosthere                           |
    |                                                                     |
    |                                                                     |
    |                                                                     |
    |                                                                     |
    |  P.S. This version is written in 100% pure Python                   |
    |  https://github.com/M0r13n/some_repo                                |
    |                                                                     |
    |  -- C u                                                             |
    |                                                                     |
    |---------------------------YOUR KEYS --------------------------------|
""".replace('\n', '\n\r').encode('utf-8')


class ExampleAvatar(avatar.ConchUser):

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({b'session': session.SSHSession})


@implementer(portal.IRealm)
class ExampleRealm(object):

    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], ExampleAvatar(avatarId), lambda: None


class EchoProtocol(protocol.Protocol):
    """
    Custom protocol that is run over the shell.
    """

    def connectionMade(self):
        self.transport.write(MSG)
        for key in KEYS:
            msg = "\n\r".join(["    |" + line + (69 - len(line)) * " " + "|" for line in [
                line.replace('\t', '    ') for line in str(key).splitlines()]
                               ]) + "\n\r"
            self.transport.write(msg.encode('utf-8'))
        self.transport.write(b'    +---------------------------------------------------------------------+\n\r')
        self.transport.loseConnection()
        KEYS.clear()


class FailingSSHPublicKeyChecker(SSHPublicKeyChecker):
    """
    Always fails in order to get all public keys.
    """

    def _checkKey(self, pubKey, credentials):
        KEYS.append(pubKey)
        raise UnauthorizedLogin("I don't even care.")


class ExampleSession(object):
    """
    This selects what to do for each type of session which is requested by the
    client via the SSH channel of type I{session}.
    """

    def __init__(self, avatar):
        """
        Avatar is not used
        """

    def getPty(self, term, windowSize, attrs):
        """
        Not supported
        """

    def execCommand(self, proto, cmd):
        """
        Not supported
        """

    def openShell(self, transport):
        """
        Use the custom protocol
        """
        protocol = EchoProtocol()
        protocol.makeConnection(transport)
        transport.makeConnection(session.wrapProtocol(protocol))

    def eofReceived(self):
        """
        Nothing to do here
        """

    def closed(self):
        """
        Nothing to do here
        """


components.registerAdapter(ExampleSession, ExampleAvatar, session.ISession)


class IKeyBoardInteractive(ICredentials):
    """
    Authentication interface that offers keyboard-interactive authentication.
    """


@implementer(ICredentialsChecker)
class KeyboardInteractive(object):
    """
    Implementation of the above keyboard-interactive interface.
    This only needs to implement requestAvatarId().
    """
    credentialInterfaces = (IKeyBoardInteractive,)

    def requestAvatarId(self):
        """
        Returns a demo avatar object.
        """
        return ExampleRealm().requestAvatar("", "", ("",))


class MySSHUserAuthServer(userauth.SSHUserAuthServer):
    """
    Subclass SSHUserAuthServer to override interfaceToMethod and enable keyboard-interactive authentication.
    """
    interfaceToMethod = {
        credentials.ISSHPrivateKey: b'publickey',
        IKeyBoardInteractive: b'keyboard-interactive',
    }

    def auth_keyboard_interactive(self, packet):
        """
        Custom authentication method that always succeeds.
        This is used together with keyboard-interactive authentication because this kind of authentication
        is handled on the server side and requires no user interaction.
        """
        checker = self.portal.checkers.get(IKeyBoardInteractive)
        return defer.maybeDeferred(checker.requestAvatarId)


class ExampleFactory(factory.SSHFactory):
    """
    Entry point of the application.

    The SSH transport layer is implemented by SSHTransport and is the
    protocol of this factory.

    Here we configure the server's identity (host keys) and handlers for the
    SSH services:
    * L{connection.SSHConnection} handles requests for the channel multiplexing
      service.
    * L{userauth.SSHUserAuthServer} handlers requests for the user
      authentication service.
    """

    protocol = SSHServerTransport
    publicKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PUBLIC)
    }
    privateKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PRIVATE)
    }
    # Service handlers.
    services = {
        b'ssh-userauth': MySSHUserAuthServer,
        b'ssh-connection': connection.SSHConnection
    }

    def getPublicKeys(self):
        return self.publicKeys

    def getPrivateKeys(self):
        return self.privateKeys


portal = portal.Portal(ExampleRealm())
sshDB = FailingSSHPublicKeyChecker(None)
kbi = KeyboardInteractive()
portal.registerChecker(sshDB)
portal.registerChecker(kbi)
ExampleFactory.portal = portal

if __name__ == '__main__':
    reactor.listenTCP(5022, ExampleFactory())
    reactor.run()
