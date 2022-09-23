from socket import *
import error_handling, os
clientSocket = socket(AF_INET, SOCK_DGRAM)



#receives data block number and builds ack packet
def build_ack (block):
    header = bytearray()
    #Acknowledge opcode = 04
    header.append(0)
    header.append(4)
    #attach block #
    header += block
    return header



###############################################
#open local file to write bytes into
#sends RRQ to TFTP server
#Handles incoming packets from server
################################################


def read_file(packet, filename, address, serverport):
    #error code if file already exists
    file_exists_code = 6

    #make copy of file to write into, if file already exists then throw error
    if os.path.exists(filename):
        error_handling.build_error_packet(file_exists_code)
    f = open(filename, "wb")
    #packet = byte packet, address = string ip address, serverport = int
        
    connection_count = 0
    block_number = 0 
    #Initial loop to initiate connection with server, has to try twice to make connection and receive packet
    while True:
    #receive message and address from TFTP server, max bufferzise of 1024 bytes
        try: 
            #receive data
            if connection_count > 5:
                break
            clientSocket.settimeout(1)
            sent = clientSocket.sendto(packet, (address, serverport))
            data, server = clientSocket.recvfrom(1024) 
            break
        except: 
            #keep trying to try and try again
            connection_count +=1  



    #Once connection is made and initial packet received, this loop
    #handles all incoming data and further packets
    #only breaks with error code or when message is less than 512 bytes
    while True:
    
            #send packet for error checking (error codes and valid packet information)       
            error_handling.check_for_errors(data, filename)
          
            #pull block number for ack packet
            block = data[2:4]
            ack = build_ack(block)
           
            #extract data and write to file
            message = data[4:]
            #message = message.decode("ascii")
            f.write(message)

            #send ack packet
            sent = clientSocket.sendto(ack, server)

            #end of message check, leave loop
            if len(message) < 512:
                #check for final error...
                data, server = clientSocket.recvfrom(1024)
                error_handling.check_for_errors(data, filename)
                clientSocket.close()
                break 
            
            #get next packet
            data, server = clientSocket.recvfrom(1024)

    f.close() 

            

               
            
