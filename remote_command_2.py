import serial
ser= serial.Serial('/dev/ttyUSB0', timeout=1)
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
while ((len(answer)==0 or len(answer)==1) and attempt < 30):  	#we make a 30 second loop (1 second timeout x 30 time)

        answer=ser.read(200)			#we read the serial with a 200 char buffer
        attempt+=1
	print("attempt number "+str(attempt))

if(len(answer)==0):				#if we can't obtail an answer (lenght == 0) exit
	print("no answer from the edir")
	exit()

if (answer[0].encode("hex")!="00"):		#if the edir recognize the command the first byte is 00 otherwise is FF
       print ("error executing the command")
       exit()

if (len(answer)<5):
	print ("lenght ",len(answer))
	print (answer[0].encode("hex"))
	print("exit with error , we have received some data")
	exit()

char='a'
count=0
checksum=256
checksum_pos=0
checksum_is=0
end=0
for char in answer:
        char=answer[count]
        ascii_char=char.encode("hex")		#convert the char into hex
	if (count==2):				#if count is equal to 2 it is the data lenght
	      	integer_number=int(ascii_char,16)	#convert the lenght into decimal
		checksum_pos+=3 # we add the value of 3 becouse we must jump to the first byte
						# after the decoded string
	if (count==3):
		frequency=int(ascii_char,16)	#frequency in decimal

	if (count==checksum_pos):		# if we are at the checksum position , memorize it
		checksum_is=ascii_char
		
	if(count!=0 and count !=1 and count !=2 and count != checksum_pos and count != checksum_pos+1): #in case we are not at this position : 	0 - executing is ok? 
		print(ascii_char),									#					1 - frame header
		checksum=checksum-int(ascii_char,16)							#					2 - data lenght
	count+=1											#				checksum_pos - the position where is the checksum	
													#				checksum_pos+1 , end data byte

#print checksum

#sample received data for my air conditioner remote command
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 18 12 40 41 06 00 00 00 00 40 09 09 36 ed   accensione  25 gradi ventola max caldo aletta fissa in alto
#00 fa 23 26 c5 a7 80 80 01 00 8a 9d c5 a7 02 00 8a 8a 8a 9d 6e 48 65 26 02 00 38 12 40 41 06 00 00 00 00 00 0a 0a 52 ed
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 38 12 40 41 06 00 00 00 00 00 0a 09 55 ed
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 38 12 60 41 06 00 00 00 00 10 0a 09 25 ed   accensione  24 gradi ventola max caldo aletta fissa in alto
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 89 8b 9c 6e 48 65 26 02 00 38 12 00 42 06 00 00 00 00 20 0a 0a 74 ed   accensione  23 gradi ventola max caldo aletta fissa in alto
print(" ")
print("count , posizioni scorse =",count)
print("len , byte ricevuti , deve essere uguale al rigo sopra=",len(answer))
print("integer_number, lunghezza del frame dati:",integer_number)
print("checksum_pos , posizione del checksum:",checksum_pos)
print(" frequency is ",frequency," khz")
edir_checksum=answer[checksum_pos-4].encode("hex")
edir_checksum=answer[checksum_pos-3].encode("hex")
edir_checksum=answer[checksum_pos-2].encode("hex")
edir_checksum=answer[checksum_pos-1].encode("hex")
edir_checksum=answer[checksum_pos].encode("hex")

first_byte=hex(checksum>>8)
second_byte=hex(checksum-int(first_byte,16)*256)

# if the computed second byte is the same as the checksum from the edir hardware we have received correctly the data

print " "
if (int(second_byte,16)==int(edir_checksum,16)):
	print " the checksum is OK"
else:
	print " the checksum is incorect"

#26 85 97 80 80 02 00 85 91 85 97 01 00 85 be 85 91 01 00 85 9d 85 be 03 00 85 94 85 9d 01 00 85 d2 85 94 02 02 85 a6 85 d3 01 00 84 91 85 a6 02 00 85 96 84 91 01 00 85 a0 85 96 01 00 85 91 85 a0 02 00 04  
#26 85 97 80 80 02 00 85 91 85 97 01 00 85 be 85 91 01 00 85 9d 85 be 03 00 85 94 85 9d 01 00 85 d2 85 94 02 02 84 a7 85 d3 01 00 84 91 84 a7 02 00 84 97 84 91 01 00 85 a0 84 97 01 00 85 91 85 a0 02 00 04  
#26 85 97 80 80 02 00 85 91 85 97 01 00 85 be 85 91 01 00 85 9d 85 be 03 00 85 94 85 9d 01 00 85 d2 85 94 02 02 84 a6 85 d3 01 00 85 91 84 a6 02 00 84 97 85 91 01 00 85 a0 84 97 01 00 85 91 85 a0 02 00 04  

send_ok=raw_input("do you want to send it back or exit? (S send back any other key exit)")
if (send_ok=="s" or send_ok=="S"):
	print "resending"
	print answer[1:]
	ser.write(answer[1:])
	return_code=ser.read(1)
	print(len(return_code))
#	print int(return_code,16)
else:
	print("exit without sending the code back")
	exit()
topolino=""
count = 1
for char in answer[1:]:
        char=answer[count]
        ascii_char=char.encode("hex")
	count+=1	
	print ascii_char,
	topolino=topolino+ascii_char+" "

print (topolino)
ser.write(topolino)
return_code=ser.read(1)
print(len(return_code))

#26 9d 89 80 80 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9e 89 8a cb 02 00 8a 9c 9e 89 09 26 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d
#26 9d 89 80 80 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 26 00 8a cb 8a 9c 01 00 9d
#26 9d 89 80 80 02 00 8a 9c 9d 89 09 46 00 89 cb 8a 9c 01 00 9d 89 89 cb 02 00 8a 9c 9d 89 09 46 00 89 cb 8a 9c 01 00 9d 89 89 cb 02 00 8a 9c 9d 89 09 46 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 46 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 46 00 8a cb 8a 9c 01 00 9d
#26 9d 89 80 80 02 00 8a 9c 9d 89 09 46 00 89 cb 8a 9c 01 00 9d 89 89 cb 02 00 8a 9c 9d 89 09 46 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 46 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 46 00 8a cb 8a 9c 01 00 9d 89 8a cc 02 00 8a 9c 9d 89 09 46 00 8a cb 8a 9c 01 00 9c

