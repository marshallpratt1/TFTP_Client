from socket import *
import os, error_handling



#handle error packets, remove bad file
def error_packet (filename):
    os.remove(filename)



#Check rnage of opcode, raise error if out of range
def opcode_check(opcode):
    if opcode <1 or opcode >5:
        raise ValueError("opcode out of range")

clientSocket = socket(AF_INET, SOCK_DGRAM)


###############################################
#open local file to send bytes from
#sends WRQ to TFTP server
#performs write operations and handles exceptions
##############################################


def write_file(packet, filename, address, serverport):

    #error check variables
    file_not_found = 1
    connection_count = 0
    

    #open target file into read bytes mode, populate a bytearray with contents
    #if file does not exist, build error packet and send to requestor
    if os.path.exists(filename):
        f = open(filename, "rb")
    else: #else handles error if filename already exists
        error_packet = error_handling.build_error_packet(file_not_found)        
        while True:
            try: 
                #send error packet to server if file error encountered
                if connection_count > 5:
                    break
                clientSocket.settimeout(1)
                sent = clientSocket.sendto(packet, (address, serverport))                
                break
            except: 
                #keep trying to try and try again
                connection_count += 1

    
    
    #write loop variables
    data_opcode = 3
    data_packet = bytearray()
    full_message = bytearray(f.read())
    #count for block number
    count = 0
    connection_count=0    

    #establish initial connection
    while True:
    #receive message and address from TFTP server, max bufferzise of 1024 bytes
        try: 
            #send initial request, then receive ack, if cannot connct, then break
            if connection_count > 5:
                break
            clientSocket.settimeout(1)
            sent = clientSocket.sendto(packet, (address, serverport))
            data, server = clientSocket.recvfrom(1024) 
            break
        except: 
            #keep trying to try and try again
            connection_count += 1 

    #write loop below:
    while True:
            #check to see if file is too big for 2 bytes, reset count if so
            if count > 65535:
                count = 0
            #error checking
            error_handling.check_for_errors(data, filename)
                           
            #no error
            #pull block from ack packet, set intitial sequence count
            block = data[2:4]
            block = int.from_bytes(block, byteorder='big')
            #look for out of order packet, raise error if found
            if block != count:
                clientSocket.close()
                os.remove(filename)
                raise ValueError("Error: packets out of order")
            
            #increment our block number for the next data packet
            count += 1
            
            #extract message from target file
            #reached end of file, send remaining data and close socket
            if len(full_message) < 512:                
                #build data packet with count byte block number
                data_packet = data_opcode + count.to_bytes(2, 'big') + full_message
                sent = clientSocket.sendto(data_packet, server)
                data, server = clientSocket.recvfrom(1024)
                #TODO: handle ack packet/error packet
                break

            #pop first 512 bytes from bytearray
            #clear message for next pop
            #send data packet and receive ack packet
            message = full_message[0:512]
            del full_message[0:512]
            data_packet = data_opcode + count.to_bytes(2, 'big') + message
            del message
            sent = clientSocket.sendto(data_packet, server)
            data, server = clientSocket.recvfrom(1024)

            
    f.close()
            

           
            