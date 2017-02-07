#!/usr/bin/python
"""
Search Algorithm Visualizer
"""

from space import Space, Type
from maps import input_file
from grid import blank_grid

from PIL import Image, ImageTk
from Tkinter import Tk, Text, TOP, BOTH, X, N, S, E, W, LEFT, RAISED, RIGHT
from ttk import Frame, Button, Label, Entry, Style

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Review")
        self.style = Style().configure("TFrame", background="#333")
        # self.style.theme_use("clam")

        tileImage = Image.open("tiles.png")
        tile = ImageTk.PhotoImage(tileImage)
        label1 = Label(self, image=tile)
        label1.image = tile
        label1.place(x=20, y=20)

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, pad=7)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(5, pad=7)

        lbl = Label(frame, text="Windows")
        lbl.grid(sticky=W, pady=4, padx=5)

        area = Text(frame)
        area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)

        abtn = Button(frame, text="Activate")
        abtn.grid(row=1, column=3)

        cbtn = Button(frame, text="Activate")
        cbtn.grid(row=2, column=3, pady=4)

        hbtn = Button(frame, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(frame, text="OK")
        obtn.grid(row=5, column=3)

        # for i in range(0,4):
            # frame.columnconfigure(i, pad=3)
        # for i in range(0,5):
            # frame.rowconfigure(i, pad=3)

        # entry = Entry(frame)
        # entry.grid(row=0, columnspan=4, sticky=W+E)
        # cls = Button(frame, text="Cls")
        # cls.grid(row=1, column=0)
        # bck = Button(frame, text="Back")
        # bck.grid(row=1, column=1)
        # lbl = Button(frame)
        # lbl.grid(row=1, column=2)
        # clo = Button(frame, text="Close")
        # clo.grid(row=1, column=3)
        # sev = Button(frame, text="7")
        # sev.grid(row=2, column=0)
        # eig = Button(frame, text="8")
        # eig.grid(row=2, column=1)
        # nin = Button(frame, text="9")
        # nin.grid(row=2, column=2)
        # div = Button(frame, text="/")
        # div.grid(row=2, column=3)

        # fou = Button(frame, text="4")
        # fou.grid(row=3, column=0)
        # fiv = Button(frame, text="5")
        # fiv.grid(row=3, column=1)
        # six = Button(frame, text="6")
        # six.grid(row=3, column=2)
        # mul = Button(frame, text="*")
        # mul.grid(row=3, column=3)

        # zer = Button(frame, text="0")
        # zer.grid(row=5, column=0)
        # dot = Button(frame, text=".")
        # dot.grid(row=5, column=1)
        # equ = Button(frame, text="=")
        # equ.grid(row=5, column=2)
        # pls = Button(frame, text="+")
        # pls.grid(row=5, column=3)

        self.pack(fill=BOTH, expand=True)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(self, text="OK")
        okButton.pack(side=RIGHT)

    def centerWindow(self):
        # TODO: Modify this to instead show second window to specific position
        w = 500
        h = 500
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    # root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
