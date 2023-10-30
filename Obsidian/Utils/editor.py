from tkinter import *
import idlelib.colorizer as ic
import idlelib.percolator as ip
import json

class editor(Text):
    def __init__(self, master, themepath=None,*args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.themepath = themepath
        theme = open(themepath, "r")
        colors = json.load(theme)        
        self.focus_set()
        self.configure(bg=colors['editorSelectedBackground'], bd=0,fg=colors['menuForeground'], wrap=NONE, highlightthickness=0, highlightcolor=colors['outlineColor'], selectbackground=colors['editorSelectedBackground'], font=("Consolas", 8), padx=0, pady=10)
        master.update_idletasks()
        height = int(master.winfo_screenheight())
        # Syntax Highlighting
        cdg = ic.ColorDelegator()
        cdg.tagdefs['COMMENT'] = {'foreground': colors['COMMENT'], 'background': colors['editorSelectedBackground']}
        cdg.tagdefs['KEYWORD'] = {'foreground': colors['KEYWORD'], 'background': colors['editorSelectedBackground']}
        cdg.tagdefs['BUILTIN'] = {'foreground': colors['BUILTIN'], 'background': colors['editorSelectedBackground']}
        cdg.tagdefs['STRING'] = {'foreground': colors['STRING'], 'background': colors['editorSelectedBackground']}
        cdg.tagdefs['DEFINITION'] = {'foreground': colors['DEFINITION'], 'background': colors['editorSelectedBackground']}
        cdg.tagdefs['NUMBER'] = {'foreground': colors['NUMBER'], 'background': colors['editorSelectedBackground']}
        ip.Percolator(self).insertfilter(cdg)