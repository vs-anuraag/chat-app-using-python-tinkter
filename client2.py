# Anuraag Venkatapuram Sreenivas
# 1001716458

import socket
import threading
import tkinter


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
buffer = 2048
uname = input("Enter user name::")
ip = '127.0.0.1'
s.connect((ip, port))
s.send(uname.encode('ascii'))



def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = s.recv(buffer).decode("ascii")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    # msg1 = my_msg.get()
    my_msg.set("")  # Clears input field.

    headers = """\
        POST /send HTTP/1.1 200 OK\r
        Content-Type: {content_type}\r
        Content-Length: {content_length}\r
        Host: {host}\r
        UserAgent: {useragent}\r
        Data: {Message}\r
        Connection: close"""

    header_bytes = headers.format(
        content_type="application/x-www-form-urlencoded",
        content_length=len(msg),
        useragent="HTTPTool/1.1",
        host=str(uname),
        Message=str(msg)
    ).encode('iso-8859-1')

    payload = header_bytes
    s.send(payload)

    # s.send(bytes(msg1, "ascii"))
    if msg == "/quit":
        s.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("/quit")
    send()


top = tkinter.Tk()
top.title(uname)


messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


receive_thread = threading.Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
