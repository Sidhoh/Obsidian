import tkinter as tk

class TextPeer(tk.Text):
    """"used from https://stackoverflow.com/a/58290100"""
    """A peer of an existing text widget"""
    count = 0
    def __init__(self, master, cnf={}, **kw):
        TextPeer.count += 1
        parent = master.master
        peerName = "peer-{}".format(TextPeer.count)
        if str(parent) == ".":
            peerPath = ".{}".format(peerName)
        else:
            peerPath = "{}.{}".format(parent, peerName)
        master.tk.call(master, 'peer', 'create', peerPath, *self._options(cnf, kw))
        tk.BaseWidget._setup(self, parent, {'name': peerName})