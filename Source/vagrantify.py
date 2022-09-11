'''
  The main goal of the vagrantify project is to save time when deploying and configuring VMs.
    Copyright (C) 2022  Chakib

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
#! /usr/bin/env python3

from base64 import decode
from cgitb import text
from cmath import exp
from sqlite3 import Cursor
import time
from encodings import utf_8
import enum
from importlib.metadata import EntryPoint, PathDistribution
import ipaddress
import linecache
import string
import subprocess
import sys
import os
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from tkinter.ttk import Combobox, Progressbar, Style
import io
import threading
from tkinter import filedialog
import uuid
import ctypes
from tkinter.messagebox import *
from subprocess import run

from re import search
# ----- Web scraping -----

from urllib.request import urlopen as uReq


# import webbrowser
import webbrowser


from PIL import Image, ImageTk
import bs4

# to remove folders
import shutil


from bs4 import BeautifulSoup as soup
# --------- psutil (to get RAM info) ----------
import psutil
from ttkthemes import ThemedTk, THEMES

# import ttkbootstrap as ttk

# allows you to determine the path of a folder from a file
from pathlib import Path

# Reference:
# msdn.microsoft.com/en-us/library/windows/desktop/bb762153(v=vs.85).aspx


# noinspection SpellCheckingInspection
class SW(enum.IntEnum):
    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):
    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26


def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:
       # noinspection SpellCheckingInspection
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None,
            'runas',
            sys.executable,
            subprocess.list2cmdline(sys.argv),
            None,
            SW.HIDE
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))


def main():

    import ctypes
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )

    absolutepath = os.path.abspath(__file__)
    GetWorkingDir = os.path.dirname(absolutepath)
    # main code
    # root = Tk()
    root = ThemedTk(themebg=True)
    root.set_theme('vista')
    root.geometry("1250x685")
    root.title("Vagrantify")
    root.configure(background='blue')
    root.iconbitmap(f"{GetWorkingDir}\\img-EN\\Program.ico")

    # Configuration and return buttons
    style = ttk.Style(root)
    style.configure("C.TButton",
        padding=8, 
    )

    style.map("C.TButton",
        foreground=[('pressed', 'red')],
        background=[('pressed', 'red'), ('active', 'yellow') ],
        highlightcolor=[('active', 'red' )] 
    )
    

    style.map("TButton",
        foreground=[('pressed', 'red')],
        background=[('active', 'yellow'), ('hover', 'red') ],
        highlightcolor=[('active', 'red' )] 
    )


    style.configure('TEntry', foreground="blue")
    style.configure(
        "TEntry",
        # Red background.
        fieldbackground="#ff0000",
        # Blue text color.
        foreground="#0000ff"
    )


    # Frame style
    style.configure('TFrame', background='#cad6ab')


    ico_btn_configuration = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\btn_configuration.png")
    ico_btn_add_replace = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\Add_replace.png")
    ico_btn_add_only = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\Add_only.png")
    ico_btn_return = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\Return.png")
    ico_btn_Search = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\Search.png")
    ico_btn_listBoxes = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\ListBoxes.png")
    ico_btn_ValidateTheNumberOfVm = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\ValidateTheNumberOfVm.png")
    ico_btn_Deploy = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\Deploy.png")
    ico_btn_SelectAFile = PhotoImage(file = f"{GetWorkingDir}\\img-EN\\SelectAFile.png")

    # ----------- connection verification -----------
    import urllib.request
    def connect(host='http://google.com'):
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False


    # ----------- End of connection check ----------


    root.wm_attributes('-transparentcolor', 'grey')

    # ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


    # Add image file
    bg = PhotoImage( file = f"{GetWorkingDir}\\img-EN\\gradient_img.png")

    # Create a canvas 
    my_canvas1 = Canvas(root, width=800, height=800)
    my_canvas1.pack(fill="both", expand=True)
    my_canvas1.create_image(0,0, image=bg, anchor="nw")

    my_canvas2 = Canvas(root, width=800, height=800)
    my_canvas2.pack(fill="both", expand=True)
    my_canvas2.create_image(0,0, image=bg, anchor="nw")


    # -<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    def Window2():
        my_canvas2.pack(fill="both", expand=True)
        my_canvas1.pack_forget()


    def Window1():
        my_canvas1.pack(fill="both", expand=True)
        my_canvas2.pack_forget()


    Window1()

    List = []

    # f = open('filtered.txt', encoding='utf-8', errors='ignore')
    def Put_txt_into_list():
        List.clear()
        Lb.delete(0, END)
        f = open('{}\\filtered2.txt'.format(GetWorkingDir), 'r').readlines()
        for line in f:
            # line = str()
            # line.encode('ascii', errors='ignore')
            line.strip()
            List.append(line)
            progress.stop()
        update(List)    
    
    
    
    dataCbPlatformType = list()

    dataCbPlatformType = ["All", "aws","cloudstack","digitalocean","docker","google","hyperv","libvirt","lxc","openstack","parallels","qemu","rackspace","softlayer","veertu","virtualbox", "vmware_esxi", "vmware_desktop","vmware_fusion","vmware_ovf","vmware_workstation","vsphere","xenserver"]

    def searchBtn():

        # Check internet access
        if connect():
            NONE
        else:
            VerifyConnectionBeforeSearch_Window =  my_canvas1.create_text(170, 590, anchor="nw", text="Please check your internet connection and try again", font=("Heveletica", 12, "bold"), fill="red")
            time.sleep(8)
            my_canvas1.itemconfig(VerifyConnectionBeforeSearch_Window, text="")

        # Show the two buttons to add the boxes to the list
        Btn_AddToListAndRemplc_window = my_canvas1.create_window(210, 550, anchor="nw", window=Btn_AddToListAndRemplc)
        Btn_AddToListWithoutRemplc_window = my_canvas1.create_window(390, 550, anchor="nw", window=Btn_AddToListWithoutRemplc)


        my_canvas1.itemconfig(PlatformType_txt_dispo_window, text="Available platforms")  
        my_canvas1.itemconfig(progress_window, window=progress)
        Lb.delete(0, END)
        if os.path.exists("{}\\filtered.txt".format(GetWorkingDir)):
            os.unlink("{}\\filtered.txt".format(GetWorkingDir))
        f = open('{}\\filtered.txt'.format(GetWorkingDir), 'w+')
        f.write('')
        f.close()
        Get_User_input = entrySearch.get() 
        slash_test = "/"
        end_count_default = 11
        if page_Number.get() != 0:
            end_count_default = page_Number.get() + 1
        elif slash_test in entrySearch.get():
            end_count_default = 3
        for down in range(1,end_count_default):
            if ComboSearchPlaformTypeVar.get() == "vmware_esxi":
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Invoke-WebRequest 'https://app.vagrantup.com/boxes/search?order=desc&page={}&q={}&provider=vmware&sort=created' -UseBasicParsing".format(down, Get_User_input), "| Select-String 'alt='", "| findstr 'alt='", "| ForEach-Object {$_.split('\"')[3]}", ">> '{}\\filtered.txt'".format(GetWorkingDir)])
                progress.config(value=down, maximum=end_count_default)
                progress.step()
            elif ComboSearchPlaformTypeVar.get() != "" and ComboSearchPlaformTypeVar.get() != "All":
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Invoke-WebRequest 'https://app.vagrantup.com/boxes/search?order=desc&page={}&q={}&provider={}&sort=created' -UseBasicParsing".format(down, Get_User_input,ComboSearchPlaformTypeVar.get()), "| Select-String 'alt='", "| findstr 'alt='", "| ForEach-Object {$_.split('\"')[3]}", ">> '{}\\filtered.txt'".format(GetWorkingDir)])
                progress.config(value=down, maximum=end_count_default)
                progress.step()
            elif ComboSearchPlaformTypeVar.get() == "":
                # Fetch content from vagrantup site and store result in filtered.txt file
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Invoke-WebRequest 'https://app.vagrantup.com/boxes/search?order=desc&page={}&provider=&q={}&sort=created' -UseBasicParsing".format(down, Get_User_input), "| Select-String 'alt='", "| findstr 'alt='", "| ForEach-Object {$_.split('\"')[3]}", ">> '{}\\filtered.txt'".format(GetWorkingDir)])
                Test_if_empty = subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Invoke-WebRequest 'https://app.vagrantup.com/boxes/search?order=desc&page={}&provider=&q={}&sort=created' -UseBasicParsing".format(down, Get_User_input), "| Select-String 'alt='", "| findstr 'alt='", "| ForEach-Object {$_.split('\"')[3]}"])
                progress.config(value=down, maximum=end_count_default)
                progress.step()
            elif ComboSearchPlaformTypeVar.get() == "All":
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Invoke-WebRequest 'https://app.vagrantup.com/boxes/search?order=desc&page={}&provider=&q={}&sort=created' -UseBasicParsing".format(down, Get_User_input), "| Select-String 'alt='", "| findstr 'alt='", "| ForEach-Object {$_.split('\"')[3]}", ">> '{}\\filtered.txt'".format(GetWorkingDir)])
                progress.config(value=down, maximum=end_count_default)
                progress.step()
        ComboSearchPlaformType['values'] = dataCbPlatformType
        with open('{}\\filtered.txt'.format(GetWorkingDir), 'rb') as source_file:
            with open('{}\\filtered2.txt'.format(GetWorkingDir), 'w+b') as dest_file:
                contents = source_file.read()
                dest_file.write(contents.decode('utf-16').encode('utf-8'))
        Put_txt_into_list()
        my_canvas1.itemconfig(progress_window, window="")



    def CallSearchBtn_Function(e):
        threading.Thread(target=searchBtn).start() 


    def update(data):
        # Delete LB content
        Lb.delete(0, END)
        # this loop inserts the content of (List) into the listbox (LB)
        for item in data:
            Lb.insert(END, item)



    # the variable e is used to receive the event of the ListboxSelect method
    def toEntry(e): 
        threading.Thread(target=selectPlatfrom(Lb.get(ANCHOR))).start()
        # Clear entry content
        entrySearch.delete(0, END)
        # Insert the content of the listbox which is currently selected in the entry (my_entry)
        entrySearch.insert(0, Lb.get(ANCHOR))
        global Selected_to_variable
        Selected_to_variable = Lb.get(ANCHOR)


    # the variable e allows to receive the event of the KeyRelease method
    def search(e):
        # Put the contents of the input typed by the user in the variable typed
        typed = entrySearch.get()
        # If we don't type anything, or when we erase everything we typed
        if typed == '':
            # The contents of the listbox (my_list) should return as it was before
            # for this reason that we reassign the list to the variable data which it will be
            # passed back as an argument to the update function, above see what update() does
            data = List
        # otherwise
        else:
            # (in case we type something), we empty the content of the variable data
            # in order to be able to store the content typed by the user
            data = []
            # we will compare what the user has typed with what is in the List()
            for item in List:
                # it is interesting to put everything in lowercase so as not to loop what is in uppercase
                if typed.lower() in item.lower():
                    # Finally we add what satisfied the if condition in the variable data
                    data.append(item)
        # Now we will pass all the content that has been compared and that has met the if condition to the update function             
        update(data)

    List_multiSelect = []
    def Lb_multipleChoice(event):
        List_multiSelect.clear()
        curselection = Lb.curselection()
        for index in curselection:
            List_multiSelect.append(Lb.get(index))    



    def CheckbuttonMultipleChoiceSelect():
        if multipleChoiceValue.get() == 1:
            Lb.config(selectmode=MULTIPLE)
            Lb.bind("<<ListboxSelect>>", Lb_multipleChoice)
        elif multipleChoiceValue.get() == 0:
            Lb.bind('<<ListboxSelect>>', toEntry)
            Lb.config(selectmode=SINGLE)
       
    



    multipleChoiceValue = IntVar()
    CheckbuttonMultipleChoice = Checkbutton(root, text=" Multiple choice", variable=multipleChoiceValue, command=CheckbuttonMultipleChoiceSelect, bg='#1474e4', relief="raised", cursor="hand2")
    def CheckbuttonMultipleChoiceColor(color):
        if multipleChoiceValue.get() == 0:
            CheckbuttonMultipleChoice.configure(bg='green')
        elif multipleChoiceValue.get() == 1:
            CheckbuttonMultipleChoice.configure(bg='#1474e4')
    CheckbuttonMultipleChoice.bind("<Button-1>", CheckbuttonMultipleChoiceColor)
    CheckbuttonMultipleChoice_window = my_canvas1.create_window(685, 95, anchor="nw", window=CheckbuttonMultipleChoice)



    # LinesNumber = len(open('filtered.txt').readlines())


    choiceVar = StringVar(value=List)


    # Add selection and replace it
    def AddToListAndRemplc():
        my_canvas2.itemconfig(Btn_ListBoxesWithoutDelete_window, window="")
        my_canvas2.itemconfig(Btn_ListBoxesAndDelete_window, window=Btn_ListBoxesAndDelete)
        Btn_ListBoxesWithoutDelete['state'] = DISABLED
        Btn_ListBoxesAndDelete['state'] = NORMAL
        Box_List.clear()
        if multipleChoiceValue.get() == 1:
            for l in List_multiSelect:
                Box_List.append(l)
            multipleChoiceValue.set(0)
            Lb.config(selectmode=SINGLE)
            Lb.bind('<<ListboxSelect>>', toEntry)
        else:
            Selected_to_variable = Lb.get(ANCHOR)
            Box_List.append(Selected_to_variable)  
 

    # Add the selection without replacing it, useful when you want to search for different types of OS
    def AddToListWithoutRemplc():
        my_canvas2.itemconfig(Btn_ListBoxesAndDelete_window, window="")
        my_canvas2.itemconfig(Btn_ListBoxesWithoutDelete_window, window=Btn_ListBoxesWithoutDelete)
        Btn_ListBoxesAndDelete['state'] = DISABLED
        Btn_ListBoxesWithoutDelete['state'] = NORMAL
        if multipleChoiceValue.get() == 1:
            for l in List_multiSelect:
                Box_ListWithoutDeleteer.append(l)
            multipleChoiceValue.set(0)
            Lb.config(selectmode=SINGLE)
            Lb.bind('<<ListboxSelect>>', toEntry)
        else:
            Selected_to_variable = Lb.get(ANCHOR)
            Box_ListWithoutDeleteer.append(Selected_to_variable)



    # ------------------------------ Function webScraping ------------------------------
    
   
    dataCb= list()



    def selectPlatfrom(e):
        cb.delete(0, END)
        
        dataCb.clear()        
        lst_BoxType = []
        Get_Selection = e
        # my_url = 'https://app.vagrantup.com/boxes/search?&provider=&q={}'.format(Lb.get(ANCHOR))
        my_url = 'https://app.vagrantup.com/boxes/search?&provider=&q={}'.format(Get_Selection)
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("div", {"class":"col-md-3"})
        container = containers[0]
        BoxType = container.span["title"]


        if "and" in BoxType:
            BoxType = BoxType.replace('and ', '')
        if "aws" in BoxType:
            lst_BoxType.append("aws")
        if "virtualbox" in BoxType:
            lst_BoxType.append("virtualbox")
        if "vmware_desktop" in BoxType:
            lst_BoxType.append("vmware_desktop")
        if "libvirt" in BoxType:
            lst_BoxType.append("libvirt")
        if "parallels" in BoxType:
            lst_BoxType.append("parallels")
        if "hyperv" in BoxType:
            lst_BoxType.append("hyperv")
        if "docker" in BoxType:
            lst_BoxType.append("docker")
        if "vmware_fusion" in BoxType:
            lst_BoxType.append("vmware_fusion")
        if "vmware_ovf" in BoxType:
            lst_BoxType.append("vmware_ovf")
        if "cloudstack" in BoxType:
            lst_BoxType.append("cloudstack")
        if "digitalocean" in BoxType:
            lst_BoxType.append("digitalocean")
        if "lxc" in BoxType:
            lst_BoxType.append("lxc")
        if "qemu" in BoxType:
            lst_BoxType.append("qemu")
        if "openstack" in BoxType:
            lst_BoxType.append("openstack")
        if "rackspace" in BoxType:
            lst_BoxType.append("rackspace")
        if "softlayer" in BoxType:
            lst_BoxType.append("softlayer")
        if "xenserver" in BoxType:
            lst_BoxType.append("xenserver")
        if "vsphere" in BoxType:
            lst_BoxType.append("vsphere")
        if "veertu" in BoxType:
            lst_BoxType.append("veertu")
        if "google" in BoxType:
            lst_BoxType.append("google")
        if "vmware" in BoxType:
            lst_BoxType.append("vmware_esxi")
        if "vmware_workstation" in BoxType:
            lst_BoxType.append("vmware_workstation")


        for l in lst_BoxType:
            dataCb.append(l)
            

        cb['values'] = dataCb


        my_canvas1.itemconfig(PlatformType_txt_window, text="{}".format('\n'.join(map(str, lst_BoxType))))

        

    # ------------------------------ END function webScraping ------------------------------
    

    progress = ttk.Progressbar(root, orient=HORIZONTAL, length=250, maximum=0, value=0, mode="determinate")
    progress_window = my_canvas1.create_window(25, 620, anchor="nw")


    Listbox_scrollbar = ttk.Scrollbar(root)
    Listbox_scrollbar_window = my_canvas1.create_window(754, 136, anchor="nw", window=Listbox_scrollbar, height=408)


    spin_default_txtPageNum_window = my_canvas1.create_text(620, 68, text="Number of pages :", font=("Times", 8, "bold"), fill="white")
    spin_default_txt_window = my_canvas1.create_text(620, 80, text="(default 10)", font=("Times", 8, "bold"), fill="white")

    page_Number = IntVar()
    spin = ttk.Spinbox(root, from_ = 0, to = 1000, textvariable=page_Number, font='Times 12', width=4)
    spin_window = my_canvas1.create_window(685, 60, anchor="nw", window=spin)

    cb_txt_window = my_canvas1.create_text(857, 155, text="Selected platform", font=("Times", 12), fill="blue")

    GetPlatformType = StringVar()
    


    cb = ttk.Combobox(root, values=dataCb, textvariable=GetPlatformType, state='readonly', width=15)
    cb_window = my_canvas1.create_window(790, 175, anchor="nw", window=cb, width=150, height=30)


    PlatformType_txt_window = my_canvas1.create_text(800, 280, text="", anchor='nw', font=("Times", 11), fill="blue")


    searchLabel = my_canvas1.create_text(65, 30, text="Search", font=("Helvetica", 18, 'bold'), fill="white")


    entrySearch = ttk.Entry(root, text="Search", width=50)
    entrySearch.bind('<KeyRelease>', search)
    entrySearch_window = my_canvas1.create_window(25, 50, anchor="nw", window=entrySearch, height=45, width=280)
    entrySearch.bind("<Return>", CallSearchBtn_Function)

    ComboSearchPlaformTypeVar = StringVar()

    

    ComboSearchPlaformType = ttk.Combobox(root, values=dataCbPlatformType, textvariable=ComboSearchPlaformTypeVar, state='readonly', width=15)
    ComboSearchPlaformType_window = my_canvas1.create_window(445, 65, anchor="nw", window=ComboSearchPlaformType)
    ComboSearchPlaformType.set("All")

    btnSearch = ttk.Button(root, text="Search", padding=0, image=ico_btn_Search, command=lambda:threading.Thread(target=searchBtn).start(), cursor="hand2")
    btnSearch_window = my_canvas1.create_window(340, 50, anchor="nw", window=btnSearch)


    def toEntry1(e):
        for i in Lb.curselection():
            Get_selection = Lb.get(i + 1)
        threading.Thread(target=selectPlatfrom(Get_selection)).start()


    Lb = Listbox(root, width=120, height=25, bg='#F7F2E6', relief=GROOVE, activestyle='none', borderwidth=4, listvariable=choiceVar, cursor="hand2", highlightcolor="blue", selectforeground="white", selectbackground="green", highlightbackground="pink")
    Lb.bind('<<ListboxSelect>>', toEntry1)
    # Lb.bind('<Down>', toEntry1)

    Lb_window = my_canvas1.create_window(25, 135, anchor="nw", window=Lb)
    Lb.config(yscrollcommand=Listbox_scrollbar.set)
    Listbox_scrollbar.config(command=Lb.yview)

    Btn_AddToListAndRemplc = ttk.Button(root, text="Add and Replace", padding=0, image=ico_btn_add_replace, command=lambda:threading.Thread(target=AddToListAndRemplc).start())


    Btn_AddToListWithoutRemplc = ttk.Button(root, text="Add to list", padding=0, image=ico_btn_add_only, command=lambda:threading.Thread(target=AddToListWithoutRemplc).start())



    update(List)

    nextBtn = ttk.Button(root, text="", command=Window2, image=ico_btn_configuration, style="C.TButton", width=2, padding=0)
    nextBtn_window = my_canvas1.create_window(660, 560, anchor="nw", window=nextBtn)



    def AutoInstallChocolatey():        
        # checkIfChocoInstalled = subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "chocolatey -?"])
        import subprocess as sp
        child = sp.Popen(["powershell.exe", "chocolatey -?"] , stdout=sp.PIPE)
        streamdata = child.communicate()[0]
        retrunCodeChocolatey = child.returncode
        if retrunCodeChocolatey == 1:
            ChocoIsInstalling_windows = my_canvas1.create_text(75, 25, text="Search", font=("Helvetica", 18), fill="blue")
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Set-ExecutionPolicy Bypass -Scope Process -Force", "; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072", " ; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"])
            my_canvas1.itemconfigure(ChocoIsInstalling_windows, state='hidden')  

    threading.Thread(target=AutoInstallChocolatey).start()

    ######################################################### Second window #########################################################


    backBtn = ttk.Button(root, text="Retour", command=Window1, padding=0, image=ico_btn_return, style="C.TButton")
    backBtn_window = my_canvas2.create_window(25, 550, anchor="nw", window=backBtn)
    
    
    Box_List = []
    Box_ListWithoutDeleteer = []

    Box_ListVirtualbox = []
    Box_ListHyperV = []


    def ReadBoxesFromFileAndRemplc():
        # Box_List.clear()
        Listbox_box.delete(0, END)
        for box in Box_List:
            Listbox_box.insert(END, box)
        if Listbox_box.get(0, END):
            Btn_ListBoxesAndDelete['state'] = DISABLED
        def Btn_AddToListAndRemplc_clicked(e):
            Btn_ListBoxesAndDelete['state'] = NORMAL
        Btn_AddToListAndRemplc.bind("<Button-1>", Btn_AddToListAndRemplc_clicked)
            
    VarListbox = StringVar(value=Box_List)



    
    def ReadBoxesFromFileWithoutRemplc():
        for box in Box_ListWithoutDeleteer:
            Box_List.append(box)
            Listbox_box.insert(END, box)
        # f = open('C:\\Projet\\testgo.txt', 'w')
        # # empty the contents of the file testgo.txt
        # f.write('')
        # f.close()
        if Listbox_box.get(0, END):
            Btn_ListBoxesAndDelete['state'] = DISABLED
        def Btn_AddToListAndRemplc_clicked(e):
            Btn_ListBoxesAndDelete['state'] = NORMAL
        Btn_AddToListAndRemplc.bind("<Button-1>", Btn_AddToListAndRemplc_clicked)
        Btn_ListBoxesAndDelete_window = my_canvas2.create_window(65, 430, anchor="nw", window=Btn_ListBoxesAndDelete)
        Btn_ListBoxesWithoutDelete['state'] = DISABLED
        Box_ListWithoutDeleteer.clear()
        

    # Declaration of a dictionary for adding values
    Modified_Box_List = {}

    # ------------------- Start Configuration function -----------------
    def FuncConfiguration():
        if ConfCheck.get() == 1:

            # Clear text RAM & CPU
            my_canvas2.itemconfig(GetValueRamActu_window, text="")
            my_canvas2.itemconfig(GetValueCpuActu_window, text="")

            # RAM
            my_canvas2.itemconfig(TxtRamEntry_window, text="RAM :")
            my_canvas2.itemconfig(RamEntry_window, window=RamEntry)
            my_canvas2.itemconfig(Ram_Scale_window, window=Ram_Scale)

            # CPU
            my_canvas2.itemconfig(TxtCpuEntry_window, text="CPU :")
            my_canvas2.itemconfig(CpuEntry_window, window=CpuEntry)
            my_canvas2.itemconfig(CpuScale_window, window=CpuScale)


        elif ConfCheck.get() == 0:
            

            # RAM
            my_canvas2.itemconfig(TxtRamEntry_window, text="")
            my_canvas2.itemconfig(RamEntry_window, window="")
            my_canvas2.itemconfig(Ram_Scale_window, window="")

            # CPU
            my_canvas2.itemconfig(TxtCpuEntry_window, text="")
            my_canvas2.itemconfig(CpuEntry_window, window="")
            my_canvas2.itemconfig(CpuScale_window, window="")

    


    # ------------------- End Configuration function -----------------
    
    
    ConfCheck = IntVar()
    
    def WhenAnchorClick(e):

        # Position the Number of VMs validation buttons
        spin_VmNumber_window = my_canvas2.create_window(220, 480, anchor="nw", window=spin_VmNumber)
        Btn_ValidateNumberOfVMs_window = my_canvas2.create_window(35, 475, anchor="nw", window=Btn_ValidateNumberOfVMs)


        # ----- Show Esxi conf -----

        if GetPlatformType.get() == "vmware_esxi":

            my_canvas2.itemconfig(SeparatorLine, text="___________________________________________________________________________________________")

            my_canvas2.itemconfig(info_ESXI, text="1- It is important to download and install OVF Tool before\n launching the deployment: Option > install > OVF Tool \n\n2- Install Vmware-Esxi plugin, Option > install > Vmware-Esxi plugin\n\n3- Please make sure ssh is enabled on your ESXI hypervisor")
            
            my_canvas2.itemconfig(Esxi_HostnameText, text="ESXI Hostname / IP")
            my_canvas2.itemconfig(Esxi_Hostname_Window, window=Esxi_Hostname)

            my_canvas2.itemconfig(Esxi_UsernameText, text="ESXI Username")
            my_canvas2.itemconfig(Esxi_Username_Window, window=Esxi_Username)

            # my_canvas2.itemconfig(Esxi_PasswordText, text="ESXI Password")
            # my_canvas2.itemconfig(Esxi_Password_Window, window=Esxi_Password)

            
        elif GetPlatformType.get() != "vmware_esxi":

            my_canvas2.itemconfig(SeparatorLine, text="")

            my_canvas2.itemconfig(info_ESXI, text="")

            my_canvas2.itemconfig(Esxi_HostnameText, text="")
            my_canvas2.itemconfig(Esxi_Hostname_Window, window="")

            my_canvas2.itemconfig(Esxi_UsernameText, text="")
            my_canvas2.itemconfig(Esxi_Username_Window, window="")

            # my_canvas2.itemconfig(Esxi_PasswordText, text="")
            # my_canvas2.itemconfig(Esxi_Password_Window, window="")
            
        # ---- End Show Esxi conf -----

        TextEntry_Deploy.delete('1.0', END)
        CheckConfProvisionProvNotSplit = Listbox_box.get(ANCHOR)
        CheckConfProvisionProv = CheckConfProvisionProvNotSplit.strip('\n') + "Prov"
        if CheckConfProvisionProv in ProvisionBox_List.keys():
            TextEntry_Deploy.insert(END, ProvisionBox_List[f'{CheckConfProvisionProv}']['Prov'])
            # print(ProvisionBox_List[f'{CheckConfProvisionProv}']['Prov'])
        else:
            TextEntry_Deploy.delete('1.0', END)
        # Reset provisioning
        CheckConfProvisionFunc()
        # Reset configuration
        ConfCheck.set(0)
        FuncConfiguration()

        my_canvas2.itemconfig(ShowVmNumWhenListboxAnchor_window, text="Number of VMs : {}".format(Box_List.count(Listbox_box.get(ANCHOR))), font=('Times 14 bold'), fill="white")
        
        # Put the global variable GetSelectionElementInListbox_boxRAM global
        global GetSelectionElementInListbox_boxRAM
        # Retrieve the content of the selected element and store it in the variable GetSelectionElementInListbox_box
        GetSelectionElementInListbox_box = Listbox_box.get(ANCHOR)
        # Remove the \n characters and put the content back in the variable GetSelectionElementInListbox_boxRAM
        GetSelectionElementInListbox_boxRAM = GetSelectionElementInListbox_box.strip('\n') + "RAM"


    
        global GetSelectionElementInListbox_boxCPU
        GetSelectionElementInListbox_box2 = Listbox_box.get(ANCHOR)
        # Remove the \n characters and put the content back in the variable GetSelectionElementInListbox_boxCPU
        GetSelectionElementInListbox_boxCPU = GetSelectionElementInListbox_box2.strip('\n') + "CPU"



        # If we find the selected element in the Modified_box.. dictionary declared above, we configure the text and we display the value of RAM and CPU
        if GetSelectionElementInListbox_boxRAM in Modified_Box_List.keys() and 'RAM' in Modified_Box_List[f'{GetSelectionElementInListbox_boxRAM}'].keys():
            my_canvas2.itemconfig(GetValueRamActu_window, text="")
            GetValueRamActuVar = Modified_Box_List[f'{GetSelectionElementInListbox_boxRAM}']['RAM']
            my_canvas2.itemconfig(GetValueRamActu_window, text="RAM : {}".format(GetValueRamActuVar))



        if GetSelectionElementInListbox_boxCPU in Modified_Box_List.keys() and 'CPU' in Modified_Box_List[f'{GetSelectionElementInListbox_boxCPU}'].keys():
            my_canvas2.itemconfig(GetValueCpuActu_window, text="")
            GetValueCpuActuVar = Modified_Box_List[f'{GetSelectionElementInListbox_boxCPU}']['CPU']
            my_canvas2.itemconfig(GetValueCpuActu_window, text="CPU : {}".format(GetValueCpuActuVar))


        if GetSelectionElementInListbox_boxRAM not in Modified_Box_List.keys():
            my_canvas2.itemconfig(GetValueCpuActu_window, text="")
            my_canvas2.itemconfig(GetValueRamActu_window, text="")



        # Button that allows us to configure a VM
        if not Box_List:
            NONE
        else:

            Btn_ConfCheck = Checkbutton(root, text='Configure', variable=ConfCheck, command=FuncConfiguration, bg='#1474e4')
            Btn_ConfCheck_window = my_canvas2.create_window(550, 20, anchor="nw", window=Btn_ConfCheck)

            # Show provision checkbox (CLI)
            Btn_CheckConfProvision = Checkbutton(root, text="Provision", variable=CheckConfProvisionVar, command=CheckConfProvisionFunc, bg='#1474e4')
            Btn_CheckConfProvision_window = my_canvas2.create_window(650, 20, anchor="nw", window=Btn_CheckConfProvision)

            # Show provision checkbox (file)
            Btn_CheckConfProvision = Checkbutton(root, text="Provision (file)", variable=CheckConfProvisionFileVar, command=CheckConfProvisionFileFunc, bg='#1474e4')
            Btn_CheckConfProvision_window = my_canvas2.create_window(750, 20, anchor="nw", window=Btn_CheckConfProvision)

 
  
    # This function validates the number of vm to deploy
    def ValidateNumberOfVMs():
        CountElementsInsideList = Box_List.count(Listbox_box.get(ANCHOR))
        if spin_VmNumberVAR.get() == 0:
            NONE
        elif spin_VmNumberVAR.get() != 0 and CountElementsInsideList < spin_VmNumberVAR.get() :
            while CountElementsInsideList < spin_VmNumberVAR.get():
                Box_List.append(Listbox_box.get(ANCHOR))
                CountElementsInsideList = Box_List.count(Listbox_box.get(ANCHOR))
                if CountElementsInsideList == spin_VmNumberVAR.get():
                    break
            spin_VmNumberVAR.set(0)
            threading.Thread(target=WhenAnchorClick)
        elif spin_VmNumberVAR.get() == 0:
            NONE
        elif spin_VmNumberVAR.get() != 0 and CountElementsInsideList > spin_VmNumberVAR.get() :
            while CountElementsInsideList > spin_VmNumberVAR.get():
                Box_List.remove(Listbox_box.get(ANCHOR))
                CountElementsInsideList = Box_List.count(Listbox_box.get(ANCHOR))
                if CountElementsInsideList == spin_VmNumberVAR.get():
                    break
            spin_VmNumberVAR.set(0)
            threading.Thread(target=WhenAnchorClick)

    
    ProvisionBox_List = {}

    def DeployAll():
        global folderName
        global pathFolder
        global randomtxt
        global box
        # the default filedialog opening path points to C:/
        folder = filedialog.askdirectory(initialdir=os.path.normpath("C://"), title="Emplacement de sauvegarde")
        # If the user has chosen his path, the deployment is triggered, otherwise the deployment button does nothing
        if folder != '':
            if GetPlatformType.get() == '':
                my_canvas2.itemconfig(PleaseSelectPlatformTypeTxt_window, text="Please select your platform")
                time.sleep(5)
                my_canvas2.itemconfig(PleaseSelectPlatformTypeTxt_window, text="")
            if GetPlatformType.get() != '':
                pathFolder = folder + "/"
                # Deployment in progress
                my_canvas1.itemconfig(PlatformTypeTxtDeploiementEncours_window1, text="Deployment in progress")
                my_canvas2.itemconfig(PlatformTypeTxtDeploiementEncours_window2, text="Deployment in progress")
                time.sleep(8)
                my_canvas1.itemconfig(PlatformTypeTxtDeploiementEncours_window1, text="")
                my_canvas2.itemconfig(PlatformTypeTxtDeploiementEncours_window2, text="")
                # For each item that is in Box List
                for box in Box_List:
                    txtNotSplited = box.strip('\n')
                    txt = txtNotSplited.split("/")
                    folderName = txt[0] + '_' + txt[1]
                    randomtxt = txt[0] + "" + txt[1] + str(uuid.uuid4())[:4]
                    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "mkdir {}{}/{}".format(pathFolder,folderName,randomtxt)])
                    txtNotSplitedRAM = txtNotSplited + "RAM"
                    txtNotSplitedCPU = txtNotSplited + "CPU"
                    # print(Var_RadioProvisionnerType.get())
                    if GetPlatformType.get() == "vmware_esxi":
                        subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "cd {}{}/{}".format(pathFolder,folderName,randomtxt), "; vagrant init -m {}".format(box)])
                        f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "r")
                        contents = f.readlines()
                        f.close()
                        contents.insert(5, f'  config.vm.provider "{GetPlatformType.get()}" do |platform| \n')
                        contents.insert(6,  '    platform.esxi_hostname = "{}" \n'.format(Esxi_Hostname.get()))
                        contents.insert(7, '    platform.esxi_username = "{}" \n'.format(Esxi_Username.get()))
                        contents.insert(8, f'    platform.esxi_password = "prompt:" \n')
                        contents.insert(9, '  end \n')
                        f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "w")
                        contents = "".join(contents)
                        f.write(contents)
                        f.close()
                    else:
                        subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "cd {}{}/{}".format(pathFolder,folderName,randomtxt), "; vagrant init -m {}".format(box)])
                    if txtNotSplitedRAM in Modified_Box_List.keys() or txtNotSplitedCPU in Modified_Box_List.keys():
                        if not "CPU" in Modified_Box_List.keys() :
                            Modified_Box_List[f'{GetSelectionElementInListbox_boxCPU}'] = {'CPU' : 1}
                        # ------------ Start configuration vagrantfile ----------------
                            GetActualRamValue = Modified_Box_List[f'{txtNotSplitedRAM}']['RAM']
                            GetActualCpuValue = Modified_Box_List[f'{txtNotSplitedCPU}']['CPU']
                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "r")
                            contents = f.readlines()
                            f.close()
                            if GetPlatformType.get() == "vmware_esxi":
                                contents.insert(6,  '    platform.guest_memsize = "{}" \n'.format(GetActualRamValue))
                                contents.insert(7, f'    platform.guest_numvcpus = {GetActualCpuValue} \n')
                            else:
                                contents.insert(5, f'  config.vm.provider "{GetPlatformType.get()}" do |platform| \n')
                                contents.insert(6,  '    platform.memory = "{}" \n'.format(GetActualRamValue))
                                contents.insert(7, f'    platform.cpus = {GetActualCpuValue} \n')
                                contents.insert(8, '  end \n')

                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "w")
                            contents = "".join(contents)
                            f.write(contents)
                            f.close()


                    # Linux deployment
                    if CheckConfProvisionVar.get() == 1 and dict_RadioType[f'{txtNotSplited}']['RadioType'] == 1:
                        Element_in_BoxListProv = box.strip('\n') + "Prov"
                        if Element_in_BoxListProv in ProvisionBox_List.keys() and Element_in_BoxListProv == Element_in_BoxListProv:
                            ProvisionBox_List[f'{CheckConfProvisionProv}'] = {'Prov' : TextEntry_Deploy.get(1.0, END+"-1c")}
                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "r")
                            contents = f.readlines()
                            f.close()
                            # Add this line
                            contents.insert(5, f'  config.vm.provision "shell", inline: <<-SHELL\n')

                            # Retrieve the number of rows in the TextEntry_deploy widget
                            Provisionlistnotsplitted = ProvisionBox_List[f"{Element_in_BoxListProv}"]['Prov']
                            Provisionlistsplitted = Provisionlistnotsplitted.split('\n')

                            xTextEntry_line = 6
                            for lineTextEntry in Provisionlistsplitted:
                                contents.insert(xTextEntry_line, f'    {lineTextEntry} \n')
                                xTextEntry_line = xTextEntry_line + 1

                            
                            contents.insert(xTextEntry_line, '{}\n'.format("SHELL"))

                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "w")
                            contents = "".join(contents)
                            f.write(contents)
                            f.close()

                    # Windows deployment
                    if CheckConfProvisionVar.get() == 1 and dict_RadioType[f'{txtNotSplited}']['RadioType'] == 2:
                        Element_in_BoxListProv = box.strip('\n') + "Prov"
                        if Element_in_BoxListProv in ProvisionBox_List.keys():
                            ProvisionBox_List[f'{CheckConfProvisionProv}'] = {'Prov' : TextEntry_Deploy.get(1.0, END+"-1c")}
                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "r")
                            contents = f.readlines()
                            f.close()
                            # Add this line
                            contents.insert(5, f'  config.vm.provision "shell", privileged: "true", powershell_elevated_interactive: "true", inline: <<-SHELL\n')

                            # Retrieve the number of rows in the TextEntry_deploy widget
                            Provisionlistnotsplitted = ProvisionBox_List[f"{Element_in_BoxListProv}"]['Prov']
                            Provisionlistsplitted = Provisionlistnotsplitted.split('\n')

                            xTextEntry_line = 6
                            for lineTextEntry in Provisionlistsplitted:
                                contents.insert(xTextEntry_line, f'    {lineTextEntry} \n')
                                xTextEntry_line = xTextEntry_line + 1
                            contents.insert(xTextEntry_line, '{}\n'.format("SHELL"))

                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "w")
                            contents = "".join(contents)
                            f.write(contents)
                            f.close()
                        
                    # Powershell file deployment
                    if CheckConfProvisionFileVar.get() == 1 and dict_RadioType[f'{txtNotSplited}']['RadioType'] == 4:
                        Element_in_BoxListProv = box.strip('\n') + "Prov"
                        if Element_in_BoxListProv in ProvisionBox_List.keys() and Element_in_BoxListProv == Element_in_BoxListProv:
                            ProvisionBox_List[f'{CheckConfProvisionProv}'] = {'Prov' : TextEntry_Deploy.get(1.0, END+"-1c")}
                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "r")
                            contents = f.readlines()
                            f.close()
                            # Add this line
                            contents.insert(5, f'  config.vm.provision "shell", path: "{PowershellFileName}"\n')

                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "w")
                            contents = "".join(contents)
                            f.write(contents)
                            f.close()

                    # Linux File Deployment
                    if CheckConfProvisionFileVar.get() == 1 and dict_RadioType[f'{txtNotSplited}']['RadioType'] == 4:
                        Element_in_BoxListProv = box.strip('\n') + "Prov"
                        if Element_in_BoxListProv in ProvisionBox_List.keys() and Element_in_BoxListProv == Element_in_BoxListProv:
                            ProvisionBox_List[f'{CheckConfProvisionProv}'] = {'Prov' : TextEntry_Deploy.get(1.0, END+"-1c")}
                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "r")
                            contents = f.readlines()
                            f.close()
                            # Add this line
                            contents.insert(5, f'  config.vm.provision "shell", path: "{LinuxFileName}"\n')

                            f = open("{}{}/{}/Vagrantfile".format(pathFolder,folderName,randomtxt), "w")
                            contents = "".join(contents)
                            f.write(contents)
                            f.close()


                        #--------------- End configuration vagrantfile ----------------

                    # subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "cd {}{}/{}".format(pathFolder,folderName,randomtxt), "; Start-Process powershell.exe ' -noexit vagrant up --provider={}'".format(GetPlatformType.get())])
                    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Start-Process powershell.exe ' -noexit cd {}{}/{} ; vagrant up --provider={}'".format(pathFolder,folderName,randomtxt,GetPlatformType.get())])
                    if box in ProvisionBox_List.keys():
                        subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "Start-Process powershell.exe ' -noexit cd {}{}/{} ; vagrant provision'".format(pathFolder,folderName,randomtxt,GetPlatformType.get())])



    # ------------ Checkconf entries configuration ------------ :


    # ***** Functions *****

    # Put contents of RAM entry into scale
    def InsertRamEnrtyOnScale(RamEntryToScale):
        Ram_Scale.set(RamEntry.get())
        Modified_Box_List[f'{GetSelectionElementInListbox_boxRAM}'] = {'RAM' : RamEntry.get()}
        # print(Modified_Box_List)

    # clear input content on click
    def GetRamValueScale(RAMValue):
        RamEntry.delete(0, END)
        RamEntry.insert(0, Ram_Scale.get())
        Modified_Box_List[f'{GetSelectionElementInListbox_boxRAM}'] = {'RAM' : RamEntry.get()}
        # print(Modified_Box_List)


    # Put content of CPU entry in scale
    def InsertCpuEnrtyOnScale(CpuEntryToScale):
        CpuScale.set(CpuEntry.get())
        # print(Modified_Box_List)

    # clear input content on click
    def GetCpuValueScale(CPUValue):
        CpuEntry.delete(0, END)
        CpuEntry.insert(0, CpuScale.get())
        Modified_Box_List[f'{GetSelectionElementInListbox_boxCPU}'] = {'CPU' : CpuEntry.get()}
        # print(Modified_Box_List)


    # ***** End Functions *****



    # RAM text
    TxtRamEntry_window = my_canvas2.create_text(380, 80, text="", font=("Times", 13, 'bold'), fill="white")

    # RAM input
    RamEntry = ttk.Entry(root)
    RamEntry.bind('<KeyRelease>', InsertRamEnrtyOnScale)
    RamEntry_window = my_canvas2.create_window(380, 120, anchor='nw', width=200)

    # Scale RAM
    ramCount = psutil.virtual_memory().total
    TotalRamAfterDevide = ramCount / 1000000
    Ram_Scale = Scale(root, label="RAM size (MB)", from_=1, to=TotalRamAfterDevide, orient=HORIZONTAL, command=GetRamValueScale, activebackground='green',bg='#1474e4')
    Ram_Scale_window = my_canvas2.create_window(380, 160, anchor="nw", width=200)

    # CPU text 
    TxtCpuEntry_window = my_canvas2.create_text(380, 260, text="", font=("Times", 13, 'bold'), fill="white")

    # CPU input
    CpuEntry = ttk.Entry(root)
    CpuEntry.bind('<KeyRelease>', InsertCpuEnrtyOnScale)
    CpuEntry_window = my_canvas2.create_window(380, 290, anchor="nw", width=200)

    # Scale CPU
    cpuCount = os.cpu_count()
    CpuScale = Scale(root, label="Number of CPUs", from_=1, to=cpuCount, orient=HORIZONTAL, command=GetCpuValueScale, activebackground='green',bg='#1474e4')
    CpuScale_window = my_canvas2.create_window(380, 320, anchor="nw", width=200)

    # -------------  End Checkconf entries configuration -------------


            
    # Show provisioning button

    def TextEntry_Deploy_WhenKeyrelease(TextRelease):
        ProvisionBox_List[f'{CheckConfProvisionProv}'] = {'Prov' : TextEntry_Deploy.get(1.0, END+"-1c")}
        # print(ProvisionBox_List.keys())
        # print(ProvisionBox_List.values())

    TextEntry_Deploy = Text(root, width=55, height=20)
    TextEntry_Deploy.bind('<KeyRelease>', TextEntry_Deploy_WhenKeyrelease)
    Var_RadioProvisionnerType = IntVar()


    TextEntry_Deploy = Text(root, width=55, height=20)
    TextEntry_Deploy.bind('<KeyRelease>', TextEntry_Deploy_WhenKeyrelease)
    TextEntry_Deploy_window = my_canvas2.create_window(695, 85, anchor="nw")



    # --------------- Start CheckConfProvisionFunc -------------------

    CheckConfProvisionVar = IntVar()
    CheckConfProvisionFileVar = IntVar()

    def CheckConfProvisionFileFunc():

        if CheckConfProvisionFileVar.get() == 1:

            
            my_canvas2.itemconfig(Btn_RadioPowershellFile_window, window=Btn_RadioPowershellFile)

            
            my_canvas2.itemconfig(Btn_RadioLinuxFile_window, window=Btn_RadioLinuxFile)

            
            CheckConfProvisionVar.set(0)

            global CheckConfProvisionProv

            CheckConfProvisionProvNotSplit = Listbox_box.get(ANCHOR)
            CheckConfProvisionProv = CheckConfProvisionProvNotSplit.strip('\n') + "Prov"
            
            my_canvas2.itemconfig(TextEntry_Deploy_window, window='')
            my_canvas2.itemconfig(Btn_RadioPowershell_window, window='')
            my_canvas2.itemconfig(Btn_RadioLinux_window, window='')


            

            
        elif CheckConfProvisionFileVar.get() == 0:

            my_canvas2.itemconfig(Dialog_fileRadioPowershell_window, window='')

            my_canvas2.itemconfig(Btn_RadioPowershellFile_window, window='')

            my_canvas2.itemconfig(Dialog_fileRadioLinux_window, window='')

            my_canvas2.itemconfig(Btn_RadioLinuxFile_window, window='')
      



    def CheckConfProvisionFunc():
        
        if CheckConfProvisionVar.get() == 1:
            global Var_RadioProvisionnerType

            my_canvas2.itemconfig(ProvisionFileNameLabel_window, text='')
       
            my_canvas2.itemconfig(Dialog_fileRadioPowershell_window, window='')

            my_canvas2.itemconfig(Dialog_fileRadioLinux_window, window='')


            CheckConfProvisionFileVar.set(0)

            my_canvas2.itemconfig(Btn_RadioPowershellFile_window, window='')

            my_canvas2.itemconfig(Btn_RadioLinuxFile_window, window='')

            my_canvas2.itemconfig(Btn_RadioPowershell_window, window=Btn_RadioPowershell)

            my_canvas2.itemconfig(Btn_RadioLinux_window, window=Btn_RadioLinux)



            global CheckConfProvisionProv

            CheckConfProvisionProvNotSplit = Listbox_box.get(ANCHOR)
            CheckConfProvisionProv = CheckConfProvisionProvNotSplit.strip('\n') + "Prov"
            # print(ProvisionBox_List.keys())
            # print(ProvisionBox_List.values())


            my_canvas2.itemconfig(TextEntry_Deploy_window, window=TextEntry_Deploy)
  

        elif CheckConfProvisionVar.get() == 0:

            my_canvas2.itemconfig(TextEntry_Deploy_window, window='')
            
            my_canvas2.itemconfig(Btn_RadioPowershell_window, window='')

            my_canvas2.itemconfig(Btn_RadioLinux_window, window='')


    # --------------- End CheckConfProvisionFunc -------------------


    # ------------------  Start of ESXI info-------------------

    SeparatorLine = my_canvas2.create_text(780, 420, text="", font=("Heveletica", 12, "bold"), fill="white")

    info_ESXI = my_canvas2.create_text(860,500, text="", font=("Heveletica", 12, "bold"), fill="red")


    # ------------------ End of ESXI info --------------------




    # --------------- Start ESXI Configuration --------------------

    Esxi_Title_Window = my_canvas2.create_text(450,420, text="")

    Esxi_HostnameText = my_canvas2.create_text(450,455, text="", font=("Heveletica", 12, "bold"), fill="white")
    Esxi_Hostname = Entry(root, text="Esxi Hostname")
    Esxi_Hostname_Window = my_canvas2.create_window(450, 480, window="")

    Esxi_UsernameText = my_canvas2.create_text(450,515, text="", font=("Heveletica", 12, "bold"), fill="white")
    Esxi_Username = Entry(root, text="Esxi Username")
    Esxi_Username_Window = my_canvas2.create_window(450, 540, window="")

    # Esxi_PasswordText = my_canvas2.create_text(450,490, text="")
    # Esxi_Password = Entry(root, text="Esxi Password")
    # Esxi_Password_Window = my_canvas2.create_window(450, 540, window="")

    # --------------- End ESXI Configuration -------------------


    # This listbox is on the second screen
    Listbox_box = Listbox(root, width=50, height=25, bg='#F7F2E6', relief=GROOVE, activestyle='none', borderwidth=4, listvariable=VarListbox, cursor="hand2", highlightcolor="blue", selectforeground="white", selectbackground="green", highlightbackground="pink", exportselection=False)
    Listbox_box_window = my_canvas2.create_window(25, 10, anchor="nw", window=Listbox_box)
    Listbox_box.bind('<<ListboxSelect>>', WhenAnchorClick)

    # it's a label
    ShowVmNumWhenListboxAnchor_window = my_canvas2.create_text(430, 25, text="", font=("Times", 8), fill="blue")


    # Show RAM value for selected item
    GetValueRamActu_window = my_canvas2.create_text(360, 80, text="", font=("Times", 8), fill="blue")


    Btn_ListBoxesAndDelete = ttk.Button(root, text="List the boxes", image=ico_btn_listBoxes, command=ReadBoxesFromFileAndRemplc)
    Btn_ListBoxesAndDelete_window = my_canvas2.create_window(65, 430, anchor="nw", window=Btn_ListBoxesAndDelete)


    Btn_ListBoxesWithoutDelete = ttk.Button(root, text="List the boxes", image=ico_btn_listBoxes, command=ReadBoxesFromFileWithoutRemplc)
    Btn_ListBoxesWithoutDelete_window = my_canvas2.create_window(65, 430, anchor="nw", window=Btn_ListBoxesWithoutDelete)
    # my_canvas2.itemconfigure(Btn_ListBoxesWithoutDelete_window, state='hidden')

    Btn_ValidateNumberOfVMs = ttk.Button(root, text="Validate the number", image=ico_btn_ValidateTheNumberOfVm, command=lambda:threading.Thread(target=ValidateNumberOfVMs).start())
    

    Btn_DeployAll = ttk.Button(root, text="Deploy", image=ico_btn_Deploy, command=lambda:threading.Thread(target=DeployAll).start())
    Btn_DeployAll_window = my_canvas2.create_window(200, 430, anchor="nw", window=Btn_DeployAll)

    spin_VmNumberVAR = IntVar()
    spin_VmNumber = ttk.Spinbox(root, from_ = 0, to = 1000, textvariable=spin_VmNumberVAR, width=5)



    PlatformType_txt_dispo_window = my_canvas1.create_text(795, 240, text="", anchor='nw', font=("Times", 12, 'bold'), fill="green")


    PleaseSelectPlatformTypeTxt_window = my_canvas2.create_text(500, 550, anchor="nw", text="", font=("Times", 18, 'bold'), fill="red")

    PlatformTypeTxtDeploiementEncours_window1 = my_canvas1.create_text(350, 580, anchor="nw", text="", font=("Times", 18, 'bold'), fill="green")
    PlatformTypeTxtDeploiementEncours_window2 = my_canvas2.create_text(500, 580, anchor="nw", text="", font=("Times", 18, 'bold'), fill="green")

    # Show CPU value for selected item
    GetValueCpuActu_window = my_canvas2.create_text(420, 100, text="", font=("Times", 12, 'bold'), fill="blue")
        
    # Show RAM value for selected item
    GetValueRamActu_window = my_canvas2.create_text(420, 80, text="", font=("Times", 12, 'bold'), fill="blue")
    
    Var_RadioProvisionnerType = IntVar() 
    
    dict_RadioType = {}



    def BindRadioLinux(BindLinux):
        AnchorWithNewline =  Listbox_box.get(ANCHOR)
        AnchorRemoveNewline = AnchorWithNewline.strip('\n')
        dict_RadioType[f'{AnchorRemoveNewline}'] = {'RadioType' : 1}
        # print(dict_RadioType[f'{AnchorRemoveNewline}']['RadioType'])
        # print(AnchorRemoveNewline)


    def BindRadioPowershell(BindPowershell):
        AnchorWithNewline =  Listbox_box.get(ANCHOR)
        AnchorRemoveNewline = AnchorWithNewline.strip('\n')
        dict_RadioType[f'{AnchorRemoveNewline}'] = {'RadioType' : 2}
        # print(dict_RadioType[f'{AnchorRemoveNewline}']['RadioType'])
        # print(AnchorRemoveNewline)



    def BindRadioPowershellFile(BindPowershellFile):
        AnchorWithNewline =  Listbox_box.get(ANCHOR)
        AnchorRemoveNewline = AnchorWithNewline.strip('\n')
        dict_RadioType[f'{AnchorRemoveNewline}'] = {'RadioType' : 4}
        # print(dict_RadioType[f'{AnchorRemoveNewline}']['RadioType'])
        # print(AnchorRemoveNewline)
        my_canvas2.itemconfig(Dialog_fileRadioPowershell_window, window=Dialog_fileRadioPowershell)
        my_canvas2.itemconfig(Dialog_fileRadioLinux_window, window='')


    def BindRadioLinuxFile(BindLinuxFile):
        AnchorWithNewline =  Listbox_box.get(ANCHOR)
        AnchorRemoveNewline = AnchorWithNewline.strip('\n')
        dict_RadioType[f'{AnchorRemoveNewline}'] = {'RadioType' : 5}
        # print(dict_RadioType[f'{AnchorRemoveNewline}']['RadioType'])
        # print(AnchorRemoveNewline)
        my_canvas2.itemconfig(Dialog_fileRadioLinux_window, window=Dialog_fileRadioLinux)
        my_canvas2.itemconfig(Dialog_fileRadioPowershell_window, window='')


        

    Btn_RadioLinux = Radiobutton(root, text="Linux", variable=Var_RadioProvisionnerType, value=1, bg='#1474e4')
    Btn_RadioLinux.bind("<Button-1>", BindRadioLinux)
    


    
    Btn_RadioLinux_window = my_canvas2.create_window(655, 50, anchor="nw")

    Btn_RadioPowershell = Radiobutton(root, text="Windows (Powershell)", variable=Var_RadioProvisionnerType, value=2, bg='#1474e4')
    Btn_RadioPowershell.bind("<Button-1>", BindRadioPowershell)
    Btn_RadioPowershell_window = my_canvas2.create_window(720, 50, anchor="nw")


    Btn_RadioPowershellFile = Radiobutton(root, text="Powershell", variable=Var_RadioProvisionnerType, value=4, bg='#1474e4')
    Btn_RadioPowershellFile.bind("<Button-1>", BindRadioPowershellFile)
    Btn_RadioPowershellFile_window = my_canvas2.create_window(760, 50, anchor="nw")

    Btn_RadioLinuxFile = Radiobutton(root, text="Linux", variable=Var_RadioProvisionnerType, value=5, bg='#1474e4')
    Btn_RadioLinuxFile.bind("<Button-1>", BindRadioLinuxFile)
    Btn_RadioLinuxFile_window = my_canvas2.create_window(865, 50, anchor="nw")



    def Dialog_fileRadioPowershellFunc():
        global PowershellFileName
        PowershellFileName = filedialog.askopenfilename(initialdir="C://", title="Select a file", filetypes=((".ps1 file", "*.ps1"), ("all files", "*.*")))
        if PowershellFileName != "" :
            ProvisionBox_List[f'{CheckConfProvisionProv}'] = {'Prov' : "Powershell"}
            # print(PowershellFileName)
            my_canvas2.itemconfig(ProvisionFileNameLabel_window, text=f"Chemin : {PowershellFileName}")


    def Dialog_fileRadioLinuxFunc():
        global LinuxFileName
        LinuxFileName = filedialog.askopenfilename(initialdir="C://", title="Select a file", filetypes=((".sh file", "*.sh"), ("all files", "*.*")))
        if LinuxFileName != "" :
            ProvisionBox_List[f'{CheckConfProvisionProv}'] = {'Prov' : "Linux"}
            # print(LinuxFileName)
            my_canvas2.itemconfig(ProvisionFileNameLabel_window, text=f"Chemin : {LinuxFileName}")


    Dialog_fileRadioPowershell = ttk.Button(root, text="Select a file", image=ico_btn_SelectAFile, command=Dialog_fileRadioPowershellFunc)
    Dialog_fileRadioPowershell_window = my_canvas2.create_window(775, 75, anchor="nw")

    Dialog_fileRadioLinux = ttk.Button(root, text="Select a file", image=ico_btn_SelectAFile, command=Dialog_fileRadioLinuxFunc)
    Dialog_fileRadioLinux_window = my_canvas2.create_window(875, 75, anchor="nw")


    ProvisionFileNameLabel_window = my_canvas2.create_text(865, 150, text="", font=("Times", 8), fill="blue")


    # ///////////// Menu creation ///////////// 
    # +++++++++++++++++++  Option ++++++++++++++++++
    ListLesBoxes_list = []
    ListLesBoxes_listVar = StringVar(value=ListLesBoxes_list)
    # list the boxes installed
    def ListBoxesInstalled_Func():
        boxesInstalledWindow = Toplevel(root)
        boxesInstalledWindow.geometry("500x500")
        boxesInstalledWindow.resizable(False,False)
        Canvas_boxesInstalled = Canvas(boxesInstalledWindow, width=450, height=450)
        Canvas_boxesInstalled.pack(fill="both", expand=True)
        Canvas_boxesInstalled.create_image(0,0, image=bg, anchor="nw")

        Listbox_ListBoxes = Listbox(Canvas_boxesInstalled, width=80, height=15, bg='#F7F2E6', relief=GROOVE, activestyle='none', borderwidth=4, listvariable=ListLesBoxes_listVar, cursor="hand2", highlightcolor="blue", selectforeground="white", selectbackground="green", highlightbackground="pink")
        Listbox_ListBoxes_Window = Canvas_boxesInstalled.create_window(250, 150, window=Listbox_ListBoxes)

        def Listbox_ListBoxes_Func():
            Listbox_ListBoxes.delete(0, END)
            Listbox_ListBoxesVar = subprocess.check_output("vagrant box list" ).decode('utf-8')
            ListLesBoxes_list = Listbox_ListBoxesVar.split("\n")
            for ListLesBoxes_listItem in range(len(ListLesBoxes_list)):
                Listbox_ListBoxes.insert(END, ListLesBoxes_list[int(f"{ListLesBoxes_listItem}")])
        Listbox_ListBoxes_Func()

        # //////  remove boxes //////
        def Deleteboxes_Func():
            Listboxes_splitToDelete = str(Listbox_ListBoxes.get(ANCHOR)).split(" ")
            global Listbox_ListBoxesVar
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "vagrant box remove {}".format(Listboxes_splitToDelete[0])])
            Listbox_ListBoxes_Func()

        def Deleteboxes_Func_Force():
            Listboxes_splitToDelete = str(Listbox_ListBoxes.get(ANCHOR)).split(" ")
            global Listbox_ListBoxesVar
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "vagrant box remove {} --force".format(Listboxes_splitToDelete[0])])
            Listbox_ListBoxes_Func()

        def Deleteboxes_Func_Copy():
            Listboxes_splitToCopy = str(Listbox_ListBoxes.get(ANCHOR)).split(" ")
            boxesInstalledWindow.clipboard_clear()
            boxesInstalledWindow.clipboard_append(Listboxes_splitToCopy[0])

        Deleteboxes_Btn = Button(boxesInstalledWindow, text="Delete", bg="#1474e4", command=lambda:threading.Thread(target=Deleteboxes_Func).start())
        Deleteboxes_Btn_Window = Canvas_boxesInstalled.create_window(235, 290, window=Deleteboxes_Btn)


        Deleteboxes_Btn_Force = Button(boxesInstalledWindow, text="Force Delete", bg="#1474e4", command=lambda:threading.Thread(target=Deleteboxes_Func_Force).start())
        Deleteboxes_Btn_Window = Canvas_boxesInstalled.create_window(235, 320, window=Deleteboxes_Btn_Force)


        Deleteboxes_Btn_Copy = Button(boxesInstalledWindow, text="Copy", bg="#1474e4", command=lambda:threading.Thread(target=Deleteboxes_Func_Copy).start())
        Deleteboxes_Btn_Window = Canvas_boxesInstalled.create_window(235, 370, window=Deleteboxes_Btn_Copy)

        
    # //////// Installation functions //////// 

    def InstallVagrant_Func():
        InstallvagrantWindow = Toplevel(root)
        InstallvagrantWindow.resizable(False,False)
        InstallvagrantWindow.configure(bg="#8c8680")
        InstallvagrantWindow.geometry("750x100")
        InstallVagrant_Label = Label(InstallvagrantWindow, text="vagrant installation in progress", font=("Heveletica", 16, 'bold'), fg="red", bg="#8c8680")
        InstallVagrant_Label.pack()
        def InstallVagrantCmd():
            if connect():
                InstallVagrant_Label.configure(text="vagrant installation in progress")
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "choco install vagrant --force --yes"])
                InstallVagrant_Label.configure(text="Vagrant installation complete, please restart your computer", fg="green")
            else:
                InstallVagrant_Label.configure(text="Please check your internet connection and try again", fg="#e60021")
        InstallVagrant_Label.configure(text="Vagrant installation complete, please restart your computer", fg="green")
        threading.Thread(target=InstallVagrantCmd).start() 
    
    def InstallVmwareEsxiPlugin_Func():
        InstallVagrantVmwareWindow = Toplevel(root)
        InstallVagrantVmwareWindow.configure(bg="#8c8680")
        InstallVagrantVmwareWindow.geometry("750x100")
        InstallVagrantVmwareWindow.resizable(False,False)
        InstallVagrantVmware_Label = Label(InstallVagrantVmwareWindow, text="Installing vmware plugin in progress", font=("Heveletica", 16, 'bold'), fg="red", bg="#8c8680")
        InstallVagrantVmware_Label.pack()
        def InstallVagrantVmwareCmd():
            if connect():
                InstallVagrantVmware_Label.configure(text="Installing vmware plugin in progress")
                subprocess.check_output("vagrant plugin install vagrant-vmware-esxi" ).decode('utf-8')
                InstallVagrantVmware_Label.configure(text="Installation of vmware plugin completed", fg="green")
            else:
                InstallVagrantVmware_Label.configure(text="Please check your internet connection and try again", fg="#e60021")
        InstallVagrantVmware_Label.configure(text="Installation of vmware plugin completed", fg="green")
        threading.Thread(target=InstallVagrantVmwareCmd).start() 
    
    def InstallVirtualbox_Func():
        InstallvirtualboxWindow = Toplevel(root)
        InstallvirtualboxWindow.configure(bg="#8c8680")
        InstallvirtualboxWindow.geometry("750x100")
        InstallvirtualboxWindow.resizable(False,False)
        Installvirtualbox_Label = Label(InstallvirtualboxWindow, text="Virtualbox installation in progress", font=("Heveletica", 16, 'bold'), fg="red", bg="#8c8680")
        Installvirtualbox_Label.pack()
        def InstallvirtualboxCmd():
            if connect():
                Installvirtualbox_Label.configure(text="Virtualbox installation in progress")
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "choco install virtualbox --force --yes"])
                Installvirtualbox_Label.configure(text="Virtualbox installation complete", fg="green")
            else:
                Installvirtualbox_Label.configure(text="Please check your internet connection and try again", fg="#e60021")
        Installvirtualbox_Label.configure(text="Virtualbox installation complete", fg="green")
        threading.Thread(target=InstallvirtualboxCmd).start() 

    def InstallHyperV_Func():
        InstallhypervWindow = Toplevel(root)
        InstallhypervWindow.configure(bg="#8c8680")
        InstallhypervWindow.geometry("750x100")
        InstallhypervWindow.resizable(False,False)
        Installhyperv_Label = Label(InstallhypervWindow, text="Installing hyperV in progress", font=("Heveletica", 16, 'bold'), fg="red", bg="#8c8680")
        Installhyperv_Label.pack()
        def InstallhypervCmd():
            if connect():
                Installhyperv_Label.configure(text="Installing hyperV in progress")
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", f"{GetWorkingDir}\\InstallHyperV.bat"])
                Installhyperv_Label.configure(text="Installation of HyperV complete, please restart your computer", fg="green")
            else:
                Installhyperv_Label.configure(text="Please check your internet connection and try again", fg="#e60021")
        Installhyperv_Label.configure(text="Installation of HyperV complete, please restart your computer", fg="green")
        threading.Thread(target=InstallhypervCmd).start()

    def InstallOVFTool_Func():
        def callback(url):
            webbrowser.open_new_tab(url)
        callback("https://customerconnect.vmware.com/downloads/get-download?downloadGroup=OVFTOOL441")

    # //////// End Installation functions //////// 

    ListLesnodes_list = []
    ListLesnodes_listVar = StringVar(value=ListLesnodes_list)
    def ListNodes_Func():
        ListNodesvWindow = Toplevel(root)
        ListNodesvWindow.geometry("750x560")
        ListNodesvWindow.resizable(False,False)
        Canvas_ListNodes = Canvas(ListNodesvWindow, width=850, height=560)
        Canvas_ListNodes.pack(fill="both", expand=True)
        Canvas_ListNodes.create_image(0,0, image=bg, anchor="nw")

        Listbox_Listnodes = Listbox(ListNodesvWindow, width=80, height=15, bg='#F7F2E6', relief=GROOVE, activestyle='none', borderwidth=4, listvariable=ListLesnodes_listVar, cursor="hand2", highlightcolor="blue", selectforeground="white", selectbackground="green", highlightbackground="pink") 
        Listbox_Listnodes_Window = Canvas_ListNodes.create_window(350, 140, window=Listbox_Listnodes)
        def Listbox_Listnodes_Func():
            Listbox_Listnodes.delete(0, END)
            subprocess.check_output("vagrant global-status --prune" ).decode('utf-8')
            Listbox_ListnodesVar = subprocess.check_output("vagrant global-status" ).decode('utf-8')
            ListLesnodes_list = Listbox_ListnodesVar.split("\n")
            CountItemsListLesnodes = len(ListLesnodes_list)
            CountItemsListLesnodes_ToDelete = int(CountItemsListLesnodes) - 8
            # print(CountItemsListLesnodes_ToDelete)
            del ListLesnodes_list[int(CountItemsListLesnodes_ToDelete):]
            del ListLesnodes_list[0:2]
            Listbox_Listnodes.delete(0, END)
            for ListLesnodes_listItem in range(len(ListLesnodes_list)):
                Listbox_Listnodes.insert(END, ListLesnodes_list[int(f"{ListLesnodes_listItem}")])
        Listbox_Listnodes_Func()


        def Startnodes_Func():
            GetIdOfNode = Listbox_Listnodes.get(ANCHOR).split(" ")
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", f"vagrant up {GetIdOfNode[0]}"])
            Listbox_Listnodes_Func()

        def Stopnodes_Func():
            GetIdOfNode = Listbox_Listnodes.get(ANCHOR).split(" ")
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", f"vagrant halt {GetIdOfNode[0]}"])
            Listbox_Listnodes_Func()

        def Pausenodes_Func():
            GetIdOfNode = Listbox_Listnodes.get(ANCHOR).split(" ")
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", f"vagrant suspend {GetIdOfNode[0]}"])
            Listbox_Listnodes_Func()

        def Resumenodes_Func():
            GetIdOfNode = Listbox_Listnodes.get(ANCHOR).split(" ")
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", f"vagrant resume {GetIdOfNode[0]}"])
            Listbox_Listnodes_Func()

        def Destroynodes_Func():
            GetIdOfNode = Listbox_Listnodes.get(ANCHOR).split(" ")
            subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", f"vagrant destroy {GetIdOfNode[0]} --force"])
            Listbox_Listnodes_Func()



        Startnodes_Btn = Button(ListNodesvWindow, text="Start", bg="#1474e4", command=lambda:threading.Thread(target=Startnodes_Func).start())
        Canvas_ListNodes.create_window(270, 290, window=Startnodes_Btn)

        
        Stopnodes_Btn = Button(ListNodesvWindow, text="Stop", bg="#1474e4", command=lambda:threading.Thread(target=Stopnodes_Func).start())
        Canvas_ListNodes.create_window(370, 290, window=Stopnodes_Btn)

        
        Pausenodes_Btn = Button(ListNodesvWindow, text="Pause", bg="#1474e4", command=lambda:threading.Thread(target=Pausenodes_Func).start())
        Canvas_ListNodes.create_window(270, 320, window=Pausenodes_Btn)

        Resumenodes_Btn = Button(ListNodesvWindow, text="Resume", bg="#1474e4", command=lambda:threading.Thread(target=Resumenodes_Func).start())
        Canvas_ListNodes.create_window(370, 320, window=Resumenodes_Btn)
        
        Destroynodes_Btn = Button(ListNodesvWindow, text="Destroy", bg="#1474e4", command=lambda:threading.Thread(target=Destroynodes_Func).start())
        Canvas_ListNodes.create_window(270, 350, window=Destroynodes_Btn)


    def ImportExportVms():
        ImportExportVmsvWindow = Toplevel(root)
        ImportExportVmsvWindow.geometry("550x85")
        ImportExportVmsvWindow.resizable(False, False)
        Canvas_ImportExportVms = Canvas(ImportExportVmsvWindow, width=850, height=560)
        Canvas_ImportExportVms.pack(fill="both", expand=True)
        Canvas_ImportExportVms.create_image(0,0, image=bg, anchor="nw")

        def Virtualbox_Btn_Func():
            # Clear buttons and fit window
            Canvas_ImportExportVms.itemconfig(Virtualbox_Btn_Window, window='')
            Canvas_ImportExportVms.itemconfig(HyperV_Btn_Window, window='')
            Canvas_ImportExportVms.itemconfig(ESXI_Btn_Window, window='')
            ImportExportVmsvWindow.geometry("750x560")
            # ***** Virtualbox Configuration ***** 
            VarListboxVirtualbox = StringVar(value=Box_ListVirtualbox) 
            ListboxVirtualbox = Listbox(ImportExportVmsvWindow, width=50, height=25, bg='#F7F2E6', relief=GROOVE, activestyle='none', borderwidth=4, listvariable=VarListboxVirtualbox, cursor="hand2", highlightcolor="blue", selectforeground="white", selectbackground="green", highlightbackground="pink")
            ListboxVirtualbox_Window = Canvas_ImportExportVms.create_window(25, 65, anchor="nw", window=ListboxVirtualbox)
            ListVirtualboxVms = subprocess.check_output("VBoxManage.exe list vms").decode('utf-8')
            ListVirtualboxVms_list = ListVirtualboxVms.split("\n")
            for ListVirtualboxVms_listItem in range(len(ListVirtualboxVms_list)):
                ListVirtualboxVms_listModified = ListVirtualboxVms_list[int(f"{ListVirtualboxVms_listItem}")].split(" ")
                ListVirtualboxVms_VMName = ListVirtualboxVms_listModified[0].strip('""')
                ListboxVirtualbox.insert(END, ListVirtualboxVms_VMName)
            
            # Function to export Virtualbox
            def ExportVmVirtualbox_Btn_Func():
                SavePathVmVirtualbox = filedialog.asksaveasfilename(filetypes=[("box file", ".box")], defaultextension=".box", initialdir=os.path.normpath("C://"), title="Emplacement de sauvegarde")
                if SavePathVmVirtualbox != "":
                    VMVirtualboxSelected = str(ListboxVirtualbox.get(ANCHOR)).split(" ")
                    VMVirtualboxSelectedStriped = VMVirtualboxSelected[0].strip('""')
                    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "vagrant package --base {} --output '{}' ".format(VMVirtualboxSelectedStriped, SavePathVmVirtualbox)])
            
            # Function to import Virtualbox
            def ImportVmVirtualbox_Btn_Func():
                OpenPathVmVirtualbox = filedialog.askopenfilename(filetypes=[("box file", ".box")], defaultextension=".box", initialdir=os.path.normpath("C://"), title="Emplacement de sauvegarde")
                print(OpenPathVmVirtualbox)
                # Retrieve file path only
                PathOfBoxFile = os.path.dirname(OpenPathVmVirtualbox)
                print(PathOfBoxFile)
                # Get file name only
                NameOfBoxFile = os.path.basename(OpenPathVmVirtualbox)
                print(NameOfBoxFile)
                if OpenPathVmVirtualbox != "":
                    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "cd '{}' ; vagrant init -f '{}' ".format(PathOfBoxFile, OpenPathVmVirtualbox)])
                    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "cd '{}' ; vagrant up --provider virtualbox".format(PathOfBoxFile)])

            # Title Export / Import Virtualbox (.box)
            TitleImportExportVms_Window = Canvas_ImportExportVms.create_text(250, 25, text="Import or export a box file", font=("Heveletica", 16, "bold"), fill="white") 

            # Virtualbox export button
            ExportVmVirtualbox_Btn = Button(ImportExportVmsvWindow, text="Export", bg="#1474e4", command=lambda:threading.Thread(target=ExportVmVirtualbox_Btn_Func).start())
            ExportVmVirtualbox_Btn_Window = Canvas_ImportExportVms.create_window(390, 85, window=ExportVmVirtualbox_Btn)
            
            # virtualbox import button
            ImportVmVirtualbox_Btn = Button(ImportExportVmsvWindow, text="Import", bg="#1474e4", command=lambda:threading.Thread(target=ImportVmVirtualbox_Btn_Func).start())
            ImportVmVirtualbox_Btn_Window = Canvas_ImportExportVms.create_window(390, 120, window=ImportVmVirtualbox_Btn)
            
            infoImportExportVmsVirtualbox_Window = Canvas_ImportExportVms.create_text(250, 500, text="* This option allows you to group an environment", font=("Heveletica", 10, "bold"), fill="white") 
            infoImportExportVmsVirtualbox2_Window = Canvas_ImportExportVms.create_text(254, 520, text="VirtualBox running in a reusable box.", font=("Heveletica", 10, "bold"), fill="white") 

        #**************++++++++++++++////////////////////

        def HyperV_Btn_Func():
            # Clear buttons and fit window
            Canvas_ImportExportVms.itemconfig(Virtualbox_Btn_Window, window='')
            Canvas_ImportExportVms.itemconfig(HyperV_Btn_Window, window='')
            Canvas_ImportExportVms.itemconfig(ESXI_Btn_Window, window='')
            ImportExportVmsvWindow.geometry("750x560")
            # ***** HyperV Configuration ***** 
            VarListboxHyperV= StringVar(value=Box_ListHyperV) 
            ListboxHyperV = Listbox(ImportExportVmsvWindow, width=50, height=25, bg='#F7F2E6', relief=GROOVE, activestyle='none', borderwidth=4, listvariable=VarListboxHyperV, cursor="hand2", highlightcolor="blue", selectforeground="white", selectbackground="green", highlightbackground="pink")
            ListboxHyperV_Window = Canvas_ImportExportVms.create_window(25, 65, anchor="nw", window=ListboxHyperV)
            ListHyperVVms = subprocess.check_output("powershell Get-Vm | Select Name").decode('utf-8')
            ListHyperVVms_list = str(ListHyperVVms).split("\n")
            del ListHyperVVms_list[0:3]
            # print(int(len(ListHyperVVms_list)) - 3)
            for ListHyperVVms_listItem in range(int(len(ListHyperVVms_list)) - 3):
                ListHyperVVms_listModified = ListHyperVVms_list[int(f"{ListHyperVVms_listItem}")]
                ListboxHyperV.insert(END, ListHyperVVms_listModified)
            
            def ExportVmHyperV_Btn_Func():
                SavePathVmHyperV = filedialog.askdirectory(initialdir=os.path.normpath("C://"), title="Save location")
                if SavePathVmHyperV != "":
                    SelectedVmHyperV = ListboxHyperV.get(ANCHOR).strip("\n\r")
                    # start progress
                    ProgressHyperVExport = Progressbar(ImportExportVmsvWindow, orient=HORIZONTAL, length=100)
                    ProgressHyperVExport_window = Canvas_ImportExportVms.create_window(500, 450, window=ProgressHyperVExport)
                    ProgressHyperVExport.config(mode="indeterminate")
                    ProgressHyperVExport.start()
                    # Exporting
                    HyperVExportLabel = Canvas_ImportExportVms.create_text(435, 410, anchor="nw", text="", font=("Heveletica", 12, "bold"), fill="red")
                    Canvas_ImportExportVms.itemconfig(HyperVExportLabel, text="Exporting", font=("Heveletica", 12, "bold"), fill="red")
                    # Start Export
                paramsHyperV = ["powershell.exe Export-VM", "-Name", "'{}'".format(SelectedVmHyperV), "-Path", "'{}'".format(SavePathVmHyperV)]
                subprocess.check_output(" ".join(paramsHyperV), shell=True)
                # Creating the metadata.json file
                f = open('{}\\{}\\metadata.json'.format(SavePathVmHyperV, SelectedVmHyperV), 'w')
                f.write('{\n')
                f.write('  "provider": "hyperv"\n')
                f.write('}')
                f.close()
                SnapshotsPath = SavePathVmHyperV + "\\{}".format(SelectedVmHyperV) + "\\Snapshots"
                # Delete Snapshots folder
                shutil.rmtree(SnapshotsPath)
                # Compress files
                CompressionPathSrcDst = SavePathVmHyperV + "\\{}".format(SelectedVmHyperV)
                paramsCompressionHyperV = ["{}\\7-Zip\\7z.exe".format(GetWorkingDir), "-mx=9", "a", "'{}\\{}.zip'".format(SavePathVmHyperV, SelectedVmHyperV), "'{}\\*'".format(CompressionPathSrcDst)]
                subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", " ".join(paramsCompressionHyperV)])
                # rename .zip file to .box
                OldNameHyperVBox = "'{}\\{}.zip'".format(SavePathVmHyperV, SelectedVmHyperV)
                OldNameHyperVBox = OldNameHyperVBox.replace("/", "\\")                                                          
                NewNameHyperVBox = "'{}\\{}.box'".format(SavePathVmHyperV, SelectedVmHyperV)
                NewNameHyperVBox = NewNameHyperVBox.replace("/", "\\")                                                          
                os.rename(r"{}".format(OldNameHyperVBox), r"{}".format(NewNameHyperVBox))
                ProgressHyperVExport.stop()
                Canvas_ImportExportVms.itemconfig(ProgressHyperVExport_window, window="")
                Canvas_ImportExportVms.itemconfig(HyperVExportLabel, text="Export completed", font=("Heveletica", 12, "bold"), fill="green")
                time.sleep(8)
                Canvas_ImportExportVms.itemconfig(HyperVExportLabel, text="")                                                   
                

                
            def ImportVmHyperV_Btn_Func():
                OpenPathVmHyperV= filedialog.askopenfilename(filetypes=[("box file", ".box"),("zip file", ".zip"),("tar file", ".tar"),("tar.gz file", ".tar.gz")], defaultextension=".box", initialdir=os.path.normpath("C://"), title="Save location")
                if OpenPathVmHyperV != "":
                    # Retrieve the path of the file only
                    PathOfBoxFileHyperV = os.path.dirname(OpenPathVmHyperV)
                    # Retrieve filename only
                    NameOfBoxFileHyperVImport = os.path.basename(OpenPathVmHyperV)
                    # Start progress
                    ProgressHyperVImport = Progressbar(ImportExportVmsvWindow, orient=HORIZONTAL, length=100)
                    ProgressHyperVImport_window = Canvas_ImportExportVms.create_window(500, 450, window=ProgressHyperVImport)
                    ProgressHyperVImport.config(mode="indeterminate")
                    ProgressHyperVImport.start()
                    # Importation en cours
                    HyperVImportLabel = Canvas_ImportExportVms.create_text(435, 410, anchor="nw", text="", font=("Heveletica", 12, "bold"), fill="red")
                    Canvas_ImportExportVms.itemconfig(HyperVImportLabel, text="Importing in progress", font=("Heveletica", 12, "bold"), fill="red")
                    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "cd '{}' ; vagrant init -m -f '{}' ".format(PathOfBoxFileHyperV, NameOfBoxFileHyperVImport)])
                    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "cd '{}' ; vagrant up --provider hyperv".format(PathOfBoxFileHyperV)])
                    Canvas_ImportExportVms.itemconfig(ProgressHyperVImport_window, window="")
                    ProgressHyperVImport.stop()
                    time.sleep(8)
                    Canvas_ImportExportVms.itemconfig(HyperVImportLabel, text="")       


            # Title HyperV Export/Import (.box)
            TitleImportExportVmsHyperV_Window = Canvas_ImportExportVms.create_text(250, 25, text="Import or export a box file", font=("Heveletica", 16, "bold"), fill="white") 

            # HyperV Export button
            ExportVmHyperV_Btn = Button(ImportExportVmsvWindow, text="Export", bg="#1474e4", command=lambda:threading.Thread(target=ExportVmHyperV_Btn_Func).start())
            ExportVmHyperV_Btn_Window = Canvas_ImportExportVms.create_window(390, 85, window=ExportVmHyperV_Btn)
            
            # HyperV import button
            ImportVmHyperV_Btn = Button(ImportExportVmsvWindow, text="Import", bg="#1474e4", command=lambda:threading.Thread(target=ImportVmHyperV_Btn_Func).start())
            ImportVmHyperV_Btn_Window = Canvas_ImportExportVms.create_window(390, 120, window=ImportVmHyperV_Btn)
            
            infoImportExportVmsHyperV_Window = Canvas_ImportExportVms.create_text(250, 500, text="* This option allows you to group an environment", font=("Heveletica", 10, "bold"), fill="white") 
            infoImportExportVmsHyperV2_Window = Canvas_ImportExportVms.create_text(254, 520, text="HyperV running in a reusable box.", font=("Heveletica", 10, "bold"), fill="white") 


        


        def ESXI_Btn_Func():
            # Clear buttons and fit window
            Canvas_ImportExportVms.itemconfig(Virtualbox_Btn_Window, window='')
            Canvas_ImportExportVms.itemconfig(HyperV_Btn_Window, window='')
            Canvas_ImportExportVms.itemconfig(ESXI_Btn_Window, window='')
            ImportExportVmsvWindow.geometry("730x560")
            # ********* ESXI Configuration  ********

            def ExportVmEsxi_Btn_Func():
                NONE

            def ImportVmEsxi_Btn_Func():
                NONE

            # ESXI Export button
            ExportVmEsxi_Btn = Button(ImportExportVmsvWindow, text="Export", bg="#1474e4", command=lambda:threading.Thread(target=ExportVmEsxi_Btn_Func).start())
            ExportVmEsxi_Btn_Window = Canvas_ImportExportVms.create_window(390, 85, window=ExportVmEsxi_Btn)
            
            # ESXI import button
            ImportVmEsxi_Btn = Button(ImportExportVmsvWindow, text="Import", bg="#1474e4", command=lambda:threading.Thread(target=ImportVmEsxi_Btn_Func).start())
            ImportVmEsxi_Window = Canvas_ImportExportVms.create_window(390, 120, window=ImportVmEsxi_Btn)


        # ---------- Buttons -------------
        Virtualbox_Btn = Button(ImportExportVmsvWindow, text="Virtualbox", bg="#1474e4", width="10", command=lambda:threading.Thread(target=Virtualbox_Btn_Func).start())
        Virtualbox_Btn_Window = Canvas_ImportExportVms.create_window(150, 40, window=Virtualbox_Btn)

        HyperV_Btn = Button(ImportExportVmsvWindow, text="HyperV", bg="#1474e4", width="10", command=lambda:threading.Thread(target=HyperV_Btn_Func).start())
        HyperV_Btn_Window = Canvas_ImportExportVms.create_window(250, 40, window=HyperV_Btn)

        ESXI_Btn = Button(ImportExportVmsvWindow, text="ESXI", bg="#1474e4", width="10", command=lambda:threading.Thread(target=ESXI_Btn_Func).start())
        ESXI_Btn_Window = Canvas_ImportExportVms.create_window(350, 40, window=ESXI_Btn)

    menuBar = Menu(root)
    root.config(menu=menuBar)
    Optionmenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Option", menu=Optionmenu)
    Optionmenu.add_command(label="Boxes installed", command=ListBoxesInstalled_Func)
    Optionmenu.add_command(label="List nodes", underline=0, command=lambda:threading.Thread(target=ListNodes_Func).start())
    Optionmenu.add_command(label="Import / Export VMs", underline=0, command=lambda:threading.Thread(target=ImportExportVms).start())
    SubmenuBarInstall = Menu(menuBar, tearoff=0)
    Optionmenu.add_cascade(label="Install", underline=0, menu=SubmenuBarInstall)
    SubmenuBarInstall.add_command(label="Vagrant", command=InstallVagrant_Func)
    SubmenuBarInstall.add_command(label="Vmware-Esxi plugin", command=InstallVmwareEsxiPlugin_Func)
    SubmenuBarInstall.add_command(label="Virtualbox", command=InstallVirtualbox_Func)
    SubmenuBarInstall.add_command(label="HyperV", command=InstallHyperV_Func)
    SubmenuBarInstall.add_command(label="OVF Tool", command=InstallOVFTool_Func)



    Optionmenu.add_separator()
    Optionmenu.add_command(label="Exit", command=root.destroy)
    


    # ++++++++++++++++++++ Aide ++++++++++++++++++++++++
    # fenêtre POPUP
    def aboutmenu():
        aboutwindow = Toplevel(root)
        aboutwindow.geometry("600x190")
        aboutwindow.resizable(False,False)
        aboutwindow.title("Vagrantify")
        Canvas_aboutwindow = Canvas(aboutwindow, width=450, height=450)
        Canvas_aboutwindow.pack(fill="both", expand=True)
        Canvas_aboutwindow.create_image(0,0, image=bg, anchor="nw")
   

        Canvas_aboutwindow_info = Canvas(Canvas_aboutwindow, width=450, height=50, bd=0, highlightthickness=0)
        Canvas_aboutwindow_info.pack(fill="both", expand=True)
        Canvas_aboutwindow_info.create_image(0,0, image=bg, anchor="nw")

        aboutwindow_title_Window = Canvas_aboutwindow_info.create_text(85, 25, text="Vagrantify", font=("Heveletica", 18, "bold"), fill="#Ec68d8")

        aboutwindow_titleseperator_Window = Canvas_aboutwindow_info.create_text(85, 35, text="________", font=("Heveletica", 18, "bold"), fill="white")

        aboutwindow_versionlabel_Window = Canvas_aboutwindow_info.create_text(100, 85, text="Version : 1.2.0", font=("Heveletica", 10, "bold"), fill="white")



        # Website redirect
        def callback(url):
            webbrowser.open_new_tab(url)
        Canvas_aboutwindow_WebSite = Canvas(Canvas_aboutwindow, width=62, height=20, bd=0, highlightthickness=0)
        Canvas_aboutwindow_WebSite.place(x=48, y=100)
        Canvas_aboutwindow_WebSite.create_image(0,0, image=bg, anchor="nw")

        aboutwindow_sitelabel_Window = Canvas_aboutwindow_WebSite.create_text(32, 10, text="website", font=("Heveletica", 10, "bold"), fill="#00bcd6")
        Canvas_aboutwindow_WebSite.config(cursor="hand2")
        Canvas_aboutwindow_WebSite.bind("<Button-1>", lambda e: callback("http://www.vagrantify.com"))

        Copyright_Label = Canvas_aboutwindow_info.create_text(135, 135, text="Copyright (C) 2022  Chakib", font=("Heveletica", 10, "bold"), fill="white")

    # Help
    Aidemenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Help", menu=Aidemenu)
    Aidemenu.add_command(label="About", command=aboutmenu)



    










    root.mainloop()



if __name__ == '__main__':
    bootstrap()












