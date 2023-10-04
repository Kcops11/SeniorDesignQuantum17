import socket
import threading
import json

class CustomPacket:
    def __init__(self, packet_type, data):
        self.packet_type = packet_type
        self.data = data

def serialize_packet(packet):
    return json.dumps({
        'packet_type': packet.packet_type,
        'data': packet.data
    }).encode('utf-8')

def deserialize_packet(packet_bytes):
    packet_dict = json.loads(packet_bytes.decode('utf-8'))
    return CustomPacket(packet_dict['packet_type'], packet_dict['data'])

class Router:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Adjust the backlog as needed
        print(f"Router listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.connections.append(conn)
            threading.Thread(target=self.handle_connection, args=(conn,)).start()

    def handle_connection(self, conn):
        while True:
            packet_bytes = conn.recv(1024)  # Adjust buffer size as needed
            if not packet_bytes:
                break
            packet = deserialize_packet(packet_bytes)
            response_packet = self.process_packet(packet)
            serialized_response = serialize_packet(response_packet)
            conn.send(serialized_response)

    def process_packet(self, packet):
        # Implement your packet processing logic here
        pass

    def broadcast(self, packet):
        serialized_packet = serialize_packet(packet)
        for conn in self.connections:
            conn.send(serialized_packet)

# Usage example:
router = Router('localhost', 8000)
router.start()
