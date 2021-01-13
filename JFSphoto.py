
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
from tkinter.colorchooser import askcolor
from tkinter import Variable, filedialog
from tkinter import messagebox
import tkinter as tk
import csv
import numpy as np
from configparser import ConfigParser
import pandas as pd
import config

import matplotlib.pyplot as plt
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
from numpy import arange, sin, pi,cos
import fnmatch
import time
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backend_bases import key_press_handler
from tkinter import ttk
import CCDpanelsetup as panel
from sklearn.metrics import r2_score
from JFShelp import *
####################################### object
class Messurement(object):
    ### nr -> na
    def __init__(self,name,data):
         split = data.split(',')
         self.id = split[0]
         self.name = name +' '+str(split[0])
         self.conc = float(split[1])
         self.absorbanz = float(split[2])
         self.SH = int(split[3])
         self.ICG = int(split[4])
         

class Methods(object) :
    ### absorbanz später für E / mymol oder so
    def __init__(self,name,data):
        self.messures = list()
        self.name = name
        split = data.split('|')
        first = True
        for s in split:
            if first==True:
                first= False
                m = s.split(',')
                self.id =m[0]
                self.nm = m[1]
                self.units = m[2]
                self.absorbanz =m[3]
                self.step = m[4]
                self.final = m[5]
            else:
               self.messures.append(Messurement(self.name,s))

    def __str__(self):
        return self.name
    
    def save(self):
        s = self.id+','+self.nm+','+self.units+','+self.absorbanz+','+self.step+','+self.final
        for p in self.messures:
            s = s+'|'+str(p.id)+','+str(p.conc)+','+str(p.absorbanz)+','+str(p.SH)+','+str(p.ICG)
        return s

    def update(self,data):
        self.messures.clear()
        split = data.split('|')
        first = True
        for s in split:
            if first==True:
                first= False
                m = s.split(',')
                self.id =m[0]
                self.nm = m[1]
                self.units = m[2]
                self.absorbanz =m[3]
                self.step = m[4]
                self.final = m[5]
            else:
               self.messures.append(Messurement(self.name,s))


    def get_name(self):
        return(self.name)


class Jfsphoto (object):

    def __init__(self):
        self.nm = 0
        self.nmi = 0
        self.nm2 = 0
        self.nm2i = 0
        self.nm_left = 0
        self.nm_right = 0
        self.nm_step = 0
        self.tnm_left = tk.StringVar()
        self.tnm_right = tk.StringVar()
        self.tnm_step = tk.StringVar()
        self.nmData16 = np.zeros(3694, np.uint16)
        ########## nm scale checkButton default nm-scale is off
        self.nm_checked = tk.IntVar()
        self.nm_checked.set(0)
        ########## darkline 
        self.darkData16 = np.zeros(3694, np.float32)
        self.darkline_checked = tk.IntVar()
        self.darkline_checked.set(0)
        ########## baseline of the lightsource transmission or absorption
        self.baseData16 = np.zeros(3694, np.float32)
        self.baseline_checked = tk.IntVar()
        self.baseline_checked.set(0)
        self.baseline_start=0
        self.baseline_end=0
        self.abs_trans= tk.IntVar()
        self.baseline_limit = tk.IntVar()
        ########## set to transition
        self.abs_trans.set(1)
        ########## dataframe to load and save photometer data
        self.pandas_count = 0
        self.df = pd.DataFrame()
        ######### jfs math
        self.ok = tk.IntVar()
        self.ok.set(0)
        self.akt_point=0
        self.akt_nm = 0
        self.log = True
        ######### jfs methods
        self.methods = []
        ######### get icons
        self.bulbOn = get_icon_image('bulb-on.jpg')
        self.bulbOff = get_icon_image('bulb-off.jpg')
        
    def do_calibrate(self):
        win = tk.Toplevel()
        win.geometry("450x200+200+200")
        #center_window([500,300],None)
        self.lab1 = tk.Label(win, text='Please enter filenames and nm of the peaks').grid(row=0,column=0,columnspan=6)
        ########## first peak
        self.tnm = tk.StringVar()
        self.tnm.set(str(self.nm))
        self.tnmi = tk.StringVar()
        self.tnmi.set(str(self.nmi))
        self.lab2 = tk.Label(win,text='first Peak nm').grid(row=1,column=0,sticky='w')
        self.en1 = tk.Entry(win,textvariable=self.tnm, width= 10).grid(row=1,column=1)
        self.bt1 = tk.Button(win,text="select File",command=lambda: self.openfile(1)).grid(row=1,column=2)
        self.lnm = tk.Label(win,textvariable =self.tnm).grid(row=1,column=3)
        self.lnm = tk.Label(win,text =" nm by index ").grid(row=1,column=4)
        self.lmi = tk.Label(win,textvariable=self.tnmi).grid(row=1,column=5)
        ########## second peak
        self.tnm2 = tk.StringVar()
        self.tnm2.set(str(self.nm2))
        self.tnm2i = tk.StringVar()
        self.tnm2i.set(str(self.nm2i))
        self.lab3 = tk.Label(win,text='second Peak nm').grid(row=2,column=0,sticky='w')
        self.en2 = tk.Entry(win,textvariable=self.tnm2, width= 10).grid(row=2,column=1)
        self.bt2 = tk.Button(win,text="select File",command=lambda: self.openfile(2)).grid(row=2,column=2)
        self.lnm2 = tk.Label(win,textvariable =self.tnm2).grid(row=2,column=3)
        self.lnm2 = tk.Label(win,text =" nm by index ").grid(row=2,column=4)
        self.lm2i = tk.Label(win,textvariable=self.tnm2i).grid(row=2,column=5)
        ########### calibration    
        self.tnm_left.set(str(self.nm_left))
        self.tnm_right.set(str(self.nm_right))
        self.tnm_step.set(str(self.nm_step))
        self.lab4 = tk.Label(win,text="left border [nm]").grid(row=3,column=0,sticky='w')
        self.lab5 = tk.Label(win,textvariable=self.tnm_left).grid(row=3,column=1)
        self.lab6 = tk.Label(win,text="right border [nm]").grid(row=3,column=2)
        self.lab7 = tk.Label(win,textvariable=self.tnm_right).grid(row=3,column=3)
        self.lab8 = tk.Label(win,text="[nm]/point").grid(row=3,column=4)
        self.lab9 = tk.Label(win,textvariable=self.tnm_step).grid(row=3,column=5)
        self.bt3  = tk.Button(win,text="Calibrate",command=self.calibrate,state=tk.DISABLED,padx=10)
        self.bt3.grid(row=4,column=0,sticky='w')
        ############ limit for the baseline the baseline starts  and ends at a higher intensisity depending on
        # the spectrum of the light source
        self.lab10 = tk.Label(win,text="threshold for the baseline").grid(row=5,column=0,columnspan=2, sticky="w")
        self.en3 = tk.Entry(win,textvariable=self.baseline_limit, width= 10).grid(row=5,column=2)
        ############ Save Load config
        self.bt4 = tk.Button(win,text="Load Config",command=self.conf_read,padx=10).grid(row=6,column=0,sticky='w')
        self.bt5 = tk.Button(win,text="Save Config",command=self.conf_write,padx=10).grid(row=6,column=1,sticky='w')
        ############ Help
        self.bt5 = tk.Button(win,text="Help me",command=lambda roots = win ,helpfor=0: jfshelpme(roots,helpfor),padx=10).grid(row=7,column=0,sticky='w')

        ########### dialog modal
        win.focus_set()
        win.grab_set()
        win.wait_window()

    def do_msg(self,txt):
        self.mroot = tk.Tk()
        self.mroot.minsize(100,50)
        self.mroot.title(" Info ")
        self.label = tk.Label(self.mroot, text=txt,bg="yellow",fg="blue")
        self.label.pack()
        self.button = tk.Button(self.mroot, text='OK', width=25, command=self.mroot.destroy)
        self.button.pack()
        self.mroot.mainloop()

    ############ Darkline
    def do_save_darkline(self,dark):
        x = np.min(dark)
        if (x < 3700):
            self.do_msg(" This is not a Darkline ")
            return 0
        else :    
            self.darkData16 = dark*1.0
            self.df['darkline']=self.darkData16
            return 1

    def get_darkline_checked(self):
        return self.darkline_checked.get()

    ############ Baseline depends on the capacity of the light source block spektralrange if the intensity is to low
    def do_save_baseline(self,base):
        ### no margin at all
        doIt = True
        #### no left margin
        left = True
        x = np.max(base)
        if (x < 500):
            self.do_msg(" This is not a Baseine \n Is the Lightsouce switch on ? ")
            return 0
        else:   
            for i in range(0,3694): 
                if (base[i] < int(self.baseline_limit.get())) :
                    if doIt:
                        if left:
                            self.baseline_start = i
                        else:
                            self.baseline_end = i
                            doIt = False
                    self.baseData16[i] = 0
                else:
                    ## 300 should be in the ini file job!
                    if (base[i] > 300):
                        left = False
                    self.baseData16[i] = base[i]*1.0
            #print(self.baseline_start,"  ",self.baseline_end)
            self.df['baseline']=self.baseData16
            return 1
        
    def get_baseline_checked(self):
        return self.baseline_checked.get()

    ############ Calibration and Load/Save Configuration Part 2
    def checkit(self):
        self.nm = int(self.tnm.get())
        self.nmi = int(self.tnmi.get())
        self.nm2 = int(self.tnm2.get())
        self.nm2i = int(self.tnm2i.get())
        if ((self.nm > 0) & (self.nmi > 0) & (self.nm2 > 0) & (self.nm2i > 0)):
            self.bt3.config(state = tk.NORMAL)

        
    def calibrate(self):
        self.nm_step = round((self.nm2 - self.nm)/(self.nm2i-self.nmi),5)
        self.nm_left = round(self.nm-(self.nm_step*self.nmi),0)
        self.nm_right = round(self.nm2 + self.nm_step*(3694-self.nm2i),0)
        self.tnm_left.set(str(self.nm_left))
        self.tnm_right.set(str(self.nm_right))  
        self.tnm_step.set(str(self.nm_step))


    def nm_scale_ok(self):
        if ((self.nm_left > 0) & (self.nm_right > 0)):
            return 1
        else:
            return 0

    def get_nm_checked(self):
        if (self.nm_scale_ok()):
            return self.nm_checked.get()
        else:
            return 0

    def set_nm_scale(self):
        if (self.nm_scale_ok):
            self.nmData16 = np.linspace(self.nm_left,self.nm_right,3694)
            self.df['nmscale']=self.nmData16

    def get_nm_scale(self):
         self.set_nm_scale()
         return self.nmData16

    def add_kinetic(self,name):        
        self.df[str(name)]=config.rxData16
        toc = time.perf_counter()
        print(f"{name} time {toc :0.4f} sec")

    def start_kinetic(self):
        self.col_list = list(self.df.columns.values.tolist())
        ##### delete remaining _trans and _abs
        ##filtered = fnmatch.filter(self.col_list,'*_*')
        self.df.drop(self.col_list,axis=1,inplace=True)
        toc = time.perf_counter()
        print(f"start time {toc :0.4f} sec")


    def save_pandas(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", title="Save file as")
        try: 
           self.df['baseline']=self.baseData16
           self.df['darkline']=self.darkData16
           self.df['nmscale']=self.nmData16
           self.df['p1']=config.rxData16
           self.df.to_csv(filename)
        except IOError:
            messagebox.showerror("By the great otter!","There's a problem saving the file.")

    def save_kinetics(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", title="Save file as")
        try:
            self.df.to_csv(filename)
        except IOError:
            messagebox.showerror("By the great otter!","There's a problem saving the file.")

    def load_kinetics(self):
        filename = filedialog.askopenfilename(defaultextension=".csv", title="Open file ")
        try:
            self.listbox.delete(0,tk.END)
            self.df = pd.read_csv(filename,index_col=0)
            self.calculate()
            self.show_first_look()
        except IOError:
            messagebox.showerror("By the great otter!","There's a problem loding the file.")

    def load_pandas(self):
        filename = filedialog.askopenfilename(defaultextension=".csv", title="Open file ")
        try: 
           self.df = pd.read_csv(filename,index_col=0)
           config.rxData16=self.df['p1'].copy()
           self.do_save_baseline(self.df['baseline'])
           self.do_save_darkline(self.df['darkline'])
           self.baseline_checked.set(1)
           self.darkline_checked.set(1)
           self.nm_checked.set(1)
        except IOError:
            messagebox.showerror("By the great otter!","There's a problem saving the file.")

    def openfile(self,xx):
        rxData16 = np.zeros(3694, np.uint16)
        filename = filedialog.askopenfilename(defaultextension=".dat", title="Open file")
        line_count = 0
        try:
            with open(filename) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=' ')

                for row in readCSV:
                    if (line_count == 3):
                        self.SHsent = int(row[1])
                        self.ICGsent = int(row[6])
                    if (line_count > 3):
                        rxData16[line_count-4] = int(row[1])
                    line_count += 1
            if (xx==1):
                self.nmi = np.argmin(rxData16)
                self.tnmi.set(str(self.nmi))
            if (xx==2):
                self.nm2i = np.argmin(rxData16)
                self.tnm2i.set(str(self.nm2i))
            self.checkit()
        except IOError:
            messagebox.showerror("By the great otter!","There's a problem opening the file.")

    def reset_settings(self):
        self.baseline_checked.set(0)
        self.darkline_checked.set(0)
        self.nm_checked.set(0)
         

    def conf_write(self):
        config = ConfigParser()
        config.read('config.ini')
        lis = config.sections()
        if ('main' not in lis):
            config.add_section('main')
        config.set('main','nm_left',str(self.nm_left))
        config.set('main','nm_right',str(self.nm_right))
        config.set('main','nm_step',str(self.nm_step))
        config.set('main','baseline_limit',str(self.baseline_limit.get()))
        if ('methods') in lis:
            config.remove_section('methods')
            with open('config.ini','w') as f:
                f.seek(0)
                config.write(f)
                f.truncate()
            config.read('config.ini')
            lis = config.sections()
        if ('methods') not in lis:
            config.add_section('methods')
        for p in self.methods:
            config.set('methods',p.get_name(),p.save())
            print(p.get_name())
        with open('config.ini','w') as f:
            config.write(f)

    def conf_read(self):
        config = ConfigParser()
        try:
            config.read('config.ini')
            self.nm_left =  float(config.get('main','nm_left',fallback='0'))
            self.tnm_left.set(config.get('main','nm_left',fallback='0'))
            self.nm_right = float(config.get('main','nm_right',fallback='0'))
            self.tnm_right.set(config.get('main','nm_right',fallback='0'))
            self.nm_step = float(config.get('main','nm_step',fallback='0'))
            self.tnm_step.set(config.get('main','nm_step',fallback='0'))
            self.set_nm_scale()
            self.baseline_limit.set(int(config.get('main','baseline_limit',fallback='20')))
            if 'methods' in config.sections():
                for i in config['methods']:
                    s = config.get('methods',i)
                    #print(i,s)
                    self.methods.append(Methods(i,s))
        except IOError:
            print("By the great otter!","No config.ini file")

    def draw_slice(self):
        self.ax2.clear()
        self.ax3.clear()
        if self.akt_point > 0:
            x=[]
            y=[]        
            for xx in self.col_list:
                x.append(int(xx))
                
                if self.ok.get() < 3:
                    yy = self.df.iloc[self.akt_point][xx]
                elif self.ok.get()==3:
                    yy = self.df.iloc[self.akt_point][xx+'_abs']
                elif self.ok.get()==4:
                    yy = self.df.iloc[self.akt_point][xx+'_trans']
                y.append(yy)
            self.ax2.plot(x, y, linewidth=0.6)
            self.ax2.set_title(f'{round(self.akt_nm,2)} [nm]')
            if self.log == True:               
                self.ax3.set_title(f'{round(self.akt_nm,2)} [nm] log')
                self.ax3.set_yscale('log')
            else:
                y1 = np.array(y)
                y = 1 / y1
                self.ax3.set_title(f'{round(self.akt_nm,2)} [nm] 1/A')
            self.ax3.plot(x, y, linewidth=0.6)

        self.canvas.draw()

    def do_math(self,panel):
     
        def onclick(event):           
            #print('%s click: button=%d, xdata=%f, ydata=%f' %('double' if event.dblclick else 'single', event.button,
            #        event.xdata, event.ydata))
            if event.button == 3:
                self.akt_nm=0
                self.akt_point=0
            else:
                self.akt_nm =  event.xdata
                self.akt_point  = int((self.akt_nm - self.nm_left)*(1/self.nm_step))
            self.draw_slice()

        def on_key_press(event):
           print("you pressed {}".format(event.key))
           key_press_handler(event, self.canvas, self.toolbar1)

        
        stati = [("Raw",1),("Raw + Baseline",2),("Transmission",4),("Absorbanz",3)]
        self.proji3d = False

        def toggle():
            if self.kbtn.config('relief')[-1] == 'sunken':
                self.kbtn.config(relief='raised')
                #self.do_2dprint()
                self.proji3d=False
            else:
                self.kbtn.config(relief='sunken') 
                #self.do_3dprint()
                self.proji3d=True
            self.look()

        def togglelog():
            if self.kbtm.config('relief')[-1] == 'sunken':
                self.kbtm.config(relief='raised')
                #self.do_2dprint()
                self.log=True
            else:
                self.kbtm.config(relief='sunken') 
                #self.do_3dprint()
                self.log=False
            self.look()

        win = tk.Toplevel()        
        self.center = tk.Frame(win, bg='gray2', width=800, height=400, padx=3, pady=3)
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(1, weight=1)
        self.center.grid(row=1, sticky="nsew")
        self.ctr_mid = tk.Frame(self.center,  width=250, height=300, padx=3, pady=3)
        self.ctr_right = tk.Frame(self.center, width=200, height=300, padx=3, pady=3)
        self.ctr_mid.grid(row=0, column=0, sticky="nsew")
        self.ctr_right.grid(row=0, column=1, sticky="ns")
        self.fig = plt.Figure(figsize=(8,4),dpi=120)
        plt.rcParams.update({'font.size': 5})
        plt.rc('legend',fontsize=5)

        self.ax1 = self.fig.add_subplot(2,3,(1,5))
        self.ax2 = self.fig.add_subplot(2,3,3)
        self.ax3 = self.fig.add_subplot(2,3,6)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.ctr_mid)
        self.canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)   
        self.toolbarFrame = tk.Frame(master=self.center,padx=5,pady=5)
        self.toolbarFrame.grid(row=1,columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

       

        self.canvas.mpl_connect("key_press_event", on_key_press)
        self.canvas.mpl_connect('button_press_event', onclick)
        #### Buttons
        n = 0
        for txt,val in stati:
            tk.Radiobutton(master=self.ctr_right,text=txt,variable=self.ok,command=self.look,value=val,padx=5,pady=5).grid(row=n,column=0,sticky="w")
            n=n+1
        self.listbox = tk.Listbox(master=self.ctr_right,selectmode = "multiple")
        self.listbox.grid(row=7,column=0,sticky='w')
        self.kbtn1 = tk.Button(master=self.ctr_right,text="show selected",command=self.show_selected,width=15)
        self.kbtn1.grid(row=14,column=0,sticky="w")
        self.kbtn2 = tk.Button(master=self.ctr_right,text="clear selected",command=self.clear_selected,width=15)
        self.kbtn2.grid(row=15,column=0,sticky="w")
        self.kbtn = tk.Button(master=self.ctr_right,text="Load Kinetic / Data",command=self.load_kinetics,width=15)
        self.kbtn.grid(row=16,column=0,sticky="w")
        self.kbtn = tk.Button(master=self.ctr_right,text="Save Kinetic / Data",command=self.save_kinetics,width=15)
        self.kbtn.grid(row=17,column=0,sticky="w")
        self.kbtn = tk.Button(master=self.ctr_right,text="3 D Print",command=toggle,width=15,relief='raised')
        self.kbtn.grid(row=18,column=0,sticky="w")
        self.kbtm = tk.Button(master=self.ctr_right,text="ln[A] 1/[A]",command=togglelog,width=15)
        self.kbtm.grid(row=19,column=0,sticky="w")
        self.kbtmhp = tk.Button(master=self.ctr_right,text="Help me",command=lambda roots = win ,helpfor=6: jfshelpme(roots,helpfor),width=15)
        self.kbtmhp.grid(row=20,column=0,sticky="w")
        if self.calculate() :
            self.show_first_look()
        else:
            t = arange(0.0, 3.0, 0.01)
            s = sin(2*pi*t)
            self.ax1.plot(t, s, linewidth=0.6)
        

        win.focus_set()
        win.grab_set()
        win.wait_window()

    def clear_selected(self):
        self.listbox.selection_clear(0,'end')
        #self.get_kin_list()
        self.col_list = list(self.listbox.get(0,tk.END))
        self.look()


    def show_selected(self):
        self.col_list = [self.listbox.get(i) for i in self.listbox.curselection()]
        self.look()

    def calculate(self):
        self.ok.set(0)
        if 'baseline' in self.df.columns:
            self.get_kin_list()
            self.do_get_range()
            for xx in self.col_list:
                self.do_absorbanz(xx)
            for xx in self.col_list:
                self.do_transmission(xx)
            return True
        else:
            return False

    def get_kin_list(self):
        self.col_list = list(self.df.columns.values.tolist())
        ##### delete remaining _trans and _abs
        filtered = fnmatch.filter(self.col_list,'*_*')
        self.df.drop(filtered,axis=1,inplace=True)
        self.col_list = list(self.df.columns.values.tolist())
        self.col_list.remove('baseline')
        self.col_list.remove('darkline')
        self.col_list.remove('nmscale')

    def show_first_look(self):
        self.ax1.clear()
        for xx in self.col_list:
            self.df.plot(x = 'nmscale',y = xx, linewidth=0.6,ax=self.ax1)
            self.listbox.insert(tk.END, xx)
        self.ok.set(1)
        self.canvas.draw()

   
    def do_get_range(self):
        self.right = 0
        self.left = 0
        #### count for random not zero values in the start of the baseline
        count = 0
        b = self.df['baseline']
        for i in range(0,3694):
            if b[i]==0:
                if (self.left > 0 and self.right==0):
                    self.right=i
            else:
                count += 1
                if (self.left==0 and count > 5):
                    self.left=i

    def do_absorbanz(self,xx):
        y = self.df['darkline'] - self.df[xx]
        b = self.df['baseline']
        c = np.zeros(3694, np.float32)
        for i in range(0,3694):
            if b[i]==0:
                c[i] = 1
            else:
                #c[i] = y[i]/b[i]
                c[i] = np.log10(b[i]/y[i])
        self.df[xx+'_abs'] = c

    def do_transmission(self,xx):
        y = self.df['darkline'] - self.df[xx]
        b = self.df['baseline']
        c = np.zeros(3694, np.float32)
        for i in range(0,3694):
            if b[i]==0:
                c[i] = 1
            else:
                c[i] = y[i]/b[i]
                #c[i] = np.log10(b[i]/y[i])
        self.df[xx+'_trans'] = c

        # self.ax1 = self.fig.gca(projection='3d')
        # for xx in self.col_list:
        #     self.df.plot(y = 'nmscale',x = xx, zs= int(xx), linewidth=0.6,ax=self.ax1)


    def look(self):
        self.draw_slice()
        self.ax1.clear()
        if self.proji3d==True:
            self.ax1 = self.fig.add_subplot(2,3,(1,5),projection='3d')
            #self.ax1 = self.fig.gca(projection='3d')
        else:
             self.ax1 = self.fig.add_subplot(2,3,(1,5))
        if self.ok.get()==1:
            for xx in self.col_list:
                if self.proji3d==True:
                    self.ax1.set_ylabel('points')
                    self.df.plot(x= 'nmscale',y = xx, zs= int(xx), linewidth=0.6,ax=self.ax1)

                else:
                    self.df.plot(x = 'nmscale',y = xx, linewidth=0.6,ax=self.ax1)
        elif self.ok.get()==2:
            for xx in self.col_list:
                if self.proji3d==True:
                    self.df.plot(x= 'nmscale',y = xx, zs= int(xx), linewidth=0.6,ax=self.ax1)
                else:
                    self.df.plot(x = 'nmscale',y = xx, linewidth=0.6,ax=self.ax1)
            self.df.plot(x = 'nmscale',y = 'baseline', color='blue',linewidth=0.6,ax=self.ax1)
            self.df.plot(x = 'nmscale',y = 'darkline', color='black',linewidth=0.6,ax=self.ax1)
        elif self.ok.get()==3:
            for xx in self.col_list:
                if self.proji3d==True:
                    self.df.plot(x= 'nmscale',y = xx+'_abs', zs= int(xx), linewidth=0.6,ax=self.ax1)
                else:
                    self.df.plot(x = 'nmscale',y = xx+'_abs', linewidth=0.6,ax=self.ax1)
            self.ax1.set_xlim([self.nm_left+self.left*self.nm_step, self.nm_left+self.right*self.nm_step])
        elif self.ok.get()==4:  
            for xx in self.col_list:
                if self.proji3d==True:
                    self.df.plot(x= 'nmscale',y = xx+'_trans', zs= int(xx), linewidth=0.6,ax=self.ax1)
                else:        
                    self.df.plot(x = 'nmscale',y = xx+'_trans',linewidth=0.6,ax=self.ax1)
            self.ax1.set_xlim([self.nm_left+self.left*self.nm_step, self.nm_left+self.right*self.nm_step])
        else:
            t = arange(0.0, 3.0, 0.01)
            s = sin(2*pi*t)
            self.ax1.plot(t, s, linewidth=0.6)
        self.canvas.draw()

    def check_requirement(self):
        ok = True
        if self.nm_checked.get() == 0:
            ok = False
            tk.messagebox.showerror('[nm]','You need to check calibration [nm]\n or first calibrate the instrument')
        else:
            s=''
            s1=''
            if (self.darkline_checked.get()==0):
                s = ' Please take a darkline messurement first \n'
            if  (self.baseline_checked.get()==0):
                s1 = ' Please take a baseline messurement first \n'
            if (len(s1)>0 or len(s)>0):
                ok = False
                tk.messagebox.showerror('ToDos',s+s1)
        return ok

    def do_methods(self,panel):


        def get_duration():
            if panel.tint.get().split()[4]=='ms':
                f = float(panel.tint.get().split()[3])
            elif panel.tint.get().split()[4] == 's':
                f = float(panel.tint.get().split()[3])*1000
            elif panel.tint.get().split()[4] == 'min':
                f = float(panel.tint.get().split()[3]) * 60000
            x = int(panel.AVGscale.get())*f
            if x < 1000:
                x = 1000
            return x

               
        
        font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 8,
        }

        def get_messurement(name):
            # get selected and save values
            #name = tree. val=selection()[0]
            # get parent for nm 
            x = name.split(' ')
            nm = tree.item(x[0])["values"][1]
            ## nm -> point
            p = int((nm - self.nm_left)*(1/self.nm_step))
            self.df['m1'] = config.rxData16
            d = self.df.iloc[p]['darkline']
            b = self.df.iloc[p]['baseline']
            w = self.df.iloc[p]["m1"]
            return np.log10(b/(d-w))

        def waitfor(x,name,val):
            # self.df['m1'] = config.rxData16
            # d = self.df.iloc[p]['darkline']
            # b = self.df.iloc[p]['baseline']
            # w = self.df.iloc[p]["m1"]
            # val[3]= np.log10(b/(d-w))
            val[3] = get_messurement(name)
            val[4]= panel.SHvalue.get()
            val[5]= panel.ICGvalue.get()
            tree.item(x, text=name,values=val)

        
        def cb(event):
            if self.check_requirement() == True:
                panel.bcollect.invoke()               
                # get selected and save values
                name = tree.selection()[0]
                val= tree.item(name)["values"]
                # get parent for nm 
                x = name.split(' ')
                #nm = tree.item(x[0])["values"][1]
                ## nm -> point
                #p = int((nm - self.nm_left)*(1/self.nm_step))
                #print(f'nm {nm} point {p}')
                s1 = str(val[2])+' '+tree.item(x[0])["values"][2]
                s = 'Is a Cuvet for '+x[0]+' in concentration\n of '+s1+' in the photometer ? '
                if  tk.messagebox.askokcancel(title='Messurement', message=s):
                    panel.bcollect.invoke()
                    #panel.after(get_duration(),waitfor(x,name,val,p))
                    panel.after(get_duration(),waitfor(x,name,val))

        def cb2(event):
            y = []
            x = []
            name = tree.selection()
            l6.config(text=name[0])
            for child in tree.get_children(name):
                x.append(float(tree.item(child)["values"][2]))
                y.append(float(tree.item(child)["values"][3]))
            ax1.clear()
            model = np.polyfit(x,y,1)
            predict = np.poly1d(model)
            x_range = np.linspace(x[0],x[-1])
            y_range = predict(x_range)
            ax1.plot(x_range,y_range,linewidth=0.6)
            ax1.plot(x, y, '+')
            ax1.set_title(f'{name[0]}',fontdict=font)
            ax1.text(x[0], 1, f'A vs {tree.item(name)["values"][2]}',fontdict=font)
            ax1.text(x[0], 0.9, f'y = {round(model[0],3)}x + {round(model[1],3)}',fontdict=font)
            ax1.text(x[0], 0.8, f'R ={round(r2_score(y,predict(x)),3)}',fontdict=font)
            #ax1.text(x[0], 0.9, r'Omega: {s} $\Omega$', {'color': 'b', 'fontsize': 8})
            canvas.draw()

        win = tk.Toplevel() 
        lf = tk.LabelFrame(win,text='Methods')
        lf.grid(column=0,row=0,sticky='w')
        tree = ttk.Treeview(lf)
        tree.tag_bind('cb','<<TreeviewSelect>>',cb)
        tree.tag_bind('cb2','<<TreeviewSelect>>',cb2)
        tree.grid(column=0,row=0)
        tree["columns"]=('id','nm','konz','absorbanz','interval','last')
        tree.column("#0",width=100,minwidth=100,stretch=tk.NO)
        tree.column("id",width=20,minwidth=20,stretch=tk.NO)
        tree.column("nm",width=40,minwidth=40,stretch=tk.NO)
        tree.column("konz",width=60,minwidth=60,stretch=tk.NO)
        tree.column("absorbanz",width=60,minwidth=60,stretch=tk.NO)
        tree.column("interval",width=60,minwidth=60,stretch=tk.NO)
        tree.column("last",width=80,minwidth=80,stretch=tk.NO)
        tree.heading("#0",text='Methode',anchor=tk.W)        
        tree.heading("id",text='ID',anchor=tk.W) 
        tree.heading("nm",text='[nm]',anchor=tk.W) 
        tree.heading("konz",text='conc',anchor=tk.W) 
        tree.heading("absorbanz",text="Absorbanz",anchor=tk.W)
        tree.heading("interval",text='interval/SH',anchor=tk.W) 
        tree.heading("last",text='last conc/ICG',anchor=tk.W)            

        einheiten = ['Mol','mmol','mymol']
        
        e1 = tk.StringVar()
        e2 = tk.IntVar()
        e3 = tk.IntVar()
        e4 = tk.StringVar()
        e4.set(einheiten[2])
        e5 = tk.IntVar()
        e6 = tk.IntVar()
        e7 = tk.StringVar()
        e7.set('0.0')
       

        def load_tree():
            for a in self.methods:
                tree.insert("",'end',a.name,text=a.name,values=(a.id,a.nm,a.units,a.absorbanz,a.step,a.final),tags=('cb2'))
                for b in a.messures:
                    tree.insert(a.name,'end',b.name,text=b.name,values=(b.id,'',b.conc,b.absorbanz,b.SH,b.ICG),tags=('cb'))
        
        def save_tree():
            for child in tree.get_children():
                name = child
                s= ",".join(str(x) for x in tree.item(child)["values"])
                for items in tree.get_children(child):
                    ss = ",".join(str(x) for x in tree.item(items)["values"] if len(str(x))>0)
                    s = s +'|'+ss   
                for p in self.methods:
                    if p.get_name()== name:
                        p.update(s)
                self.conf_write()

        def add_method():
            tree.insert("",'end',e1.get(),text=e1.get(),values=(e2.get(),e3.get(),e4.get(),e7.get(),e5.get(),e6.get()),tags=('cb2'))
            stp = e6.get()/e5.get()
            for i in range(1,e5.get()+1):
                na = e1.get()+' '+str(i)
                tree.insert(e1.get(),'end',na,text= na ,values=(i,'',stp * (i),0.0,0,0),tags=('cb'))
            s= ",".join(str(x) for x in tree.item(e1.get())["values"])
            for items in tree.get_children(e1.get()):
                ss = ",".join(str(x) for x in tree.item(items)["values"] if len(str(x))>0)
                s = s +'|'+ss
            self.methods.append(Methods(e1.get(),s))
              
        def del_method():
            curItem = tree.focus()
            name =tree.item(curItem,"text")
            if  tk.messagebox.askyesno(title='Delete', message='You you really want to delete '+name ):
                tree.delete(curItem)
                for p in self.methods:
                    if p.name == name:
                        self.methods.remove(p)

        def waitfor_darkline():
            panel.bcollect.invoke()
            if (self.do_save_darkline(config.rxData16)==1):
                        panel.jfsdark_check.config(state=tk.NORMAL)

        def waitfor_baseline():
            panel.bcollect.invoke()
            base = self.darkData16-config.rxData16
            if (self.do_save_baseline(base)==1):
                panel.jfsbase_check.config(state=tk.NORMAL)

        def do_zero_messurement():
            #print(l6['text'])
            if l6['text'].find('Select')  >= 0:
                tk.messagebox.showerror(title='Sorry',message='Select Method first')
            else:
                for child in tree.get_children(l6['text']):
                    sh =int(tree.item(child)["values"][4])
                    icg =int(tree.item(child)["values"][5])
                    break
                panel.SHvalue.set(sh)
                panel.ICGvalue.set(icg)
                if  tk.messagebox.askokcancel(title='Darkline', message='Insert the empty Cuvet\nturn lightsource [off]'):
                    panel.bcollect.invoke()
                    panel.after(1000,waitfor_darkline)  
                    ## messure Darkline
                    if  tk.messagebox.askokcancel(title='Baseline', message= 'Leave the empty Cuvet\nturn lightsource [on]'):
                        panel.bcollect.invoke()
                        panel.after(1000,waitfor_baseline)
                       
                        
        def do_messurement():
            panel.bcollect.invoke()
            if  tk.messagebox.askokcancel(title='Messurements', message= 'Sample Cuvet inside \n lightsource [on]'):
                panel.bcollect.invoke()
                x=[]
                y=[]
                for child in tree.get_children(l6['text']):
                    x.append(float(tree.item(child)["values"][2]))
                    y.append(float(tree.item(child)["values"][3]))
                model = np.polyfit(x,y,1)
                a = get_messurement(l6['text'])
                #print(a)
                #a = model[0]* c +model[1]
                c = (a - model[1])/model[0]               
                l8.config(text=str(round(c,3))+' '+tree.item(l6['text'])['values'][2])

        #### Tree 
        lf1 = tk.LabelFrame(win,text='Edit the method')
        lf1.grid(column=0,row=1,sticky='w')
        l1 = tk.Label(lf1,text='Name of the Method')
        l1.grid(column=0,row=0,sticky='w')
        le1 =tk.Entry(lf1,textvariable=e1,width=20)
        le1.grid(column=1,row=0,sticky='w')
        l2 = tk.Label(lf1,text='ID of the Method')
        l2.grid(column=0,row=1,sticky='w')
        le2 =tk.Entry(lf1,textvariable=e2,width=5)
        le2.grid(column=1,row=1,sticky='w')
        l3 = tk.Label(lf1,text='Enter wavelength')
        l3.grid(column=0,row=2,sticky='w')
        le3 =tk.Entry(lf1,textvariable=e3,width=5)
        le3.grid(column=1,row=2,sticky='w')
        l4 = tk.Label(lf1,text='Unit of Concentration')
        l4.grid(column=0,row=3,sticky='w')
        le4 =tk.OptionMenu(lf1,e4,*einheiten)
        le4.grid(column=1,row=3,sticky='w')
        l5 = tk.Label(lf1,text='Numbers of samples')
        l5.grid(column=0,row=4,sticky='w')
        le5 =tk.Entry(lf1,textvariable=e5,width=5)
        le5.grid(column=1,row=4,sticky='w')
        l6 = tk.Label(lf1,text='Last Sampel Concentration')
        l6.grid(column=0,row=5,sticky='w')
        le6 =tk.Entry(lf1,textvariable=e6,width=5)
        le6.grid(column=1,row=5,sticky='w')
        lb1 = tk.Button(lf1,text='Add Method',command=add_method)
        lb1.grid(column=0,row=6,sticky='w')
        lb2 = tk.Button(lf1,text='Delete Method',command=del_method)
        lb2.grid(column=1,row=6,sticky='w')
        lb3 = tk.Button(lf1,text='Save Methods',command=save_tree)
        lb3.grid(column=0,row=7,sticky='w')
        #### canvas
        fig = plt.Figure(figsize=(4,2),dpi=100)
        plt.rcParams.update({'font.size': 5})
        ax1 = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master = win )
        canvas.get_tk_widget().grid(column=1,row=0,sticky='nesw')
        #### test output
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t) 
        ax1.plot(t, s, linewidth=0.6)
        canvas.draw()
        #### do messurements
        lf3 = tk.LabelFrame(win,text='Do messurements')
        lf3.grid(column=1,row=1,sticky='nw')
        l6 = tk.Label(lf3,text='Select Messurement')
        l6.grid(column=0,row=0,sticky='w')
        lmb1=tk.Button(lf3,text='Zero Messurements',command=do_zero_messurement)
        lmb1.grid(column=0,row=1,sticky='w')
        lmb2=tk.Button(lf3,text='Messurement',command=do_messurement)
        lmb2.grid(column=0,row=2,sticky='w')
        l7 = tk.Label(lf3,text='Result :',width=12)
        l7.grid(column=1,row=1,sticky='e')
        l8 = tk.Label(lf3,text='empty',width=12)
        l8.grid(column=1,row=2,sticky='e')
        #### go on
        load_tree()
        
        win.focus_set()
        win.grab_set()
        win.wait_window()