import serial
ser= serial.Serial('/dev/ttyUSB0', timeout=2)
print (ser.name)

version='\xFA\xF2'
start_learning='\xFA\xF5' #auto exit
start_learning2='\xFA\xFD' #non auto
stop_learning='\xFA\xF4'
sleep='\xFA\xF8'
wake='\xFA\xF7'
repeat='\xFA\xF3'
reset='\xFA\xF6'
start='\xFA'
stop='\xED'

#test
#        FA         18       25       xx xx xx xx xx       FC   ED
#     frame header       frequency			check sum
#               data length	     data packet		end


# first test to see if the hardware work
# we ask to the hardware the version

ser.write(version)
print("version",ser.read(105))  # we read at least 105 character , if we haven't it the function exit by the timeout 

# setting the EDIR in learning mode, normal frequency 38 khz
ser.write(start_learning2)

print ("start code acquiring")

answer=""
attempt=0
while (len(answer)==0 and attempt < 10):

        answer=ser.read(100)
        attempt=attempt+1
        print "lenght of the answer inside the while loop=",
	print len(answer),
	print "attempt number ",
	print attempt

print "lenght of the answer outside the while loop=",
print len(answer),
print "attempt number ",
print attempt

if (answer[0].encode("hex")!="00"):
       print("answer 0 =",answer[0].encode("hex"))
       print ("errore")
       exit()


print "lenght of the received string=",
print len(answer)

char='a'
count=0
checksum=256
checksum_pos=0
checksum_is=0
end=0
for char in answer:
        char=answer[count]
        ascii_char=char.encode("hex")
	if (count==2):
	      	integer_number=int(ascii_char,16)
		print "decoded lenght=",
	      	print integer_number,
		print "add the received third byte"
              	checksum=checksum-integer_number
		checksum_pos=integer_number+3 # we add the value of 3 becouse we must jump to the first byte
						# after the decoded string
	if (count==checksum_pos):
		checksum_is=ascii_char
		
	if(count!=0 and count !=1 and count !=2 and count != checksum_pos and count != checksum_pos+1):
		print(ascii_char),
		#print count,
		checksum=checksum-int(ascii_char,16)
		#print checksum,
	count=count+1

#print checksum

#sample received data for my air conditioner remote command
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 18 12 40 41 06 00 00 00 00 40 09 09 36 ed   accensione  25 gradi ventola max caldo aletta fissa in alto
#00 fa 23 26 c5 a7 80 80 01 00 8a 9d c5 a7 02 00 8a 8a 8a 9d 6e 48 65 26 02 00 38 12 40 41 06 00 00 00 00 00 0a 0a 52 ed
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 38 12 40 41 06 00 00 00 00 00 0a 09 55 ed
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 38 12 60 41 06 00 00 00 00 10 0a 09 25 ed   accensione  24 gradi ventola max caldo aletta fissa in alto
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 89 8b 9c 6e 48 65 26 02 00 38 12 00 42 06 00 00 00 00 20 0a 0a 74 ed   accensione  23 gradi ventola max caldo aletta fissa in alto
edir_checksum=answer[checksum_pos].encode("hex")
print " "
print "checksum from the edir hardware :",
print edir_checksum
print "computed checksum in decimal ",
print checksum,
print " in hex :",
print hex(checksum)

first_byte=hex(checksum>>8)
print "first byte of the computed checksum in hex value, obtained shifting the computed value by 8 bit =",
print first_byte
second_byte=hex(checksum-int(first_byte,16)*256)
print "second byte computed by the difference between computed checksum and first_byte *256=",
print second_byte

# if the computed second byte is the same as the checksum from the edir hardware we have received correctly the data

print " the received value is ",
print edir_checksum

if (int(second_byte,16)==int(edir_checksum,16)):
	print " the checksum is OK"
else:
	print " the checksum is incorect"
