import os

error_message = {
 0 : "Not defined, see error message (if any).",
 1 : "File not found.",
 2 : "Access violation.",
 3 : "Disk full or allocation exceeded.",
 4 : "Illegal TFTP operation.",
 5 : "Unknown transfer ID.",
 6 : "File already exists.",
 7 : "No such user."   
}

#handles error packets (opode 5), removes bad file
def read_error_packet (filename, error_code, data):
    if (error_code in error_message):
        if (error_code == 0):
            #get index at end of custom error message
            length = len(data)-1
            print ("Error: ", data[4:length].decode("utf-8"))
        else: print ("Error: ", error_message[error_code])
    else:
        raise ValueError ("Error: error code out of range (must be 0-7 inclusive)")
    os.remove(filename)



#Check rnage of opcode, raise error if out of range
def opcode_check(opcode):
    if opcode <1 or opcode >5:
        raise ValueError("Error: opcode out of range (must be 1-5 inclusive)")


#check for errors in incoming packets
def check_for_errors(data, filename):
    opcode = int.from_bytes(data[0:2], "big")
    opcode_check(opcode)
    if opcode == 5:
        error_code = int.from_bytes(data[2:4], "big")
        read_error_packet(filename, error_code, data)
    

#build error packet for delivery to server
def build_error_packet (code):
    #header will be our error packet
    header = bytearray()
    
    #Acknowledge opcode = 04
    header.append(0)
    header.append(5)
    
    #attach error code #
    header.append(0)
    header.append(code)
    
    #attach error message terminated by 0 byte
    header =+ error_message[code].encode("ascii")
    header.append(0)
    
    #return constructed error packet
    return header