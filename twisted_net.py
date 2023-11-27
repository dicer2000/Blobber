from twisted.internet.protocol import DatagramProtocol
from twisted.internet import protocol
from settings import VERBOSITY

# Define TCP Handlers
# Twisted documentation found here: https://twisted.org/documents/9.0.0/core/howto/

class BlobberServerProtocol(protocol.Protocol):
    ''' Handles TCP connections for the server side of the game. '''
    def connectionMade(self):
        ''' Called when a client connects to the server. Logs the connection and adds the new player to the game. '''
        if VERBOSITY > 2:
            print(f"Connection from {self.transport.getPeer()}")
        self.factory.game.add_player(self)

    def dataReceived(self, data):
        ''' Called when data is received from a client. Logs the received data and handles player actions. '''
        if VERBOSITY > 2:
            print(f"Received: {data}")

class BlobberServerFactory(protocol.Factory):
    ''' Factory for creating BlobberServerProtocol instances. '''
    protocol = BlobberServerProtocol

    def __init__(self, game):
        ''' Initializes the factory with a reference to the game instance. '''
        self.game = game

class BlobberClientProtocol(protocol.Protocol):
    ''' Handles TCP connections for the client side of the game. '''
    def connectionMade(self):
        ''' Called when the client successfully connects to the server. Logs the connection and can send initial data to the server. '''
        print("Connected to the server.")

    def dataReceived(self, data):
        ''' Called when data is received from the server. Logs the received data and updates the game state based on this data. '''
        if VERBOSITY > 2:
            print(f"Data received from server: {data}")

class BlobberClientFactory(protocol.ClientFactory):
    ''' Factory for creating BlobberClientProtocol instances. '''
    protocol = BlobberClientProtocol

    def __init__(self, game):
        ''' Initializes the factory with a reference to the game instance. '''
        self.game = game

    def clientConnectionFailed(self, connector, reason):
        ''' Called when the client connection fails. Logs the reason for failure. '''
        print(f"Connection failed: {reason}")

    def clientConnectionLost(self, connector, reason):
        ''' Called when the client connection is lost. Logs the reason for the connection loss. '''
        print(f"Connection lost: {reason}")

# Define UDP Handlers

class BlobberUDPServer(DatagramProtocol):
    ''' Handles UDP datagrams for the server side of the game. '''
    def __init__(self, game):
        ''' Initializes the UDP server with a reference to the game instance. '''
        self.game = game

    def datagramReceived(self, datagram, address):
        ''' Called when a UDP datagram is received. Processes the incoming data using the game instance and optionally sends a response back. '''
        self.game.processIncomingData(datagram, address)

class BlobberUDPClient(DatagramProtocol):
    ''' Handles UDP datagrams for the client side of the game. '''
    def __init__(self, game):
        ''' Initializes the UDP client with a reference to the game instance. '''
        self.game = game

    def startProtocol(self):
        ''' Called when the protocol starts. Connects to the server and sends an initial message. '''
        self.transport.connect('localhost', 12345)
        self.transport.write(b"Hello from client")

    def datagramReceived(self, datagram, address):
        ''' Called when a UDP datagram is received from the server. Processes the incoming data using the game instance. '''
        self.game.processIncomingData(datagram, address)
