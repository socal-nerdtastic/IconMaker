#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#

import os
import base64
import io
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import ttk

PIL = False

# remove this try block to force direct conversion mode.
try:
    from PIL import Image, ImageTk
    PIL = True
except ImportError:
    pass
###

FILETYPES = (
    ("Image files",
        ("*.jpg", "*.jpeg", "*.gif", "*.png", )
        ),
    ("All files","*.*"))

TEMPLATE = r"""#!/usr/bin/env python3

import tkinter as tk

def apply_icon(w):
    try:
        icon = tk.PhotoImage(data=icondata)
        w.iconphoto(True, icon)
    except Exception as e:
        print("Could not load icon due to:\n  ",e)

def main():
    root = tk.Tk()
    apply_icon(root)
    root.geometry('200x200')

    # YOUR CODE HERE!!
    lbl = tk.Label(root, text="Icon test program")
    lbl.pack()

    root.mainloop()

icondata = '''
{data}'''

if __name__ == '__main__':
    main()
"""

def pip_install_popup():
    INSTALL = "pillow"
    from subprocess import Popen, PIPE
    import sys
    import threading
    from tkinter.scrolledtext import ScrolledText

    def pipe_reader(pipe, term=False):
        for line in iter(pipe.readline, b''):
            st.insert(tk.END, line)
            st.see(tk.END)
        if term:
            tk.Label(popup, fg='red', text="DONE. Restart required.", font=('bold',14)).pack()
            ttk.Button(popup, text="Exit program", command=sys.exit).pack()

    popup = tk.Toplevel()
    tk.Label(popup, text="Installing: "+INSTALL, font=('bold',14)).pack()
    st= ScrolledText(popup, width=60, height=12)
    st.pack()
    sub_proc = Popen([sys.executable, '-m','pip', 'install', INSTALL], stdout=PIPE, stderr=PIPE)
    threading.Thread(target=pipe_reader, args=[sub_proc.stdout]).start()
    threading.Thread(target=pipe_reader, args=[sub_proc.stderr, True]).start()

class GUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.path = None

        self.warn_lbl = tk.Label(self, fg='red')
        self.warn_lbl.grid(columnspan=2)
        if not PIL:
            self.warn_lbl.config(text="Pillow (PIL) not installed, only small .gif files will work")
            btn = ttk.Button(self, text="Install Pillow", command=pip_install_popup)
            btn.grid()
        lbl = tk.Label(self, text='Choose an image file')
        lbl.grid()
        btn = ttk.Button(self, text="browse", command=self.browse)
        btn.grid()
        self.fn = tk.StringVar()
        self.ent = tk.Entry(self, textvariable=self.fn)
        self.ent.grid(sticky='ew')
        self.resize = tk.BooleanVar(value=True)
        resize = tk.Checkbutton(self, text="Resize?", variable=self.resize)
        resize.grid(sticky='w')
        subframe = tk.Frame(self)
        subframe.grid(sticky='w')
        lbl = tk.Label(subframe, text="Size:")
        lbl.pack(side=tk.LEFT)
        self.size = tk.IntVar(value=64)
        size = tk.Entry(subframe, textvariable=self.size, width=3)
        size.pack(side=tk.LEFT)
        lbl = tk.Label(subframe, text="pixels")
        lbl.pack(side=tk.LEFT)
        btn = ttk.Button(self, text='Recalculate', command=self.calculate)
        btn.grid()
        btn = ttk.Button(self, text='Copy data out', command=self.copy_data)
        btn.grid()
        btn = ttk.Button(self, text='Save data file', command=self.save_data)
        btn.grid()

        self.disp_lbl = tk.Label(self, text='image')
        self.disp_lbl.grid()
        cols, rows = self.grid_size()
        self.rowconfigure(rows-1, weight=1)
        self.st = ScrolledText(self, width=80)
        self.st.grid(row=1, column=1, rowspan=rows)

    def save_data(self):
        fn = filedialog.asksaveasfilename(filetypes=(("Python file", "*.py"),))
        if not fn: return # user cancelled
        data = self.st.get('0.0', tk.END)
        with open(fn, 'w') as f:
            f.write(data)
        self.warn_lbl.config(text="Data saved.")

    def copy_data(self):
        data = self.st.get('0.0', tk.END)
        self.clipboard_clear()
        self.clipboard_append(data)
        self.warn_lbl.config(text="Data copied.")

    def browse(self):
        self.path = filedialog.askopenfilename(filetypes=FILETYPES)
        if not self.path: return # user cancel
        _, name = os.path.split(self.path)
        self.fn.set(name)
        self.calculate()

    def calculate(self):
        if not self.path:
            self.warn_lbl.config(text="No file loaded")
            return
        self.warn_lbl.config(text="")
        try:
            if PIL:
                img = Image.open(self.path)

                if self.resize.get():
                    size = self.size.get()
                    img = img.resize((size, size)) # assume a square

                self.pi = ImageTk.PhotoImage(img)
                f = io.BytesIO()
                img.save(f, format='GIF')
                b64_img = base64.encodebytes(f.getvalue())
            else:
                self.pi = tk.PhotoImage(file=self.path)
                with open(self.path, 'rb') as f:
                    b64_img = base64.encodebytes(f.read())

            self.disp_lbl.config(image=self.pi)
            self.st.delete('0.0', tk.END)
            self.st.insert(tk.END, TEMPLATE.format(data=b64_img.decode()))
            self.warn_lbl.config(text="Done. Data is {} lines ({:,} bytes).".format(b64_img.count(b'\n'), len(b64_img)))

        except Exception as e:
            self.warn_lbl.config(text=e)
            raise

def apply_icon(w):
    try:
        icon = tk.PhotoImage(data=icondata)
        w.iconphoto(True, icon)
    except Exception as e:
        print("Could not load icon due to:\n  ",e)

def main():
    root = tk.Tk()
    apply_icon(root)
    window = GUI(root)
    window.pack()
    root.mainloop()

icondata = '''
R0lGODlhQABAAIf/AAABAAcAAAkBABAAAAIFAQsDAhYAAwQHAiEAAAUIBB4CACUAAwcJBQ4HBSkA
AC4AAQgLBzEAAjIAAAoMCAsNChEMCgwPCz0CAkUAAA4QDEsAADsGARUQDxASD1UAAFACAFgBAxMU
EmAAAVoCAGgAABcYFm0BAHYAACkWCSkVFC0UFRkbGH0AAIEAAC0YGHoEADIXGYkAAoMCAIwAAIQD
AC8aGh8fGI0BAJMAADAbG5QAAZUAAo4DADEeDpkCADUhEiImKCYoJSUpKzUnGigsLj0oGSYuKiwt
K0crEy4wLTMyKzczMjc5Njs6M0Q8MkE8O0A/OEA+QjtAQkM/PjxBQ2A7Hz9DRV0+IERDPEBERkJG
SGBBKEdHP2BGK0xLRE5KSV1JMU1MRU5ORk9PR0xRSFVSRkxUUE5US1FTUGFWRlRYW3xSMF9cT1hd
X4JYNV9fV15iU2RhVFhjZGtgT2BiX15jZZBeOJJfM2tmZWlraG9sX2ttam5wbW1xdHByb6drOnN1
cnF1eHN5cHR4e3l+gHx+e4J/cXuBd7V2P7Z4R4SGg4yJe4iLfI2KfMiARIeMj4qNfo+MfoyPgI6R
goyQk6WOc5CThMuJUdGITJaZitGOUJWanJqdjdqQVJidn5ufj5ygkJ2fnJ6ikqGjoKSlj6ClqOeb
V7Goj6mrqPahWauwsrCxnPOlYbC0pPulXbO0nvanXfymXv6oYP+pYba4tfStbPysYu2vefavbv+v
ZLy9p7q8uf60Z/i4e/+5ecTGw8PIy8jKx8rMyf/Ehc7PuNDSz9PUvtLU0dPV0tTW09HX2dbY1dna
w9ja19zdx9vd2tze29/gyvPeuuHizOPkzeHj4PbhvOjj4uPl4ebn0OXn5PPnxunq0+fp5vbqyenr
6Ovu6u3v6/Hy2/7wye/x7vLz3PDy7/fx8PHz8PT13vL08fP18vb34Pn32vT38/f44fj54vb49Pn6
4/761vz63fj69/v85f783/n7+Pz95v/94Pr8+f/+7/z/7///6Pz++yH+EUNyZWF0ZWQgd2l0aCBH
SU1QACwAAAAAQABAAEAI/wDJCRxIsKBBgurUNVu4bBk6dOQiSpxIsaLFixXNaVy27IjHDx92iLxx
Y4dJDx5WrAjG0p07cjBjypxJUya6mzcJEdrAkwaNG0CDCh1K9IaMowEChFpqzhy5p1CjSpWqTFme
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
CAA7
'''

if __name__ == '__main__':
    main()
