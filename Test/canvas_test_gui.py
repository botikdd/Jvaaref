import tkinter

class Test:
    def __init__(self, master):
        master.geometry('{}x{}-1+0'.format(master.winfo_screenwidth(),\
                                           master.winfo_screenheight() - 75))
        self.canvas = tkinter.Canvas(master, width=master.winfo_screenwidth(),\
        height=master.winfo_screenheight() - 175, bg='black')
        self.canvas.pack(expand='yes', fill='both')
        self.photo = tkinter.PhotoImage(file = './Resources/audi.png')

        self.photo2 = tkinter.PhotoImage(file = './Resources/audi.png')
        self.canvas.create_image(1025, 500, image=self.photo)
        self.canvas.create_image(0, 0, image=self.photo2)

root = tkinter.Tk()
test = Test(root)
root.mainloop()