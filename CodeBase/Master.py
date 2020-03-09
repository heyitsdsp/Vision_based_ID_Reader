import numpy as np
import cv2
import pyocr
import pyocr.builders
from PIL import Image
import re

#Regex for Registration Number
def extract_reg_number(string):
    pat3=re.compile(r'[0-2][0-9][B|M][A-Z][A-Z][0-2][0-9][0-9][0-9]')
    re3=pat3.findall(string)
    re3=''.join(re3)
    return re3
    
#Regex for Name
def extract_names(string):
    pattern=re.compile(r'[A-Z][a-z]+')
    names=pattern.findall(string)
    newname=' '.join(names)
    return newname

#Activate Tesseract
tools = pyocr.get_available_tools()
tool = tools[0]

cap = cv2.VideoCapture(0)
f = open("data.txt","w")
while(True):
     # Capture frame-by-frame
    ret, frame = cap.read()
            
    # Our operations on the frame come here
    txt = tool.image_to_string(Image.fromarray(frame),builder = pyocr.builders.TextBuilder())
        
    RegID = extract_reg_number(txt)
    Name = extract_names(txt)

    #Writing the on file; Empty files should not be written
    if Name != "":
        if RegID !="":
            f.write(Name)
            f.write(",")
            f.write(RegID)
            f.write("\n")

    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        f.flush()
        f.close()
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

with open('data.txt', 'r') as file:
    data = file.read()

regs=[]

#Split the string into Names and Registration numbers
string=re.split('\n|,',data)

#Separate Registration numbers and other redundant data(if any) from list
for i in string:
    if(i.isalpha()==False):
        string.remove(i)
        regs.append(i)

#Get the frequency of elements and the elements as lists (in ascending order)
freq=np.unique(string,return_counts=True)[1].tolist()
val=np.unique(string,return_counts=True)[0].tolist()

regfreq=np.unique(regs,return_counts=True)[1].tolist()
regval=np.unique(regs,return_counts=True)[0].tolist()

#Get the index where the maximum value is located
maxindex=freq.index(max(freq))
maxregindex=regfreq.index(max(regfreq))

#Get the most frequently occuring element
maxstr=val[maxindex]
maxreg=regval[maxregindex]

#printing the filtered values
print(maxstr)
print(maxreg)