def main():
    import tkinter as tk
    from tkinter.filedialog import askopenfilename
    from PIL import Image, ImageTk
    import cv2
    import PIL
    from tkinter import ttk
    root = tk.Tk()
    root.title("Diabetic Eye Detection")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.configure(background="gold")

    tabControl = ttk.Notebook(root)          # Create Tab Control
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='  Pre-Process   ') # Add the tab

    tab3 = tk.ttk.Frame(tabControl)            # Create a tab
    tabControl.pack(expand=True, fill="both")

    def bphoto():

            global fn
            fileName = askopenfilename(initialdir='/dataset', title='Select image for analysis ',
                                       filetypes=[("all files", "*.*")])



            fn = fileName
            """
            Sel_F = fileName.split('/').pop()
            Sel_F = Sel_F.split('.').pop(0)
            """
            load = PIL.Image.open(fileName)
            render = ImageTk.PhotoImage(load)

            x1 = 250
            y1 = 250

            img = tk.Label(root, image=render, height=x1, width=y1)
            img.image = render

            img.place(x=5,y=100)


    def Gray_Scale():
        global fn
        FName = fn

        imgpath = FName


        gs = cv2.cvtColor(cv2.imread(imgpath, 1), cv2.COLOR_RGB2GRAY)

        x1 = 250
        y1 = 250

        gs = cv2.resize(gs, (x1, y1))

        retval, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        im = Image.fromarray(gs)
        imgtk = ImageTk.PhotoImage(image=im)
        img = tk.Label(root, image=imgtk, height=x1, width=y1)
        img.image = imgtk
        img.place(x=300, y=100)

    def analysis():
            global fn
            FName = fn

            imgpath = FName

            gs = cv2.cvtColor(cv2.imread(imgpath, 1), cv2.COLOR_RGB2GRAY)

            x1 = 250
            y1 = 250
            gs = cv2.resize(gs, (x1, y1))

            retval, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            im = Image.fromarray(threshold)
            imgtk = ImageTk.PhotoImage(image=im)

            img2 = tk.Label(root, image=imgtk, height=x1, width=y1)
            img2.image = imgtk
            img2.place(x=600, y=100)

    def edges():
        global fn
        FName = fn

        global eg

        imgpath = FName

        BLUR = 21
        CANNY_THRESH_1 = 10
        CANNY_THRESH_2 = 200
        MASK_DILATE_ITER = 10
        MASK_ERODE_ITER = 10

        img = cv2.imread(imgpath, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        x1 = 250
        y1 = 250
        gray = cv2.resize(gray, (x1, y1))

        edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
        edges = cv2.dilate(edges, None)
        edges = cv2.erode(edges, None)

        # display image
        im = Image.fromarray(edges)
        imgtk = ImageTk.PhotoImage(image=im)
        img3 = tk.Label(root, image=imgtk, height=x1, width=y1)
        img3.image = imgtk
        img3.place(x=900, y=100)

        eg = edges

    heading = tk.Label(root,width=120,height=3,text="Diabetic Disease Detection",font=("Tempus Sans ITC",15,"bold"),foreground="white",background="black")
    heading.place(x=0,y=5)

    button_p1 = tk.Button(tab1,text="Browse Photo", command=bphoto,width=15,height=2,background="purple3",foreground="snow",font=("Tempus Sans ITC",14,"bold"))
    button_p1.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)
    button_p1.place(x=50, y=520)

    button_p2 = tk.Button(tab1,text="Gray Scale", command=Gray_Scale, width=15,height=2,background="purple3",foreground="snow",font=("Tempus Sans ITC",14,"bold"))
    button_p2.grid(column=1, row=1, sticky=tk.W, padx=10, pady=10)
    button_p2.place(x=250, y=520)

    button_p3 = tk.Button(tab1, text="Threshold", command=analysis,width=15,height=2,background="purple3",foreground="snow",font=("Tempus Sans ITC",14,"bold"))
    button_p3.grid(column=2, row=1, sticky=tk.W, padx=10, pady=10)
    button_p3.place(x=450, y=520)

    button_p4 = tk.Button(tab1, text="Edges", command=edges,width=15,height=2,background="purple3",foreground="snow",font=("Tempus Sans ITC",14,"bold"))
    button_p4.grid(column=2, row=1, sticky=tk.W, padx=10, pady=10)
    button_p4.place(x=650, y=520)

    quitWindow = tk.Button(tab1, text="Quit", command=root.destroy,width=15,height=2,background="purple3",foreground="snow",font=("Tempus Sans ITC",14,"bold"))
    quitWindow.place(x=850, y=520)

    root.mainloop()
main()