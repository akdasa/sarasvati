import tkinter.messagebox


def show(ex):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo("Sarasvati", ex.args[0])
