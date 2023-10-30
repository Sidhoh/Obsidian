from tkinter import *
from tklinenums import TkLineNumbers

class linenums(TkLineNumbers):
    def __init__(self, master, textwidget, *args, **kwargs):
        super().__init__(master, textwidget, *args, **kwargs)
        self.configure(bd=0)
        self.bind("<<Modified>>", lambda event: master.after_idle(linenums.redraw), add=True)