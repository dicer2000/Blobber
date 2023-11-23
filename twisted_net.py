from twisted.internet import protocol
from settings import VERBOSITY

# Define a Protocol for your game
class BlobberServerProtocol(protocol.Protocol):
    def connectionMade(self):
        ''' Method is called when a client connects'''
        if VERBOSITY > 2:
            print(f"Connection from {self.transport.getPeer()}")
        # Here you can add the new player to the game, for example
        self.factory.game.add_player(self)

    def dataReceived(self, data):
        ''' Method is called when data is received from a client'''
        if VERBOSITY > 2:
            print(f"Received: {data}")
        # Handle the incoming data, such as player actions

class BlobberServerFactory(protocol.Factory):
    protocol = BlobberServerProtocol

    def __init__(self, game):
        self.game = game

class BlobberClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connected to the server.")
        # Here, you can send some initial data to the server if needed
        # self.transport.write("Hello from client".encode())

    def dataReceived(self, data):
        if VERBOSITY > 2:
            print(f"Data received from server: {data}")
        # Here you can update your game state based on data received from the server

class BlobberClientFactory(protocol.ClientFactory):
    protocol = BlobberClientProtocol

    def __init__(self, game):
        self.game = game

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason}")

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason}")
