from socket import *
from threading import *
import argparse

parser = argparse.ArgumentParser(description="""TCP/UDP server to demonstrate the operation of the 
                                                corresponding protocols in chat.""", epilog="""
                                                Uses TCP by default. To work with UDP it is required 
                                                to specify the -UDP switch.""")
parser.add_argument('-UDP', action='store_false')
args = parser.parse_args()

protocol = args.UDP
HOST = '127.0.0.1'
PORT = 12345


def main() -> None:

    def tcp_broadcast_message(message: bytes) -> None:
        """Retransmits a message from the client to all clients"""
        for client in connection_list:
            client.send(message)

    def udp_broadcast_message(message: bytes, server_socket: socket, addr_list: list) -> None:
        for udp_address in addr_list:
            server_socket.sendto(message, udp_address)

    def tcp_message_processing(connection: socket) -> None:
        """Receives data in bytes and passes it to the tcp_broadcast_message() function"""
        print(f'Message processing for {connection}')
        while True:
            tcp_data = connection.recv(1024)
            tcp_broadcast_message(tcp_data)

    def udp_message_processing(server_socket: socket, addr_list: list) -> None:
        while True:
            udp_data, udp_address = server_socket.recvfrom(1024)
            addr_list.append(udp_address)
            addr_list = list(set(addr_list))
            print(f'[UDP]: IPv4 and Port: {udp_address}')
            udp_broadcast_message(udp_data, server_socket, addr_list)

    if protocol is True:
        server = socket(type=SOCK_STREAM)
        server.bind((HOST, PORT))
        connection_list = []
        server.listen()
        print('[TCP]: The server listens for incoming connections')

        while True:
            conn, addr = server.accept()
            print(f'[TCP]: Connection: {conn}')
            print(f'[TCP]: IPv4 and Port: {addr}')
            connection_list.append(conn)
            conn.send('Welcome to the Server!'.encode())
            thread = Thread(target=tcp_message_processing, args=(conn, ))
            if thread.is_alive() is False:
                thread.start()
    else:
        server = socket(type=SOCK_DGRAM)
        server.bind((HOST, PORT))
        addresses_list = []
        print('[UDP]: The server listens for incoming connections')

        thread = Thread(target=udp_message_processing, args=(server, addresses_list))
        if thread.is_alive() is False:
            thread.start()


if __name__ == '__main__':
    main()
