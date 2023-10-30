from tkinter import *
from ctypes import windll, wintypes
from tkinter import filedialog, ttk
from Utils.editor import editor
from Utils.linenums import linenums
import os, json, sys
from tkterminal import Terminal
from Utils.TextPeer import TextPeer

tk_title = "Obsidian"

root = Tk()
root.title(tk_title)
root.overrideredirect(True)
root.geometry("1000x650+75+75")
root.iconbitmap("Obsidian.ico")

root.minimized = False
root.maximized = False

tokyoLight = "./Themes/tokyo-light.json"
tokyoNight = "./Themes/tokyo-night.json"
with open('./themes/settings.json', 'r') as json_file:
    data = json.load(json_file)
themePath = data['themePath']
data['themePath'] = themePath
with open('./themes/settings.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

themeVal = open("./themes/settings.json", "r")
tpath = json.load(themeVal)
theme = open(tpath['themePath'], "r")
colors = json.load(theme)
altBackground = colors['altBackground']
selectedBackground = colors['selectedBackground']
activeBackground = colors['activeBackground']
outlineColor = colors['outlineColor']
menuForeground = colors['menuForeground']
hoverColor = colors['hoverColor']

Saved = False
opSaved = False
opPath = ""
path = ""
ofPath = ""

root.config(background=altBackground)
title_bar = Frame(root, bg=altBackground, bd=0, highlightbackground=outlineColor, highlightthickness=1)
layout = Frame(root, background=outlineColor)
ttk.Style().theme_use("default")
style = ttk.Style()
style.configure("Custom.Treeview", background=altBackground, foreground=colors['menuForeground'], fieldbackground=altBackground, borderwidth=0, font=("Segoi UI", 8))
style.map("Custom.Treeview", background=[('selected', colors['selectedBackground'])], foreground=[('selected', menuForeground)])

def set_appwindow(mainWindow):
    GWL_EXSTYLE=-20
    WS_EX_APPWINDOW=0x00040000
    WS_EX_TOOLWINDOW=0x00000080
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    root.withdraw()
    root.after(10, lambda:root.wm_deiconify())

    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())


def minimize_me():
    root.attributes("-alpha", 0)
    root.minimized = True
    root.bind("<FocusIn>", deminimize)


def deminimize(event):
    root.attributes("-alpha", 1)
    if root.minimized == True:
        root.minimized = False


def maximize_me():
    root.update()
    if root.maximized == False:  # if the window was not maximized
        root.update_idletasks()
        root.normal_size = root.geometry()
        expand_button.config(text="\ueabb")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.maximized = not root.maximized

    else:  # if the window was maximized
        root.update_idletasks()
        expand_button.config(text="\ueab9")
        root.geometry(root.normal_size)
        root.maximized = not root.maximized


def on_click(event):
    global _edit
    global _file
    global isOpen

    _file = False
    _edit = False
    file_frame.place_forget()
    edit_frame.place_forget()
    setting_frame.place_forget()
    themeList.place_forget()
    isOpen = False

def settings():
    setting_frame.place(x=132, y=-24, relx=0, rely=1, anchor="s")

isOpenTL = False
def themepicker():
    global isOpenTL
    global themePath
    if isOpenTL == False:
        themeList.place(x=277, y=-24, relx=0, rely=1, anchor="s")
        isOpenTL = True
    elif isOpenTL == True:
        themeList.place_forget()
        isOpenTL = False

isOpenT = False
def openTerminal():
    global isOpenT
    if isOpenT == False:
        terminalFram.grid(row=2, columnspan=3, column=2, sticky='nesw', padx=(1,1), pady=(1,0))
        statusbar.grid(row=3, columnspan=5, sticky='nesw')
        fileSystem.grid(rowspan=3,row=0, column=1, sticky="nsew")
        sidePanel.grid(rowspan=3, row=0, column=0, sticky="nsew")
        isOpenT = True
    elif isOpenT == True:
        terminalFram.grid_forget()
        isOpenT = False

layout.columnconfigure(1, weight=1)
layout.columnconfigure(3, weight=1000)
layout.rowconfigure(0, weight=0)
layout.rowconfigure(1, weight=100)

# Tabs
tabs = Frame(layout ,background=outlineColor, height=30)
tabFill = Label(tabs, padx=5, pady=5, background=altBackground, bd=0)
tabFill.pack(side=RIGHT, fill=BOTH, expand=True, padx=(1,0), pady=(0,1))

# TextBox
def mousewheel(evt):
    editor.yview_scroll(int(-1*(evt.delta/110)), 'units')
    minimap.yview_scroll(int(-1*(evt.delta/120)), 'units')

editor = editor(layout, themepath=themePath)
editor.bind_class("Text", '<MouseWheel>', mousewheel)
linenums = linenums(layout ,editor)
minimap = TextPeer(editor, width=45, height=8, background=colors["editorSelectedBackground"], font=("Consolas", 3), fg=menuForeground)
minimap.config(state=DISABLED, wrap=NONE, highlightthickness=0, padx=5, pady=10, bd=0, relief=RIDGE, cursor="arrow")

# Terminal
terminalFram = Frame(layout, background=altBackground, bd=0, width=200, height=200)
termLabel = Label(terminalFram, text="TERMINAL", anchor=W, font=("Consolas", 7), height=0, bg=altBackground, fg=menuForeground)
termLabel.pack(anchor=NW, padx=10, pady=5)
terminal = Terminal(terminalFram, bg=altBackground,fg=menuForeground, bd=0, yscrollcommand=Scrollbar().set, height=11, selectbackground=colors['editorSelectedBackground'], font=("Consolas", 8))
terminal.shell = True
Termpath = ">"
terminal.basename = Termpath
terminal.pack(fill=X, padx=10, pady=5)

# Status Bar
statusbar = Frame(layout, background=altBackground, bd=0, height=15, highlightbackground=outlineColor, highlightthickness=1, highlightcolor=outlineColor)
statusbar.grid(row=2, columnspan=5, sticky='nesw')
termialSB = Button(statusbar, command=openTerminal, text="\uebca", width=7, height=2, bg="#3d59a1", bd=0, fg=menuForeground, font=("codicon", 7, "bold"), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
notifcationSB = Button(statusbar, text="\ueaa2", width=7, height=2, bg=altBackground, bd=0, fg=menuForeground, font=("codicon", 7), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
termialSB.pack(side=LEFT)
notifcationSB.pack(side=RIGHT)

# File Tree
fileSystem = Frame(layout, background=altBackground, bd=0, highlightcolor=altBackground, highlightthickness=0, width=180)
fileSystem.grid(rowspan=2,row=0, column=1, sticky="nsew")
ExpLabel = Label(layout, text="EXPLORER", anchor=W, justify=LEFT, font=("Consolas", 8), height=0, bg=altBackground, fg=menuForeground)
root.update_idletasks()
width = int(layout.winfo_width() - 200)
ExpLabel.configure(width=width)
ExpLabel.place(x=50, y=11)

# Side Panel
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def lighttheme():
    themePath = tokyoLight
    with open('./themes/settings.json', 'r') as json_file:
        data = json.load(json_file)
    data['themePath'] = themePath
    with open('./themes/settings.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    themeList.place_forget()
    restart_program()

def darktheme():
    themePath = tokyoNight
    with open('./themes/settings.json', 'r') as json_file:
        data = json.load(json_file)
    data['themePath'] = themePath
    with open('./themes/settings.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    themeList.place_forget()
    restart_program()

sidePanel = Frame(layout, background=altBackground, bd=0,width=8)
sidePanel.grid(rowspan=2, row=0, column=0, sticky="nsew", padx=(1,0))
themeList = Frame(root, background=altBackground, width=200, height=161, bd=0, highlightbackground=outlineColor, highlightthickness=1, padx=3, pady=3)
tkNight = Button(themeList, command=darktheme,text="Tokyo Night", bg=altBackground, padx=15, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
tkLight = Button(themeList, command=lighttheme, text="Tokyo Light", bg=altBackground, padx=15, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
tkLight.pack()
tkNight.pack()

Files = Button(sidePanel, text="\ueaf0", width=5, height=2, bg=altBackground, bd=0, fg=menuForeground, font=("codicon", 11), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
Files.pack()
finder = Button(sidePanel, text="\uea6d", width=5, height=2, bg=altBackground, bd=0, fg=menuForeground, font=("codicon", 11), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
finder.pack()
settings = Button(sidePanel, text="\ueb51", width=5, height=2, bg=altBackground, bd=0, fg=menuForeground, font=("codicon", 11), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN, command=settings)
settings.pack(side=BOTTOM)
setting_frame = Frame(root, background=altBackground, width=200, height=161, bd=0, highlightbackground=outlineColor, highlightthickness=1, padx=3, pady=3)
themes_btn = Button(setting_frame, command=themepicker, text="Themes                                   \ueab6", bg=altBackground, padx=15, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
shortcuts_btn = Button(setting_frame, text="Keyboard Shortcuts                  ", bg=altBackground, padx=15, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
terminal_btn = Button(setting_frame, command=openTerminal, text="Terminal                                     ", bg=altBackground, padx=15, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
cmdPalette_btn = Button(setting_frame, text="Command Palette                       ", bg=altBackground, padx=15, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
cmdPalette_btn.pack()
terminal_btn.pack()
shortcuts_btn.pack()
themes_btn.pack()

editor.bind("<Button-1>", on_click)
fileSystem.bind("<Button-1>", on_click)
sidePanel.bind("<Button-1>", on_click)

# Menu Bar
def filetree(directory, tree):
    ybar = Scrollbar(fileSystem, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=ybar.set)
    path = os.path.abspath(directory)
    node = tree.insert("", "end", text=path, open=True, values=(path))
    heading = Label(fileSystem, text=os.path.basename(directory).upper(), anchor=W, justify=LEFT, bg=altBackground, foreground=menuForeground, font=("Segoi UI", 8), height=0, pady=2)
    root.update_idletasks()
    width = int(layout.winfo_width() - 200)
    heading.configure(width=width)
    heading.place(x=15, y=31)

    def selectItem(event):
        global path
        global Saved
        global ofPath
    
        item = tree.identify_row(event.y)

        def is_child(tree, item):
            children = tree.get_children(item)
            return bool(children)

        if item:
            # Check if the clicked item is a child item (not a parent or separator)
            if is_child(tree, item):
                pass
            else:
                def tabClick(item):
                    global path
                    f = open(full_path, "r", encoding="utf8")
                    content = f.read()
                    editor.delete("1.0", END)
                    editor.insert(END, content)
                    tree.selection_set(item)
                    path = full_path
                    
                item = tree.selection()[0]
                full_path = tree.item(item, "text")
                parent_item = tree.parent(item)
                print(full_path)
                while parent_item:
                    full_path = tree.item(parent_item, "text") + r"\ "[0] + full_path
                    parent_item = tree.parent(parent_item)

                print(full_path)
                print(ofPath)
                f = open(full_path, "r", encoding="utf8")
                content = f.read()
                editor.delete("1.0", END)
                editor.insert(END, content)
                path = full_path
                Saved = True
                fileName = os.path.basename(full_path)
                tabTitle = Button(tabs, command=lambda item_id=item: tabClick(item_id),text=fileName, padx=8, pady=2, background=altBackground, fg=menuForeground, relief=SUNKEN, bd=0,font=("Segoi UI", 10), activebackground=selectedBackground, activeforeground="#fff")
                tabTitle.pack(side=LEFT, padx=(1,0), pady=(0,1))



    def traverse_dir(parent, path):
        for d in os.listdir(path):
            full_path = os.path.join(path, d)
            isdir = os.path.isdir(full_path)
            id = tree.insert(parent, "end", text=d, open=False)
            tree.bind("<Double-Button-1>", selectItem)
            if isdir:
                traverse_dir(id, full_path)

    traverse_dir(node, path)
    tree.place(x=0, y=33)
    root.update_idletasks()
    height = int(root.winfo_screenheight())
    tree.configure(height=height)

def _NText_file():
    global _file
    editor.grid(row=0, column=3, sticky="nsew")
    linenums.grid(row=0, column=2, sticky="nsew")
    minimap.grid(row=0, column=4, sticky="nsew")
    _file = False
    file_frame.place_forget()
    pass

def _New_File():
    global path
    global Saved
    global opSaved
    global Termpath
    global _file

    path = filedialog.asksaveasfilename()
    f = open(path, "w+")
    content = f.read()
    editor.insert(END, content)
    print("Saved @ " + path)
    tree_OF = ttk.Treeview(fileSystem, show="tree", style="Custom.Treeview")
    tree_OF.bind("<Button-1>", on_click)
    filetree(os.path.dirname(path), tree_OF)
    Saved = TRUE
    Termpath = path
    opSaved = False
    _file = False
    file_frame.place_forget()
    tabs.grid(row=0, column=2, columnspan=4, sticky="nsew")
    editor.grid(row=1, column=3, sticky="nsew")
    linenums.grid(row=1, column=2, sticky="nsew")
    minimap.grid(row=1, column=4, sticky="nsew")
    welcomeScreen.grid_forget()

def _Open_File():
    global opSaved
    global opPath
    global Saved
    global Termpath
    global Terminal
    global _file

    opPath = filedialog.askopenfilename()
    f = open(opPath, "r", encoding="utf8")
    content = f.read()
    editor.delete("1.0", END)
    editor.insert(END, content)
    opSaved = True
    Saved = False
    Termpath = opPath
    terminal.basename = Termpath + ">"
    terminal.run_command(cmd="cd "+ofPath)
    print(Termpath)
    print(opSaved)
    for widget in fileSystem.winfo_children():
        widget.destroy()
    tree_OF = ttk.Treeview(fileSystem, show="tree", style="Custom.Treeview")
    tree_OF.bind("<Button-1>", on_click)
    filetree(os.path.dirname(opPath), tree_OF)
    _file = False
    file_frame.place_forget()
    editor.grid(row=0, column=3, sticky="nsew")
    linenums.grid(row=0, column=2, sticky="nsew")
    minimap.grid(row=0, column=4, sticky="nsew")
    welcomeScreen.grid_forget()

def _Save_File():
    global Saved
    global opPath
    global opSaved
    global path
    global _file

    print(opSaved)
    print(Saved)
    
    if Saved == False:
        if opSaved == False:
            path = filedialog.asksaveasfilename()
            f = open(path, "w", encoding="utf8")
            conent = editor.get(1.0, "end-1c")
            f.write(conent)
            print("Saved @ " + path)
            Saved = True
        else:
            f = open(opPath, "w")
            conent = editor.get(1.0, "end-1c")
            f.write(conent)
            print("Saved @ " + path)
            print("hh")
            Saved = True
    elif Saved == True:
        if opSaved == True:
            f = open(opPath, "w", encoding="utf8")
            conent = editor.get(1.0, "end")
            f.write(conent)
            print("Saved @ " + path)
            print("hh")
            Saved = True
        else:
            f = open(path, "w", encoding="utf8")
            conent = editor.get(1.0, "end-1c")
            f.write(conent)
            print("Saved @ " + path)
    elif opSaved == True:
        f = open(opPath, "w")
        conent = editor.get(1.0, "end-1c")
        f.write(conent)
        print("Saved @ " + opPath)
    else:
        pass
    _file = False
    file_frame.place_forget()
    welcomeScreen.grid_forget()

def _Save_As():
    global Saved
    global path
    global opSaved
    global _file

    path = filedialog.asksaveasfilename()
    f = open(path, "w", encoding="utf8")
    conent = editor.get(1.0, "end-1c")
    f.write(conent)
    print("Saved @ " + path)
    print("hh")
    Saved = True
    opSaved = False
    file_frame.place_forget()
    _file = False

def _Open_folder():
    global ofPath
    global Saved
    global path
    global Termpath
    global Terminal
    global _file

    for widget in fileSystem.winfo_children():
        widget.destroy()
    ofPath = filedialog.askdirectory()
    tree_OF = ttk.Treeview(fileSystem, show="tree", style="Custom.Treeview")
    tree_OF.bind("<Button-1>", on_click)
    filetree(ofPath, tree_OF)
    Termpath = ofPath+ ">"
    terminal.run_command(cmd="cd "+ofPath)
    terminal.basename = Termpath
    _file = False
    file_frame.place_forget()
    tabs.grid(row=0, column=2, columnspan=4, sticky="nsew")
    editor.grid(row=1, column=3, sticky="nsew")
    linenums.grid(row=1, column=2, sticky="nsew", padx=(1,0))
    minimap.grid(row=1, column=4, sticky="nsew", padx=(1,1))
    welcomeScreen.grid_forget()
    
file_frame = Frame(root, background=altBackground, width=200, height=161, bd=0, highlightbackground=outlineColor, highlightthickness=1,)
NText_file = Button(file_frame, command=_NText_file, text="New Text File                    Ctrl + N", bg=altBackground, padx=15, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
New_file = Button(file_frame, command=_New_File, text="New File                    Ctrl + Alt + N", bg=altBackground, padx=14, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
Open_file = Button(file_frame, command=_Open_File, text="Open File                           Ctrl + O", bg=altBackground, padx=14, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
Open_folder = Button(file_frame, command=_Open_folder, text="Open Folder                       Ctrl + K", bg=altBackground, padx=14, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
save = Button(file_frame, command=_Save_File, text="Save                                  Ctrl + S", bg=altBackground, padx=14, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
save_as = Button(file_frame, command=_Save_As, text="Save As                 Ctrl + Shift + S", bg=altBackground, padx=14, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
exit = Button(file_frame, text="Exit                                                ", bg=altBackground, padx=14, pady=2, bd=0, fg=menuForeground, font=("Segoi UI", 8), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN, command=root.destroy)

NText_file.place(x=3, y=3)
New_file.place(x=3, y=25)
Open_file.place(x=3, y=47)
Open_folder.place(x=3, y=69)
save.place(x=3, y=91)
save_as.place(x=3, y=113)
exit.place(x=3, y=135)

# Welcome Screen
welcomeScreen = Frame(layout, bg=colors['editorSelectedBackground'])
welcomeTitle1 = Label(welcomeScreen, text="Obsidian", font=("Consolas", 13, 'bold'), fg=menuForeground, bg=colors['editorSelectedBackground'])
welcomeTitle2 = Label(welcomeScreen, text="Made with ❤️", font=("Consolas", 12), fg=menuForeground, bg=colors['editorSelectedBackground'])
welcomeStart = Label(welcomeScreen, text="Start", font=("Consolas", 11), fg=menuForeground, bg=colors['editorSelectedBackground'])
NFileW = Button(welcomeScreen, command=_New_File ,text="\uea7f New File", bg=colors['editorSelectedBackground'], bd=0, fg="#3d59a1", font=("Consolas", 9), highlightthickness=0, activebackground=colors['editorSelectedBackground'], activeforeground="#7dcfff", relief=SUNKEN)
OFileW = Button(welcomeScreen, command=_Open_File ,text="\uea94 Open File", bg=colors['editorSelectedBackground'], bd=0, fg="#3d59a1", font=("Consolas", 9), highlightthickness=0, activebackground=colors['editorSelectedBackground'], activeforeground="#7dcfff", relief=SUNKEN)
OFolderW = Button(welcomeScreen, command=_Open_folder ,text="\ueaf7 Open Folder", bg=colors['editorSelectedBackground'], bd=0, fg="#3d59a1", font=("Consolas", 9), highlightthickness=0, activebackground=colors['editorSelectedBackground'], activeforeground="#7dcfff", relief=SUNKEN)
welcomeScreen.bind("<Button-1>", on_click)
welcomeTitle1.place(x=50, y=70)
welcomeTitle2.place(x=50, y=95)
welcomeStart.place(x=50, y=150)
NFileW.place(x=50, y=180)
OFileW.place(x=50, y=200)
OFolderW.place(x=50, y=220)
welcomeScreen.grid(row=1, column=3, sticky="nsew", padx=(1,1))

_file = False
edit_frame = Frame(root, background=altBackground, width=200, height=250, bd=0, highlightbackground=outlineColor, highlightthickness=1)
_edit = False

# Menu Function


def file():
    global file_frame
    global _file
    global _edit
    if _file == False:
        file_frame.place(x=0, y=32)
        _file = True
        _edit = False
        edit_frame.place_forget()
    elif _file == True:
        _file = False
        file_frame.place_forget()


# Menu Function
def edit():
    global edit_frame
    global _edit
    global _file
    if _edit == False:
        edit_frame.place(x=45, y=32)
        _edit = True
        _file = False
        file_frame.place_forget()
    elif _edit == True:
        _edit = False
        edit_frame.place_forget()


# Title bar
close_button = Button(title_bar, text="\ueab8", command=root.destroy, bg=altBackground, fg=menuForeground, padx=2, pady=2, font=("codicon", 13), bd=0, highlightthickness=0, relief=SUNKEN, activebackground="#990b17")
expand_button = Button(title_bar, text="\ueab9", command=maximize_me, bg=altBackground, padx=2, pady=2, bd=0, fg=menuForeground, font=("codicon", 13), highlightthickness=0, relief=SUNKEN, activebackground=selectedBackground)
minimize_button = Button(title_bar, text="\ueaba", command=minimize_me, bg=altBackground, padx=2, pady=2, bd=0, fg=menuForeground, font=("codicon", 13), highlightthickness=0, relief=SUNKEN, activebackground=selectedBackground)

# Menu Bar
file_button = Button(title_bar, command=file, text="File", bg=altBackground, padx=2, pady=5, bd=0, fg=menuForeground, font=("Segoi UI", 9), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
edit_button = Button(title_bar, command=edit, text="Edit", bg=altBackground, padx=2, pady=5, bd=0, fg=menuForeground, font=("Segoi UI", 9), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)
help_button = Button(title_bar, text="Help", bg=altBackground, padx=2, pady=5, bd=0, fg=menuForeground, font=("Segoi UI", 9), highlightthickness=0, activebackground=selectedBackground, activeforeground="#fff", relief=SUNKEN)

#FS
openFolderFS = Button(fileSystem, command=_Open_folder, text="Open Folder", bg="#3d59a1", padx=2, pady=5, width=20, bd=0, fg="white", font=("Segoi UI", 8), highlightthickness=0, activebackground="#304376", activeforeground="#fff", relief=SUNKEN)
openFolderFS.place(x=20, y=50)

# pack the widgets
title_bar.pack(fill=X)
layout.pack(fill=BOTH, expand=True)
close_button.pack(side=RIGHT, ipadx=7, ipady=1)
expand_button.pack(side=RIGHT, ipadx=7, ipady=1)
minimize_button.pack(side=RIGHT, ipadx=7, ipady=1)
file_button.pack(side=LEFT, ipadx=7, ipady=1)
edit_button.pack(side=LEFT, ipadx=7, ipady=1)
help_button.pack(side=LEFT, ipadx=7, ipady=1)

def changex_on_hovering(event):
    global close_button
    close_button["bg"] = "red"
def returnx_to_normalstate(event):
    global close_button
    close_button["bg"] = altBackground

def changen_size_on_hovering(event):
    global expand_button
    expand_button["bg"] = hoverColor
def return_size_on_hovering(event):
    global expand_button
    expand_button["bg"] = altBackground

def changem_size_on_hovering(event):
    global minimize_button
    minimize_button["bg"] = hoverColor
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button["bg"] = altBackground

def changef_size_on_hovering(event):
    global file_button
    file_button["bg"] = hoverColor
def returnf_size_on_hovering(event):
    global file_button
    file_button["bg"] = altBackground

def changee_size_on_hovering(event):
    global edit_button
    edit_button["bg"] = hoverColor
def returne_size_on_hovering(event):
    global edit_button
    edit_button["bg"] = altBackground

def changeh_size_on_hovering(event):
    global help_button
    help_button["bg"] = hoverColor
def returnh_size_on_hovering(event):
    global help_button
    help_button["bg"] = altBackground

def changeNTF_size_on_hovering(event):
    global NText_file
    NText_file["bg"] = hoverColor
def returnNTF_size_on_hovering(event):
    global NText_file
    NText_file["bg"] = altBackground

def changeNF_size_on_hovering(event):
    global New_file
    New_file["bg"] = hoverColor
def returnNF_size_on_hovering(event):
    global New_file
    New_file["bg"] = altBackground

def changeOF_size_on_hovering(event):
    global Open_file
    Open_file["bg"] = hoverColor
def returnOF_size_on_hovering(event):
    global Open_file
    Open_file["bg"] = altBackground

def changeOFD_size_on_hovering(event):
    global Open_folder
    Open_folder["bg"] = hoverColor
def returnOFD_size_on_hovering(event):
    global Open_folder
    Open_folder["bg"] = altBackground

def changeS_size_on_hovering(event):
    global save
    save["bg"] = hoverColor
def returnS_size_on_hovering(event):
    global save
    save["bg"] = altBackground

def changeSA_size_on_hovering(event):
    global save_as
    save_as["bg"] = hoverColor
def returnSA_size_on_hovering(event):
    global save_as
    save_as["bg"] = altBackground

def changeE_size_on_hovering(event):
    global exit
    exit["bg"] = hoverColor
def returnE_size_on_hovering(event):
    global exit
    exit["bg"] = altBackground

def changeFls_size_on_hovering(event):
    global Files
    Files["bg"] = hoverColor
def returnFls_size_on_hovering(event):
    global Files
    Files["bg"] = altBackground

def changeFd_size_on_hovering(event):
    global finder
    finder["bg"] = hoverColor
def returnFd_size_on_hovering(event):
    global finder
    finder["bg"] = altBackground

def changeSt_size_on_hovering(event):
    global settings
    settings["bg"] = hoverColor
def returnSt_size_on_hovering(event):
    global settings
    settings["bg"] = altBackground

def get_pos(event):
    if root.maximized == False:
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):  # runs when window is dragged
            root.config(cursor="fleur")
            root.geometry(f"+{event.x_root + xwin}+{event.y_root + ywin}")

        def release_window(event):  # runs when window is released
            root.config(cursor="arrow")

        title_bar.bind("<B1-Motion>", move_window)
        title_bar.bind("<ButtonRelease-1>", release_window)


title_bar.bind("<Button-1>", get_pos)

# button effects in the title bar when hovering over buttons
close_button.bind("<Enter>", changex_on_hovering)
close_button.bind("<Leave>", returnx_to_normalstate)
expand_button.bind("<Enter>", changen_size_on_hovering)
expand_button.bind("<Leave>", return_size_on_hovering)
minimize_button.bind("<Enter>", changem_size_on_hovering)
minimize_button.bind("<Leave>", returnm_size_on_hovering)
file_button.bind("<Enter>", changef_size_on_hovering)
file_button.bind("<Leave>", returnf_size_on_hovering)
edit_button.bind("<Enter>", changee_size_on_hovering)
edit_button.bind("<Leave>", returne_size_on_hovering)
help_button.bind("<Enter>", changeh_size_on_hovering)
help_button.bind("<Leave>", returnh_size_on_hovering)
NText_file.bind("<Enter>", changeNTF_size_on_hovering)
NText_file.bind("<Leave>", returnNTF_size_on_hovering)
New_file.bind("<Enter>", changeNF_size_on_hovering)
New_file.bind("<Leave>", returnNF_size_on_hovering)
Open_file.bind("<Enter>", changeOF_size_on_hovering)
Open_file.bind("<Leave>", returnOF_size_on_hovering)
Open_folder.bind("<Enter>", changeOFD_size_on_hovering)
Open_folder.bind("<Leave>", returnOFD_size_on_hovering)
save.bind("<Enter>", changeS_size_on_hovering)
save.bind("<Leave>", returnS_size_on_hovering)
save_as.bind("<Enter>", changeSA_size_on_hovering)
save_as.bind("<Leave>", returnSA_size_on_hovering)
exit.bind("<Enter>", changeE_size_on_hovering)
exit.bind("<Leave>", returnE_size_on_hovering)
Files.bind("<Enter>", changeFls_size_on_hovering)
Files.bind("<Leave>", returnFls_size_on_hovering)
finder.bind("<Enter>", changeFd_size_on_hovering)
finder.bind("<Leave>", returnFd_size_on_hovering)
settings.bind("<Enter>", changeSt_size_on_hovering)
settings.bind("<Leave>", returnSt_size_on_hovering)

root.bind("<Control-`>", lambda event: openTerminal())
root.bind("<Control-n>", lambda event: _NText_file())
root.bind("<Control-Alt-n>", lambda event: _New_File())
root.bind("<Control-o>", lambda event: _Open_File())
root.bind("<Control-k>", lambda event: _Open_folder())
root.bind("<Control-s>", lambda event: _Save_File())
root.bind("<KeyPress-S>", lambda event: _Save_As())

root.after(10, lambda: set_appwindow(root))
root.mainloop()