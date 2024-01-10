from tkinter import *
from socket import *
from threading import *


HOST = '127.0.0.1'
PORT = 12345


def start_chat(chat_username: str, chat_protocol: bool) -> None:

    print(chat_protocol)

    def send_message_via_tcp(sender: str, client_socket: socket, gui_text_area_input: Entry) -> None:
        message = f'{sender} > ' + gui_text_area_input.get()
        client_socket.send(message.encode())
        gui_text_area_input.delete(0, END)

    def listening_to_server_via_tcp(connection_state: bool, client_socket: socket, gui_text_area: Text) -> None:
        while connection_state:
            answer_from_server = client_socket.recv(1024)
            gui_text_area.insert(END, answer_from_server.decode() + '\n')

    def send_message_via_udp(sender: str, client_socket: socket, gui_text_area_input: Entry) -> None:
        message = f'{sender} > ' + gui_text_area_input.get()
        client_socket.sendto(message.encode(), (HOST, PORT))
        gui_text_area_input.delete(0, END)

    def listening_to_server_via_udp(client_socket: socket, gui_text_area: Text) -> None:
        while True:
            answer_from_server, address = client_socket.recvfrom(1024)
            gui_text_area.insert(END, answer_from_server.decode() + '\n')

    if chat_protocol is True:
        client = socket(type=SOCK_STREAM)  # TCP socket
        try:
            client.connect((HOST, PORT))
        except ConnectionRefusedError:
            print('Unable connect to server')
        else:
            connection = True

            chat_window = Tk()
            chat_window.title(f'Your username - {chat_username}')
            text_area = Text(master=chat_window, width=45)
            text_area.grid(row=0, column=0)
            text_input_area = Entry(master=chat_window, width=40)
            text_input_area.grid(row=1, column=0)
            scroll = Scrollbar(master=text_area, orient="vertical",
                               command=text_area.yview)
            scroll.place(relheight=1.0, relx=0.98)
            text_area["yscrollcommand"] = scroll.set
            send_button = Button(master=chat_window, text='Send',
                                 command=lambda: send_message_via_tcp(chat_username, client, text_input_area))
            send_button.grid(row=1, column=1)

            if connection is True:
                thread = Thread(target=listening_to_server_via_tcp, args=(connection, client, text_area))
                if thread.is_alive() is False:
                    thread.start()

            chat_window.mainloop()
    else:
        client = socket(type=SOCK_DGRAM)
        chat_window = Tk()
        chat_window.title(f'Your username - {chat_username}')
        text_area = Text(master=chat_window, width=45)
        text_area.grid(row=0, column=0)
        text_input_area = Entry(master=chat_window, width=40)
        text_input_area.grid(row=1, column=0)
        scroll = Scrollbar(master=text_area, orient="vertical",
                           command=text_area.yview)
        scroll.place(relheight=1.0, relx=0.98)
        text_area["yscrollcommand"] = scroll.set
        send_button = Button(master=chat_window, text='Send',
                             command=lambda: send_message_via_udp(chat_username, client, text_input_area))
        send_button.grid(row=1, column=1)

        client.sendto(f'{chat_username} joined to the server!'.encode(), (HOST, PORT))
        thread = Thread(target=listening_to_server_via_udp, args=(client, text_area))
        if thread.is_alive() is False:
            thread.start()

        chat_window.mainloop()


def main() -> None:

    # Login GUI
    login_window = Tk()
    login_window.title('Login')
    login_window.geometry('500x500')
    frame = Frame(master=login_window, borderwidth=1, relief=RAISED)
    label = Label(master=frame, text='Your username')
    label.pack(anchor="center", padx=5, pady=5)
    username = StringVar()
    entry = Entry(master=frame, textvariable=username)
    entry.pack(anchor="center", padx=5, pady=5)
    radio_label = Label(master=frame, text="Protocol to be used:")
    radio_label.pack(anchor="center", padx=5, pady=5)
    protocol = BooleanVar()
    protocol.set(True)
    tcp_radio_button = Radiobutton(master=frame, text='TCP', width=5, value=True, variable=protocol)
    tcp_radio_button.pack(anchor="center", padx=5, pady=5)
    udp_radio_button = Radiobutton(master=frame, text='UDP', width=5, value=False, variable=protocol)
    udp_radio_button.pack(anchor="center", padx=5, pady=5)
    button = Button(master=frame, text='Enter the chat', command=lambda: start_chat(username.get(), protocol.get()))
    button.pack(anchor="center", padx=5, pady=5)
    frame.place(anchor="center", relx=0.5, rely=0.5)
    login_window.mainloop()


if __name__ == '__main__':
    main()
