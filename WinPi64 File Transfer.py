from tkinter import *
import paramiko, os, glob, pysftp
from os.path import isfile, join

try: from tkinter import *
except: from Tkinter import *
import paramiko, os, glob, pysftp
from os.path import isfile, join

class Main(Tk):

    def __init__(self):

        super().__init__()

        self.click_flag = False

        self.eval("tk::PlaceWindow . center")

        self.title("WinPi64 File Transfer")
        #Entry for username
        self.login = Frame(self)
        Label(self.login, text="Username:").grid(row=0,column=0)
        self.username_box = Entry(self.login, width=25)
        self.username_box.insert(0, "pi")
        self.username_box.grid(row=0,column=1)
        #Entry for password
        Label(self.login, text="Password:").grid(row=1,column=0)
        self.password_box = Entry(self.login, width=25, show='*')
        self.password_box.insert(0, "raspberry")
        self.password_box.grid(row=1,column=1)
        #Button to begin transfer
        Button(self.login, text="Begin File Transfer", command=self.open_transfer).grid(row=2, columnspan=2)
        
        self.login.pack(fill="both", expand=True)        
        self.mainloop()

    def open_transfer(self):
        self.username = self.username_box.get()
        self.password = self.password_box.get()
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            self.connection = pysftp.Connection("localhost", username=self.username, port=2222, password=self.password, cnopts=cnopts)
            self.file_transfer_window()
        except paramiko.ssh_exception.AuthenticationException:
            warning_window = Toplevel(self)
            self.eval(f"tk::PlaceWindow {str(warning_window)} center")
            warning_window.title("Could not connect!")
            Label(warning_window, width=30, height=4, justify=CENTER, wraplength=180, text="Authentication failed; please double-check your login info and try again.").pack()
            Button(warning_window, text="Close", width=20, command=warning_window.destroy).pack()
            warning_window.mainloop()
        except paramiko.ssh_exception.NoValidConnectionsError:
            warning_window = Toplevel(self)
            self.eval(f"tk::PlaceWindow {str(warning_window)} center")
            warning_window.title("Could not connect!")
            Label(warning_window, width=30, height=4, justify=CENTER, wraplength=180, text="Could not connect to virtual machine; please make sure that virtual machine is running and try again.").pack()
            Button(warning_window, text="Close", width=20, command=warning_window.destroy).pack()
            warning_window.mainloop()
        except paramiko.ssh_exception.SSHException:
            warning_window = Toplevel(self)
            self.eval(f"tk::PlaceWindow {str(warning_window)} center")
            warning_window.title("Could not connect!")
            Label(warning_window, width=30, height=4, justify=CENTER, wraplength=180, text="Could not connect to virtual machine; please make sure that virtual machine is running and try again.").pack()
            Button(warning_window, text="Close", width=20, command=warning_window.destroy).pack()
            warning_window.mainloop()
        except Exception as e:
            raise(e)

        
    def file_transfer_window(self):

        self.login.destroy()
        self.transfer_page = Frame(self)
        button_menu = Frame(self.transfer_page)

        self.local_path = "C:/"
        self.guest_path = "/home/"+self.username

        Label(self.transfer_page, text="This PC", width=40).grid(row=0,column=0)
        Label(self.transfer_page, text="Virtual Machine", width=40).grid(row=0,column=1)
        
        self.local_path_entry = Entry(self.transfer_page, width=40)
        self.local_path_entry.insert(0, self.local_path)
        self.local_path_entry.bind("<Return>", self.show_local_short)
        self.local_path_entry.grid(row=1,column=0)
        
        self.guest_path_entry = Entry(self.transfer_page, width=40)
        self.guest_path_entry.insert(0, self.guest_path)
        self.guest_path_entry.bind("<Return>", self.show_guest_short)
        self.guest_path_entry.grid(row=1,column=1)
        
        self.local_files = Text(self.transfer_page, width=40, height=32, wrap="none")
        self.local_files.configure(selectbackground=self.local_files.cget("bg"), inactiveselectbackground=self.local_files.cget('bg'), selectforeground="#000000")
        self.local_files.tag_configure("bold", font=("Courier",11, "bold"), underline=True)
        self.guest_files = Text(self.transfer_page, width=40, height=32, wrap="none")
        self.guest_files.configure(selectbackground=self.guest_files.cget("bg"), inactiveselectbackground=self.guest_files.cget('bg'), selectforeground="#000000")
        self.guest_files.tag_configure("bold", font=("Courier",11, "bold"), underline=True)

        self.local_files.bind("<Key>", lambda e: "break")
        self.local_files.bind("<ButtonRelease-1>", self.get_local_selection)
        self.local_files.bind("<Double-Button-1>", self.show_local)
        self.guest_files.bind("<Key>", lambda e: "break")
        self.guest_files.bind("<ButtonRelease-1>", self.get_guest_selection)
        self.guest_files.bind("<Double-Button-1>", self.show_guest)

        Button(button_menu, text="Quick Trans. -> VM", width=30, command=self.quick_transfer_to_guest).pack()
        Button(button_menu, text="Quick Trans. -> HST", width=30, command=self.quick_transfer_to_local).pack()

        self.local_files.grid(row=2,column=0)
        self.guest_files.grid(row=2,column=1)
        button_menu.grid(row=0,column=2, rowspan=3)

        self.transfer_page.pack(fill="both", expand=True)

        self.show_local_short()
        self.show_guest_short()

        self.eval("tk::PlaceWindow . center")



    def show_local_short(self, event=None):
        self.show_local()
        self.click_flag = False

    def show_local(self, event=None):
        
        self.local_path = self.local_path_entry.get()
        
        if self.local_path[-1]!='/': self.local_path += '/'
        files = glob.glob(self.local_path+'*')
        if len(self.local_path)>3: files.insert(0,self.local_path+"[BACK]")

        self.local_files.delete('1.0',END)
        for file in files:
            file = file[(len(self.local_path)):len(file)]
            self.local_files.insert(END,file+'\n')

        self.click_flag = True

    def show_guest_short(self, event=None):
        self.show_guest()
        self.click_flag = False

    def show_guest(self, event=None):

        self.guest_path = self.guest_path_entry.get()

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys=None
        try:
            with self.connection.cd(self.guest_path):
                files = self.connection.listdir()
                if self.connection.pwd != '/': files.insert(0,"[BACK]")
                self.guest_files.delete("1.0",END)
                for file in files:
                    self.guest_files.insert(END,file+'\n')
        except:
            self.guest_files.delete("1.0",END)
            self.guest_files.insert(END,"[BACK]\n")

        self.click_flag = True

                

    def get_local_selection(self, event=None):

        if not self.click_flag:

            tk_index = self.local_files.index(INSERT)
            line = self.local_files.get(tk_index + " linestart", tk_index + " lineend")
            self.local_files.tag_remove("bold", "1.0", END)
            self.local_files.tag_add("bold", tk_index + " linestart", tk_index + " lineend")
            if line!= '[BACK]':
                self.local_path_entry.delete(0,END)
                self.local_path_entry.insert(0, self.local_path + ('/'+line if self.local_path[-1]!='/' else line))
            else:
                path = self.local_path
                if path[-1]=='/': path = path[:-1]
                if path.find('/') != path.rfind('/'): path = path[:path.rfind('/')]
                else: path = path[0]+":/"
                self.local_path_entry.delete(0,END)
                self.local_path_entry.insert(0, path)

        else:
            self.click_flag = False

    def get_guest_selection(self, event=None):

        if not self.click_flag:

            tk_index = self.guest_files.index(INSERT)
            line = self.guest_files.get(tk_index + " linestart", tk_index + " lineend")
            self.guest_files.tag_remove("bold", "1.0", END)
            self.guest_files.tag_add("bold", tk_index + " linestart", tk_index + " lineend")
            if line!= '[BACK]':
                self.guest_path_entry.delete(0,END)
                self.guest_path_entry.insert(0, self.guest_path + ('/'+line if self.guest_path[-1]!='/' else line))
            else:
                path = self.guest_path
                if path[-1]=='/': path = path[:-1]
                path = path[:path.rfind('/')]
                if path=='': path='/'
                self.guest_path_entry.delete(0,END)
                self.guest_path_entry.insert(0, path)

        else:
            self.click_flag = False

    def quick_transfer_to_guest(self):
        
        temp_guest_path = self.guest_path_entry.get()
        temp_local_path = self.local_path_entry.get()
        
        with self.connection.cd(temp_guest_path):
            self.connection.put(temp_local_path, preserve_mtime=True)
        self.show_guest_short()

    def quick_transfer_to_local(self):

        temp_guest_path = self.guest_path_entry.get()
        temp_local_path = self.local_path_entry.get()

        new_local_path = temp_local_path + '/' + temp_guest_path[temp_guest_path.rfind('/')+1:]
        
        try: self.connection.get(temp_guest_path, new_local_path, preserve_mtime=True)
        except: pass
        self.show_local_short()
            

if __name__ == "__main__":
    Main()




