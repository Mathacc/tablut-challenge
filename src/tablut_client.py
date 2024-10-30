import socket
import json

class TablutClient:
    def __init__(self, host='localhost', port=5800, player_color='white', timeout=60):
        """
        Initialize a Tablut client to connect to the Java server.
        Parameters:
            host (str): The server's hostname or IP address.
            port (int): The server's port number.
            player_color (str): Player color ('white' or 'black').
        """
        self.host = host
        self.port = port
        self.player_color = player_color
        self.socket = None
        self.connected = False
        self.timeout = timeout

    def connect(self):
        """Connect to the Java server."""
        try:
            self.socket = socket.create_connection((self.host, self.port), timeout=self.timeout)
            self.connected = True
            print(f"Connected to server on port {self.port} as {self.player_color}.")
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            self.connected = False

    def send_move(self, move_data):
        """Send move data as JSON to the server."""
        if not self.connected:
            raise ConnectionError("Client is not connected to the server.")
        
        try:
            json_data = json.dumps(move_data)
            self.socket.sendall(json_data.encode('utf-8'))
            print(f"Sent move: {json_data}")
        except socket.error as e:
            print(f"Error sending move data: {e}")

    def receive_game_state(self):
        """Receive game state from the server and decode JSON."""
        if not self.connected:
            raise ConnectionError("Client is not connected to the server.")
        
        try:
            data = self.socket.recv(4096).decode('utf-8')
            game_state = json.loads(data)
            print(f"Received game state: {game_state}")
            return game_state
        except socket.error as e:
            print(f"Error receiving game state: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            return None

    def close(self):
        """Close the connection to the server."""
        if self.socket:
            self.socket.close()
            print("Disconnected from server.")
            self.connected = False

# Example usage
if __name__ == "__main__":
    player_color = 'white'  # Choose 'white' or 'black'
    port = 5800 if player_color == 'white' else 5801

    client = TablutClient(port=port, player_color=player_color)
    client.connect()

    # Example move data
    move_data = {
        'from': {'row': 1, 'col': 1},
        'to': {'row': 2, 'col': 2}
    }

    client.send_move(move_data)
    game_state = client.receive_game_state()

    client.close()
