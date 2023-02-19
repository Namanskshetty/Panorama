import cv2
import os #to open folders from the image
import random
num = random.random()
mainFolder="images"
d = os.path.dirname(__file__)
print(d)
folder_save=d+"\output"
myfolders=os.listdir(mainFolder)
for folder in myfolders:
    path=mainFolder+"/"+folder
    Images=[]
    mylist=os.listdir(path)
    print(mylist)
    for imgn in mylist:
        curimg=cv2.imread(path+'/'+imgn)
        curimg=cv2.resize(curimg,(0,0),None,0.5,0.5)#this here helps you changes window and the image size change this accordingly
        Images.append(curimg)

    stitcher=cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    stitcher.setPanoConfidenceThresh(0.0)#this threshold too aggreasive change it accordingly
    status,result=stitcher.stitch(Images)
    assert status == 0 #let the be considered in order to main the staus by the opencv
    if(status==cv2.STITCHER_OK):
        print("done")
        cv2.imshow(folder,result)
        filename_out=folder_save+'/'+str(num)+"_namanskshetty.png"
        cv2.imwrite(filename_out,result)
        print("The panoroma is svaed in OUTPUT folder..")
        cv2.waitKey(1)
    else:
        print("not done")
cv2.waitKey(0)