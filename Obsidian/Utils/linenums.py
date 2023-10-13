from tkinter import *
from tklinenums import TkLineNumbers

class linenums(TkLineNumbers):
    def __init__(self, master, textwidget):
        super().__init__(master, textwidget)
        self.configure(bd=0)
        self.bind("<<Modified>>", lambda event: master.after_idle(linenums.redraw), add=True)