import csv
import os
from PIL import Image, ImageDraw, ImageFont
empty='C:/Users/Yun/Desktop/GoFly/pathway/Z.tif'
fileout='C:/Users/Yun/Desktop/GoFly/Output/'
#im = Image.open(pathline)
font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf",20)
font2= ImageFont.truetype("C:/Windows/Fonts/Arial.ttf",12)
#--------------------------------------------------------------------------------------
def DataInput():
    with open('C:/Users/Yun/Desktop/GoFly/ryan_seq.txt', newline='') as inputfile: #user input from openfile 
        reader = csv.reader(inputfile, delimiter="\t")
        l = list(reader)    #list of lists
        result = [[s.strip() for s in inner] for inner in l]    #strip away blankspace
        for eachlist in result: # For each data pair
                eachlist[0]=str(eachlist[0])   #Convert CG number to string
                eachlist[1]=float(eachlist[1]) #Convert fold change to a floating number
                eachlist[2]=float(eachlist[2]) #Convert P-value to float
                eachlist[3]=str(eachlist[3])   #Convert annontation to string
        sorted_list = sorted(result, key=lambda x: x[1]) #Sort the list by fold change
        return sorted_list  #return the fold change sorted list

#---------------------------------------------------------------------------------------
def GeneFilesToList ():
    path='C:/Users/Yun/Desktop/GoFly/genelists'
    dirListing = os.listdir(path)
    editFiles = []
    for item in dirListing:
        if ".txt" in item:
            editFiles.append(path+'/'+item)
    return editFiles
#---------------------------------------------------------------------------------------
def TiffFilesToList ():
    path='C:/Users/Yun/Desktop/GoFly/pathway'
    dirListing = os.listdir(path)
    editFiles = []
    for item in dirListing:
        if ".tif" in item:
            editFiles.append(path+'/'+item)
    return editFiles
#----------------------------------------------------------------------------------------

def Heatmapper (compared_list,pathline,pathway_list,same):
    x=150
    y=55
    z=x+20
    t=y+20
    up=0
    down=0
    no=0
    pathcount=0
    #for pathway in tiffname_list:
    im=Image.open(empty)
    draw= ImageDraw.Draw(im)
    for item in compared_list:
        array_color=int(50*abs(item[1]))
        if item[1] > 1.2 and item[2] <0.05: 
            draw = ImageDraw.Draw(im)
            draw.rectangle([x,y,z,t], fill= (array_color,0,0),outline="black")
            draw.text((185,y),item[3],(0,0,0),font=font)
            up=up+1
            if item[2] < 0.001:
                draw.text((x+3,y),"***",(250,250,210),font=font2)
            if item[2] <0.01:
                draw.text((x+3,y),"**",(250,250,210),font=font2)
            if item[2] <0.05:
                draw.text((x+3,y),"*",(250,250,210),font=font2)
        elif item[1] < -1.2 and item[2] <0.05:
            draw = ImageDraw.Draw(im)
            draw.rectangle([x,y,z,t], fill= (0,array_color,0),outline="black")
            draw.text((185,y),item[3],(0,0,0),font=font)
            down=down+1
            if item[2] < 0.001:
                draw.text((x+3,y),"***",(250,250,210),font=font2)
            if item[2] <0.01:
                draw.text((x+3,y),"**",(250,250,210),font=font2)
            if item[2] <0.05:
                draw.text((x+3,y),"*",(250,250,210),font=font2)    
        else:
            #draw = ImageDraw.Draw(im)
            #draw.rectangle([x,y,z,t], fill= (119,136,153),outline="black")
            #draw.text((185,y),item[3],(0,0,0),font=font)
            no=no+1
            y=y-20
            t=t-20
        y=y+20
        t=t+20
    for eachlist in pathway_list:
        pathcount=pathcount+1
    tot=up+down+no
    tots=str(tot)
    comp= pathcount
    roundup= round((up/comp),2)
    rounddown= round ((down/comp),2)
    roundno= round((no/comp),2)
    comps=str(comp)
    ups=str(up)
    downs=str(down)
    nos=str(no)
    roundups=str(roundup)
    rounddowns=str(rounddown)
    roundnos=str(roundno)
    stringall= str("Total  "+tots+"/"+comps)
    stringup= str("UP:"+ups+"/"+comps+" ("+roundups+")")
    stringdown=str("DOWN:"+ downs+"/"+comps+" ("+rounddowns+")")
    stringno= str("NC:"+nos+"/"+comps+" ("+roundnos+")")
    stringme= (stringall+"    "+stringno+"    "+stringup+"    "+stringdown+"    ")
    draw.text((50,2800),same,(0,0,0),font=font)
    draw.text((150,2850),stringme,(0,0,0),font=font)

    (drive, path) = os.path.splitdrive(pathline)# splits the input tiff file name 
    (path, file)  = os.path.split(pathline)     # splits the input tiff file name
    sep="."                                     # declares "." as seperator
    perth=file.split(sep,1)[0]                  # splits the filename away from ".tiff"
    filepath=fileout+perth+".jpeg"              # converts filepath and name to .jpeg"
    print (filepath)                            # Print tests the file path
    im.save(filepath,"jpeg")                    # Saves new drawing into GoFly/Output/Name.jpeg
    del draw
 
#-----------------------------------------------------------------
def CanOpener(txtfilename):
    pathway_list=[]
    with open(txtfilename, newline='') as inputfile:      #Open the text file
        reader = csv.reader(inputfile, delimiter="\t")    #Reader it using tab delineation  
        temp_list = list(reader)    #list of lists        #Read line into a list  
        for cg in temp_list:                              #For each list in the list
            pathway_list=pathway_list+cg                  #Add that list into a single list
        return pathway_list                                 #Print test that its one list     
#-----------------------------------------------------------------
def CompareLists (sorted_list,pathway_list):
        compared_list=[]
        for item in sorted_list:
            if item[0] in pathway_list:
                compared_list.append(item)
        return compared_list
#-----------------------------------------------------------------            
            

#-----MAIN PROGRAM -----------------------------------------------
sorted_list=DataInput()                      # Inputs and sorts our input data text file (CG#,FOLD)
#print (sorted_list)                         # Print tests the sorted list
filename_list=GeneFilesToList()              # Inputs text files from pathway and saves them into a list
#print (filename_list)                       # Print test the gene lists
tiffname_list=TiffFilesToList()              # Inputs tiff file names into a list
#print (tiffname_list)                       # Print tests the tiff file list
upc=0
downc=0
noc=0
#---------------Make this a function that inputs sorted_list and returns same-----------#
for item in sorted_list:
    do=float(item[1])
    if do >1.5:
        upc=upc+1
    elif do <-1.5:
        downc=downc+1
    else:
        noc=noc+1
c=(upc+downc+noc)
up_r=(round((upc/c),2))
down_r=(round((downc/c),2))
no_r=(round((noc/c),2))
sc=str(c)
sup_r=str(up_r)
sdown_r=str(down_r)
supc=str(upc)
sdownc=str(downc)
snoc=str(noc)
sno_r=str(no_r)
saall= str("Total  "+sc+"/"+sc)
saup= str("UP:"+supc+"/"+sc+" ("+sup_r+")")
sadown=str("DOWN:"+ sdownc+"/"+sc+" ("+sdown_r+")")
sano= str("NC:"+snoc+"/"+sc+" ("+sno_r+")")
same= (saall+"    "+sano+"    "+saup+"    "+sadown+"    ")
#--------------------------------------------------------------------------------------

for name,txtfilename in zip(tiffname_list,filename_list):
    str_name=str(name)
    #print (str_name)
    #print (txtfilename)                        #For all textfiles in the text file name list...
    pathway_list= CanOpener(txtfilename)     #Return the CG#s from that pathways list using CanOpener
    #print (pathway_list)                    #Print test the pathway CG list    
    compared_list=CompareLists(sorted_list,pathway_list)
    #print (compared_list)
    Heatmapper(compared_list,str_name,pathway_list,same)

