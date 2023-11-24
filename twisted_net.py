from twisted.internet.protocol import DatagramProtocol
from twisted.internet import protocol
from settings import VERBOSITY

# Define TCP Handlers
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
        self.game.processIncomingTCPDataFromClient(data)

class BlobberServerFactory(protocol.Factory):
    protocol = BlobberServerProtocol

    def __init__(self, game):
        self.game = game

class BlobberClientProtocol(protocol.Protocol):
    def connectionMade(self):
        if VERBOSITY > 2:
            print("Connected to the server.")
        # Here, you can send some initial data to the server if needed
        # self.transport.write("Hello from client".encode())

    def dataReceived(self, data):
        if VERBOSITY > 2:
            print(f"Data received from server: {data}")
        # Here you can update your game state based on data received from the server
        self.game.processIncomingTCPDataFromServer(data)

class BlobberClientFactory(protocol.ClientFactory):
    protocol = BlobberClientProtocol

    def __init__(self, game):
        self.game = game

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason}")

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason}")


# Define UDP Handlers
class BlobberUDPServer(DatagramProtocol):
    def __init__(self, game):
        self.game = game

    def datagramReceived(self, datagram, address):
        if VERBOSITY > 2:
            print(f"UDP Data received from client: {datagram}")
        self.game.processIncomingUDPDataFromClient(datagram, address)
        # Optionally, send a response back using game.sendData

class BlobberUDPClient(DatagramProtocol):
    def __init__(self, game):
        self.game = game

    def startProtocol(self):
        self.transport.connect('localhost', 12345)
        self.transport.write(b"Hello from client")

    def datagramReceived(self, datagram, address):
        if VERBOSITY > 2:
            print(f"Data received from server: {datagram}")
        self.game.processIncomingUDPDataFromServer(datagram, address)
