# Copyright (c) 2020 Jens Fröhlich
 # All rights reserved.
 #
 # Author: Jens Fröhlich <science@fsksoft.de>
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions
 # are met:
 # 1. Redistributions of source code must retain the above copyright
 #    notice, this list of conditions and the following disclaimer.
 # 2. Redistributions in binary form must reproduce the above copyright
 #    notice, this list of conditions and the following disclaimer in the
 #    documentation and/or other materials provided with the distribution.
 #
 # THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 # ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
 # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 # OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 # HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 # LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 # OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 # SUCH DAMAGE.
import tkinter as tk
import matplotlib.pyplot as plt
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from numpy import arange, sin, pi

from JFSphoto import *

class JfsMath(object):

    def __init__(self,master,JFSphoto):
        self.master = master
        master.title("Mathoptions")
        self.ok = tk.IntVar()

        self.center = tk.Frame(self.master, bg='gray2', width=50, height=40, padx=3, pady=3)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(1, weight=1)
        self.center.grid(row=1, sticky="nsew")
        self.ctr_mid = tk.Frame(self.center, bg='yellow', width=250, height=190, padx=3, pady=3)
        self.ctr_right = tk.Frame(self.center, bg='green', width=100, height=190, padx=3, pady=3)
        self.ctr_mid.grid(row=0, column=0, sticky="nsew")
        self.ctr_right.grid(row=0, column=1, sticky="ns")
        self.fig = plt.Figure(figsize=(8,4),dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.ax1.plot(t, s, linewidth=0.6)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.ctr_mid)
        self.canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)   
        self.chb = tk.Checkbutton(master=self.ctr_right,text='Hi there',variable=self.ok,command=self.look)
        self.chb.grid(row=0,column=0)


    def look(self):
        print(self.ok.get())



#jfsmath()
root = tk.Tk()
jfs = Jfsphoto()
jfs.conf_read()
my = JfsMath(root,jfs)
root.mainloop()