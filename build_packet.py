import struct, logging


#add opcode and send to build_request
def make_RRQ(file_name, mode):
    opcode = 1
    return build_request (file_name, opcode, mode)

def make_WRQ(file_name, mode):
    opcode = 2
    return build_request (file_name, opcode, mode)


################################################################
#name: build_request
#input: filename, opcode, mode
#output: wrq/rrq packet with the opcode, filename, and mode
################################################################

def build_request (file_name, opcode, mode):
    mode = mode.encode("ascii")
    file_name = file_name.encode("ascii")
    file_name_length = str(len(file_name))

    #build packet format with length of filename
    format_string = "!H" + file_name_length + 'sx8sx'

    #build packet
    packet = struct.pack(format_string, opcode, file_name, mode)
    return packet


