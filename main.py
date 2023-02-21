from ast import main
from tkinter.tix import WINDOW
import cv2
import os #to open folders from the image
import random
from tkinter import *
from tkinter import filedialog
import subprocess
import webbrowser
import sys
import time
from PIL import Image, ImageTk
import shutil

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe') #this is set for windows explorer change this accordingly
# see line number 87 for differnet approach


mainFolder=""
done=10101
num = random.random()
d = os.path.dirname(__file__)
print(d)

icon=d+"\\imp\\logo.ico"
# starting ui with tk inter
window = Tk()
window.geometry('920x720')
window.title("TTG Panorama")
window.iconbitmap(icon)
window.config(bg = "black")
lbbl = Label(window, text="Panorama", font=("Arial Bold", 50),bg="black", fg="#DDDDDD")
lbbl.place(relx=0.5, rely=0.09, anchor="center")


def close():
    sys.exit()

def pro():
    webbrowser.open('https://github.com/Namanskshetty/Panorama#program-usage-instructions') #this rediects to github page

#defention for slecting the directory
def imgfileselect():
    global mainFolder
    open_file = filedialog.askdirectory()
    mainFolder=open_file

icon2 = PhotoImage(file=d+'/imp/folder.png')
icon22=icon2.subsample(9, 12)
bt22=Button(window,text="   Select DIR!!  ",image=icon22,font=("Arial Bold", 15),compound = LEFT,command=imgfileselect)
bt22.place(relx=0.5, rely=0.44, anchor="center")
#for closing
icon_close = PhotoImage(file=d+'/imp/close.png')
icon_close2=icon_close.subsample(9, 12)
bt_close=Button(window,image=icon_close2,relief=FLAT,command=close,bg='black')
bt_close.place(relx=0.9,rely=0.01)


########## for help ########
icon_help = PhotoImage(file=d+'/imp/help.png')
icon_help2=icon_help.subsample(9, 12)
bt_help=Button(window,image=icon_help2,relief=FLAT,command=pro,bg='black')
bt_help.place(relx=0.01,rely=0.01)

labell=Label(window, text="",bg="black")
########## Sucess message ##############
def success(done): 
    global mainFolder
    if done==1:
        labell.configure(text = "Process completed check the output folder!!!",fg="green",bg="#FCFFE7", borderwidth=2, relief="raised")
        destination=d+"\copy"
        shutil.move(mainFolder, destination)# this places the main folder into copy so that to remove duplicate images to be stiched
        return
    elif done==0:
        labell.configure(text = "Process cannot be completed",fg="red",bg="#FCFFE7", borderwidth=2, relief="raised")
        return

    ###### return ##

########## Open output folder #######
def output_open():
    outop=d+"\output\\"
    #subprocess.Popen(r'explorer /select,'+outop)
    subprocess.run([FILEBROWSER_PATH, outop])
    return

# To open copy folder
def copy_open():
    outyp=d+"\copy\\"
    print(d)
    subprocess.run([FILEBROWSER_PATH, d+"\copy"])
    return

##### files for open cv ########
def open_cv():
    folder_save=d+"\output"
    global mainFolder
    global done
    if mainFolder=="":
        labell.configure(text = "Error 404: Plese select the directory before starting the process",fg="red",bg="#FCFFE7", borderwidth=2, relief="raised")
        return
    else:
        print(mainFolder)
        myfolders=os.listdir(mainFolder)
        labell.configure()
        if len(myfolders)==0:
            labell.configure(text = "Error 404_2: Could not find the subfolders where images are located",fg="red",bg="#FCFFE7", borderwidth=2, relief="raised")
            return
        else:
            for folder in myfolders:
                path=mainFolder+"/"+folder
                Images=[]
                mylist=os.listdir(path)
                print(mylist)
                for imgn in mylist:
                    curimg=cv2.imread(path+'/'+imgn)
                    curimg=cv2.resize(curimg,(0,0),None,0.5,0.5)#this here helps you changes window and the image size change this accordingly
                    Images.append(curimg)

                stitcher=cv2.Stitcher.create()
                #stitcher.setPanoConfidenceThresh(0.0)#this threshold too aggreasive change it accordingly
                status,result=stitcher.stitch(Images)
                #assert status == 0 #let the be considered in order to main the staus by the opencv

                if(status==cv2.STITCHER_OK):
                    print("done")
                    done=1
                    #lb_done = Label(window, text="Panorama Completed. Check the output folder", font=("Arial Bold", 15),bg="black", fg="green")
                    #lb_done.place(relx=0.5, rely=0.81, anchor="center")
                    cv2.imshow(folder,result)
                    filename_out=folder_save+'/'+str(num)+"_namanskshetty.png" #change the name accordingly
                    cv2.imwrite(filename_out,result)
                    print("The panoroma is saved in OUTPUT folder!!!!")
                    cv2.waitKey(1)
                else:
                    print("Could not perform")
                    done=0
                    time.sleep(2)
                    lb_done = Label(window, text="Could not perform", font=("Arial Bold", 15),bg="black", fg="red")
                    lb_done.place(relx=0.5, rely=0.81, anchor="center")
            success(done)
            cv2.waitKey(0)#this makes the window of the cv2 open to review

labell.configure()
labell.pack(side=LEFT, ipadx=5, ipady=5)
    ########## end of open cv ##############

#defining the line to open the open cv definition
icon_start = PhotoImage(file=d+'/imp/flash.png')
icon_start2=icon_start.subsample(9, 12)
bt21=Button(window,text="Start  ",image=icon_start2,compound = LEFT,command=open_cv,fg="green",font=("Comic Sans MS", 20,"bold"))
bt21.place(relx=0.5, rely=0.56, anchor="center")

# writing line for opening the output folder
icon_out = PhotoImage(file=d+'/imp/output.png')
icon_out2=icon_out.subsample(9, 12)
bt211=Button(window,image=icon_out2,compound = LEFT,text="  Output Folder ",font=("Arial Bold", 10),command=output_open)
bt211.place(relx=0.5, rely=0.68, anchor="center")

# Writing line for opening copy folder.
icon_copy=PhotoImage(file=d+'/imp/trash.png')
icon_copy2=icon_copy.subsample(9, 12)
btcopy=Button(window,image=icon_copy2,compound = LEFT,text="  Copy Folder ",font=("Arial Bold", 10),command=copy_open)
btcopy.place(relx=0.5, rely=0.76, anchor="center")
window.mainloop()#This makes the window open
