#by protongamer 2018

#Update 22/02/2019
#Add support to convert array 24 bits to 16 bits(RGB565)

import binascii
import os

print("24BMP2C - by protongamer")
print("Drag your .bmp file(only 24 bit supported) to the same folder of BMP2C")
print("Enter file name(ex: myPicture.bmp)")
#img = os.path.dirname(os.path.abspath()) # /a/b/c/d/e
#img = img + "\\"

img = raw_input()


p = 0 #counter to read img buffer
w = 1 #counter to fill new var buffer
slash = 0 #slash character detection
name_array = "" #name of the final array
while(img[p] != '.'):
    p = p + 1
    if(img[p] == "\\"):
        slash = p
        #print p

new = img[0]
while(w < p):
    new = new + img[w]
    w = w + 1
    
new = new + ".c"

w = slash
while(w < p):
    name_array = name_array + img[w] #fill the name array
    w = w + 1
#print(name_array)

#print(new)

file=open(new,"w+") #create fill with the same name of selected file
with open(img, 'rb') as f:
    content = f.read() #read bytes of bmp file

#calculate coordinates(w,h) number of bytes and offset
a = list(content)
width = ord(a[21])
width = width << 8
width = width | ord(a[20])
width = width << 8
width = width | ord(a[19])
width = width << 8
width = width | ord(a[18])
print "Image width :",width
height = ord(a[25])
height = height << 8
height = height | ord(a[24])
height = height << 8
height = height | ord(a[23])
height = height << 8
height = height | ord(a[22])
print "Image height :",height
offset_byte = ord(a[13])
offset_byte = offset_byte << 8
offset_byte = offset_byte | ord(a[12])
offset_byte = offset_byte << 8
offset_byte = offset_byte | ord(a[11])
offset_byte = offset_byte << 8
offset_byte = offset_byte | ord(a[10])
print "Adress of offset byte :",offset_byte
byte_size = ord(a[5])
byte_size = byte_size << 8
byte_size = byte_size | ord(a[4])
byte_size = byte_size << 8
byte_size = byte_size | ord(a[3])
byte_size = byte_size << 8
byte_size = byte_size | ord(a[2])
byte_size = byte_size - offset_byte
print "RAW byte size :",byte_size
#print("Image width :",wh[0])
#print("Image height :",wh[1])
#print(data)
i = 0
h = 0
c1 = 0;


mode = 0
#ask mode for bmp array convert
print "Array 16 bits(RGB565) or Array 24 bits(RGB888) ? 1 for 16 bits, 2 for 24 bits \n"
while mode != '1' and mode != '2':
	mode = 0
	mode = raw_input()

#16 bits
if(mode == '1'):
	mode = 16

#24 bits	
if(mode == '2'):
	mode = 24

if(mode == 24):
	file.write("const uint32_t "+ name_array +"[%s"%height + "][%s"%width + "] = { \n")
if(mode == 16):
	file.write("const uint16_t "+ name_array +"[%s"%height + "][%s"%width + "] = { \n")

if(mode == 24):
	while i < byte_size-3:
		if(c1 == 0):
			file.write("{")
		
		h = ord(a[i+offset_byte])
		h = h << 8
		h = h | ord(a[i+offset_byte+1])
		h = h << 8
		h = h | ord(a[i+offset_byte+2])
		
		if(h == 0):
			file.write("0x0000")
		if(h > 0):
			file.write("%s"%hex(h))
		if(c1 < width-1 and i < byte_size-3):
			file.write(",")
    
		c1 = c1 + 1
		if(c1 == width and i != byte_size-3):
			file.write("},\n")
			c1 = 0
		i = i + 3
	
if(mode == 16):
	while i < byte_size-3:
		if(c1 == 0):
			file.write("{")
		
    
		h = (ord(a[i+offset_byte+2])*31)/255
		h = h << 11
		h = h | (((ord(a[i+offset_byte+1])*63)/255) << 5)
		h = h | (ord(a[i+offset_byte])*31)/255
		
		if(h == 0):
			file.write("0x0000")
		if(h > 0):
			file.write("%s"%hex(h))
		if(c1 < width-1 and i < byte_size-3):
			file.write(",")
    
		c1 = c1 + 1
		if(c1 == width and i != byte_size-3):
			file.write("},\n")
			c1 = 0
		i = i + 3
	
if(mode == 16):
		h = (ord(a[i+offset_byte+2])*31)/255
		h = h << 11
		h = h | (((ord(a[i+offset_byte+1])*63)/255) << 5)
		h = h | (ord(a[i+offset_byte])*31)/255
		
if(mode == 24):
	h = ord(a[i+offset_byte])
	h = h << 8
	h = h | ord(a[i+offset_byte+1])
	h = h << 8
	h = h | ord(a[i+offset_byte+2])

if(h == 0):
    file.write("0x0000}\n")
if(h > 0):
    file.write("%s}\n"%hex(h))
file.write("};")
file.close()
print("Done")
print("Press Enter to close...")
raw_input()
