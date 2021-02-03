from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from PIL import Image , ImageTk
import tkinter as tk

# main Class
class main:
    def __init__(self, master):
        # Window
        self.master = master
        # Some Useful variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.n_username = tk.StringVar()
        self.n_password = tk.StringVar()
        # Create Widgets
        self.widgets()

    # Login Function
    def login(self):
        # Establish Connection
        
        with sqlite3.connect('user1.db') as db:
            c = db.cursor()

        # Find user If there is any take proper action
        db = sqlite3.connect('user1.db')
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS entry"
                       "(Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)")
        db.commit()
        find_entry = ('SELECT * FROM entry WHERE username = ? and password = ?')
        c.execute(find_entry, [(self.username.get()), (self.password.get())])
        result = c.fetchall()

        if result:
            msg = ""
            self.logf.pack_forget()
            # self.head['text'] = self.username.get() + '\n Loged In'
            # msg = self.head['text']
            #            self.head['pady'] = 150
            print(msg)
            ms.showinfo("messege","LogIn sucessfully")
            # ===========================================
            root.destroy()

            # import GUI_master
            # GUI_master.main()
            from subprocess import call
            call(['python','GUI_master.py'])

            # ================================================
        else:
            ms.showerror('Oops!', 'Username Or Password Did Not Found/Match.')

    def new_user(self):
        # Establish Connection
        with sqlite3.connect('user1.db') as db:
            c = db.cursor()

        # Find Existing username if any take proper action
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(self.username.get())])
        if c.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
        else:
            ms.showinfo('Success!', 'Account Created Successfully !')
            self.log()
        # Create New Account
        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        db.commit()

        # Frame Packing Methords
    def registration(self):
        root.destroy()
        from subprocess import call
        call(["python", "Registration.py"])
        
        # mainloop(root)

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()



    # Draw Widgets
    def widgets(self):
        self.head = tk.Label(self.master, text='Welcome To Login', background="cyan3", font=('Times New Roman', 20), pady=20)
        self.head.pack()

        # self.head.pack()
        # self.head = Label(self.master, text='LOGIN',background="gold", font=('Times New Roman', 35), pady=10)
        # self.head.pack()
        self.logf = tk.Frame(self.master, padx=50, pady=20, background="cyan3")
        tk.Label(self.logf, text='Username: ', background="cyan3", font=("Times New Roman", 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.logf, textvariable=self.username, bd=5, background="white", font=('', 15)).grid(row=0, column=1)
        tk.Label(self.logf, text='Password: ', background="cyan3", font=("Times New Roman", 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.logf, textvariable=self.password, bd=5, background="white", font=('', 15), show='*').grid(row=1, column=1)
        tk.Button(self.logf, text=' Login ', bd=3, font=("Times New Roman", 20), background="black", foreground="white", padx=5, pady=5, command=self.login).grid(row = 2, column = 1, pady = 10)
        tk.Button(self.logf, text=' Create Account ', font=("Times New Roman", 20), background="black", foreground="white", bd=3, padx=5, pady=5, command=self.registration).grid(row=3,
                                                                                                              column=1, pady = 10)


        self.logf.pack()
        self.crf = tk.Frame(self.master, padx=500, pady=500)

root = tk.Tk()

root.configure(background="cyan3")
# canvas=Canvas(root,width=300,height=160)
# image=ImageTk.PhotoImage(Image.open("C:\\Users\\Yogesh Mali\\PycharmProjects\\login_system\\333.jpg"))
# canvas.create_image(0,0,anchor=NW,image=image)
# canvas.pack()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Login")

main(root)

root.mainloop()
