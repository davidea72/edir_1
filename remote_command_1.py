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

ser.write(version)
print("version",ser.read(105))  # we read at least 105 character , if we haven't it the function exit by the timeout 

# setting the EDIR in learning mode, normal frequency 38 khz
ser.write(start_learning2)

print ("start code acquiring")

risposta=""
tentativi=0
while (len(risposta)==0 and tentativi < 10):

        risposta=ser.read(100)
        tentativi=tentativi+1
        print "lunghezza risposta dentro secondo while=",
	print len(risposta),
	print "tentativo numero ",
	print tentativi

print "lunghezza risposta fuori secondo while=",
print len(risposta),
print "tentativo numero ",
print tentativi

if (risposta[0].encode("hex")!="00"):
       print("risposta 0 =",risposta[0].encode("hex"))
       print ("errore")
       exit()


print "lunghezza stringa ricevuta=",
print len(risposta)

carattere='a'
conteggio=0
checksum=256
checksum_pos=0
checksum_is=0
end=0
for carattere in risposta:
        carattere=risposta[conteggio]
        ascii_char=carattere.encode("hex")
	if (conteggio==2):
	      	intero=int(ascii_char,16)
		print "lunghezza decodifica=",
	      	print intero,
		print "aggiunta terzo byte ricevuto"
              	checksum=checksum-intero
		checksum_pos=intero+3 #piu uno perche' alla lunghezza siamo sull' ultimo byte
	if (conteggio==checksum_pos):
		checksum_is=ascii_char
		
	if(conteggio!=0 and conteggio !=1 and conteggio !=2 and conteggio != checksum_pos and conteggio != checksum_pos+1):
		print(ascii_char),
		#print conteggio,
		checksum=checksum-int(ascii_char,16)
		#print checksum,
	conteggio=conteggio+1

print checksum
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 18 12 40 41 06 00 00 00 00 40 09 09 36 ed   accensione  25 gradi ventola max caldo aletta fissa in alto
#00 fa 23 26 c5 a7 80 80 01 00 8a 9d c5 a7 02 00 8a 8a 8a 9d 6e 48 65 26 02 00 38 12 40 41 06 00 00 00 00 00 0a 0a 52 ed
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 38 12 40 41 06 00 00 00 00 00 0a 09 55 ed
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 8a 8b 9c 6e 48 65 26 02 00 38 12 60 41 06 00 00 00 00 10 0a 09 25 ed   accensione  24 gradi ventola max caldo aletta fissa in alto
#00 fa 23 26 c5 a6 80 80 01 00 8b 9c c5 a6 02 00 8a 89 8b 9c 6e 48 65 26 02 00 38 12 00 42 06 00 00 00 00 20 0a 0a 74 ed   accensione  23 gradi ventola max caldo aletta fissa in alto
print "nello stream dati il checksum e' di :",
print risposta[checksum_pos].encode("hex")
print "il checksum calcolato in decimale e' ",
print checksum,
print " in esadecimale :",
print hex(checksum)

primo_byte=hex(checksum>>8)
print "primo byte ottenuto convertendo in esadecimale il valore decimale shiftato di 8 bit =",
print primo_byte
secondo_byte=hex(checksum-int(primo_byte,16)*256)
print "secondo byte ottenuto dalla differenza tra checksum e primo_byte*256=",
print secondo_byte

