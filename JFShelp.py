# Copyright (c) 2019 Esben Rossel
 # All rights reserved.
 #
 # Author: Esben Rossel <esbenrossel@gmail.com>
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

import os
import tkinter as tk
from tkinter.constants import END
from PIL import Image,ImageTk

def center_window(size, window) :
    window_width = size[0] #Fetches the width you gave as arg. Alternatively window.winfo_width can be used if width is not to be fixed by you.
    window_height = size[1] #Fetches the height you gave as arg. Alternatively window.winfo_height can be used if height is not to be fixed by you.
    if window==None:
        window_x = 200
        window_y = 200
    else:
        window_x = int((window.winfo_screenwidth() / 2) - (window_width / 2)) #Calculates the x for the window to be in the centre
        window_y = int((window.winfo_screenheight() / 2) - (window_height / 2)) #Calculates the y for the window to be in the centre

    window_geometry = str(window_width) + 'x' + str(window_height) + '+' + str(window_x) + '+' + str(window_y) #Creates a geometric string argument
    window.geometry(window_geometry) #Sets the geometry accordingly.
    return


def get_icon_image(xx):
    directory_path = os.path.dirname(__file__)
    file_path = os.path.join(directory_path, 'images\\')
    image =Image.open(file_path+xx)
    photo = ImageTk.PhotoImage(image) 
    return photo


      
def jfshelpme(win,helpfor):
    top = tk.Toplevel(win)
    scrolling = tk.Scrollbar(top)
    scrolling.pack(side=tk.RIGHT, fill=tk.Y)
    
    frame = tk.Frame(top)
    frame.pack()
    text = tk.Text(frame, height=30, width=100, wrap=tk.WORD)
    text.pack(side=tk.LEFT, fill=tk.Y)
    scrolling.config(command=text.yview)
    text.config(yscrollcommand=scrolling.set)
   
    photoImg = get_icon_image('nm405.gif')
    photoImg2= get_icon_image('methods.gif')
    photoImg3= get_icon_image('kinetics.gif')
    photoImg4= get_icon_image('xenon.gif')

    text.tag_configure('it', font=('Arial', 10, 'italic'))
    text.tag_configure('h1', font=('Verdana', 16, 'bold'))
    text.tag_configure('h2', font=('Verdana', 12, 'bold'))
    text.tag_configure('h3', font=('Verdana', 10, 'bold'))

    if (helpfor == 0): #do you need help with the device?
        text.image_create(tk.END,image=photoImg)
        text.insert(tk.END, " Calibration\n", 'h1')
        text.insert(tk.END, "\nTo calibrate the Instrument we need two laserpointer of different colors und known wavelength.\nFor example a blue [405nm] and red [650nm] one.\n")
        text.insert(tk.END, "1) First take two measurements with your device und save the files with the [Save] button under a comprehensible name (e.g. 405nm.data) \n")
        text.insert(tk.END, "2) Open the calibration dialog and insert the wavelength in [nm] and afterwards select the respective file. <first peak> stands for the lower and <second peak> for the higher wavelength.\n")
        text.insert(tk.END, "3) Now you can use the [Calibrate] button to calibrate the instrument and [Save Config] will the store the configuration.\n")
        text.insert(tk.END,"\nAfter this procedure you can switch the [nm] scale on and use other option:\n")
        text.insert(tk.END,'\nMethods\n','h2')
        text.insert(tk.END,"\nAs a Photometer to messure the transmittance or absorbance depending on the concentration of colored compounds.\n\n")
        text.image_create(tk.END,image=photoImg2)
        text.insert(tk.END,"\n\nKinetic\n",'h2')
        text.insert(tk.END,"\nThe instrument can messure in specific intervalls over time the change in absorbance. From this data it is possible to determine the rate of the reaction.\n")
        text.image_create(tk.END,image=photoImg3)
        text.insert(tk.END,"\n Baseline\n",'h1')
        text.insert(tk.END,"\nIn order to messure the absorption of a compound in the cuvette, you have to messure the intensity of the the light passing through the reference cell.\n")
        text.insert(tk.END,"The intensity of the light at a specific wavelength depends on the kind of light source. The spectrum of a tungstone lamp is different from a LED etc.\n")
        text.insert(tk.END,"\nTo make things easy: the value <threshold for the baseline> cuts off the beginning and the end where the light source is not strong enought to give reasonable results ")
        text.image_create(tk.END,image=photoImg4)
        text.insert(tk.END,"\nFor example xenon-lamp as a source. If the value of the threshold is set to 100 (green), the baseline will start at 380nm and end at 510nm\n")
        text.insert(tk.END,"If the value of the threshold is set to 50 (red), the baseline will start at 370nm and end at 695nm. The baseline determines the range of messurement\n")
    
    elif (helpfor == 1): #do you need help with the device?
        text.image_create(tk.END,image=photoImg)
        text.insert(tk.END, " Calibration\n", 'h1')
        text.insert(tk.END, "\nTo calibrate the Instrument we need two laserpointer of different colors und known wavelength.\nFor example a blue [405nm] and red [650nm] one.\n")
        text.insert(tk.END, "1) First take two measurements with your device und save the files with the [Save] button under a comprehensible name (e.g. 405nm.data) \n")
        text.insert(tk.END, "2) Open the calibration dialog and insert the wavelength in [nm] and afterwards select the respective file. <first peak> stands for the lower and <second peak> for the higher wavelength.\n")
        text.insert(tk.END, "3) Now you can use the [Calibrate] button to calibrate the instrument and [Save Config] will the store the configuration.\n")
        text.insert(tk.END,"\nAfter this procedure you can switch the [nm] scale on and use other option:\n")
        text.insert(tk.END,'\nMethods\n','h2')
        text.insert(tk.END,"\nAs a Photometer to messure the transmittance or absorbance depending on the concentration of colored compounds.\n\n")
        text.image_create(tk.END,image=photoImg2)
        text.insert(tk.END,"\n\nKinetic\n",'h2')
        text.insert(tk.END,"\nThe instrument can messure in specific intervalls over time the change in absorbance. From this data it is possible to determine the rate of the reaction.\n")
        text.image_create(tk.END,image=photoImg3)
    elif (helpfor == 2):
        text.insert(tk.END," Dark spectrum\n",'h1')
        text.insert(tk.END,"\nPlease turn off the light source and take a messurement with the actual parameter. Afterwards save this spektrum of the dark noise\n")
        text.insert(tk.END,"\nClick the checkbutton of [Darkline] to proceed")
    elif (helpfor == 3):
        text.insert(tk.END," Zero solution \n",'h1')
        text.insert(tk.END,"\nIn order to messure the absorbance or transmittance of a sample, you need to messure a zero solution first\n")
        text.insert(tk.END,"\n1) Check the darkline checkbutton\n2) Turn on the light source and insert a cuvette with a solution without a compound -> \'zero solution\'\n")
        text.insert(tk.END,"3) Save the messurement with [save Base]. This will also cut the range of messurement depending of the lightsoure -> Baseline\n" )
        text.insert(tk.END,"4) Click the checkbutton of [Baseline] to proceed\n")   
        text.insert(tk.END,"Now you can messure the absorbance or transmittance of different compounds by using the radiobuttons \n") 
        text.insert(tk.END,"\nWith the Dialog [Calibration] you can change the range of the light source\n\n")
        text.insert(tk.END,"\n Baseline\n",'h2')
        text.insert(tk.END,"\nIn order to messure the absorption of a compound in the cuvette, you have to messure the intensity of the the light passing through the reference cell.\n")
        text.insert(tk.END,"The intensity of the light at a specific wavelength depends on the kind of light source. The spectrum of a tungstone lamp is different from a LED etc.\n")
        text.insert(tk.END,"\nTo make things easy: the value <threshold for the baseline> cuts off the beginning and the end where the light source is not strong enought to give reasonable results ")
        text.image_create(tk.END,image=photoImg4)
        text.insert(tk.END,"\nFor example xenon-lamp as a source. If the value of the threshold is set to 100 (green), the baseline will start at 380nm and end at 510nm\n")
        text.insert(tk.END,"If the value of the threshold is set to 50 (red), the baseline will start at 370nm and end at 695nm. The baseline determines the range of messurement\n")
    elif (helpfor == 4):
        text.insert(tk.END," Load / Save \n",'h1')
        text.insert(tk.END,"\nThese Buttons save und load the photometer data of the absorbance of a compound. The baseline of the light source and the dark spectrum of the instrument will also be saved\n")
        text.insert(tk.END,"\nThis will not work with with simple spetra saves over the [Save] button")
    elif (helpfor == 5):
        text.image_create(tk.END,image=photoImg3)
        text.insert(tk.END,"\nKinetic\n",'h1')
        text.insert(tk.END,"\nTo run kinetic measurements with this photometer, make sure that:\n")
        text.insert(tk.END,"1) The instrument is calibrated\n2) A dark spektrum is taken/saved [save Dark]\n3) A zero solution is messured a saved [save Base].\n\n")
        text.insert(tk.END,"If all parameters a ok. Adjust the numbers of repetitions and the time between the messurement in the dialog.\nThe [start Kinetic] Button will start the process.\n")
        text.insert(tk.END,"When the messurement is finished the [Math] Dialog appears and the data can be saved and inspected.\n")
    elif (helpfor == 6):
        #text.image_create(tk.END,image=photoImg3)
        text.insert(tk.END,"\nMath on Kinetics\n",'h1')
        text.insert(tk.END,"\nRaw - Absorbanz\n\n",'h2')
        text.insert(tk.END,"- Raw: is the raw output of the instrument\n- Raw + Baseline: is raw plus the darkline und the baseline of the lighsource\n")
        text.insert(tk.END,"- Transmission: is the relation of the intensity of the light absorpt by the sample and the intensity of the light source.\n")
        text.insert(tk.END,"- Absorbanz: is the relation of the log(I of light source/I of transmitted)\n-- For more information please look for Beer-Lambert law\n")
        text.insert(tk.END,"\nSlicing\n\n",'h2')
        text.insert(tk.END,"If you move the mouse in the left diagram, the coordinats will be displayed in the bottom of the diagram < x=.. and y=.. > x means the point of the nmscale.\n")
        text.insert(tk.END,"Clicking with the left mousebutton will select a slice through the curves at the x-value. This slice is displayed in the upper left window. This function works only if the [3 D Print] is not toggled.\n") 
        text.insert(tk.END,"To check the kinetic order the log(absorbance) is displayed in the lower left window. This can be toggled with the [ln[A] 1/[A]]-button to display 1/[A]\n")   
        text.insert(tk.END,"\nSelection\n\n",'h2')
        text.insert(tk.END,"It is possible to display only parts of the measurements by selecting with the mouse. All other functions should work.\n")
    elif (helpfor == 7):
        text.image_create(tk.END,image=photoImg2)
        text.insert(tk.END," Methods\n",'h1')
        text.insert(tk.END,"\nIn this part of the programm it is possible to determine the concentration of a compound with the spectrometer.\n")
        text.insert(tk.END,"1) Try out  concentration of the compount, ICG, SH, light source etc. that works fine and give an absorbance of approx 1.\nCheck [nm], [Darkline] and [Baseline]\n")
        text.insert(tk.END,"2) Dilute the solution for the standard curve.\nFor example if the last concentration in 30mmol and 5 solution are made. You have to prepare 6mmol,12mmol,18mmol,24mmol and 30mmol.\n")
        text.insert(tk.END,"3) Complete the dialog <Edit the method> and [add Method]. The method will appear in the methods window, with a line for each concentration.\n")
        text.insert(tk.END,"4) Now insert the cuvette with the specific concentration and select the line.\nThe measurement takes place and the absorbance will be stored\n")
        text.insert(tk.END,"5) If everything is ok, you can save the method and it's values.\n")
        text.insert(tk.END,"\nThe fitting curve is determined by numpy's polyfit and the r2_score and displayed.\n")
        text.insert(tk.END,"\nAfterwards an unknown concentration of a compound can be determined over the dialog <Do measurements>")
    ### at the end
    text.config(state=tk.DISABLED)
    top.focus_set()
    top.grab_set()
    top.wait_window()